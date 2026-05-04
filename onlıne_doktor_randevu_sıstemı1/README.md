
##  🛠️ Kurulum ve Çalıştırma

1️⃣ Gerekli ortamı hazırlayın
Python sisteminizde kurulu olmalıdır.

2️⃣ Gerekli kütüphaneyi yükleyin
pip install PyQt5

3️⃣ Projeyi çalıştırın
python randevu_qui.py

----
# 🧠 YEDİPSİKOLOG RANDEVU SİSTEMİ

Bu proje, kullanıcıların kolayca doktor randevusu almasını, doktorların ise randevuları görüntülemesini sağlayan PyQt5 tabanlı bir masaüstü uygulamasıdır.
----
## 🧠 Sistem Yapısı ve Özellikler

### 👤 Kullanıcı (User)
**Özellikler:**
- tc  
- ad_soyad  
- tel  
- sifre  

**Metotlar:**
- uyeOl  
- girisYap  

**Yapabildikleri:**
- Yeni kullanıcı kaydı oluşturma  
- Sisteme güvenli giriş yapma  
----
### 📅 Randevu (Appointment)
**Özellikler:**
- tc  
- ad_soyad  
- tarih  
- saat  
- doktor  

**Metotlar:**
- randevuOlustur  
- randevuSil  

**Yapabildikleri:**
- Takvim üzerinden randevu seçme  
- Saatlerin doluluk durumunu görüntüleme  
- Randevu oluşturma ve listeleme  
- Aynı saat için çakışma kontrolü  
----
### 👨‍⚕️ Doktor (Doctor)
**Özellikler:**
- doktor_adi  
- uzmanlik  

**Metotlar:**
- randevulariGoruntule    

**Yapabildikleri:**
- Şifre ile sisteme giriş  
- Kendi randevularını görüntüleme  
- Hasta bilgilerini listeleme  

## 🔐 Doktor Giriş Bilgisi
-Şifre: 133238
----

## ⚙️ Sistem Özellikleri
- Aynı saat için çakışma engelleme
- JSON tabanlı veri saklama
- Dinamik arayüz güncelleme
- Kullanıcı hatalarına karşı uyarı sistemi

----

## 🖥️ Uygulama Arayüzleri
📌 Ana Giriş Ekranı
- Kullanıcıların sisteme giriş yaptığı, kayıt olabildiği ve doktor paneline erişebildiği başlangıç ekranıdır.

📌 Kayıt Ol Ekranı
- Yeni kullanıcıların sisteme dahil edildiği ekrandır. Gerekli bilgiler alınarak veri dosyasına kaydedilir.

📌 Randevu Alma Ekranı
Kullanıcılar:
- Tarih seçer
- Doktor belirler
- Uygun saatleri görüntüler
- Randevu oluşturur

📌 Doktor Paneli
- Doktorlar kendi randevularını:
- Tarih
- Saat
- Hasta bilgisi
şeklinde görüntüleyebilir.

## 📸 Ekran Görüntüleri

### 🔐 Giriş Ekranı
![Kayıt](./ekran_goruntuleri/giriş1.png)

- Kullanıcı ad, TC kimlik numarası ve şifre ile sisteme giriş yapar.  
Ayrıca kullanıcı kayıt olabilir veya doktor girişi yapabilir.

![Kayıt](./ekran_goruntuleri/girişuyarı2.png)

- Girilen bilgiler yanlışsa kullanıcıya:
“Giriş bilgileri hatalı veya kullanıcı bulunamadı!”
uyarısı gösterilir.



### 📝 Kayıt Ekranı
![ÜYE OLMA](./ekran_goruntuleri/üyeol1.png)

- Yeni kullanıcıların sisteme kayıt olduğu ekrandır.
  
![ÜYE BOŞ ALAN UYARI](./ekran_goruntuleri/üyeboşalanmesajı2.png)

- Eğer kullanıcı tüm alanları doldurmazsa:
- “Lütfen tüm alanları doldurun!” uyarısı gösterilir.

![ÜYE ŞİFRE](./ekran_goruntuleri/üyeşifreuyarı3.png)

- Şifre kurallara uymadığında (büyük/küçük harf vb.) kullanıcıya hata mesajı gösterilir.

![ÜYE KAYIT](./ekran_goruntuleri/üyekayıtoluşturma4.png)

- Tüm bilgiler doğru girildiğinde:
- “Kayıt işlemi tamamlandı!” mesajı gösterilir ve kullanıcı sisteme kaydedilir.

----

### 👨‍⚕️ Doktor Paneli
![DOKTOR](./ekran_goruntuleri/doktorgiriş1.png)

- Doktor yönetim panelinde mevcut doktorlar listeden seçilerek giriş yapılabilir, yeni doktor eklenebilir veya seçili doktor silinebilir.
 
![DOKTOR SEÇME](./ekran_goruntuleri/doktorgirişdoktorseme2.png)

- Açılır listede sistemde kayıtlı tüm doktorlar ve branşları görüntülenir, istenilen doktor seçilir.
  
![DOKTOR ŞİFRE](./ekran_goruntuleri/seçilendoktorşifresi3.png)

- Seçilen doktorun sisteme giriş yapabilmesi için kendine ait şifreyi girmesi gerekir.
  
![DOKTOR ŞİFRE UYARI](./ekran_goruntuleri/doktorşifreuyarı4.png)

- Girilen şifre yanlışsa sistem hata mesajı vererek girişe izin vermez.
  
![DOKTOR RANDEVULARI](./ekran_goruntuleri/seçilendoktorrandevuları5.png)

- Doktor giriş yaptıktan sonra kendisine ait tüm randevuları hasta adı, tarih ve saat bilgisiyle listelenmiş şekilde görür.



  
### 👨‍⚕️ Doktor EKLEME
![DOKTOR EKLME](./ekran_goruntuleri/doktorekleme1.png)

- Yeni doktor ekleme ekranında doktor adı, uzmanlık alanı ve şifre girilerek sisteme kayıt yapılır.
  
![DOKTOR ŞİFRE UYARI](./ekran_goruntuleri/doktoreklemeveşifreuyarı2.png)

- Alanlar eksik doldurulursa veya şifre 8 haneli değilse sistem hata mesajı gösterir.
  
![DOKTOR EKLEME BİLGİSİ](./ekran_goruntuleri/doktoreklendibilgisi3.png)

- Tüm bilgiler doğru girildiğinde doktor başarıyla sisteme eklenir ve bilgilendirme mesajı gösterilir.




### 👨‍⚕️ Doktor SİLME
![DOKTOR SİLME](./ekran_goruntuleri/silinicekdoktoruseçme1.png)

- Doktor yönetim panelinde listeden silinmek istenen doktor seçilir.
- Seçilen doktoru silmeden önce sistem kullanıcıdan emin olup olmadığını soran onay mesajı gösterir.
  
![DOKTOR SİLME](./ekran_goruntuleri/doktorsilmeuyarıs2.png)

- Onay verildiğinde doktor sistemden silinir ve işlem başarılı mesajı gösterilir.

----




### 📅 Randevu Alma
![RANDEVU](./ekran_goruntuleri/randevualma1.png)

- Kullanıcıların tarih, doktor ve saat seçerek randevu oluşturduğu ekrandır.
  
![RANDEVU DOKTOR SEÇME](./ekran_goruntuleri/randevudoktorseçme2.png)

- Açılır listeden doktor seçilerek uygun randevu seçenekleri belirlenir.
  
![ÇAKIŞMA](./ekran_goruntuleri/doluolansaatlerx3.png)

- Daha önce alınmış saatler seçilemez ve kullanıcıya o saatlerin dolu olduğu görsel olarak belirtilir.
  
![HAFTASONU](./ekran_goruntuleri/haftasonuuyarı4.png)

- Kullanıcı Cumartesi veya Pazar günü seçtiğinde sistem randevu alınamayacağını uyarı mesajı ile bildirir.
  
![ÇAKIŞMA](./ekran_goruntuleri/çakışmarandevuuyarı5.png)

- Kullanıcı aynı tarih ve saate tekrar randevu almaya çalışırsa sistem çakışma olduğunu belirten hata verir.
  
![RANDEVU ALINDI](./ekran_goruntuleri/randevualınndıbilgisi6.png)

- Randevu başarıyla oluşturulduğunda kullanıcıya işlemin tamamlandığını belirten bilgilendirme mesajı gösterilir.


 

### 📅 Randevu Silme

![Randevusilme](./ekran_goruntuleri/randevusilmeonay1ı.png)

- Kullanıcı seçtiği randevuyu silmek istediğinde sistem işlemi gerçekleştirmeden önce onay mesajı gösterir.



## 🔍 Test Senaryosu

Uygulamayı test etmek için:
- Yeni bir kullanıcı kaydı oluşturun
- Sisteme giriş yapın
- Bir tarih ve saat seçerek randevu alın
- Aynı saat için tekrar seçim yapmayı deneyin (engellenecektir)
- Doktor paneline girerek randevuyu görüntüleyin

## 🧩 Teknik Detaylar
- Arayüz PyQt5 ile geliştirilmiştir
- Veri saklama JSON dosyaları üzerinden yapılmaktadır
- Tüm işlemler fonksiyonel yapı ile yönetilmektedir
- Arayüz ve veri katmanı birbirinden ayrılmıştır

## 📌 Genel Değerlendirme
- Bu proje ile:
- GUI geliştirme mantığı öğrenilmiş
- Veri yönetimi uygulanmış
- Gerçek hayata yakın bir sistem modellenmiştir
- Uygulama, yazılım geliştirme sürecinde pratik kazanmak amacıyla hazırlanmıştır.
