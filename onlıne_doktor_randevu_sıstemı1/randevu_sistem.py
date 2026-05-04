import json # Bilgileri dosyaya yazmamıza yarayan kütüphaneyi çağırır.

# ---------- KULLANICI İŞLEMLERİ (Üye Bilgileri) ----------

def kullanici_yukle():
    # Bu kutu, "kullanicilar.json" dosyasına gider. 
    # Eğer orada kayıtlı insanlar varsa onları alıp programa getirir.
    # Dosya yoksa veya boşsa "kimse yok" der (boş liste döndürür).
    try:
        with open("kullanicilar.json", "r") as f:
            return json.load(f)
    except:
        return {}

def kullanici_kaydet(data):
    # Bu kutu, yeni bir üye kayıt olduğunda o bilgiyi alır,
    # "kullanicilar.json" dosyasının içine kalıcı olarak yazar.
    with open("kullanicilar.json", "w") as f:
        json.dump(data, f, indent=4)


# ---------- RANDEVU İŞLEMLERİ (Randevu Defteri) ----------

def randevu_yukle():
    # Bu kutu, "randevular.json" dosyasına bakar. 
    # Daha önce kim hangi doktora randevu almışsa o listeyi programa yükler.
    try:
        with open("randevular.json", "r") as f:
            return json.load(f)
    except:
        return []

def randevu_kaydet(data):
    # Bu kutu, biri "Randevu Al" butonuna bastığında o randevuyu kapar,
    # "randevular.json" dosyasına gidip bir daha silinmesin diye kaydeder.
    with open("randevular.json", "w") as f:
        json.dump(data, f, indent=4)