import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
from PIL import ImageGrab, Image
import numpy as np
import time
import threading
import win32gui
import win32ui
import win32con
import winsound
import os
import requests

# Sistem seslerini bul ve listele
def get_system_sounds():
    sound_folder = r"C:\Windows\Media"  # Sistem seslerinin bulunduğu klasör
    if not os.path.exists(sound_folder):
        return []
    return [f for f in os.listdir(sound_folder) if f.endswith('.wav')]

# Telegram mesaj gönderme işlevi
def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Telegram mesajı gönderildi.")
        else:
            print(f"Telegram mesajı gönderilemedi: {response.text}")
    except Exception as e:
        print(f"Telegram hatası: {e}")

# Telegram mesaj gönderme zamanlayıcısı
def wait_and_send_telegram(delay, telegram_settings, telegram_trigger):
    time.sleep(delay)
    if telegram_trigger[0]:  # Tetikleyici etkinse mesaj gönder
        send_telegram_message(
            telegram_settings["token"],
            telegram_settings["chat_id"],
            "Match found, but no action was taken within the specified time."
        )
        telegram_trigger[0] = False  # Mesaj gönderimi tamamlandıktan sonra sıfırla

# İzleme işlevi
def monitor_window(selected_window, regions, interval, sound, stop_flag, status_label, telegram_settings, telegram_trigger):
    hwnd = gw.getWindowsWithTitle(selected_window)[0]._hWnd
    last_screenshots = [None] * len(regions)  # Her bölge için ayrı ekran görüntüsü sakla

    status_label.config(text="Status: Monitoring Started", fg="green")
    telegram_trigger[0] = False  # İzleme başlatıldığında tetikleyici sıfırlanır

    while not stop_flag[0]:  # Kullanıcı durdurulana kadar çalış
        for i, region in enumerate(regions):
            full_image = get_window_image(hwnd)
            cropped_image = full_image.crop(region)
            current_array = np.array(cropped_image)

            # İlk ekran görüntüsü varsa karşılaştır
            if last_screenshots[i] is not None:
                difference = np.abs(current_array - last_screenshots[i])
                if np.all(difference == 0):  # Eşleşme bulundu
                    stop_flag[0] = True  # İzlemeyi durdur
                    status_label.config(text="Status: Match Detected!", fg="orange")
                    if sound:
                        winsound.PlaySound(sound, winsound.SND_FILENAME)  # Ses çal

                    # Telegram mesajını eşleşme sonrası belirli bir süre içinde gönder
                    delay = int(telegram_settings["delay"])
                    telegram_trigger[0] = True  # Mesaj tetiklendi
                    threading.Thread(
                        target=wait_and_send_telegram,
                        args=(delay, telegram_settings, telegram_trigger),
                        daemon=True
                    ).start()
                    return  # Döngüyü sonlandır

            last_screenshots[i] = current_array  # Güncel ekran görüntüsünü sakla

        time.sleep(interval)

# Arka plandaki pencerenin görüntüsünü al
def get_window_image(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(bitmap)

    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)

    image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return image

# İzlemeyi başlatan işlev
def start_monitoring(selected_window, interval, sound_var, status_label, stop_flag, telegram_settings, telegram_trigger):
    if not selected_window:
        status_label.config(text="Status: Please select a window!", fg="red")
        return

    if not sound_var.get():
        status_label.config(text="Status: Please select a sound!", fg="red")
        return

    try:
        interval = float(interval)
        if interval <= 0:
            raise ValueError
    except ValueError:
        status_label.config(text="Status: Invalid control interval!", fg="red")
        return

    # Yeni izleme başlatıldığında tetikleyiciyi sıfırla
    stop_flag[0] = False
    telegram_trigger[0] = False  # Eski tetikleyici iptal edilir

    hwnd = gw.getWindowsWithTitle(selected_window)[0]._hWnd
    left, top, _, _ = win32gui.GetWindowRect(hwnd)
    regions = [
        (2251 - left, 33 - top, 2538 - left, 34 - top),
        (2251 - left, 272 - top, 2538 - left, 273 - top)
    ]

    sound = os.path.join(r"C:\Windows\Media", sound_var.get())

    # İzleme işlemi için ayrı bir iş parçacığı başlat
    threading.Thread(
        target=monitor_window,
        args=(selected_window, regions, interval, sound, stop_flag, status_label, telegram_settings, telegram_trigger),
        daemon=True
    ).start()

# İzlemeyi durdurma işlevi
def stop_monitoring(status_label, stop_flag, telegram_trigger):
    stop_flag[0] = True  # İzleme işlemini durdur
    telegram_trigger[0] = False  # Mevcut tetikleyiciyi iptal et
    status_label.config(text="Status: Monitoring Stopped", fg="red")

# Kullanıcı arayüzü
def main():
    root = tk.Tk()
    root.title("Pencere İzleme Uygulaması")

    stop_flag = [False]  # İzleme durumu kontrolü
    telegram_trigger = [False]  # Telegram mesaj tetikleyicisi
    telegram_settings = {"token": "", "chat_id": "", "delay": 30}  # Telegram ayarları

    # Telegram bilgileri girişi
    tk.Label(root, text="Telegram Bot Token:").pack(pady=5)
    token_var = tk.StringVar()
    tk.Entry(root, textvariable=token_var).pack(pady=5)

    tk.Label(root, text="Telegram Chat ID:").pack(pady=5)
    chat_id_var = tk.StringVar()
    tk.Entry(root, textvariable=chat_id_var).pack(pady=5)

    tk.Label(root, text="Message Duration After Match (seconds):").pack(pady=5)
    delay_var = tk.StringVar(value="")
    tk.Entry(root, textvariable=delay_var).pack(pady=5)

    # Pencere seçimi
    tk.Label(root, text="Open Windows:").pack(pady=5)
    window_var = tk.StringVar()
    window_list = ttk.Combobox(root, textvariable=window_var)
    window_list['values'] = [w.title for w in gw.getAllWindows() if w.title]
    window_list.pack(pady=5)

    # Kontrol süresi girişi
    tk.Label(root, text="Control Interval (seconds):").pack(pady=5)
    interval_var = tk.StringVar(value="2")
    tk.Entry(root, textvariable=interval_var).pack(pady=5)

    # Bildirim sesi seçimi
    tk.Label(root, text="Notification Sound:").pack(pady=5)
    sound_var = tk.StringVar(value="")
    sound_list = ttk.Combobox(root, textvariable=sound_var)
    sound_list['values'] = get_system_sounds()  # Sistem seslerini ekle
    sound_list.pack(pady=5)

    # Durum etiketi
    status_label = tk.Label(root, text="Status: Waiting", fg="blue")
    status_label.pack(pady=10)

    # Başlat/Durdur butonları
    start_button = tk.Button(
        root,
        text="Start Monitoring",
        command=lambda: start_monitoring(
            window_var.get(),
            interval_var.get(),
            sound_var,
            status_label,
            stop_flag,
            {"token": token_var.get(), "chat_id": chat_id_var.get(), "delay": delay_var.get()},
            telegram_trigger
        )
    )
    start_button.pack(pady=5)

    stop_button = tk.Button(
        root,
        text="Stop Monitoring",
        command=lambda: stop_monitoring(status_label, stop_flag, telegram_trigger)
    )
    stop_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
