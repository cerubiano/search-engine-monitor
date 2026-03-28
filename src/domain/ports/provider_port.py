from abc import ABC, abstractmethod
from typing import Any


class ProviderPort(ABC):

    @abstractmethod
    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
    ) -> dict[str, Any]:
        """
        Search for flight offers between two airports.

        Args:
            origin: IATA origin airport code
            destination: IATA destination airport code
            departure_date: Departure date in YYYY-MM-DD format

        Returns:
            Raw API response as dictionary

        Raises:
            AdapterError: When the API call fails
        """