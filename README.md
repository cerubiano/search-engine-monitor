# Search Engine Performance Monitor

A data pipeline that monitors flight search engine performance across
routes and market segments — measuring coverage, price stability, and
anomaly detection using the Amadeus API.

---

## Problem

Flight search engines return results that vary significantly depending
on the route, search parameters, and time of query. Without a structured
monitoring system, it is difficult to determine whether that variation
is expected or represents a problem.

Three core challenges:

- **Visibility:** Teams need a centralized view of how search results
behave across routes and market segments to support informed decisions.
- **Detection:** Identifying when results deviate from expected patterns
requires a systematic and repeatable monitoring process.
- **Measurement:** Understanding the impact of parameter changes on
result quality and coverage requires structured and comparable data
over time.

---

## Architecture

```
Amadeus GET /v2/shopping/flight-offers
        ↓
    Bronze → Silver → Gold
        ↓
    PostgreSQL
        ↓
    Tableau Public
```

Hexagonal Architecture (Ports & Adapters) combined with Medallion
Architecture (Bronze → Silver → Gold) to ensure clean separation
between business logic and infrastructure.

---

## Key Metrics

- **Coverage:** Number of offers and unique carriers returned per route
and segment.
- **Price Stability:** Minimum, average, and maximum price per route
tracked over time.
- **Days in Advance:** Price variation according to days between search
and departure date.
- **Anomaly Detection:** Routes where coverage or price deviates from
expected patterns.

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| Data processing | Pandas + PyArrow |
| Data validation | Pydantic v2 |
| Database | PostgreSQL 16 |
| Dashboard | Tableau Public |
| Version control | Git + GitHub |

---

## Project Structure

```
search-engine-monitor/
    data/
        bronze/     ← Raw JSON from Amadeus
        silver/     ← Normalized snapshots (Parquet)
        gold/       ← Coverage metrics + anomaly flags (Parquet)
    src/
        domain/
            models/
            services/
            ports/
            exceptions.py
        adapters/
            providers/
            repositories/
        main.py
    tests/
        conftest.py
    docs/
        PRD.md
        SYSTEM_ARCHITECTURE.md
        specs/
```

---

## Documentation

| Document | Description |
|---|---|
| [PRD](docs/PRD.md) | Problem statement, scope, and success criteria |
| [System Architecture](docs/SYSTEM_ARCHITECTURE.md) | Technical design, data flow, and data dictionary |
| [SPEC-001](docs/specs/SPEC-001-bronze-layer.md) | Bronze layer ingestion specification |
| [SPEC-002](docs/specs/SPEC-002-silver-layer.md) | Silver layer normalization specification |
| [SPEC-003](docs/specs/SPEC-003-gold-layer.md) | Gold layer coverage analysis and anomaly detection specification |

---

## How to Run

### Prerequisites
- Python 3.12
- PostgreSQL 16
- Amadeus API credentials

### Setup
```bash
git clone https://github.com/cerubiano/search-engine-monitor
cd search-engine-monitor
pip install -r requirements.txt
cp .env.example .env
# Add your credentials to .env
```

### Run
```bash
python src/main.py
```

---

## Results

### Key Insights
- LAX and ORD show the highest average offer coverage across all segments
- 67 of 103 snapshots triggered a price anomaly — indicating high price spread across most routes
- Long international routes average ~667 EUR vs ~280 EUR for domestic
- Price anomalies concentrate in the 7-day advance window across most routes

### Dashboard
[Search Engine Performance Monitor](https://public.tableau.com/app/profile/carlos.rubiano3854/viz/Searchenginemonitor/SearchEnginePerformanceMonitor)

---

## Author

Carlos Eduardo Rubiano Robles
[LinkedIn](https://www.linkedin.com/in/cerubiano/) · [GitHub](https://github.com/cerubiano)