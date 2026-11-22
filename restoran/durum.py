"""State kalıbı: siparişin her durumu kendi kurallarını kendi sınıfında taşır.

Akış: Alındı -> Hazırlanıyor -> (Yolda) -> Teslim Edildi, ya da İptal.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restoran.siparis import Siparis, Urun


class GecersizIslemHatasi(Exception):
    """Siparişin o anki durumunda izin verilmeyen bir işlem istendi."""


# [State] State
class SiparisDurumu(ABC):
    @property
    @abstractmethod
    def ad(self) -> str: ...

    # Varsayılan olarak hiçbir işleme izin verilmez; her durum yalnızca
    # kendisinde geçerli olan işlemleri yeniden tanımlar.
    def urun_ekle(self, siparis: Siparis, urun: Urun) -> None:
        self._reddet("ürün eklenemez")

    def hazirla(self, siparis: Siparis) -> None:
        self._reddet("hazırlığa alınamaz")

    def yola_cikar(self, siparis: Siparis) -> None:
        self._reddet("yola çıkarılamaz")

    def teslim_et(self, siparis: Siparis) -> None:
        self._reddet("teslim edilemez")

    def iptal_et(self, siparis: Siparis) -> None:
        self._reddet("iptal edilemez")

    def _reddet(self, islem: str) -> None:
        raise GecersizIslemHatasi(f"'{self.ad}' durumundaki sipariş {islem}.")


# [State] ConcreteState
class AlindiDurumu(SiparisDurumu):
    ad = "Alındı"

    def urun_ekle(self, siparis: Siparis, urun: Urun) -> None:
        siparis.urunler.append(urun)

    def hazirla(self, siparis: Siparis) -> None:
        if not siparis.urunler:
            raise GecersizIslemHatasi("Boş sipariş hazırlığa alınamaz.")
        siparis.durum_degistir(HazirlaniyorDurumu())

    def iptal_et(self, siparis: Siparis) -> None:
        siparis.durum_degistir(IptalDurumu())


# [State] ConcreteState
class HazirlaniyorDurumu(SiparisDurumu):
    ad = "Hazırlanıyor"

    def yola_cikar(self, siparis: Siparis) -> None:
        if not siparis.kurye_gerekir:
            self._reddet("yola çıkarılamaz (kurye gerektirmeyen sipariş)")
        siparis.durum_degistir(YoldaDurumu())

    def teslim_et(self, siparis: Siparis) -> None:
        if siparis.kurye_gerekir:
            self._reddet("kuryeye verilmeden teslim edilemez")
        siparis.durum_degistir(TeslimEdildiDurumu())

    def iptal_et(self, siparis: Siparis) -> None:
        siparis.durum_degistir(IptalDurumu())


# [State] ConcreteState
class YoldaDurumu(SiparisDurumu):
    ad = "Yolda"

    def teslim_et(self, siparis: Siparis) -> None:
        siparis.durum_degistir(TeslimEdildiDurumu())


# [State] ConcreteState
class TeslimEdildiDurumu(SiparisDurumu):
    ad = "Teslim Edildi"


# [State] ConcreteState
class IptalDurumu(SiparisDurumu):
    ad = "İptal Edildi"
