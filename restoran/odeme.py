"""Adapter kalıbı: arayüzleri farklı dış ödeme servisleri tek bir arayüze uyarlanır."""

from __future__ import annotations

import itertools
from abc import ABC, abstractmethod


# [Adapter] Target
class OdemeIslemcisi(ABC):
    @abstractmethod
    def ode(self, tutar: float) -> bool:
        """Tutarı tahsil eder; başarılıysa True döner."""


# --- Dış servisler (değiştiremediğimiz kod, burada benzetim olarak yazıldı) ---

# [Adapter] Adaptee
class KartServisiApi:
    """Kredi kartı sağlayıcısının kütüphanesi: kuruş cinsinden çalışır, sözlük döner."""

    _islem_no = itertools.count(1000)

    def charge(self, amount_cents: int, card_token: str) -> dict:
        if amount_cents <= 0 or not card_token:
            return {"status": "declined", "id": None}
        return {"status": "approved", "id": next(self._islem_no)}


# [Adapter] Adaptee
class KapidaOdemeSistemi:
    """Kapıda ödeme kayıt sistemi: tahsilat kaydı açar, kayıt numarası döner."""

    def __init__(self) -> None:
        self.kayitlar: list[tuple[int, float]] = []

    def tahsilat_kaydi_olustur(self, miktar_tl: float) -> int:
        kayit_no = len(self.kayitlar) + 1
        self.kayitlar.append((kayit_no, miktar_tl))
        return kayit_no


# [Adapter] Adapter
class KartOdemeAdaptoru(OdemeIslemcisi):
    def __init__(self, api: KartServisiApi, kart_token: str) -> None:
        self._api = api
        self._kart_token = kart_token

    def ode(self, tutar: float) -> bool:
        sonuc = self._api.charge(round(tutar * 100), self._kart_token)
        return sonuc["status"] == "approved"


# [Adapter] Adapter
class KapidaOdemeAdaptoru(OdemeIslemcisi):
    def __init__(self, sistem: KapidaOdemeSistemi) -> None:
        self._sistem = sistem

    def ode(self, tutar: float) -> bool:
        if tutar <= 0:
            return False
        self._sistem.tahsilat_kaydi_olustur(tutar)
        return True
