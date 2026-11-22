import unittest

from restoran.bildirim import KuryeBildirimi, MusteriBildirimi, MutfakEkrani
from restoran.fabrika import GelAlOlusturucu, PaketServisOlusturucu


class ObserverTestleri(unittest.TestCase):
    def setUp(self):
        self.musteri = MusteriBildirimi(sessiz=True)
        self.mutfak = MutfakEkrani(sessiz=True)
        self.kurye = KuryeBildirimi(sessiz=True)
        self.gozlemciler = [self.musteri, self.mutfak, self.kurye]

    def test_her_durum_degisikliginde_bildirim_gider(self):
        paket = PaketServisOlusturucu("Adres").yeni_siparis("A", self.gozlemciler)
        paket.urun_ekle("Lahmacun", 90)
        paket.hazirla()
        paket.yola_cikar()
        paket.teslim_et()
        self.assertEqual(len(self.musteri.mesajlar), 3)
        self.assertEqual(len(self.mutfak.mesajlar), 3)
        self.assertEqual(len(self.kurye.mesajlar), 3)
        self.assertIn("Teslim Edildi", self.musteri.mesajlar[-1])

    def test_kurye_gel_al_siparisini_dinlemez(self):
        gel_al = GelAlOlusturucu().yeni_siparis("B", self.gozlemciler)
        gel_al.urun_ekle("Tost", 60)
        gel_al.hazirla()
        self.assertEqual(len(self.musteri.mesajlar), 1)
        self.assertEqual(self.kurye.mesajlar, [])

    def test_cikarilan_gozlemci_bildirim_almaz(self):
        gel_al = GelAlOlusturucu().yeni_siparis("B", self.gozlemciler)
        gel_al.cikar(self.mutfak)
        gel_al.urun_ekle("Tost", 60)
        gel_al.hazirla()
        self.assertEqual(self.mutfak.mesajlar, [])


if __name__ == "__main__":
    unittest.main()
