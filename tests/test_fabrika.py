import unittest

from restoran.fabrika import GelAlOlusturucu, MasaOlusturucu, PaketServisOlusturucu
from restoran.bildirim import MusteriBildirimi
from restoran.siparis import GelAlSiparisi, MasaSiparisi, PaketServisSiparisi


class FactoryMethodTestleri(unittest.TestCase):
    def test_her_olusturucu_kendi_siparis_turunu_uretir(self):
        self.assertIsInstance(PaketServisOlusturucu("Adres").yeni_siparis("A"), PaketServisSiparisi)
        self.assertIsInstance(GelAlOlusturucu().yeni_siparis("B"), GelAlSiparisi)
        self.assertIsInstance(MasaOlusturucu(3).yeni_siparis("C"), MasaSiparisi)

    def test_paket_servis_adres_ve_teslimat_ucreti_tasir(self):
        siparis = PaketServisOlusturucu("Kampüs Cad. 5").yeni_siparis("A")
        self.assertEqual(siparis.adres, "Kampüs Cad. 5")
        self.assertTrue(siparis.kurye_gerekir)
        self.assertEqual(siparis.teslimat_ucreti, 30.0)

    def test_gel_al_ve_masa_kurye_gerektirmez(self):
        self.assertFalse(GelAlOlusturucu().yeni_siparis("B").kurye_gerekir)
        masa = MasaOlusturucu(7).yeni_siparis("C")
        self.assertFalse(masa.kurye_gerekir)
        self.assertEqual(masa.masa_no, 7)

    def test_olusturucu_gozlemcileri_siparise_baglar(self):
        musteri = MusteriBildirimi(sessiz=True)
        siparis = GelAlOlusturucu().yeni_siparis("B", [musteri])
        siparis.urun_ekle("Tost", 60)
        siparis.hazirla()
        self.assertEqual(len(musteri.mesajlar), 1)


if __name__ == "__main__":
    unittest.main()
