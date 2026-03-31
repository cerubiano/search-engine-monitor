import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.domain.exceptions import RepositoryError
from src.domain.ports.repository_port import RepositoryPort


class FileRepository(RepositoryPort):

    def __init__(self, base_path: Path):
        self._base_path = base_path

    def save_bronze(self, data: dict[str, Any], filename: str) -> None:
        try:
            path = self._base_path / "bronze"
            path.mkdir(parents=True, exist_ok=True)
            (path / filename).write_text(json.dumps(data, indent=2))
        except OSError as e:
            raise RepositoryError(f"Failed to save Bronze file {filename}: {e}")

    def save_silver(self, data: dict[str, Any], filename: str) -> None:
        try:
            path = self._base_path / "silver"
            path.mkdir(parents=True, exist_ok=True)
            pd.DataFrame([data]).to_parquet(path / filename, compression="snappy")
        except OSError as e:
            raise RepositoryError(f"Failed to save Silver file {filename}: {e}")

    def save_gold(self, data: dict[str, Any], filename: str) -> None:
        try:
            path = self._base_path / "gold"
            path.mkdir(parents=True, exist_ok=True)
            pd.DataFrame([data]).to_parquet(path / filename, compression="snappy")
        except OSError as e:
            raise RepositoryError(f"Failed to save Gold file {filename}: {e}")

    def save_snapshot(self, snapshot: dict[str, Any]) -> None:
        pass
