CREATE TABLE IF NOT EXISTS search_snapshots (
    id                   SERIAL PRIMARY KEY,
    snapshot_at          TIMESTAMP NOT NULL,
    origin               VARCHAR(3) NOT NULL,
    destination          VARCHAR(3) NOT NULL,
    departure_date       DATE NOT NULL,
    days_in_advance      INTEGER NOT NULL,
    segment              VARCHAR(30) NOT NULL,
    total_offers         INTEGER NOT NULL,
    unique_carriers      INTEGER NOT NULL,
    direct_flights       INTEGER NOT NULL,
    connecting_flights   INTEGER NOT NULL,
    price_min            DECIMAL(10,2),
    price_avg            DECIMAL(10,2),
    price_max            DECIMAL(10,2),
    currency             VARCHAR(3),
    is_coverage_anomaly  BOOLEAN NOT NULL DEFAULT FALSE,
    is_price_anomaly     BOOLEAN NOT NULL DEFAULT FALSE
);
