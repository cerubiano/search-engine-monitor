import requests
from typing import Any

from src.domain.exceptions import AdapterError
from src.domain.ports.provider_port import ProviderPort

AMADEUS_TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_SEARCH_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"


class AmadeusAdapter(ProviderPort):

    def __init__(self, api_key: str, api_secret: str):
        self._api_key = api_key
        self._api_secret = api_secret

    def _get_token(self) -> str:
        try:
            response = requests.post(
                AMADEUS_TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._api_key,
                    "client_secret": self._api_secret,
                },
            )
            if response.status_code != 200:
                raise AdapterError(
                    f"Failed to get Amadeus token: HTTP {response.status_code}"
                )
            data = response.json()
            if "access_token" not in data:
                raise AdapterError("Amadeus token response missing access_token")
            return data["access_token"]
        except requests.exceptions.RequestException as e:
            raise AdapterError(f"Amadeus token request failed: {e}")

    def search_flights(
        self,
        origin: str,
        destination: str,
        departure_date: str,
    ) -> dict[str, Any]:
        try:
            token = self._get_token()
            response = requests.get(
                AMADEUS_SEARCH_URL,
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "originLocationCode": origin,
                    "destinationLocationCode": destination,
                    "departureDate": departure_date,
                    "adults": 1,
                    "travelClass": "ECONOMY",
                },
            )
            if response.status_code != 200:
                raise AdapterError(
                    f"Amadeus search failed for {origin}→{destination}: "
                    f"HTTP {response.status_code}"
                )
            return response.json()
        except requests.exceptions.Timeout:
            raise AdapterError(
                f"Amadeus search timed out for {origin}→{destination}"
            )
        except requests.exceptions.RequestException as e:
            raise AdapterError(f"Amadeus search request failed: {e}")
