# Restoran Sipariş ve Teslimat Yönetim Sistemi

Tasarım Kalıpları dersi dönem projesi – Hasan Celal Aydın (20232013038)

Orta ölçekli bir restoranın masa, gel-al ve paket servis siparişlerini yöneten Python konsol uygulaması. Sipariş alınır, hazırlanır, kuryeye verilir ve teslim edilir; her adımda müşteri, mutfak ve kurye bilgilendirilir. Ödeme farklı dış servislerle yapılır ve fiyata kampanyalar uygulanır.

Proje önerisi: [docs/proje_onerisi.pdf](docs/proje_onerisi.pdf)

## Kurulum

Gereksinim: Python 3.10 veya üstü. Harici kütüphane kullanılmaz.

```bash
git clone https://github.com/hasancelalaydin/tasarim-kaliplari-restoran-siparis.git
cd tasarim-kaliplari-restoran-siparis
```

## Çalıştırma

```bash
python main.py
```

Örnek senaryo üç sipariş oluşturur (paket servis, gel-al, masa) ve beş kalıbın birlikte çalışmasını ekrana yazar: sipariş durumları, bildirimler, indirimli tutarlar ve ödeme sonuçları.

## Testler

```bash
python -m unittest discover -s tests -v
```

Ayrıntılar: [docs/TEST.md](docs/TEST.md)

## Kullanılan Tasarım Kalıpları

| Kalıp (Grup) | Sistemdeki yeri | Roller → sınıflar | Dosya |
| --- | --- | --- | --- |
| Factory Method (Yaratımsal) | Sipariş türüne göre sipariş oluşturma | Creator: `SiparisOlusturucu` · ConcreteCreator: `PaketServisOlusturucu`, `GelAlOlusturucu`, `MasaOlusturucu` · Product: `Siparis` · ConcreteProduct: `PaketServisSiparisi`, `GelAlSiparisi`, `MasaSiparisi` | `restoran/fabrika.py`, `restoran/siparis.py` |
| Adapter (Yapısal) | Ödeme servisleri | Target: `OdemeIslemcisi` · Adapter: `KartOdemeAdaptoru`, `KapidaOdemeAdaptoru` · Adaptee: `KartServisiApi`, `KapidaOdemeSistemi` | `restoran/odeme.py` |
| State (Davranışsal) | Sipariş durumu | Context: `Siparis` · State: `SiparisDurumu` · ConcreteState: `AlindiDurumu`, `HazirlaniyorDurumu`, `YoldaDurumu`, `TeslimEdildiDurumu`, `IptalDurumu` | `restoran/durum.py`, `restoran/siparis.py` |
| Strategy (Davranışsal) | İndirim ve kampanya hesabı | Context: `FiyatHesaplayici` · Strategy: `IndirimStratejisi` · ConcreteStrategy: `IndirimYok`, `OgrenciIndirimi`, `KuponIndirimi`, `SaatlikKampanya` | `restoran/indirim.py` |
| Observer (Davranışsal) | Durum bildirimleri | Subject: `SiparisYayincisi` · ConcreteSubject: `Siparis` · Observer: `SiparisGozlemcisi` · ConcreteObserver: `MusteriBildirimi`, `MutfakEkrani`, `KuryeBildirimi` | `restoran/bildirim.py`, `restoran/siparis.py` |

Tüm arayüzler `abc.ABC` ile soyut sınıf olarak yazılmıştır. Koddaki her rol sınıfının üstünde kalıp adını ve rolü belirten bir yorum bulunur, örneğin `# [State] ConcreteState`.

## Proje Yapısı

```
restoran/
  siparis.py   Sipariş sınıfları (Product, Context, ConcreteSubject)
  fabrika.py   Factory Method
  odeme.py     Adapter
  durum.py     State
  indirim.py   Strategy
  bildirim.py  Observer
tests/         Birim testleri (unittest)
docs/          Proje önerisi ve test dokümanı
main.py        Örnek senaryo
```
