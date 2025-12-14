# Veri İletişimi Hata Tespit Projesi

Bu proje, veri iletişiminde kullanılan hata tespit yöntemlerini gösteren bir uygulamadır. Sistem üç parçadan oluşur: gönderici, sunucu ve alıcı.

## Nasıl Çalışır?

1. **Gönderici (Client 1)**: Metin alır, kontrol bilgisi üretir ve sunucuya gönderir
2. **Sunucu (Server)**: Veriyi alır, bazen hata ekler ve alıcıya iletir (hata ekleme oranı %75 olarak ayarlanmıştır.)
3. **Alıcı (Client 2)**: Veriyi alır, kontrol bilgisini hesaplar ve hata olup olmadığını kontrol eder

## Kurulum

Python 3.6 veya üzeri yeterli. Ekstra bir şey kurmanıza gerek yok.

## Çalıştırma

En kolay yol:

```bash
python3 run.py
```

Bu komut her şeyi otomatik başlatır. İsterseniz manuel olarak da çalıştırabilirsiniz:

1. Terminal 1: `python3 server.py`
2. Terminal 2: `python3 client2.py`
3. Terminal 3: `python3 client1.py`

## Kullanım

Programı çalıştırdığınızda:

1. Göndermek istediğiniz metni yazın
2. Hata tespit yöntemini seçin (1-5 arası)
3. Sistem otomatik olarak kontrol bilgisini üretir ve gönderir

### Hata Tespit Yöntemleri

1. **Parity Bit**: Basit parite kontrolü
2. **2D Parity**: Matris tabanlı parite kontrolü
3. **CRC**: Döngüsel artıklık kontrolü
4. **Hamming Code**: Hamming kod ile hata tespiti
5. **Internet Checksum**: IP checksum algoritması

### Hata Enjeksiyon Yöntemleri

Sunucu, gelen verilere %75 ihtimalle şu hatalardan birini ekler:

1. **Bit Flip**: Bir bit ters çevrilir
2. **Karakter Değiştirme**: Bir karakter başka bir karakterle değiştirilir
3. **Karakter Silme**: Bir karakter silinir
4. **Karakter Ekleme**: Rastgele bir karakter eklenir
5. **Karakter Yer Değiştirme**: İki komşu karakter yer değiştirir
6. **Çoklu Bit Ters Çevirme**: Birden fazla bit ters çevrilir
7. **Toplu Hata**: 3-8 karakterlik bir bölüm bozulur

## Örnek Çıktı

Alıcı tarafında şöyle bir çıktı görürsünüz:

```
==================================================
Client 2 - Received Packet
==================================================
Received Data        : HEZLO
Method               : CRC
Sent Check Bits      : 87AF
Computed Check Bits  : 92B1
Status               : DATA CORRUPTED
==================================================
```

## Dosyalar

- `run.py` - Tüm programı başlatır
- `client1.py` - Gönderici
- `server.py` - Sunucu
- `client2.py` - Alıcı
- `utils.py` - Hata tespit fonksiyonları

## Önemli Notlar

- Sunucu ve alıcı aynı anda çalışmalı
- Göndericiyi en son başlatın
- Sistem localhost üzerinde çalışır (port 8888 ve 9999)
- Sunucu paketlerin %75'ine hata ekler, %25'i hatasız geçer
