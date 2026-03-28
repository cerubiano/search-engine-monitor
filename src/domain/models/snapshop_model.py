from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


class Segment(str, Enum):
    DOMESTIC = "domestic"
    SHORT_INTERNATIONAL = "short_international"
    LONG_INTERNATIONAL = "long_international"


class SnapshotModel(BaseModel):
    # Search parameters
    snapshot_at: datetime
    origin: str
    destination: str
    departure_date: date
    days_in_advance: int
    segment: Segment

    # Coverage
    total_offers: int
    unique_carriers: int
    direct_flights: int
    connecting_flights: int

    # Price
    price_min: Optional[Decimal]
    price_avg: Optional[Decimal]
    price_max: Optional[Decimal]
    currency: Optional[str]

    # Quality
    avg_dq_score: Optional[Decimal]

    # Anomaly flags
    is_coverage_anomaly: bool = False
    is_price_anomaly: bool = False

    @field_validator("origin", "destination")
    @classmethod
    def must_be_iata(cls, v: str) -> str:
        if len(v) != 3 or not v.isalpha():
            raise ValueError("Must be a valid IATA code (3 letters)")
        return v.upper()

    @field_validator("days_in_advance")
    @classmethod
    def must_be_positive(cls, v: int) -> int:
        if v < 0:
            raise ValueError("days_in_advance must be zero or positive")
        return v