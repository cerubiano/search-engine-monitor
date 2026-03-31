import pytest
from unittest.mock import patch, Mock, MagicMock
from src.adapters.repositories.postgres_repository import PostgresRepository
from src.domain.exceptions import RepositoryError


class TestPostgresRepository:

    @patch("src.adapters.repositories.postgres_repository.psycopg2.connect")
    def test_save_snapshot_executes_insert(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        repo = PostgresRepository(
            host="localhost", port=5432, dbname="search_monitor",
            user="test", password="test"
        )
        repo.save_snapshot({
            "snapshot_at": "2026-03-24 10:00:00",
            "origin": "YUL",
            "destination": "LAX",
            "departure_date": "2026-04-15",
            "days_in_advance": 22,
            "segment": "short_international",
            "total_offers": 5,
            "unique_carriers": 2,
            "direct_flights": 3,
            "connecting_flights": 2,
            "price_min": 200.00,
            "price_avg": 350.00,
            "price_max": 500.00,
            "currency": "EUR",
            "is_coverage_anomaly": False,
            "is_price_anomaly": False,
        })

        assert mock_cursor.execute.called

    @patch("src.adapters.repositories.postgres_repository.psycopg2.connect")
    def test_save_snapshot_commits_after_insert(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)

        repo = PostgresRepository(
            host="localhost", port=5432, dbname="search_monitor",
            user="test", password="test"
        )
        repo.save_snapshot({
            "snapshot_at": "2026-03-24 10:00:00",
            "origin": "YUL",
            "destination": "LAX",
            "departure_date": "2026-04-15",
            "days_in_advance": 22,
            "segment": "short_international",
            "total_offers": 5,
            "unique_carriers": 2,
            "direct_flights": 3,
            "connecting_flights": 2,
            "price_min": 200.00,
            "price_avg": 350.00,
            "price_max": 500.00,
            "currency": "EUR",
            "is_coverage_anomaly": False,
            "is_price_anomaly": False,
        })

        assert mock_conn.commit.called

    @patch("src.adapters.repositories.postgres_repository.psycopg2.connect")
    def test_raises_repository_error_when_connection_fails(self, mock_connect):
        import psycopg2
        mock_connect.side_effect = psycopg2.OperationalError("Connection refused")

        repo = PostgresRepository(
            host="localhost", port=5432, dbname="search_monitor",
            user="test", password="test"
        )
        with pytest.raises(RepositoryError):
            repo.save_snapshot({"origin": "YUL"})

    @patch("src.adapters.repositories.postgres_repository.psycopg2.connect")
    def test_raises_repository_error_when_insert_fails(self, mock_connect):
        import psycopg2
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value.__enter__ = Mock(return_value=mock_conn)
        mock_connect.return_value.__exit__ = Mock(return_value=False)
        mock_conn.cursor.return_value.__enter__ = Mock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = Mock(return_value=False)
        mock_cursor.execute.side_effect = psycopg2.DatabaseError("Insert failed")

        repo = PostgresRepository(
            host="localhost", port=5432, dbname="search_monitor",
            user="test", password="test"
        )
        with pytest.raises(RepositoryError):
            repo.save_snapshot({
                "snapshot_at": "2026-03-24 10:00:00",
                "origin": "YUL",
                "destination": "LAX",
                "departure_date": "2026-04-15",
                "days_in_advance": 22,
                "segment": "short_international",
                "total_offers": 5,
                "unique_carriers": 2,
                "direct_flights": 3,
                "connecting_flights": 2,
                "price_min": 200.00,
                "price_avg": 350.00,
                "price_max": 500.00,
                "currency": "EUR",
                "is_coverage_anomaly": False,
                "is_price_anomaly": False,
            })
