import pytest
from decimal import Decimal
from src.domain.services.anomaly_detection_service import AnomalyDetectionService
from src.domain.models.snapshot_model import SnapshotModel


class TestAnomalyDetectionService:

    def test_returns_snapshot_model(self, valid_snapshot):
        service = AnomalyDetectionService()
        result = service.detect(valid_snapshot)
        assert isinstance(result, SnapshotModel)

    def test_no_coverage_anomaly_when_offers_and_carriers_are_sufficient(self, valid_snapshot):
        service = AnomalyDetectionService()
        result = service.detect(valid_snapshot)
        assert result.is_coverage_anomaly is False

    def test_coverage_anomaly_when_total_offers_below_threshold(self, anomaly_snapshot):
        service = AnomalyDetectionService()
        result = service.detect(anomaly_snapshot)
        assert result.is_coverage_anomaly is True

    def test_coverage_anomaly_when_unique_carriers_below_threshold(self, anomaly_snapshot):
        service = AnomalyDetectionService()
        result = service.detect(anomaly_snapshot)
        assert result.is_coverage_anomaly is True

    def test_no_price_anomaly_when_spread_is_acceptable(self, valid_snapshot):
        service = AnomalyDetectionService()
        result = service.detect(valid_snapshot)
        assert result.is_price_anomaly is False

    def test_price_anomaly_when_spread_exceeds_threshold(self, anomaly_snapshot):
        service = AnomalyDetectionService()
        result = service.detect(anomaly_snapshot)
        assert result.is_price_anomaly is True

    def test_no_price_anomaly_when_price_min_is_none(self, valid_snapshot):
        valid_snapshot.price_min = None
        service = AnomalyDetectionService()
        result = service.detect(valid_snapshot)
        assert result.is_price_anomaly is False
