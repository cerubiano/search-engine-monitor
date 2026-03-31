from typing import Any

import psycopg2

from src.domain.exceptions import RepositoryError
from src.domain.ports.repository_port import RepositoryPort

INSERT_SNAPSHOT = """
    INSERT INTO search_snapshots (
        snapshot_at, origin, destination, departure_date,
        days_in_advance, segment, total_offers, unique_carriers,
        direct_flights, connecting_flights, price_min, price_avg,
        price_max, currency, is_coverage_anomaly, is_price_anomaly
    ) VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
"""


class PostgresRepository(RepositoryPort):

    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        self._host = host
        self._port = port
        self._dbname = dbname
        self._user = user
        self._password = password

    def save_bronze(self, data: dict[str, Any], filename: str) -> None:
        raise NotImplementedError("save_bronze is handled by FileRepository")

    def save_silver(self, data: dict[str, Any], filename: str) -> None:
        raise NotImplementedError("save_silver is handled by FileRepository")

    def save_gold(self, data: dict[str, Any], filename: str) -> None:
        raise NotImplementedError("save_gold is handled by FileRepository")

    def save_snapshot(self, snapshot: dict[str, Any]) -> None:
        try:
            with psycopg2.connect(
                host=self._host,
                port=self._port,
                dbname=self._dbname,
                user=self._user,
                password=self._password,
            ) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        INSERT_SNAPSHOT,
                        (
                            snapshot["snapshot_at"],
                            snapshot["origin"],
                            snapshot["destination"],
                            snapshot["departure_date"],
                            snapshot["days_in_advance"],
                            snapshot["segment"],
                            snapshot["total_offers"],
                            snapshot["unique_carriers"],
                            snapshot["direct_flights"],
                            snapshot["connecting_flights"],
                            snapshot["price_min"],
                            snapshot["price_avg"],
                            snapshot["price_max"],
                            snapshot["currency"],
                            snapshot["is_coverage_anomaly"],
                            snapshot["is_price_anomaly"],
                        ),
                    )
                conn.commit()
        except psycopg2.OperationalError as e:
            raise RepositoryError(f"PostgreSQL connection failed: {e}") from e
        except psycopg2.Error as e:
            raise RepositoryError(f"PostgreSQL operation failed: {e}") from e
