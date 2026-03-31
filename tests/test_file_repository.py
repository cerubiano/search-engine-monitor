import pytest
import json
import pandas as pd
from pathlib import Path
from src.adapters.repositories.file_repository import FileRepository
from src.domain.exceptions import RepositoryError


class TestFileRepository:

    def test_save_bronze_creates_file(self, tmp_path):
        repo = FileRepository(base_path=tmp_path)
        data = {"data": [{"price": {"grandTotal": "200.00"}}]}
        repo.save_bronze(data=data, filename="20260324_100000_amadeus.json")
        assert (tmp_path / "bronze" / "20260324_100000_amadeus.json").exists()

    def test_save_bronze_content_is_unchanged(self, tmp_path):
        repo = FileRepository(base_path=tmp_path)
        data = {"data": [{"price": {"grandTotal": "200.00"}}]}
        repo.save_bronze(data=data, filename="20260324_100000_amadeus.json")
        saved = json.loads(
            (tmp_path / "bronze" / "20260324_100000_amadeus.json").read_text()
        )
        assert saved == data

    def test_save_silver_creates_parquet_file(self, tmp_path):
        repo = FileRepository(base_path=tmp_path)
        data = {"origin": "YUL", "destination": "LAX", "total_offers": 5}
        repo.save_silver(data=data, filename="20260324_100000_snapshot.parquet")
        assert (tmp_path / "silver" / "20260324_100000_snapshot.parquet").exists()

    def test_save_gold_creates_parquet_file(self, tmp_path):
        repo = FileRepository(base_path=tmp_path)
        data = {"origin": "YUL", "destination": "LAX", "is_coverage_anomaly": False}
        repo.save_gold(data=data, filename="20260324_100000_metrics.parquet")
        assert (tmp_path / "gold" / "20260324_100000_metrics.parquet").exists()

    def test_raises_repository_error_when_path_is_invalid(self):
        repo = FileRepository(base_path=Path("/invalid/path/that/does/not/exist"))
        with pytest.raises(RepositoryError):
            repo.save_bronze(data={}, filename="test.json")
