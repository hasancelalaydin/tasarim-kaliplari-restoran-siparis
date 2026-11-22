import unittest

from restoran.odeme import (
    KapidaOdemeAdaptoru,
    KapidaOdemeSistemi,
    KartOdemeAdaptoru,
    KartServisiApi,
    OdemeIslemcisi,
)


class AdapterTestleri(unittest.TestCase):
    def test_adaptorler_ortak_arayuzu_uygular(self):
        self.assertIsInstance(KartOdemeAdaptoru(KartServisiApi(), "tok"), OdemeIslemcisi)
        self.assertIsInstance(KapidaOdemeAdaptoru(KapidaOdemeSistemi()), OdemeIslemcisi)

    def test_kart_odemesi_basarili(self):
        self.assertTrue(KartOdemeAdaptoru(KartServisiApi(), "tok").ode(127.75))

    def test_kart_bilgisi_yoksa_odeme_reddedilir(self):
        self.assertFalse(KartOdemeAdaptoru(KartServisiApi(), "").ode(50))

    def test_kapida_odeme_kayit_acar(self):
        sistem = KapidaOdemeSistemi()
        self.assertTrue(KapidaOdemeAdaptoru(sistem).ode(96.0))
        self.assertEqual(sistem.kayitlar, [(1, 96.0)])

    def test_sifir_tutar_odenemez(self):
        self.assertFalse(KapidaOdemeAdaptoru(KapidaOdemeSistemi()).ode(0))


if __name__ == "__main__":
    unittest.main()
