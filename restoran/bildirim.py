"""Observer kalıbı: sipariş durumu değişince ilgili taraflara haber verilir."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from restoran.siparis import Siparis


# [Observer] Observer
class SiparisGozlemcisi(ABC):
    @abstractmethod
    def guncelle(self, siparis: Siparis) -> None:
        """Sipariş durumu değiştiğinde çağrılır."""


# [Observer] Subject
class SiparisYayincisi(ABC):
    @abstractmethod
    def ekle(self, gozlemci: SiparisGozlemcisi) -> None: ...

    @abstractmethod
    def cikar(self, gozlemci: SiparisGozlemcisi) -> None: ...

    @abstractmethod
    def bildir(self) -> None: ...


class _MesajTutanGozlemci(SiparisGozlemcisi):
    """Somut gözlemcilerin ortak kısmı: mesajı saklar ve ekrana yazar."""

    etiket = ""

    def __init__(self, sessiz: bool = False) -> None:
        self.mesajlar: list[str] = []
        self.sessiz = sessiz

    def guncelle(self, siparis: Siparis) -> None:
        mesaj = self.mesaj_olustur(siparis)
        self.mesajlar.append(mesaj)
        if not self.sessiz:
            print(f"  [{self.etiket}] {mesaj}")

    @abstractmethod
    def mesaj_olustur(self, siparis: Siparis) -> str: ...


# [Observer] ConcreteObserver
class MusteriBildirimi(_MesajTutanGozlemci):
    etiket = "Müşteri"

    def mesaj_olustur(self, siparis: Siparis) -> str:
        return f"Sayın {siparis.musteri}, #{siparis.no} numaralı siparişiniz: {siparis.durum_adi}"


# [Observer] ConcreteObserver
class MutfakEkrani(_MesajTutanGozlemci):
    etiket = "Mutfak"

    def mesaj_olustur(self, siparis: Siparis) -> str:
        urunler = ", ".join(u.ad for u in siparis.urunler)
        return f"#{siparis.no} ({siparis.tur_adi}) -> {siparis.durum_adi} | {urunler}"


# [Observer] ConcreteObserver
class KuryeBildirimi(_MesajTutanGozlemci):
    etiket = "Kurye"

    def guncelle(self, siparis: Siparis) -> None:
        # Kurye yalnızca kendisini ilgilendiren paket servis siparişlerini dinler.
        if siparis.kurye_gerekir:
            super().guncelle(siparis)

    def mesaj_olustur(self, siparis: Siparis) -> str:
        return f"#{siparis.no} -> {siparis.durum_adi} | Adres: {siparis.adres}"
