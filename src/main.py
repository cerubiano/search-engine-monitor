import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

import yaml
from dotenv import load_dotenv

from src.adapters.providers.amadeus_adapter import AmadeusAdapter
from src.adapters.repositories.file_repository import FileRepository
from src.adapters.repositories.postgres_repository import PostgresRepository
from src.domain.models.snapshot_model import Segment
from src.domain.services.anomaly_detection_service import AnomalyDetectionService
from src.domain.services.coverage_analysis_service import CoverageAnalysisService

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)
logger = logging.getLogger(__name__)


def load_config() -> dict:
    config_path = Path("config/routes.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_segment(segment_name: str) -> Segment:
    return Segment(segment_name)


def main() -> None:
    config = load_config()
    params = config["search_parameters"]
    routes = config["routes"]

    amadeus = AmadeusAdapter(
        api_key=os.getenv("AMADEUS_API_KEY"),
        api_secret=os.getenv("AMADEUS_API_SECRET"),
    )

    file_repo = FileRepository(base_path=Path("data"))

    postgres_repo = PostgresRepository(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        dbname=os.getenv("DB_NAME", "search_monitor"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    coverage_service = CoverageAnalysisService()
    anomaly_service = AnomalyDetectionService()

    snapshot_at = datetime.now()
    timestamp = snapshot_at.strftime("%Y%m%d_%H%M%S")

    for segment_name, segment_routes in routes.items():
        segment = get_segment(segment_name)

        for route in segment_routes:
            origin = route["origin"]
            destination = route["destination"]

            for days in params["days_in_advance"]:
                departure_date = (snapshot_at + timedelta(days=days)).date()

                logger.info(
                    "Processing %s → %s | departure: %s | days_in_advance: %d",
                    origin, destination, departure_date, days,
                )

                try:
                    raw_response = amadeus.search_flights(
                        origin=origin,
                        destination=destination,
                        departure_date=departure_date.isoformat(),
                    )

                    filename = f"{timestamp}_{origin}_{destination}_{days}d"
                    file_repo.save_bronze(
                        data=raw_response,
                        filename=f"{filename}_amadeus.json",
                    )

                    snapshot = coverage_service.analyze(
                        raw_response=raw_response,
                        origin=origin,
                        destination=destination,
                        departure_date=departure_date,
                        snapshot_at=snapshot_at,
                        segment=segment,
                    )

                    snapshot = anomaly_service.detect(snapshot)

                    snapshot_dict = snapshot.model_dump()
                    snapshot_dict["segment"] = snapshot.segment.value

                    file_repo.save_silver(
                        data=snapshot_dict,
                        filename=f"{filename}_snapshot.parquet",
                    )

                    file_repo.save_gold(
                        data=snapshot_dict,
                        filename=f"{filename}_metrics.parquet",
                    )

                    postgres_repo.save_snapshot(snapshot_dict)

                    logger.info(
                        "Saved snapshot %s → %s | offers: %d | anomaly: %s",
                        origin, destination,
                        snapshot.total_offers,
                        snapshot.is_coverage_anomaly or snapshot.is_price_anomaly,
                    )

                except Exception as e:
                    logger.error(
                        "Failed %s → %s | days: %d | error: %s",
                        origin, destination, days, e,
                    )
                    continue


if __name__ == "__main__":
    main()
