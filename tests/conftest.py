import pytest
from datetime import datetime, date
from decimal import Decimal

from src.domain.models.snapshot_model import SnapshotModel, Segment


@pytest.fixture
def raw_amadeus_response():
    return {
        "data": [
            {
                "itineraries": [
                    {"segments": [{"departure": {"iataCode": "YUL"}}]}
                ],
                "price": {"grandTotal": "200.00", "currency": "EUR"},
                "validatingAirlineCodes": ["AC"]
            },
            {
                "itineraries": [
                    {"segments": [{"departure": {"iataCode": "YUL"}}]}
                ],
                "price": {"grandTotal": "300.00", "currency": "EUR"},
                "validatingAirlineCodes": ["AC"]
            },
            {
                "itineraries": [
                    {"segments": [
                        {"departure": {"iataCode": "YUL"}},
                        {"departure": {"iataCode": "YVR"}}
                    ]}
                ],
                "price": {"grandTotal": "500.00", "currency": "EUR"},
                "validatingAirlineCodes": ["WS"]
            },
        ]
    }


@pytest.fixture
def valid_snapshot():
    return SnapshotModel(
        snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
        origin="YUL",
        destination="LAX",
        departure_date=date(2026, 4, 24),
        days_in_advance=31,
        segment=Segment.SHORT_INTERNATIONAL,
        total_offers=10,
        unique_carriers=4,
        direct_flights=6,
        connecting_flights=4,
        price_min=Decimal("200.00"),
        price_avg=Decimal("350.00"),
        price_max=Decimal("800.00"),
        currency="EUR",
        is_coverage_anomaly=False,
        is_price_anomaly=False,
    )


@pytest.fixture
def anomaly_snapshot():
    return SnapshotModel(
        snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
        origin="YUL",
        destination="YYZ",
        departure_date=date(2026, 4, 24),
        days_in_advance=31,
        segment=Segment.DOMESTIC,
        total_offers=2,
        unique_carriers=1,
        direct_flights=2,
        connecting_flights=0,
        price_min=Decimal("100.00"),
        price_avg=Decimal("350.00"),
        price_max=Decimal("600.00"),
        currency="EUR",
        is_coverage_anomaly=False,
        is_price_anomaly=False,
    )
