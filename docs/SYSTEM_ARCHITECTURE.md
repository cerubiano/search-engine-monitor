# System Architecture — Search Engine Performance Monitor

## 1. Overview

This platform combines Medallion Architecture (Bronze → Silver → Gold)
with Hexagonal Architecture (Ports & Adapters) to monitor flight search
engine performance across routes and market segments. The Medallion
layers ensure clean separation between raw data, normalized snapshots,
and aggregated metrics. The Hexagonal Architecture ensures the domain
logic is fully decoupled from external APIs and storage infrastructure.

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                    DATA SOURCE                       │
│                                                      │
│   ┌─────────────────────────────────────────┐       │
│   │              Amadeus (GDS)              │       │
│   │      GET /v2/shopping/flight-offers     │       │
│   └────────────────────┬────────────────────┘       │
└────────────────────────┼────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │          BRONZE LAYER         │
         │    Raw JSON — untouched       │
         │       Local filesystem        │
         │ data/bronze/                  │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │          SILVER LAYER         │
         │  Normalized snapshots         │
         │       Local filesystem        │
         │ data/silver/                  │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │           GOLD LAYER          │
         │   Coverage + Price metrics    │
         │   Anomaly flags               │
         │       Local filesystem        │
         │ data/gold/                    │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │          POSTGRESQL           │
         │  Snapshots + metrics          │
         │     Database: search_monitor  │
         │     Table: search_snapshots   │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │        TABLEAU PUBLIC         │
         │  Search Performance Dashboard │
         │     Public URL                │
         └───────────────────────────────┘
```

---

## 3. Hexagonal Architecture

```
┌──────────────────────────────────────────────────────┐
│                      DOMAIN                          │
│                                                      │
│   models/                  services/                 │
│   snapshot_model.py        coverage_analysis_        │
│                            service.py                │
│                            anomaly_detection_        │
│                            service.py                │
│                                                      │
│   ports/                   exceptions.py             │
│   provider_port.py                                   │
│   repository_port.py                                 │
└──────────────────────────────┬───────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────┐
│                    ADAPTERS                          │
│                                                      │
│   providers/               repositories/             │
│   amadeus_adapter.py       file_repository.py        │
│                            postgres_repository.py    │
└──────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│                      TESTS                           │
│                                                      │
│   conftest.py                                        │
│   test_coverage_analysis_service.py                  │
│   test_anomaly_detection_service.py                  │
│   test_amadeus_adapter.py                            │
│   test_file_repository.py                            │
│   test_postgres_repository.py                        │
└──────────────────────────────────────────────────────┘
```

**Ports define contracts. Adapters implement them.**

- `provider_port.py` — contract that every flight search adapter must implement
- `repository_port.py` — contract that every storage adapter must implement
- `exceptions.py` — domain error contracts
- Adding a new provider requires only a new adapter — domain is never touched

---

## 4. Components

### 4.1 Data Source

| Source | Type | Endpoint | Environment |
|---|---|---|---|
| Amadeus | GDS | GET /v2/shopping/flight-offers | test.api.amadeus.com |

### 4.2 Bronze Layer
- **Purpose:** Store raw API responses without modification
- **Storage:** Local filesystem
- **Format:** JSON
- **Path:** `data/bronze/{YYYYMMDD_HHMMSS}_amadeus.json`
- **Retention:** Permanent — source of truth for all transformations

### 4.3 Silver Layer
- **Purpose:** Normalize raw responses into a standard snapshot schema
- **Storage:** Local filesystem
- **Format:** Parquet (snappy compression)
- **Path:** `data/silver/{YYYYMMDD_HHMMSS}_snapshot.parquet`
- **Key transformation:** Aggregate individual offers into a single
snapshot per route and search parameters

### 4.4 Gold Layer
- **Purpose:** Apply coverage analysis and anomaly detection to generate
metrics per route and segment
- **Storage:** Local filesystem
- **Format:** Parquet (snappy compression)
- **Path:** `data/gold/{YYYYMMDD_HHMMSS}_metrics.parquet`
- **Key output:** Coverage metrics, price stability metrics, and anomaly
flags per route

### 4.5 PostgreSQL
- **Purpose:** Store snapshots and metrics for querying and dashboard
- **Host:** localhost (development)
- **Database:** search_monitor
- **Table:** search_snapshots
- **Key queries:** Coverage by route, price stability by segment,
anomaly log

### 4.6 Tableau Public
- **Purpose:** Visualize search engine performance and anomalies
- **Access:** Public URL
- **Connection:** PostgreSQL localhost
- **Refresh:** Manual per monitoring run

---

## 5. Data Flow

```
Step 1 — Extraction
Input:  origin, destination, departure_date
        adults = 1 (fixed)
        cabin_class = economy (fixed)
Action: Call Amadeus flight search endpoint for each defined route
Output: Raw JSON per route → data/bronze/

Step 2 — Normalization
Input:  Bronze JSON per route
Action: Aggregate individual offers into a single snapshot per route
        Map fields to standard snapshot schema via Pydantic
Output: Normalized snapshot → data/silver/ (Parquet)

Step 3 — Analysis
Input:  Silver Parquet
Action: Apply coverage analysis per route and segment
        Apply price stability analysis per route
        Apply anomaly detection based on defined thresholds
Output: Coverage metrics + price metrics + anomaly flags → data/gold/
        (Parquet)

Step 4 — Storage
Input:  Gold Parquet
Action: Persist snapshots and metrics to PostgreSQL
Output: search_snapshots table updated

Step 5 — Visualization
Input:  PostgreSQL search_snapshots
Action: Tableau Public reads metrics
Output: Search Performance Dashboard — public URL
```

---

## 6. Repository Structure

```
search-engine-monitor/
    config/
        routes.yaml
    data/
        bronze/
        silver/
        gold/
    src/
        domain/
            models/
                snapshot_model.py
            services/
                coverage_analysis_service.py
                anomaly_detection_service.py
            ports/
                provider_port.py
                repository_port.py
            exceptions.py
        adapters/
            providers/
                amadeus_adapter.py
            repositories/
                file_repository.py
                postgres_repository.py
        main.py
    tests/
        conftest.py
        test_coverage_analysis_service.py
        test_anomaly_detection_service.py
        test_amadeus_adapter.py
        test_file_repository.py
        test_postgres_repository.py
    docs/
        PRD.md
        SYSTEM_ARCHITECTURE.md
        specs/
            SPEC-001-bronze-layer.md
            SPEC-002-silver-layer.md
            SPEC-003-gold-layer.md
    .env.example
    requirements.txt
    README.md
```

---

## 7. Technology Stack

| Component | Technology | Version |
|---|---|---|
| Language | Python | 3.12 |
| Data processing | Pandas + PyArrow | Latest |
| Data validation | Pydantic | v2 |
| Database | PostgreSQL | 16 |
| DB connector | Psycopg2 | Latest |
| Dashboard | Tableau Public | Latest |
| Version control | Git + GitHub | — |

---

## 8. Data Dictionary

### Standard Snapshot Schema — Silver Layer

| Field | Type | Description |
|---|---|---|
| `snapshot_at` | datetime | Timestamp when the search was executed |
| `origin` | string | IATA origin airport code (3 characters) |
| `destination` | string | IATA destination airport code (3 characters) |
| `departure_date` | date | Departure date searched |
| `days_in_advance` | integer | Days between snapshot and departure date |
| `segment` | string | Route segment: domestic, short_international, long_international |
| `total_offers` | integer | Total number of offers returned by Amadeus |
| `unique_carriers` | integer | Number of unique airlines in results |
| `direct_flights` | integer | Number of non-stop offers |
| `connecting_flights` | integer | Number of connecting offers |
| `price_min` | decimal | Minimum price across all offers |
| `price_avg` | decimal | Average price across all offers |
| `price_max` | decimal | Maximum price across all offers |
| `currency` | string | ISO 4217 currency code |
| `is_coverage_anomaly` | boolean | True when total_offers falls below defined threshold |
| `is_price_anomaly` | boolean | True when price deviates from expected range |

---

## 9. Development Workflow

This project follows a strict development order based on Hexagonal
Architecture principles and Test-Driven Development (TDD).

1. Domain base — exceptions and models first, no external dependencies
2. Ports — contracts defined before any implementation
3. Services — business logic implemented test-first
4. Adapters — infrastructure implemented test-first against port contracts
5. Orchestration — pipeline assembled only after all components are tested
6. Configuration — environment variables and dependencies locked last

---

## 10. Environment Variables

```
# Amadeus
AMADEUS_API_KEY=
AMADEUS_API_SECRET=

# PostgreSQL
DB_HOST=localhost
DB_PORT=5432
DB_NAME=search_monitor
DB_USER=
DB_PASSWORD=
```
