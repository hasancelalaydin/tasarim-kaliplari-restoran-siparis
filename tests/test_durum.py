import unittest

from restoran.durum import GecersizIslemHatasi
from restoran.fabrika import GelAlOlusturucu, PaketServisOlusturucu


class StateTestleri(unittest.TestCase):
    def setUp(self):
        self.paket = PaketServisOlusturucu("Adres").yeni_siparis("A")
        self.paket.urun_ekle("Lahmacun", 90)

    def test_paket_servis_tam_akis(self):
        self.assertEqual(self.paket.durum_adi, "Alındı")
        self.paket.hazirla()
        self.assertEqual(self.paket.durum_adi, "Hazırlanıyor")
        self.paket.yola_cikar()
        self.assertEqual(self.paket.durum_adi, "Yolda")
        self.paket.teslim_et()
        self.assertEqual(self.paket.durum_adi, "Teslim Edildi")

    def test_gel_al_yola_cikmadan_teslim_edilir(self):
        gel_al = GelAlOlusturucu().yeni_siparis("B")
        gel_al.urun_ekle("Köfte", 120)
        gel_al.hazirla()
        with self.assertRaises(GecersizIslemHatasi):
            gel_al.yola_cikar()
        gel_al.teslim_et()
        self.assertEqual(gel_al.durum_adi, "Teslim Edildi")

    def test_paket_servis_kuryesiz_teslim_edilemez(self):
        self.paket.hazirla()
        with self.assertRaises(GecersizIslemHatasi):
            self.paket.teslim_et()

    def test_yoldaki_siparis_iptal_edilemez(self):
        self.paket.hazirla()
        self.paket.yola_cikar()
        with self.assertRaises(GecersizIslemHatasi):
            self.paket.iptal_et()

    def test_hazirlanan_siparise_urun_eklenemez(self):
        self.paket.hazirla()
        with self.assertRaises(GecersizIslemHatasi):
            self.paket.urun_ekle("Ayran", 25)

    def test_bos_siparis_hazirlanamaz(self):
        bos = GelAlOlusturucu().yeni_siparis("C")
        with self.assertRaises(GecersizIslemHatasi):
            bos.hazirla()

    def test_iptal_edilen_siparis_ilerleyemez(self):
        self.paket.iptal_et()
        self.assertEqual(self.paket.durum_adi, "İptal Edildi")
        with self.assertRaises(GecersizIslemHatasi):
            self.paket.hazirla()


if __name__ == "__main__":
    unittest.main()
