# Veri İletişimi Hata Tespit Projesi

Bu proje, veri iletişiminde kullanılan hata tespit yöntemlerini gösteren bir uygulamadır. Sistem üç parçadan oluşur: gönderici, sunucu ve alıcı.

## Nasıl Çalışır?

1. **Gönderici (Client 1)**: Metin alır, kontrol bilgisi üretir ve sunucuya gönderir
2. **Sunucu (Server)**: Veriyi alır, bazen hata ekler ve alıcıya iletir (hata ekleme oranı %75 olarak ayarlanmıştır.)
3. **Alıcı (Client 2)**: Veriyi alır, kontrol bilgisini hesaplar ve hata olup olmadığını kontrol eder

## Kurulum

Python 3.6 veya üzeri yeterli.

1. Gerekli kütüphaneleri yükleyin (Tkinter genellikle Python ile gelir):
   ```bash
   # Gerekirse
   pip install tk
   ```

## Çalıştırma (Önerilen)

Projenin grafik arayüzünü (GUI) başlatmak için:

```bash
python3 gui/main.py
```

Bu arayüz üzerinden:
1. **"🚀 Sistemi Başlat"** butonuna basarak Server ve Alıcı'yı otomatik başlatabilirsiniz.
2. Metin girip yöntem seçerek **"Gönder"** butonuyla veri gönderebilirsiniz.
3. Tüm sonuçları ve hataları log ekranında görebilirsiniz.

## Manuel Çalıştırma (Terminal)

İsterseniz bileşenleri terminalden tek tek de çalıştırabilirsiniz (GUI kullanmadan):

1. Terminal 1 (Sunucu): `python3 server.py`
2. Terminal 2 (Alıcı): `python3 client2.py`
3. Terminal 3 (Gönderici): `python3 client1.py`

## Kullanım Detayları

### Hata Tespit Yöntemleri

1. **Parity Bit**: Basit parite kontrolü
2. **2D Parity**: Matris tabanlı parite kontrolü
3. **CRC**: Döngüsel artıklık kontrolü
4. **Hamming Code**: Hamming kod ile hata tespiti (ve düzeltme)
5. **Internet Checksum**: IP checksum algoritması

### Hata Enjeksiyon Yöntemleri

Sunucu, gelen verilere %75 ihtimalle rastgele bir hata ekler:
- Bit Flip, Karakter Değiştirme, Silme, Ekleme, Yer Değiştirme, Çoklu Bit Hata, Toplu Hata (Burst)

## Örnek Arayüz Çıktısı

```
==================================================
Gönderilen Paket:
Veri                 : MERHABA
Yöntem               : CRC
Kontrol Bilgisi      : A1B2
==================================================
Client 2 - Received Packet
Status               : DATA CORRUPTED
==================================================
```

## Dosyalar

- `gui/main.py` - Grafik Arayüz (Ana Program)
- `server.py` - Hata enjekte eden ara sunucu (Port 8888 -> 9999)
- `client2.py` - Alıcı ve doğrulayıcı (Port 9999)
- `client1.py` - Manuel gönderici scripti
- `utils.py` - Algoritma kütüphanesi

## Önemli Notlar

- Sistem **8888** ve **9999** portlarını kullanır.
- "Port kullanımda" hatası alırsanız bu portları kullanan diğer uygulamaları kapatın (veya eski python process'lerini sonlandırın).
