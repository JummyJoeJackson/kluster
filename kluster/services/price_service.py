from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json
import math
from random import Random

from kluster.models import db, PriceCache

@dataclass
class PricePoint:
    t: int
    value: float

class PriceService:
    TTL_HOURS = 12

    @staticmethod
    def _generate_series(item_id: int, base: float, periods: int = 12) -> list[PricePoint]:
        rng = Random(item_id or 42)
        series: list[PricePoint] = []
        val = base if base > 0 else 100.0
        for t in range(periods):
            drift = math.sin(t / 3.0) * (base * 0.03 if base else 3.0)
            noise = rng.uniform(-1.0, 1.0) * (base * 0.02 if base else 2.0)
            val = max(0.0, val + drift + noise)
            series.append(PricePoint(t=t, value=round(val, 2)))
        return series

    @staticmethod
    def get_series(item_id: int, base: float, periods: int = 12, currency: str = "USD") -> list[PricePoint]:
        cached = PriceCache.query.filter_by(item_id=item_id, currency=currency).first()
        now = datetime.utcnow()
        if cached and (now - cached.refreshed_at) < timedelta(hours=PriceService.TTL_HOURS):
            data = json.loads(cached.series_json)
            return [PricePoint(**p) for p in data]

        series = PriceService._generate_series(item_id, base, periods)
        payload = json.dumps([asdict(p) for p in series])
        if cached:
            cached.series_json = payload
            cached.refreshed_at = now
        else:
            cached = PriceCache(item_id=item_id, series_json=payload, currency=currency, refreshed_at=now)
            db.session.add(cached)
        db.session.commit()
        return series
