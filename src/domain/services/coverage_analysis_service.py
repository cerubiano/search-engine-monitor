from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from src.domain.exceptions import CoverageAnalysisError
from src.domain.models.snapshot_model import SnapshotModel, Segment


class CoverageAnalysisService:

    def analyze(
        self,
        raw_response: dict[str, Any],
        origin: str,
        destination: str,
        departure_date: date,
        snapshot_at: datetime,
        segment: Segment,
    ) -> SnapshotModel:

        offers = raw_response.get("data", [])

        if not offers:
            raise CoverageAnalysisError(
                f"No offers found for {origin} → {destination} "
                f"on {departure_date}"
            )

        total_offers = len(offers)

        unique_carriers = len({
            offer["validatingAirlineCodes"][0]
            for offer in offers
        })

        direct_flights = sum(
            1 for offer in offers
            if len(offer["itineraries"][0]["segments"]) == 1
        )
        connecting_flights = total_offers - direct_flights

        prices = [
            Decimal(offer["price"]["grandTotal"])
            for offer in offers
        ]
        price_min = min(prices)
        price_max = max(prices)
        price_avg = (sum(prices) / len(prices)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        currency = offers[0]["price"]["currency"]

        days_in_advance = (departure_date - snapshot_at.date()).days

        return SnapshotModel(
            snapshot_at=snapshot_at,
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            days_in_advance=days_in_advance,
            segment=segment,
            total_offers=total_offers,
            unique_carriers=unique_carriers,
            direct_flights=direct_flights,
            connecting_flights=connecting_flights,
            price_min=price_min,
            price_avg=price_avg,
            price_max=price_max,
            currency=currency,
        )
