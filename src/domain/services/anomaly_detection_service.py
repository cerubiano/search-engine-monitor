from src.domain.exceptions import AnomalyDetectionError
from src.domain.models.snapshot_model import SnapshotModel

MIN_OFFERS_THRESHOLD = 3
MIN_CARRIERS_THRESHOLD = 2
MAX_PRICE_SPREAD_RATIO = 5


class AnomalyDetectionService:

    def detect(self, snapshot: SnapshotModel) -> SnapshotModel:

        if snapshot is None:
            raise AnomalyDetectionError("Snapshot cannot be None")

        is_coverage_anomaly = (
            snapshot.total_offers < MIN_OFFERS_THRESHOLD
            or snapshot.unique_carriers < MIN_CARRIERS_THRESHOLD
        )

        is_price_anomaly = False
        if snapshot.price_min is not None and snapshot.price_min > 0:
            is_price_anomaly = (
                snapshot.price_max / snapshot.price_min > MAX_PRICE_SPREAD_RATIO
            )

        return snapshot.model_copy(update={
            "is_coverage_anomaly": is_coverage_anomaly,
            "is_price_anomaly": is_price_anomaly,
        })
