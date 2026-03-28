from abc import ABC, abstractmethod
from typing import Any


class RepositoryPort(ABC):

    @abstractmethod
    def save_bronze(self, data: dict[str, Any], filename: str) -> None:
        """
        Save raw API response to Bronze layer.

        Args:
            data: Raw API response as dictionary
            filename: Target filename

        Raises:
            RepositoryError: When the save operation fails
        """

    @abstractmethod
    def save_silver(self, data: dict[str, Any], filename: str) -> None:
        """
        Save normalized snapshot to Silver layer.

        Args:
            data: Normalized snapshot as dictionary
            filename: Target filename

        Raises:
            RepositoryError: When the save operation fails
        """

    @abstractmethod
    def save_gold(self, data: dict[str, Any], filename: str) -> None:
        """
        Save metrics and anomaly flags to Gold layer.

        Args:
            data: Metrics and anomaly flags as dictionary
            filename: Target filename

        Raises:
            RepositoryError: When the save operation fails
        """

    @abstractmethod
    def save_snapshot(self, snapshot: dict[str, Any]) -> None:
        """
        Persist snapshot to PostgreSQL.

        Args:
            snapshot: Snapshot data as dictionary

        Raises:
            RepositoryError: When the database operation fails
        """