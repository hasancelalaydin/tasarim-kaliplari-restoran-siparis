import unittest

from restoran.fabrika import GelAlOlusturucu, PaketServisOlusturucu
from restoran.indirim import (
    FiyatHesaplayici,
    IndirimYok,
    KuponIndirimi,
    OgrenciIndirimi,
    SaatlikKampanya,
)


class StrategyTestleri(unittest.TestCase):
    def setUp(self):
        self.siparis = GelAlOlusturucu().yeni_siparis("A")
        self.siparis.urun_ekle("Pide", 150)
        self.siparis.urun_ekle("Künefe", 110)  # ara toplam 260

    def test_indirimsiz(self):
        self.assertEqual(FiyatHesaplayici(IndirimYok()).hesapla(self.siparis), 260.0)

    def test_ogrenci_indirimi(self):
        self.assertEqual(FiyatHesaplayici(OgrenciIndirimi()).hesapla(self.siparis), 221.0)

    def test_kupon_alt_limiti_gecince_uygulanir(self):
        self.assertEqual(FiyatHesaplayici(KuponIndirimi(50, alt_limit=200)).hesapla(self.siparis), 210.0)
        self.assertEqual(FiyatHesaplayici(KuponIndirimi(50, alt_limit=300)).hesapla(self.siparis), 260.0)

    def test_saatlik_kampanya_yalnizca_kampanya_saatinde(self):
        self.assertEqual(FiyatHesaplayici(SaatlikKampanya(saat=15)).hesapla(self.siparis), 208.0)
        self.assertEqual(FiyatHesaplayici(SaatlikKampanya(saat=20)).hesapla(self.siparis), 260.0)

    def test_strateji_calisma_aninda_degisir(self):
        hesaplayici = FiyatHesaplayici()
        self.assertEqual(hesaplayici.hesapla(self.siparis), 260.0)
        hesaplayici.strateji_degistir(OgrenciIndirimi())
        self.assertEqual(hesaplayici.hesapla(self.siparis), 221.0)

    def test_teslimat_ucreti_indirimden_sonra_eklenir(self):
        paket = PaketServisOlusturucu("Adres").yeni_siparis("B")
        paket.urun_ekle("Lahmacun", 90)
        paket.urun_ekle("Ayran", 25)  # 115 - %15 = 97.75 + 30
        self.assertEqual(FiyatHesaplayici(OgrenciIndirimi()).hesapla(paket), 127.75)


if __name__ == "__main__":
    unittest.main()
