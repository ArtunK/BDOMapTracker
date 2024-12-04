# **BDOMapTracker User Manual**

## **What is BDOMapTracker?**
**BDOMapTracker** is a Python application designed to help Black Desert Online players monitor whether their ship has reached the next island for bartering. The application checks if the map remains unchanged and alerts you when your ship stops, ensuring you know when it’s time to proceed.

---

## **How It Works**
### **1. Application Setup:**
- Set your game resolution to **2K**.
- Adjust the UI size in the game settings to **98**.

### **2. Map Check Interval:**
- The application checks your map at a user-defined interval.
- **Recommended interval:** 1 second.

### **3. Notifications:**
- When your ship stops, the application notifies you with a **sound alert**.
- If Telegram integration is enabled, the application can send a **Telegram message** if no interaction occurs after reaching your destination.

---

## **Using Telegram (Optional):**
If you don’t want to use Telegram integration, simply follow these steps:
1. Configure the **check interval**.
2. Select the **active BDO window**.
3. Choose a **notification sound**.
4. Start the bot.

To enable Telegram integration:
1. Enter your Telegram Bot Token and Chat ID.
2. Enable the Telegram messaging feature.
3. The application will send a message to your Telegram account if no interaction is detected for the configured time.

# **BDOMapTracker Kullanım Kılavuzu**



------------

## **BDOMapTracker Nedir?**
**BDOMapTracker**, Black Desert Online oynarken geminizin haritada belirlediğiniz noktaya ulaşıp ulaşmadığını kontrol eden bir Python uygulamasıdır. Uygulama, geminizin hareketini izleyerek haritanın aynı durumda olup olmadığını kontrol eder ve geminizin durduğunu algıladığında sizi bilgilendirir. Bu sayede, bir sonraki adaya takas (bartering) yapmaya ulaşıp ulaşmadığınızı takip edebilirsiniz.

---

## **Nasıl Çalışır?**
### **1. Uygulama Ayarları:**
- Oyun çözünürlüğünüzü **2K** olarak ayarlayın.
- UI büyüklüğünü oyun ayarlarından **98** olarak değiştirin.

### **2. Harita Kontrol Süresi:**
- Uygulama, haritanızın durumunu belirlediğiniz bir süre aralığında kontrol eder.
- **Önerilen süre:** 1 saniye.

### **3. Bildirimler:**
- Geminiz durduğunda uygulama, seçtiğiniz bir **sesli bildirim** ile size bilgi verir.
- Telegram entegrasyonunu etkinleştirirseniz, uygulama geminizin varış noktasına ulaşıp bir süre boyunca etkileşim olmadığında size **Telegram mesajı** gönderebilir.

---

## **Telegram Kullanımı (Opsiyonel):**
Eğer Telegram entegrasyonunu etkinleştirmek istemiyorsanız, sadece aşağıdaki adımları tamamlamanız yeterlidir:
1. **Saniye Ayarını** belirleyin.
2. **Açık olan BDO penceresini** seçin.
3. **Uyarı Sesini** seçin.
4. Botu başlatın.

Telegram entegrasyonu yapmak için:
1. Telegram Bot Token ve Chat ID bilgilerinizi girin.
2. Telegram mesajlaşma özelliğini etkinleştirin.
3. Ayarlanan süre boyunca bir etkileşim olmazsa, uygulama size otomatik olarak bir mesaj gönderecektir.
