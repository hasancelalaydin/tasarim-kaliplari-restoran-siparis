# Test Dokümanı

Testler Python'un standart `unittest` modülüyle yazılmıştır; ek kurulum gerekmez.

## Çalıştırma

Proje klasöründe:

```bash
python -m unittest discover -s tests -v
```

Beklenen sonuç: `Ran 25 tests ... OK`

Tek bir dosyayı çalıştırmak için, örneğin: `python -m unittest discover -s tests -p test_durum.py -v`

## Test Kapsamı

| Dosya | Kalıp | Test sayısı | Kontrol edilenler |
| --- | --- | --- | --- |
| `tests/test_fabrika.py` | Factory Method | 4 | Her oluşturucu kendi sipariş türünü üretir; paket servis adres ve teslimat ücreti taşır; gel-al ve masa kurye gerektirmez; oluşturucu gözlemcileri siparişe bağlar. |
| `tests/test_durum.py` | State | 7 | Paket servisin tam akışı; gel-al siparişin yola çıkmadan teslimi; kuryesiz teslim, yoldaki siparişin iptali ve hazırlanan siparişe ürün eklenmesinin reddedilmesi; boş siparişin hazırlanamaması; iptal edilen siparişin ilerleyememesi. |
| `tests/test_odeme.py` | Adapter | 5 | Adaptörlerin ortak arayüzü uygulaması; başarılı kart ödemesi; kart bilgisi yoksa red; kapıda ödemede kayıt açılması; sıfır tutarın reddi. |
| `tests/test_indirim.py` | Strategy | 6 | İndirimsiz, öğrenci, kupon ve saatlik kampanya hesapları; stratejinin çalışma anında değişmesi; teslimat ücretinin indirimden sonra eklenmesi. |
| `tests/test_bildirim.py` | Observer | 3 | Her durum değişikliğinde müşteri, mutfak ve kuryeye bildirim gitmesi; kuryenin gel-al siparişini dinlememesi; çıkarılan gözlemcinin bildirim almaması. |

## Örnek Hesaplar

| Sipariş | Strateji | Ara toplam | Ödenecek |
| --- | --- | --- | --- |
| Pide 150 + Künefe 110 (gel-al) | İndirim yok | 260 TL | 260 TL |
| Aynı sipariş | Öğrenci (%15) | 260 TL | 221 TL |
| Aynı sipariş | Kupon 50 TL (200 TL üstü) | 260 TL | 210 TL |
| Aynı sipariş | Saatlik kampanya (%20, saat 15) | 260 TL | 208 TL |
| Lahmacun 90 + Ayran 25 (paket) | Öğrenci (%15) + 30 TL teslimat | 115 TL | 127,75 TL |
