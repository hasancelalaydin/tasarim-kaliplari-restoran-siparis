"""Factory Method kalıbı: sipariş türüne göre doğru sipariş nesnesi oluşturulur.

İstemci kod somut sipariş sınıflarını bilmez; yalnızca bir oluşturucu ile çalışır.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from restoran.bildirim import SiparisGozlemcisi
from restoran.siparis import GelAlSiparisi, MasaSiparisi, PaketServisSiparisi, Siparis


# [Factory Method] Creator
class SiparisOlusturucu(ABC):
    @abstractmethod
    def siparis_olustur(self, musteri: str) -> Siparis:
        """Factory method: alt sınıf hangi siparişin üretileceğine karar verir."""

    def yeni_siparis(
        self, musteri: str, gozlemciler: Iterable[SiparisGozlemcisi] = ()
    ) -> Siparis:
        siparis = self.siparis_olustur(musteri)
        for gozlemci in gozlemciler:
            siparis.ekle(gozlemci)
        return siparis


# [Factory Method] ConcreteCreator
class PaketServisOlusturucu(SiparisOlusturucu):
    def __init__(self, adres: str) -> None:
        self.adres = adres

    def siparis_olustur(self, musteri: str) -> Siparis:
        return PaketServisSiparisi(musteri, self.adres)


# [Factory Method] ConcreteCreator
class GelAlOlusturucu(SiparisOlusturucu):
    def siparis_olustur(self, musteri: str) -> Siparis:
        return GelAlSiparisi(musteri)


# [Factory Method] ConcreteCreator
class MasaOlusturucu(SiparisOlusturucu):
    def __init__(self, masa_no: int) -> None:
        self.masa_no = masa_no

    def siparis_olustur(self, musteri: str) -> Siparis:
        return MasaSiparisi(musteri, self.masa_no)
