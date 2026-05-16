import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import random

# PENCERE AYARLARI
pen = Tk()
pen.title("Kargo Takip ve Yönetim Sistemi")
penWidth = 1400
penHeight = 850

pcWidth = pen.winfo_screenwidth()
pcHeight = pen.winfo_screenheight()

x = (pcWidth - penWidth) // 2
y = (pcHeight - penHeight) // 2

pen.geometry(f"{penWidth}x{penHeight}+{x}+{y}")
pen.resizable(width=False, height=False)
pen.config(bg="lightblue")


# VERİ TABANI BAĞLANTISI
def baglan():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=8889,
        user="root",
        password="root",
        database="kargo_db"
    )


def saatGuncelle():
    zamanString = time.strftime("%H:%M:%S")
    tarihString = time.strftime("%d.%m.%Y")
    saatLabel.config(text=f"{tarihString}\n{zamanString}")
    pen.after(1000, saatGuncelle)


# KARGO TAKİP EKRANI
def kargoTakipEkrani():
    takipPen = Toplevel()
    takipPen.title("Kargo Sorgulama")
    takipPen.geometry(f"{penWidth}x{penHeight}+{x}+{y}")
    takipPen.resizable(False, False)
    takipPen.config(bg="lightblue")

    def takipGeriDon():
        takipPen.destroy()

    def takipSaatGuncelle():
        zaman = time.strftime("%H:%M:%S")
        tarih = time.strftime("%d.%m.%Y")
        takipSaatLabel.config(text=f"{tarih}\n{zaman}")
        takipPen.after(1000, takipSaatGuncelle)

    def sorgula():
        kod = entry_TakipNo.get()

        # Temizlik
        listeGecmis.delete(0, END)
        lbl_DurumSonuc.config(text="...")
        lbl_GondericiS.config(text="...")
        lbl_AliciS.config(text="...")
        lbl_CikisSubeSonuc.config(text="...")
        lbl_VarisSubeSonuc.config(text="...")
        lbl_TipSonuc.config(text="...")
        lbl_OdemeSonuc.config(text="...")
        lbl_TarihSonuc.config(text="...")

        if kod == "":
            messagebox.showwarning("Uyarı", "Lütfen bir takip kodu giriniz!")
            return

        baglanti = baglan()
        cursor = baglanti.cursor()

        # Kargo Bilgisini Çekme
        sql = """SELECT gonderici_ad, alici_ad, durum, varis_birimi, kargo_tipi, odeme_turu, 
                 DATE_FORMAT(cikis_tarihi, '%d.%m.%Y')
                 FROM kargolar WHERE takip_kodu=%s"""
        cursor.execute(sql, (kod,))
        kargo = cursor.fetchone()

        if kargo:
            lbl_GondericiS.config(text=kargo[0])
            lbl_AliciS.config(text=kargo[1])
            lbl_DurumSonuc.config(text=kargo[2])
            lbl_CikisSubeSonuc.config(text="İzmir Merkez")
            lbl_VarisSubeSonuc.config(text=kargo[3])
            lbl_TipSonuc.config(text=kargo[4])
            lbl_OdemeSonuc.config(text=kargo[5])
            lbl_TarihSonuc.config(text=kargo[6])

            # Geçmişi Çekme
            cursor.execute("SELECT id FROM kargolar WHERE takip_kodu=%s", (kod,))
            kargo_id = cursor.fetchone()[0]

            sql_gecmis = """SELECT yeni_durum, DATE_FORMAT(degisim_tarihi, '%d.%m.%Y %H:%i') 
                            FROM kargo_tarihce WHERE kargo_id=%s ORDER BY degisim_tarihi DESC"""
            cursor.execute(sql_gecmis, (kargo_id,))
            gecmis = cursor.fetchall()

            for durum, tarih in gecmis:
                satir = f" {tarih:<30} |   {durum}"
                listeGecmis.insert(END, satir)

        else:
            messagebox.showerror("Hata", "Kargo Bulunamadı!")

        baglanti.close()

    # TASARIM

    # Header
    Button(takipPen, text="< Geri", command=takipGeriDon, width=5, bg="lightblue", fg="black", height=2,font=("Arial", 12, "bold")).place(x=20, y=20)
    Label(takipPen, text="KARGO SORGULAMA", font=("Arial", 30, "bold"), bg="lightblue", fg="black").place(x=515,y=25)
    takipSaatLabel = Label(takipPen, text="", font=("Arial", 18, "bold"), bg="lightblue", fg="darkblue")
    takipSaatLabel.place(x=1280, y=5)

    # Arama Alanı
    Label(takipPen, text="Takip Kodu:", font=("Arial", 14, "bold"), bg="lightblue", fg="black").place(x=480, y=120)
    entry_TakipNo = Entry(takipPen, width=20, font=("Arial", 16), justify="center", bg="white", fg="black")
    entry_TakipNo.place(x=600, y=120)
    Button(takipPen, text="SORGULA", command=sorgula, font=("Arial", 11, "bold"), bg="green", fg="black", width=12, height=2,).place(x=850, y=118)

    # SON DURUM
    Label(takipPen, text="SON DURUM:", font=("Arial", 14, "bold"), bg="lightblue", fg="black").place(x=555, y=180)
    lbl_DurumSonuc = Label(takipPen, text="...", font=("Arial", 16, "bold"), bg="lightblue", fg="black")
    lbl_DurumSonuc.place(x=655, y=178)

    # SOL SÜTUN
    Label(takipPen, text="Gönderici:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=350, y=240)
    lbl_GondericiS = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_GondericiS.place(x=440, y=240)

    Label(takipPen, text="Alıcı:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=350, y=280)
    lbl_AliciS = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_AliciS.place(x=440, y=280)

    Label(takipPen, text="Çıkış Şubesi:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=350, y=320)
    lbl_CikisSubeSonuc = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_CikisSubeSonuc.place(x=440, y=320)

    Label(takipPen, text="Varış Şubesi:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=350, y=360)
    lbl_VarisSubeSonuc = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_VarisSubeSonuc.place(x=440, y=360)

    # SAĞ SÜTUN
    Label(takipPen, text="Kargo Tipi:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=850, y=240)
    lbl_TipSonuc = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_TipSonuc.place(x=940, y=240)

    Label(takipPen, text="Ödeme Türü:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=850, y=280)
    lbl_OdemeSonuc = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_OdemeSonuc.place(x=940, y=280)

    Label(takipPen, text="Çıkış Tarihi:", font=("Arial", 13, "bold"), bg="lightblue", fg="black").place(x=850, y=320)
    lbl_TarihSonuc = Label(takipPen, text="...", font=("Arial", 13), bg="lightblue", fg="black")
    lbl_TarihSonuc.place(x=940, y=320)

    # GEÇMİŞ LİSTESİ
    Label(takipPen, text="HAREKET GEÇMİŞİ", font=("Arial", 14, "bold", "underline"), bg="lightblue", fg="black").place(x=620, y=470)

    # Basit Listbox
    listeGecmis = Listbox(takipPen, width=50, height=7, font=("Courier New", 16), bg="white", fg="black", bd=2,relief="sunken")
    listeGecmis.place(x=440, y=510)

    takipSaatGuncelle()


# PERSONEL GİRİŞİ VE KAYIT EKRANI
def personelGirisi():
    girisPen = Toplevel()
    girisPen.title("Personel Girişi")
    girisPen.geometry(f"{penWidth}x{penHeight}+{x}+{y}")
    girisPen.resizable(False, False)
    girisPen.config(bg="lightblue")

    def geriDon():
        girisPen.destroy()

    def girisYapKontrol():
        kadi = kadiInput.get()
        sifre = sifreInput.get()

        baglanti = baglan()
        cursor = baglanti.cursor()
        cursor.execute("SELECT * FROM personel WHERE kullanici_adi=%s AND sifre=%s", (kadi, sifre))
        kullanici = cursor.fetchone()
        baglanti.close()

        if kullanici:
            girisPen.destroy()
            adminPaneli()
        else:
            messagebox.showerror("Hata", "Hatalı Giriş!")

    # YENİ PERSONEL KAYIT EKRANI
    def kayitEkraniAc():
        kayitPen = Toplevel()
        kayitPen.title("Yeni Personel Kaydı")
        kayitPen.geometry(f"{penWidth}x{penHeight}+{x}+{y}")
        kayitPen.resizable(False, False)
        kayitPen.config(bg="lightblue")

        def kayitGeriDon():
            kayitPen.destroy()

        def kayitSaatGuncelle():
            zaman = time.strftime("%H:%M:%S")
            tarih = time.strftime("%d.%m.%Y")
            kayitSaatLabel.config(text=f"{tarih}\n{zaman}")
            kayitPen.after(1000, kayitSaatGuncelle)

        def kayitOl():
            kadi = regKadiInput.get()
            sifre = regSifreInput.get()
            sifre2 = regSifreInput2.get()

            if kadi == "" or sifre == "":
                messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz!")
                return

            if sifre != sifre2:
                messagebox.showerror("Hata", "Şifreler uyuşmuyor!")
                return

            baglanti = baglan()
            cursor = baglanti.cursor()

            cursor.execute("SELECT * FROM personel WHERE kullanici_adi=%s", (kadi,))
            if cursor.fetchone():
                messagebox.showerror("Hata", "Bu kullanıcı adı zaten alınmış!")
                baglanti.close()
                return

            sql = "INSERT INTO personel (kullanici_adi, sifre) VALUES (%s, %s)"
            cursor.execute(sql, (kadi, sifre))
            baglanti.commit()
            baglanti.close()

            messagebox.showinfo("Başarılı", "Yeni personel kaydı oluşturuldu!")
            kayitPen.destroy()

        # KAYIT EKRANI WIDGETLAR
        btn_Geri = Button(kayitPen, text="< Geri", command=kayitGeriDon, width=5, bg="lightblue", fg="black", height=2,font=("Arial", 12, "bold"))
        kayitSaatLabel = Label(kayitPen, text="", font=("Arial", 18, "bold"), bg="lightblue", fg="darkblue")
        lbl_Baslik = Label(kayitPen, text="YENİ PERSONEL KAYDI", font=("Arial", 30, "bold"), bg="lightblue", fg="black")

        lbl_Kadi = Label(kayitPen, text="Kullanıcı Adı:", font=("Arial", 12), bg="lightblue", fg="black")
        regKadiInput = Entry(kayitPen, width=25, font=("Arial", 14), bg="white", fg="black")

        lbl_Sifre = Label(kayitPen, text="Şifre:", font=("Arial", 12), bg="lightblue", fg="black")
        regSifreInput = Entry(kayitPen, width=25, font=("Arial", 14), show="*", bg="white", fg="black")

        lbl_Sifre2 = Label(kayitPen, text="Şifre Tekrar:", font=("Arial", 12), bg="lightblue", fg="black")
        regSifreInput2 = Entry(kayitPen, width=25, font=("Arial", 14), show="*", bg="white", fg="black")

        btn_Kayit = Button(kayitPen, text="KAYIT OL", command=kayitOl, font=("Arial", 12, "bold"), width=15, bg="green",fg="black", height=3)

        # KAYIT EKRANI YERLEŞİMİ
        btn_Geri.place(x=20, y=20)
        kayitSaatLabel.place(x=1280, y=5)

        lbl_Baslik.grid(row=0, column=0, pady=(100, 50), padx=540)

        lbl_Kadi.grid(row=1, column=0, sticky="w", padx=610)
        regKadiInput.grid(row=2, column=0, padx=610, pady=(0, 15))

        lbl_Sifre.grid(row=3, column=0, sticky="w", padx=610)
        regSifreInput.grid(row=4, column=0, padx=610, pady=(0, 15))

        lbl_Sifre2.grid(row=5, column=0, sticky="w", padx=610)
        regSifreInput2.grid(row=6, column=0, padx=610, pady=(0, 25))

        btn_Kayit.grid(row=7, column=0, pady=10)

        kayitSaatGuncelle()

    def girisSaatGuncelle():
        zamanString = time.strftime("%H:%M:%S")
        tarihString = time.strftime("%d.%m.%Y")
        girisSaatLabel.config(text=f"{tarihString}\n{zamanString}")
        girisPen.after(1000, girisSaatGuncelle)

    # GİRİŞ EKRANI WIDGETLAR
    girisSaatLabel = Label(girisPen, text="", font=("Arial", 18, "bold"), bg="lightblue", fg="darkblue")
    btn_Geri = Button(girisPen, text="< Geri", command=geriDon, width=5, bg="lightblue", fg="black", height=2,font=("Arial", 12, "bold"))

    lbl_Baslik = Label(girisPen, text="PERSONEL GİRİŞİ", font=("Arial", 30, "bold"), bg="lightblue", fg="black")

    lbl_Kadi = Label(girisPen, text="Kullanıcı Adı:", font=("Arial", 12), bg="lightblue", fg="black")
    kadiInput = Entry(girisPen, width=25, font=("Arial", 14), bg="white", fg="black")

    lbl_Sifre = Label(girisPen, text="Şifre:", font=("Arial", 12), bg="lightblue", fg="black")
    sifreInput = Entry(girisPen, width=25, font=("Arial", 14), show="*", bg="white", fg="black")

    btn_Giris = Button(girisPen, text="GİRİŞ YAP", command=girisYapKontrol, font=("Arial", 12, "bold"), width=15,bg="lightblue", fg="black", height=4)
    btn_YeniKayit = Button(girisPen, text="Yeni Personel Kaydı Oluştur", command=kayitEkraniAc,font=("Arial", 10, "bold"), fg="black", bg="lightblue", height=2)

    # GİRİŞ EKRANI YERLEŞİMİ
    girisSaatLabel.place(x=1280, y=5)
    btn_Geri.place(x=20, y=20)

    lbl_Baslik.grid(row=0, column=0, pady=(100, 100), padx=585)

    lbl_Kadi.grid(row=1, column=0, sticky="w", padx=610)
    kadiInput.grid(row=2, column=0, padx=610, pady=(0, 15))

    lbl_Sifre.grid(row=3, column=0, sticky="w", padx=610)
    sifreInput.grid(row=4, column=0, padx=610, pady=(0, 20))

    btn_Giris.grid(row=5, column=0, pady=(0, 15))
    btn_YeniKayit.grid(row=6, column=0, pady=(30, 5))

    girisSaatGuncelle()



# ADMİN PANELİ
def adminPaneli():
    adminPen = Toplevel()
    adminPen.title("Personel Yönetim Paneli")
    adminPen.geometry(f"{penWidth}x{penHeight}+{x}+{y}")
    adminPen.resizable(False, False)
    adminPen.config(bg="lightblue")

    # İŞLEV FONKSİYONLARI
    def cikisYap():
        adminPen.destroy()

    def adminSaatGuncelle():
        zamanString = time.strftime("%H:%M:%S")
        tarihString = time.strftime("%d.%m.%Y")
        adminSaatLabel.config(text=f"{tarihString}\n{zamanString}")
        adminPen.after(1000, adminSaatGuncelle)

    def listele():
        for i in liste.get_children():
            liste.delete(i)

        baglanti = baglan()
        cursor = baglanti.cursor()

        sql = """SELECT id, takip_kodu, gonderici_ad, alici_ad, kargo_tipi, odeme_turu, durum, varis_birimi, 
                 DATE_FORMAT(cikis_tarihi, '%d.%m.%Y %H:%i')
                 FROM kargolar ORDER BY id DESC"""
        cursor.execute(sql)
        kayitlar = cursor.fetchall()

        for kayit in kayitlar:
            liste.insert("", END, values=kayit)

        baglanti.close()

    def temizle():
        entryGonderici.delete(0, END)
        entryGTel.delete(0, END)
        entryAlici.delete(0, END)
        entryATel.delete(0, END)
        entryAAdres.delete("1.0", END)
        entryAgirlik.delete(0, END)
        comboTip.current(0)
        comboOdeme.current(0)
        comboVaris.set("")
        comboDurum.current(0)

    def ekle():
        g_ad = entryGonderici.get()
        g_tel = entryGTel.get()
        a_ad = entryAlici.get()
        a_tel = entryATel.get()
        a_adres = entryAAdres.get("1.0", END).strip()
        agirlik = entryAgirlik.get()
        tip = comboTip.get()
        odeme = comboOdeme.get()
        varis = comboVaris.get()
        durum = comboDurum.get()

        if g_ad == "" or a_ad == "" or varis == "":
            messagebox.showwarning("Uyarı", "Lütfen isim ve şube bilgilerini giriniz!")
            return

        baglanti = baglan()
        cursor = baglanti.cursor()

        while True:
            takip_kodu = f"TR{random.randint(100000, 999999)}"

            cursor.execute("SELECT id FROM kargolar WHERE takip_kodu=%s", (takip_kodu,))

            if not cursor.fetchone():
                break

        # Kargo Ekle
        sql_kargo = """INSERT INTO kargolar 
        (takip_kodu, gonderici_ad, gonderici_tel, alici_ad, alici_tel, alici_adres, 
            kargo_agirlik, kargo_tipi, odeme_turu, varis_birimi, durum) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        veriler_kargo = (takip_kodu, g_ad, g_tel, a_ad, a_tel, a_adres,
                         agirlik, tip, odeme, varis, durum)

        cursor.execute(sql_kargo, veriler_kargo)

        # Tarihçe Ekle
        yeni_kargo_id = cursor.lastrowid
        sql_tarihce = "INSERT INTO kargo_tarihce (kargo_id, eski_durum, yeni_durum) VALUES (%s, %s, %s)"
        cursor.execute(sql_tarihce, (yeni_kargo_id, "Sistem Girişi", durum))

        baglanti.commit()
        baglanti.close()

        messagebox.showinfo("Başarılı", f"Kargo Eklendi!\nTakip Kodu: {takip_kodu}")
        temizle()
        listele()

    def sil():
        secili = liste.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Silmek İçin Lütfen Listeden Seçim yapınız.")
            return
        id_no = liste.item(secili)["values"][0]

        # Soru sormadan direkt sil
        baglanti = baglan()
        cursor = baglanti.cursor()
        cursor.execute("DELETE FROM kargolar WHERE id=%s", (id_no,))
        baglanti.commit()
        baglanti.close()
        listele()
        temizle()
        messagebox.showinfo("Bilgi", "Kayıt Silindi.")

    def veriyi_doldur(e):
        secili = liste.selection()
        if secili:
            id_no = liste.item(secili)["values"][0]
            baglanti = baglan()
            cursor = baglanti.cursor()
            cursor.execute("SELECT * FROM kargolar WHERE id=%s", (id_no,))
            kayit = cursor.fetchone()
            baglanti.close()

            if kayit:
                temizle()
                entryGonderici.insert(0, kayit[2])
                entryGTel.insert(0, kayit[3])
                entryAlici.insert(0, kayit[4])
                entryATel.insert(0, kayit[5])
                entryAAdres.insert("1.0", kayit[6])
                comboVaris.set(kayit[7])
                comboDurum.set(kayit[8])
                entryAgirlik.insert(0, kayit[9])
                comboOdeme.set(kayit[10])
                comboTip.set(kayit[11])

    def guncelle():
        secili = liste.selection()
        if not secili:
            messagebox.showwarning("Uyarı", "Güncelleme için seçim yapınız.")
            return

        id_no = liste.item(secili)["values"][0]
        yeni_durum = comboDurum.get()
        yeni_varis = comboVaris.get()

        baglanti = baglan()
        cursor = baglanti.cursor()

        cursor.execute("SELECT durum FROM kargolar WHERE id=%s", (id_no,))
        eski_durum = cursor.fetchone()[0]

        if eski_durum != yeni_durum:
            sql_tarihce = "INSERT INTO kargo_tarihce (kargo_id, eski_durum, yeni_durum) VALUES (%s, %s, %s)"
            cursor.execute(sql_tarihce, (id_no, eski_durum, yeni_durum))

        sql_update = "UPDATE kargolar SET durum=%s, varis_birimi=%s WHERE id=%s"
        cursor.execute(sql_update, (yeni_durum, yeni_varis, id_no))

        baglanti.commit()
        baglanti.close()

        listele()
        messagebox.showinfo("Bilgi", "Kargo güncellendi.")

    # ADMİN PANELİ WIDGETLAR

    # Header
    btn_Cikis = Button(adminPen, text="< ÇIKIŞ", command=cikisYap, width=5, height=2, bg="lightblue", fg="black",font=("Arial", 12, "bold"))
    lbl_AdminBaslik = Label(adminPen, text="KARGO YÖNETİM PANELİ", font=("Arial", 24, "bold"), bg="lightblue",fg="black")
    adminSaatLabel = Label(adminPen, text="", font=("Arial", 18, "bold"), bg="lightblue", fg="darkblue")

    # Form Alanı (Sol)
    lbl_GondericiAd = Label(adminPen, text="Gönderici Ad Soyad:", font=("Arial", 11, "bold"), bg="lightblue",fg="black")
    entryGonderici = Entry(adminPen, width=30, font=("Arial", 11), bg="white", fg="black")

    lbl_GondericiTel = Label(adminPen, text="Gönderici Tel:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    entryGTel = Entry(adminPen, width=30, font=("Arial", 11), bg="white", fg="black")

    lbl_AliciAd = Label(adminPen, text="Alıcı Ad Soyad:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    entryAlici = Entry(adminPen, width=30, font=("Arial", 11), bg="white", fg="black")

    lbl_AliciTel = Label(adminPen, text="Alıcı Tel:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    entryATel = Entry(adminPen, width=30, font=("Arial", 11), bg="white", fg="black")

    lbl_AliciAdres = Label(adminPen, text="Alıcı Adres:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    entryAAdres = Text(adminPen, width=30, height=3, font=("Arial", 11), bg="white", fg="black")

    lbl_KargoTipi = Label(adminPen, text="Kargo Tipi:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    comboTip = ttk.Combobox(adminPen, values=["Standart Koli", "Dosya/Evrak", "Kırılacak Eşya", "Elektronik"], width=28,font=("Arial", 11))
    comboTip.current(0)

    lbl_Agirlik = Label(adminPen, text="Kargo Ağırlığı (kg):", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    entryAgirlik = Entry(adminPen, width=30, font=("Arial", 11), bg="white", fg="black")

    lbl_Odeme = Label(adminPen, text="Ödeme Türü:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    comboOdeme = ttk.Combobox(adminPen, values=["Gönderici Ödemeli", "Alıcı Ödemeli"], width=28, font=("Arial", 11))
    comboOdeme.current(0)

    lbl_Varis = Label(adminPen, text="Varış Şubesi:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    comboVaris = ttk.Combobox(adminPen, values=["İzmir", "İstanbul", "Ankara", "Bursa", "Antalya"], width=28,font=("Arial", 11))
    comboVaris.place(x=200, y=440)

    lbl_Durum = Label(adminPen, text="Kargo Durumu:", font=("Arial", 11, "bold"), bg="lightblue", fg="black")
    comboDurum = ttk.Combobox(adminPen, values=["📦 Hazırlanıyor", "🚛 Yola Çıktı","🛵 Dağıtımda", "✅ Teslim Edildi"], width=28,font=("Arial", 11))
    comboDurum.current(0)

    # Butonlar
    btn_Kaydet = Button(adminPen, text="KAYDET", command=ekle, bg="green", fg="black", font=("Arial", 12, "bold"),width=16, height=2)
    btn_Guncelle = Button(adminPen, text="GÜNCELLE", command=guncelle, bg="blue", fg="black",font=("Arial", 12, "bold"), width=16, height=2)
    btn_Sil = Button(adminPen, text="SİL", command=sil, bg="red", fg="black", font=("Arial", 12, "bold"),width=16,height=2)
    btn_Temizle = Button(adminPen, text="TEMİZLE", command=temizle, bg="white", fg="black", font=("Arial", 12, "bold"),width=16, height=2)

    # Treeview
    lbl_ListeBaslik = Label(adminPen, text="Kargo Listesi", font=("Arial", 14, "bold"), bg="lightblue", fg="black")

    cols = ("id", "takip", "gonderici", "alici", "tip", "odeme", "durum", "varis", "tarih")
    liste = ttk.Treeview(adminPen, columns=cols, show="headings", height=32)

    liste.heading("id", text="ID")
    liste.column("id", width=35)
    liste.heading("takip", text="Takip No")
    liste.column("takip", width=90)
    liste.heading("gonderici", text="Gönderici")
    liste.column("gonderici", width=120)
    liste.heading("alici", text="Alıcı")
    liste.column("alici", width=120)
    liste.heading("tip", text="Tipi")
    liste.column("tip", width=110)
    liste.heading("odeme", text="Ödeme")
    liste.column("odeme", width=110)
    liste.heading("durum", text="Durum")
    liste.column("durum", width=100)
    liste.heading("varis", text="Varış")
    liste.column("varis", width=80)
    liste.heading("tarih", text="Tarih")
    liste.column("tarih", width=130)

    liste.bind("<Double-1>", veriyi_doldur)

    # ADMİN PANELİ YERLEŞİMİ

    # Header Yerleşimi
    btn_Cikis.place(x=20, y=20)
    lbl_AdminBaslik.place(x=500, y=20)
    adminSaatLabel.place(x=1280, y=5)

    # Form Yerleşimi
    lbl_GondericiAd.place(x=30, y=90)
    entryGonderici.place(x=200, y=90)

    lbl_GondericiTel.place(x=30, y=130)
    entryGTel.place(x=200, y=130)

    lbl_AliciAd.place(x=30, y=170)
    entryAlici.place(x=200, y=170)

    lbl_AliciTel.place(x=30, y=210)
    entryATel.place(x=200, y=210)

    lbl_AliciAdres.place(x=30, y=250)
    entryAAdres.place(x=200, y=250)

    lbl_KargoTipi.place(x=30, y=320)
    comboTip.place(x=200, y=320)

    lbl_Agirlik.place(x=30, y=360)
    entryAgirlik.place(x=200, y=360)

    lbl_Odeme.place(x=30, y=400)
    comboOdeme.place(x=200, y=400)

    lbl_Varis.place(x=30, y=440)
    comboVaris.place(x=200, y=440)

    lbl_Durum.place(x=30, y=480)
    comboDurum.place(x=200, y=480)

    # Buton Yerleşimi
    btn_Kaydet.place(x=50, y=560)
    btn_Guncelle.place(x=240, y=560)
    btn_Sil.place(x=50, y=620)
    btn_Temizle.place(x=240, y=620)

    # Liste Yerleşimi
    lbl_ListeBaslik.place(x=500, y=70)
    liste.place(x=480, y=100)

    listele()
    adminSaatGuncelle()



# ANA EKRAN

# ANA EKRAN WIDGETLARI
saatLabel = Label(pen, text="", font=("Arial", 18, "bold"), bg="lightblue", fg="darkblue")
baslikLabel = Label(pen, text="KARGO TAKİP SİSTEMİ", font=("Arial", 30, "bold"), bg="lightblue", fg="black")
musteriButon = Button(pen, text="📦 Kargo Sorgula", font=("Arial", 14), width=25, height=2, command=kargoTakipEkrani)
personelButon = Button(pen, text="🔐 Personel Girişi", font=("Arial", 14), width=25, height=2, command=personelGirisi)

# ANA EKRAN YERLEŞİMİ
saatLabel.grid(row=0, column=0, sticky="e", padx=15, pady=5)
baslikLabel.grid(row=1, column=0, pady=(150, 100))
musteriButon.grid(row=2, column=0, padx=585, pady=10)
personelButon.grid(row=3, column=0, padx=585, pady=10)

saatGuncelle()
pen.mainloop()