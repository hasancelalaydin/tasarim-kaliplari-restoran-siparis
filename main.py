"""Örnek senaryo: beş kalıbın birlikte çalıştığı bir restoran günü.

Çalıştırma: python main.py
"""

from restoran.bildirim import KuryeBildirimi, MusteriBildirimi, MutfakEkrani
from restoran.durum import GecersizIslemHatasi
from restoran.fabrika import GelAlOlusturucu, MasaOlusturucu, PaketServisOlusturucu
from restoran.indirim import FiyatHesaplayici, KuponIndirimi, OgrenciIndirimi, SaatlikKampanya
from restoran.odeme import KapidaOdemeAdaptoru, KapidaOdemeSistemi, KartOdemeAdaptoru, KartServisiApi


def baslik(metin: str) -> None:
    print(f"\n=== {metin} ===")


def main() -> None:
    gozlemciler = [MusteriBildirimi(), MutfakEkrani(), KuryeBildirimi()]
    hesaplayici = FiyatHesaplayici()

    # 1) Paket servis: Factory Method + State + Observer + Strategy + Adapter
    baslik("Paket servis siparişi (öğrenci indirimi, kartla ödeme)")
    paket = PaketServisOlusturucu("Kampüs Cad. No:5").yeni_siparis("Ayşe", gozlemciler)
    paket.urun_ekle("Lahmacun", 90)
    paket.urun_ekle("Ayran", 25)
    hesaplayici.strateji_degistir(OgrenciIndirimi())
    tutar = hesaplayici.hesapla(paket)
    odeme = KartOdemeAdaptoru(KartServisiApi(), kart_token="tok_ayse")
    print(f"Ara toplam: {paket.ara_toplam()} TL, ödenecek: {tutar} TL, ödeme: "
          f"{'başarılı' if odeme.ode(tutar) else 'başarısız'}")
    paket.hazirla()
    paket.yola_cikar()
    try:
        paket.iptal_et()
    except GecersizIslemHatasi as hata:
        print(f"Hata: {hata}")
    paket.teslim_et()

    # 2) Gel-al: kurye gerekmez, kapıda (kasada) ödeme
    baslik("Gel-al siparişi (saatlik kampanya, kasada ödeme)")
    gel_al = GelAlOlusturucu().yeni_siparis("Mehmet", gozlemciler)
    gel_al.urun_ekle("Köfte Ekmek", 120)
    hesaplayici.strateji_degistir(SaatlikKampanya(saat=15))
    tutar = hesaplayici.hesapla(gel_al)
    kasada = KapidaOdemeAdaptoru(KapidaOdemeSistemi())
    print(f"Ara toplam: {gel_al.ara_toplam()} TL, ödenecek: {tutar} TL, ödeme: "
          f"{'başarılı' if kasada.ode(tutar) else 'başarısız'}")
    gel_al.hazirla()
    gel_al.teslim_et()

    # 3) Masa siparişi: kupon, sonra iptal
    baslik("Masa siparişi (kupon) ve iptal")
    masa = MasaOlusturucu(masa_no=7).yeni_siparis("Masa 7", gozlemciler)
    masa.urun_ekle("Pide", 150)
    masa.urun_ekle("Künefe", 110)
    hesaplayici.strateji_degistir(KuponIndirimi(tutar=50, alt_limit=200))
    print(f"Ara toplam: {masa.ara_toplam()} TL, ödenecek: {hesaplayici.hesapla(masa)} TL")
    masa.hazirla()
    masa.iptal_et()


if __name__ == "__main__":
    main()
