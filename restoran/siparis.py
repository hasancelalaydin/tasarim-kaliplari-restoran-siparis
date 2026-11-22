"""Sipariş sınıfları.

Siparis aynı anda üç kalıpta rol alır:
- Factory Method: Product (somut alt sınıflar ConcreteProduct)
- State: Context (davranışını o anki durum nesnesine devreder)
- Observer: ConcreteSubject (durum değişince gözlemcilere haber verir)
"""

from __future__ import annotations

import itertools
from abc import abstractmethod
from dataclasses import dataclass

from restoran.bildirim import SiparisGozlemcisi, SiparisYayincisi
from restoran.durum import AlindiDurumu, SiparisDurumu

_siparis_no = itertools.count(1)


@dataclass(frozen=True)
class Urun:
    ad: str
    fiyat: float


# [Factory Method] Product · [State] Context · [Observer] ConcreteSubject
class Siparis(SiparisYayincisi):
    def __init__(self, musteri: str) -> None:
        self.no = next(_siparis_no)
        self.musteri = musteri
        self.urunler: list[Urun] = []
        self._gozlemciler: list[SiparisGozlemcisi] = []
        self._durum: SiparisDurumu = AlindiDurumu()

    # --- Factory Method alt sınıflarının doldurduğu bilgiler ---
    @property
    @abstractmethod
    def tur_adi(self) -> str: ...

    @property
    @abstractmethod
    def teslimat_ucreti(self) -> float: ...

    @property
    @abstractmethod
    def kurye_gerekir(self) -> bool: ...

    @property
    def adres(self) -> str:
        return "-"

    # --- State: işlemler o anki durum nesnesine devredilir ---
    @property
    def durum_adi(self) -> str:
        return self._durum.ad

    def urun_ekle(self, ad: str, fiyat: float) -> None:
        self._durum.urun_ekle(self, Urun(ad, fiyat))

    def hazirla(self) -> None:
        self._durum.hazirla(self)

    def yola_cikar(self) -> None:
        self._durum.yola_cikar(self)

    def teslim_et(self) -> None:
        self._durum.teslim_et(self)

    def iptal_et(self) -> None:
        self._durum.iptal_et(self)

    def durum_degistir(self, yeni_durum: SiparisDurumu) -> None:
        self._durum = yeni_durum
        self.bildir()

    def ara_toplam(self) -> float:
        return round(sum(u.fiyat for u in self.urunler), 2)

    # --- Observer ---
    def ekle(self, gozlemci: SiparisGozlemcisi) -> None:
        if gozlemci not in self._gozlemciler:
            self._gozlemciler.append(gozlemci)

    def cikar(self, gozlemci: SiparisGozlemcisi) -> None:
        if gozlemci in self._gozlemciler:
            self._gozlemciler.remove(gozlemci)

    def bildir(self) -> None:
        for gozlemci in list(self._gozlemciler):
            gozlemci.guncelle(self)


# [Factory Method] ConcreteProduct
class PaketServisSiparisi(Siparis):
    tur_adi = "Paket Servis"
    teslimat_ucreti = 30.0
    kurye_gerekir = True

    def __init__(self, musteri: str, adres: str) -> None:
        super().__init__(musteri)
        self._adres = adres

    @property
    def adres(self) -> str:
        return self._adres


# [Factory Method] ConcreteProduct
class GelAlSiparisi(Siparis):
    tur_adi = "Gel-Al"
    teslimat_ucreti = 0.0
    kurye_gerekir = False


# [Factory Method] ConcreteProduct
class MasaSiparisi(Siparis):
    tur_adi = "Masa"
    teslimat_ucreti = 0.0
    kurye_gerekir = False

    def __init__(self, musteri: str, masa_no: int) -> None:
        super().__init__(musteri)
        self.masa_no = masa_no
