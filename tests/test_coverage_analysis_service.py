import pytest
from datetime import datetime, date
from decimal import Decimal

from src.domain.services.coverage_analysis_service import CoverageAnalysisService
from src.domain.models.snapshot_model import SnapshotModel, Segment
from src.domain.exceptions import CoverageAnalysisError


class TestCoverageAnalysisService:

    def test_builds_snapshot_from_raw_response(self, raw_amadeus_response):
        service = CoverageAnalysisService()
        result = service.analyze(
            raw_response=raw_amadeus_response,
            origin="YUL",
            destination="LAX",
            departure_date=date(2026, 4, 15),
            snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
            segment=Segment.SHORT_INTERNATIONAL,
        )
        assert isinstance(result, SnapshotModel)

    def test_counts_total_offers(self, raw_amadeus_response):
        service = CoverageAnalysisService()
        result = service.analyze(
            raw_response=raw_amadeus_response,
            origin="YUL",
            destination="LAX",
            departure_date=date(2026, 4, 15),
            snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
            segment=Segment.SHORT_INTERNATIONAL,
        )
        assert result.total_offers == 3

    def test_counts_unique_carriers(self, raw_amadeus_response):
        service = CoverageAnalysisService()
        result = service.analyze(
            raw_response=raw_amadeus_response,
            origin="YUL",
            destination="LAX",
            departure_date=date(2026, 4, 15),
            snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
            segment=Segment.SHORT_INTERNATIONAL,
        )
        assert result.unique_carriers == 2

    def test_counts_direct_and_connecting_flights(self, raw_amadeus_response):
        service = CoverageAnalysisService()
        result = service.analyze(
            raw_response=raw_amadeus_response,
            origin="YUL",
            destination="LAX",
            departure_date=date(2026, 4, 15),
            snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
            segment=Segment.SHORT_INTERNATIONAL,
        )
        assert result.direct_flights == 2
        assert result.connecting_flights == 1

    def test_calculates_price_metrics(self, raw_amadeus_response):
        service = CoverageAnalysisService()
        result = service.analyze(
            raw_response=raw_amadeus_response,
            origin="YUL",
            destination="LAX",
            departure_date=date(2026, 4, 15),
            snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
            segment=Segment.SHORT_INTERNATIONAL,
        )
        assert result.price_min == Decimal("200.00")
        assert result.price_avg == Decimal("333.33")
        assert result.price_max == Decimal("500.00")

    def test_calculates_days_in_advance(self, raw_amadeus_response):
        service = CoverageAnalysisService()
        result = service.analyze(
            raw_response=raw_amadeus_response,
            origin="YUL",
            destination="LAX",
            departure_date=date(2026, 4, 15),
            snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
            segment=Segment.SHORT_INTERNATIONAL,
        )
        assert result.days_in_advance == 22

    def test_raises_error_when_response_is_empty(self):
        service = CoverageAnalysisService()
        with pytest.raises(CoverageAnalysisError):
            service.analyze(
                raw_response={"data": []},
                origin="YUL",
                destination="LAX",
                departure_date=date(2026, 4, 15),
                snapshot_at=datetime(2026, 3, 24, 10, 0, 0),
                segment=Segment.SHORT_INTERNATIONAL,
            )
