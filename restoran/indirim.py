"""Strategy kalıbı: indirim hesabı kampanyaya göre çalışma anında değiştirilir."""

from __future__ import annotations

from abc import ABC, abstractmethod

from restoran.siparis import Siparis


# [Strategy] Strategy
class IndirimStratejisi(ABC):
    @abstractmethod
    def indirim_hesapla(self, ara_toplam: float) -> float:
        """Ara toplamdan düşülecek indirim tutarını döner."""


# [Strategy] ConcreteStrategy
class IndirimYok(IndirimStratejisi):
    def indirim_hesapla(self, ara_toplam: float) -> float:
        return 0.0


# [Strategy] ConcreteStrategy
class OgrenciIndirimi(IndirimStratejisi):
    ORAN = 0.15

    def indirim_hesapla(self, ara_toplam: float) -> float:
        return ara_toplam * self.ORAN


# [Strategy] ConcreteStrategy
class KuponIndirimi(IndirimStratejisi):
    def __init__(self, tutar: float, alt_limit: float = 0.0) -> None:
        self.tutar = tutar
        self.alt_limit = alt_limit

    def indirim_hesapla(self, ara_toplam: float) -> float:
        if ara_toplam < self.alt_limit:
            return 0.0
        return min(self.tutar, ara_toplam)


# [Strategy] ConcreteStrategy
class SaatlikKampanya(IndirimStratejisi):
    """Belirli saatler arasında yüzde indirim (ör. 14:00-17:00 arası %20)."""

    def __init__(self, saat: int, baslangic: int = 14, bitis: int = 17, oran: float = 0.20) -> None:
        self.saat = saat
        self.baslangic = baslangic
        self.bitis = bitis
        self.oran = oran

    def indirim_hesapla(self, ara_toplam: float) -> float:
        if self.baslangic <= self.saat < self.bitis:
            return ara_toplam * self.oran
        return 0.0


# [Strategy] Context
class FiyatHesaplayici:
    def __init__(self, strateji: IndirimStratejisi | None = None) -> None:
        self._strateji = strateji or IndirimYok()

    def strateji_degistir(self, strateji: IndirimStratejisi) -> None:
        self._strateji = strateji

    def hesapla(self, siparis: Siparis) -> float:
        ara_toplam = siparis.ara_toplam()
        indirim = self._strateji.indirim_hesapla(ara_toplam)
        return round(max(ara_toplam - indirim, 0.0) + siparis.teslimat_ucreti, 2)
