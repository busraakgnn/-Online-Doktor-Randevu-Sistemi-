import sys
import json
import re
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QRegularExpression, QDate
from PyQt5.QtGui import QPixmap, QRegularExpressionValidator, QIcon

# ---------- VERİ YÖNETİMİ ----------
def verileri_yukle():
    if not os.path.exists("kullanicilar.json"):
        with open("kullanicilar.json", "w") as f: json.dump({}, f)
    if not os.path.exists("randevular.json"):
        with open("randevular.json", "w") as f: json.dump([], f)
    if not os.path.exists("doktorlar.json"):
        baslangic_doktorlari = {
            "Dr. AHMET ÇAVUŞ - PEDAGOG": "12345678",
            "Dr. ELİF KARACA - PSİKOLOG": "87654321"
        }
        with open("doktorlar.json", "w") as f: json.dump(baslangic_doktorlari, f)
    
    try:
        with open("kullanicilar.json", "r") as f: kullanicilar = json.load(f)
        with open("randevular.json", "r") as f: randevular = json.load(f)
        with open("doktorlar.json", "r") as f: doktorlar = json.load(f)
    except:
        kullanicilar, randevular, doktorlar = {}, [], {}
    return kullanicilar, randevular, doktorlar

# ---------- STİLLER ----------
BG = "QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8EC5FC, stop:1 #3AAFA9); }"
CARD = "QFrame { background:#EAF4F4; border-radius:20px; }"
INPUT = "QLineEdit { padding:10px; border-radius:12px; background:white; border: 1px solid #ddd; color: black; }"
BTN = "QPushButton { background:#2A9D8F; color:white; padding:10px; border-radius:15px; font-weight:bold; }"
BTN2 = "QPushButton { border:2px solid #2A9D8F; color:#2A9D8F; padding:10px; border-radius:15px; font-weight:bold; background: transparent; }"
BTN_SIL = "QPushButton { background:#E76F51; color:white; padding:10px; border-radius:15px; font-weight:bold; }"

# ---------- RANDEVU KAYIT EKRANI ----------
class RandevuKayit(QWidget):
    def __init__(self, ad, tc):
        super().__init__()
        self.ad, self.tc = ad, tc 
        self.setWindowTitle(f"Randevu Sistemi - {self.ad}")
        self.setStyleSheet(BG)
        
        lay = QHBoxLayout(self)
        
        # --- SOL TARAF: FORM KARTI (İlk kodundaki özellikler korunmuştur) ---
        card = QFrame()
        card.setFixedSize(500, 700)
        card.setStyleSheet(CARD)
        c_lay = QVBoxLayout(card)
        
        lbl = QLabel(f"HOŞ GELDİN {self.ad}\nRandevu Formu")
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #264653;")
        
        self.cb_doktor = QComboBox(); self.cb_doktor.setStyleSheet(INPUT)
        # Veri yükleme mantığı korunmuştur[cite: 1, 4]
        _, _, d_liste = verileri_yukle() 
        self.cb_doktor.addItems(d_liste.keys())
        self.cb_doktor.currentIndexChanged.connect(self.saat_guncelle)
        
        self.takvim = QCalendarWidget()
        self.takvim.setNavigationBarVisible(True)
        self.takvim.setFirstDayOfWeek(Qt.Monday)
        self.takvim.setStyleSheet("background: white; color: black; border-radius: 10px;")
        self.takvim.clicked.connect(self.saat_guncelle)
        
        self.cb_saat = QComboBox(); self.cb_saat.setStyleSheet(INPUT)
        
        btn_al = QPushButton("RANDEVUYU ONAYLA", styleSheet=BTN, clicked=self.kaydet)
        btn_cikis = QPushButton("ÇIKIŞ YAP", styleSheet=BTN2, clicked=self.cikis)
        
        c_lay.addWidget(lbl)
        c_lay.addWidget(QLabel("Doktor Seçin:")); c_lay.addWidget(self.cb_doktor)
        c_lay.addWidget(QLabel("Tarih Seçin:")); c_lay.addWidget(self.takvim)
        c_lay.addWidget(QLabel("Saat Seçin:")); c_lay.addWidget(self.cb_saat)
        c_lay.addSpacing(10); c_lay.addWidget(btn_al); c_lay.addWidget(btn_cikis)
        
        # --- SAĞ TARAF: RANDEVU LİSTESİ VE SİLME (Tüm özellikler korunmuştur) ---
        sag_panel = QVBoxLayout()
        self.liste = QListWidget()
        self.liste.setStyleSheet("background: white; color: black; border-radius: 20px; padding: 10px;")
        
        # İlk kodundaki silme butonu özelliği korunmuştur[cite: 4]
        btn_sil = QPushButton("SEÇİLİ RANDEVUYU İPTAL ET", styleSheet=BTN_SIL, clicked=self.randevu_sil)
        
        sag_panel.addWidget(QLabel("RANDEVULARIM:")); sag_panel.addWidget(self.liste); sag_panel.addWidget(btn_sil)
        
        lay.addStretch()
        lay.addWidget(card, 1)
        lay.addLayout(sag_panel, 1)
        lay.addStretch()

        self.saat_guncelle(); self.liste_yenile(); self.showMaximized()

    def randevu_sil(self):
        # Randevu silme mantığı ve mesajları ilk kodundakiyle aynıdır[cite: 4]
        secili_item = self.liste.currentItem()
        if not secili_item:
            QMessageBox.warning(self, "Hata", "Lütfen silmek istediğiniz randevuyu seçin!")
            return
            
        secilen_metin = secili_item.text()
        cevap = QMessageBox.question(self, "Onay", "Bu randevuyu iptal etmek istediğinize emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        
        if cevap == QMessageBox.Yes:
            _, r_list, _ = verileri_yukle()
            yeni_liste = []
            for r in r_list:
                formatli = f"📅 {r['tarih_tr']} | ⏰ {r['saat']} | 👨‍⚕️ {r['doktor']}"
                if not (r["tc"] == self.tc and formatli == secilen_metin):
                    yeni_liste.append(r)
            
            with open("randevular.json", "w") as f:
                json.dump(yeni_liste, f, indent=4) # JSON kayıt yapısı korunmuştur[cite: 1, 2]
                
            QMessageBox.information(self, "Bilgi", "Randevunuz iptal edildi.")
            self.saat_guncelle()
            self.liste_yenile()

    def saat_guncelle(self):
        self.cb_saat.clear()
        secilen_gun = self.takvim.selectedDate()
        
        # Başlangıçta uyarı vermemesi için QMessageBox buradan kaldırıldı[cite: 4]
        if secilen_gun < QDate.currentDate():
            self.cb_saat.addItem("GEÇMİŞ TARİH"); return
        
        if secilen_gun.dayOfWeek() >= 6:
            self.cb_saat.addItem("KAPALI"); return # Sadece seçeneklerde görünür[cite: 4]
            
        t_slash = secilen_gun.toString("dd/MM/yyyy")
        _, r_list, _ = verileri_yukle()
        for h in range(9, 18):
            s = f"{h:02d}:00"
            dolu = any(r for r in r_list if r.get("tarih_tr") == t_slash and r["saat"] == s and r["doktor"] == self.cb_doktor.currentText())
            self.cb_saat.addItem(f"{'❌' if dolu else '🟢'} {s}")

    def kaydet(self):
        secilen_gun = self.takvim.selectedDate()
        
        # UYARI BURAYA TAŞINDI: Başlangıçta değil, sadece Onayla deyince çıkar[cite: 4]
        if secilen_gun.dayOfWeek() >= 6:
            QMessageBox.information(self, "Bilgi", "Kliniğimiz Cumartesi ve Pazar günleri kapalıdır.") # İlk mesajın aynısı[cite: 4]
            return

        if secilen_gun < QDate.currentDate():
            return # Geçmiş tarih engeli
            
        t_slash = secilen_gun.toString("dd/MM/yyyy")
        saat_text = self.cb_saat.currentText()
        if "❌" in saat_text or "KAPALI" in saat_text: return
            
        saat_temiz = saat_text.replace("🟢 ", "")
        _, r_list, _ = verileri_yukle()
        
        # Çakışma kontrolü ve kayıt özellikleri korunmuştur[cite: 1, 2, 4]
        if any(r for r in r_list if r["tc"] == self.tc and r.get("tarih_tr") == t_slash and r["saat"] == saat_temiz):
            QMessageBox.warning(self, "Hata", "Zaten bu saatte bir randevunuz var!"); return
        
        r_list.append({"ad_soyad": self.ad, "tc": self.tc, "doktor": self.cb_doktor.currentText(), "tarih_tr": t_slash, "saat": saat_temiz})
        with open("randevular.json", "w") as f: json.dump(r_list, f, indent=4)
        
        QMessageBox.information(self, "Başarılı", "Randevunuz oluşturuldu.")
        self.saat_guncelle(); self.liste_yenile()

    def liste_yenile(self):
        self.liste.clear()
        _, r_list, _ = verileri_yukle()
        for r in r_list:
            if r["tc"] == self.tc:
                self.liste.addItem(f"📅 {r['tarih_tr']} | ⏰ {r['saat']} | 👨‍⚕️ {r['doktor']}")

    def cikis(self):
        self.l = LoginScreen(); self.l.show(); self.close()

# ---------- DOKTOR TANIMLAMA PANELİ ----------
class DoktorTanimla(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yeni Doktor Tanımla")
        self.setStyleSheet(BG)
        lay = QVBoxLayout(self); lay.setAlignment(Qt.AlignCenter)
        card = QFrame(); card.setFixedSize(400, 480); card.setStyleSheet(CARD)
        c_lay = QVBoxLayout(card)

        lbl = QLabel("YENİ DOKTOR EKLE"); lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #264653;")

        harf_validator = QRegularExpressionValidator(QRegularExpression("^[A-Za-zÇĞİÖŞÜçğıöşü ]*$"))
        rakam_validator = QRegularExpressionValidator(QRegularExpression("^[0-9]*$"))

        self.dr_ad = QLineEdit(placeholderText="DOKTOR AD SOYAD"); self.dr_ad.setStyleSheet(INPUT)
        self.dr_ad.setValidator(harf_validator)
        self.dr_ad.textChanged.connect(lambda: self.dr_ad.setText(self.dr_ad.text().upper()))
        
        self.dr_uzmanlik = QLineEdit(placeholderText="UZMANLIK ALANI"); self.dr_uzmanlik.setStyleSheet(INPUT)
        self.dr_uzmanlik.setValidator(harf_validator)
        self.dr_uzmanlik.textChanged.connect(lambda: self.dr_uzmanlik.setText(self.dr_uzmanlik.text().upper()))
        
        s_lay = QHBoxLayout()
        self.dr_sifre = QLineEdit(placeholderText="ŞİFRE (8 HANELİ RAKAM)", echoMode=QLineEdit.Password); self.dr_sifre.setStyleSheet(INPUT)
        self.dr_sifre.setValidator(rakam_validator); self.dr_sifre.setMaxLength(8)
        
        self.btn_bak = QPushButton()
        if os.path.exists("sifre.png"): self.btn_bak.setIcon(QIcon("sifre.png"))
        self.btn_bak.setFixedSize(30, 30); self.btn_bak.setStyleSheet("background: transparent; border: none;")
        self.btn_bak.clicked.connect(self.sifre_goster_gizle)
        s_lay.addWidget(self.dr_sifre); s_lay.addWidget(self.btn_bak)

        btn_kaydet = QPushButton("DOKTORU KAYDET VE GİRİŞE GİT", styleSheet=BTN, clicked=self.kaydet)
        btn_iptal = QPushButton("GERİ", styleSheet=BTN2, clicked=self.geri)

        c_lay.addWidget(lbl); c_lay.addSpacing(10)
        c_lay.addWidget(self.dr_ad); c_lay.addWidget(self.dr_uzmanlik); c_lay.addLayout(s_lay)
        c_lay.addSpacing(15); c_lay.addWidget(btn_kaydet); c_lay.addWidget(btn_iptal)
        lay.addWidget(card); self.showMaximized()

    def sifre_goster_gizle(self):
        self.dr_sifre.setEchoMode(QLineEdit.Normal if self.dr_sifre.echoMode() == QLineEdit.Password else QLineEdit.Password)

    def kaydet(self):
        ad, uzm, sifre = self.dr_ad.text().strip(), self.dr_uzmanlik.text().strip(), self.dr_sifre.text()
        if not all([ad, uzm, sifre]) or len(sifre) != 8:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun! (Şİfre 8 rakam olmalı)")
            return
        
        tam_isim = f"Dr. {ad} - {uzm}"
        k, r, d = verileri_yukle()
        d[tam_isim] = sifre
        with open("doktorlar.json", "w") as f: json.dump(d, f, indent=4)
        QMessageBox.information(self, "Başarılı", f"{tam_isim} sisteme eklendi.")
        self.d = DoktorSecimPaneli(); self.d.show(); self.close()

    def geri(self):
        self.d = DoktorSecimPaneli(); self.d.show(); self.close()

# ---------- DOKTOR SEÇİM VE SİLME PANELİ ----------
class DoktorSecimPaneli(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Doktor Yönetim Paneli")
        self.setStyleSheet(BG)
        lay = QVBoxLayout(self); lay.setAlignment(Qt.AlignCenter)
        card = QFrame(); card.setFixedSize(400, 420); card.setStyleSheet(CARD)
        c_lay = QVBoxLayout(card)

        lbl = QLabel("DOKTOR SEÇİN VEYA SİLİN"); lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-weight: bold; color: #264653; font-size: 16px;")
        
        self.cb = QComboBox(); self.cb.setStyleSheet(INPUT); self.liste_guncelle()
        
        btn_ileri = QPushButton("GİRİŞ YAP", styleSheet=BTN, clicked=self.sifreye_git)
        btn_ekle = QPushButton("YENİ DOKTOR EKLE", styleSheet=BTN2, clicked=self.yeni_ekle)
        btn_sil = QPushButton("SEÇİLİ DOKTORU SİL", styleSheet=BTN_SIL, clicked=self.doktor_sil)
        btn_geri = QPushButton("ANA SAYFA", styleSheet=BTN2, clicked=self.geri)

        c_lay.addWidget(lbl); c_lay.addWidget(self.cb)
        c_lay.addSpacing(10); c_lay.addWidget(btn_ileri); c_lay.addWidget(btn_ekle)
        c_lay.addWidget(btn_sil); c_lay.addSpacing(10); c_lay.addWidget(btn_geri)
        lay.addWidget(card); self.showMaximized()

    def liste_guncelle(self):
        self.cb.clear()
        _, _, doktorlar = verileri_yukle()
        self.cb.addItems(doktorlar.keys())

    def doktor_sil(self):
        secilen = self.cb.currentText()
        if not secilen: return
        cevap = QMessageBox.question(self, "Onay", f"{secilen} silinecek. Emin misiniz?", QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            k, r, d = verileri_yukle()
            if secilen in d:
                del d[secilen]
                with open("doktorlar.json", "w") as f: json.dump(d, f, indent=4)
                self.liste_guncelle()
                QMessageBox.information(self, "Bilgi", "Doktor sistemden silindi.")

    def sifreye_git(self):
        if self.cb.currentText():
            self.s = DoktorSifrePaneli(self.cb.currentText()); self.s.show(); self.close()

    def yeni_ekle(self):
        self.dt = DoktorTanimla(); self.dt.show(); self.close()

    def geri(self):
        self.l = LoginScreen(); self.l.show(); self.close()

# ---------- DOKTOR ŞİFRE PANELİ ----------
class DoktorSifrePaneli(QWidget):
    def __init__(self, doktor_adi):
        super().__init__()
        self.doktor_adi = doktor_adi
        self.setWindowTitle("Şifre Doğrulama")
        self.setStyleSheet(BG)
        lay = QVBoxLayout(self); lay.setAlignment(Qt.AlignCenter)
        card = QFrame(); card.setFixedSize(400, 320); card.setStyleSheet(CARD)
        c_lay = QVBoxLayout(card)

        lbl = QLabel(f"{self.doktor_adi}\nŞifrenizi Giriniz"); lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet("font-weight: bold; color: #264653;")

        s_lay = QHBoxLayout()
        self.sifre_input = QLineEdit(placeholderText="8 HANELİ ŞİFRE", echoMode=QLineEdit.Password); self.sifre_input.setStyleSheet(INPUT)
        self.sifre_input.setMaxLength(8); self.sifre_input.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*$")))
        
        self.btn_bak = QPushButton()
        if os.path.exists("sifre.png"): self.btn_bak.setIcon(QIcon("sifre.png"))
        self.btn_bak.setFixedSize(30, 30); self.btn_bak.setStyleSheet("background: transparent; border: none;")
        self.btn_bak.clicked.connect(self.sifre_goster_gizle)
        s_lay.addWidget(self.sifre_input); s_lay.addWidget(self.btn_bak)

        btn_onay = QPushButton("GİRİŞ", styleSheet=BTN, clicked=self.dogrula)
        btn_geri = QPushButton("İPTAL", styleSheet=BTN2, clicked=self.geri)

        c_lay.addWidget(lbl); c_lay.addLayout(s_lay); c_lay.addSpacing(10); c_lay.addWidget(btn_onay); c_lay.addWidget(btn_geri)
        lay.addWidget(card); self.showMaximized()

    def sifre_goster_gizle(self):
        self.sifre_input.setEchoMode(QLineEdit.Normal if self.sifre_input.echoMode() == QLineEdit.Password else QLineEdit.Password)

    def dogrula(self):
        _, _, doktorlar = verileri_yukle()
        if self.sifre_input.text() == doktorlar.get(self.doktor_adi):
            self.p = DoktorPanel(self.doktor_adi); self.p.show(); self.close()
        else:
            QMessageBox.critical(self, "Hata", "Hatalı şifre!")

    def geri(self):
        self.d = DoktorSecimPaneli(); self.d.show(); self.close()

# ---------- DOKTOR PANELİ (Randevu Listesi) ----------
class DoktorPanel(QWidget):
    def __init__(self, doktor_adi):
        super().__init__()
        self.doktor_adi = doktor_adi
        self.setWindowTitle(f"Doktor Paneli - {self.doktor_adi}")
        self.setStyleSheet(BG)
        l = QVBoxLayout(self)
        lbl = QLabel(f"Hoş Geldiniz {self.doktor_adi}"); lbl.setStyleSheet("font-weight: bold; color: white; font-size: 16px;")
        self.lst = QListWidget(); self.lst.setStyleSheet("background: white; color: black; border-radius: 10px;")
        btn = QPushButton("ÇIKIŞ", styleSheet=BTN2, clicked=self.cikis)
        l.addWidget(lbl); l.addWidget(self.lst); l.addWidget(btn)
        self.yenile(); self.showMaximized()

    def yenile(self):
        self.lst.clear()
        _, r_list, _ = verileri_yukle()
        for r in r_list:
            if r["doktor"] == self.doktor_adi:
                self.lst.addItem(f"📅 {r['tarih_tr']} | ⏰ {r['saat']} | Hasta: {r['ad_soyad']}")

    def cikis(self):
        self.l = LoginScreen(); self.l.show(); self.close()

# ---------- KAYIT EKRANI (Hasta) ----------
class RegisterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YEDİPSİKOLOG - Kayıt Ol")
        self.setStyleSheet(BG)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        card = QFrame(); card.setFixedSize(400, 700); card.setStyleSheet(CARD)
        l = QVBoxLayout(card)

        l.addSpacing(25) 
        self.logo = QLabel()
        if os.path.exists("logo.png"): self.logo.setPixmap(QPixmap("logo.png").scaled(120, 120, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)
        
        lbl_baslik = QLabel("YENİ KAYIT")
        lbl_baslik.setStyleSheet("font-size: 20px; font-weight: bold; color: #264653;")
        lbl_baslik.setAlignment(Qt.AlignCenter)

        self.ad_soyad = QLineEdit(placeholderText="AD SOYAD")
        self.ad_soyad.setStyleSheet(INPUT)
        self.ad_soyad.setValidator(QRegularExpressionValidator(QRegularExpression("^[A-Za-zÇĞİÖŞÜçğıöşü ]*$")))
        
        tel_layout = QHBoxLayout()
        self.sabit_kod = QLabel("+90")
        self.sabit_kod.setStyleSheet("font-weight: bold; color: #264653; background: white; padding: 10px; border-radius: 12px; border: 1px solid #ddd;")
        self.tel = QLineEdit(placeholderText="5xxxxxxxxx"); self.tel.setStyleSheet(INPUT)
        self.tel.setMaxLength(10); self.tel.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*$")))
        tel_layout.addWidget(self.sabit_kod); tel_layout.addWidget(self.tel)
        
        self.tc = QLineEdit(placeholderText="TC KİMLİK NO", maxLength=11); self.tc.setStyleSheet(INPUT)
        self.tc.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*$")))
        
        s_lay = QHBoxLayout()
        self.sifre = QLineEdit(placeholderText="ŞİFRE", echoMode=QLineEdit.Password); self.sifre.setStyleSheet(INPUT)
        self.btn_bak = QPushButton()
        if os.path.exists("sifre.png"): self.btn_bak.setIcon(QIcon("sifre.png"))
        self.btn_bak.setFixedSize(30, 30); self.btn_bak.setStyleSheet("background: transparent; border: none;")
        self.btn_bak.clicked.connect(lambda: self.sifre.setEchoMode(QLineEdit.Normal if self.sifre.echoMode() == QLineEdit.Password else QLineEdit.Password))
        s_lay.addWidget(self.sifre); s_lay.addWidget(self.btn_bak)

        btn = QPushButton("KAYIT OL", styleSheet=BTN, clicked=self.kayit)
        btn_g = QPushButton("GERİ", styleSheet=BTN2, clicked=self.geri)

        l.addWidget(self.logo); l.addWidget(lbl_baslik); l.addSpacing(10) 
        l.addWidget(self.ad_soyad); l.addLayout(tel_layout); l.addWidget(self.tc); l.addLayout(s_lay)
        l.addSpacing(15); l.addWidget(btn); l.addWidget(btn_g)
        
        main_layout.addWidget(card)
        self.ad_soyad.textChanged.connect(lambda: self.ad_soyad.setText(self.ad_soyad.text().upper()))
        self.showMaximized()

    def kayit(self):
        ad, tc, tel, sifre = self.ad_soyad.text().strip(), self.tc.text().strip(), self.tel.text().strip(), self.sifre.text()
        
        # Boş alan kontrolü
        if not all([ad, tc, tel, sifre]):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return
        
        # Uzunluk kontrolü
        if len(tc) < 11 or len(tel) < 10:
            QMessageBox.warning(self, "Hata", "TC veya Telefon numarası eksik!")
            return

        # --- ŞİFRE KURALLARI KONTROLÜ ---
        if len(sifre) < 5 or not re.search("[A-Z]", sifre) or not re.search("[a-z]", sifre):
            QMessageBox.warning(self, "Şifre Hatası", "Şifre en az 5 karakter, 1 büyük ve 1 küçük harf içermelidir!")
            return

        k, _, _ = verileri_yukle() 
        k[tc] = {"ad_soyad": ad.upper(), "tel": "+90 " + tel, "sifre": sifre}
        with open("kullanicilar.json", "w") as f: json.dump(k, f, indent=4)
        QMessageBox.information(self, "Başarılı", "Kayıt işlemi tamamlandı!")
        self.geri()

    def geri(self):
        self.l = LoginScreen(); self.l.show(); self.close()

# ---------- ANA GİRİŞ EKRANI ----------
class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YEDİPSİKOLOG")
        self.setStyleSheet(BG)
        lay = QVBoxLayout(self); lay.setAlignment(Qt.AlignCenter)
        card = QFrame(); card.setFixedSize(400, 650); card.setStyleSheet(CARD)
        c_lay = QVBoxLayout(card)

        c_lay.addSpacing(25) 
        self.logo = QLabel()
        if os.path.exists("logo.png"): self.logo.setPixmap(QPixmap("logo.png").scaled(120, 120, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)
        
        lbl_baslik = QLabel("YEDİPSİKOLOG")
        lbl_baslik.setStyleSheet("font-size: 20px; font-weight: bold; color: #264653;")
        lbl_baslik.setAlignment(Qt.AlignCenter)

        self.ad_soyad = QLineEdit(placeholderText="AD SOYAD")
        self.ad_soyad.setStyleSheet(INPUT)
        self.ad_soyad.setValidator(QRegularExpressionValidator(QRegularExpression("^[A-Za-zÇĞİÖŞÜçğıöşü ]*$")))
        
        self.tc = QLineEdit(placeholderText="TC KİMLİK NO", maxLength=11); self.tc.setStyleSheet(INPUT)
        self.tc.setValidator(QRegularExpressionValidator(QRegularExpression("^[0-9]*$")))
        
        s_lay = QHBoxLayout()
        self.sifre = QLineEdit(placeholderText="ŞİFRE", echoMode=QLineEdit.Password); self.sifre.setStyleSheet(INPUT)
        self.btn_bak = QPushButton()
        if os.path.exists("sifre.png"): self.btn_bak.setIcon(QIcon("sifre.png"))
        self.btn_bak.setFixedSize(30, 30); self.btn_bak.setStyleSheet("background: transparent; border: none;")
        self.btn_bak.clicked.connect(lambda: self.sifre.setEchoMode(QLineEdit.Normal if self.sifre.echoMode() == QLineEdit.Password else QLineEdit.Password))
        s_lay.addWidget(self.sifre); s_lay.addWidget(self.btn_bak)

        btn_g = QPushButton("GİRİŞ YAP", styleSheet=BTN); btn_g.clicked.connect(self.giris)
        btn_u = QPushButton("ÜYE OL", styleSheet=BTN2); btn_u.clicked.connect(self.uye)
        btn_d = QPushButton("DOKTOR GİRİŞİ", styleSheet=BTN2); btn_d.clicked.connect(self.dr_paneli)

        c_lay.addWidget(self.logo); c_lay.addWidget(lbl_baslik); c_lay.addSpacing(15) 
        c_lay.addWidget(self.ad_soyad); c_lay.addWidget(self.tc); c_lay.addLayout(s_lay)
        c_lay.addSpacing(15); c_lay.addWidget(btn_g); c_lay.addWidget(btn_u); c_lay.addWidget(btn_d)
        
        lay.addWidget(card)
        self.ad_soyad.textChanged.connect(lambda: self.ad_soyad.setText(self.ad_soyad.text().upper()))
        self.showMaximized()

    def giris(self):
        k, _, _ = verileri_yukle() 
        tc = self.tc.text().strip()
        sifre = self.sifre.text().strip()
        
        if tc in k and k[tc]["sifre"] == sifre:
            ad = k[tc]["ad_soyad"]
            self.r = RandevuKayit(ad, tc)
            self.r.show()
            self.close()
        else:
            QMessageBox.critical(self, "Hata", "Giriş bilgileri hatalı veya kullanıcı bulunamadı!")

    def uye(self):
        self.u = RegisterScreen(); self.u.show(); self.close()

    def dr_paneli(self):
        self.d = DoktorSecimPaneli(); self.d.show(); self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv); p = LoginScreen(); p.show(); sys.exit(app.exec_())