# SPEC-002: Silver Layer — Data Normalization

## Overview
Aggregate individual offers returned by Amadeus into a single normalized
snapshot per route and search parameters.

## Standard Snapshot Schema

| Field | Type | Description |
|---|---|---|
| `snapshot_at` | datetime | Timestamp when the search was executed |
| `origin` | string | IATA origin airport code (3 characters) |
| `destination` | string | IATA destination airport code (3 characters) |
| `departure_date` | date | Departure date searched |
| `days_in_advance` | integer | Days between snapshot_at and departure_date |
| `segment` | string | domestic, short_international, long_international |
| `total_offers` | integer | Total number of offers returned by Amadeus |
| `unique_carriers` | integer | Number of unique airlines in results |
| `direct_flights` | integer | Number of non-stop offers |
| `connecting_flights` | integer | Number of connecting offers |
| `price_min` | decimal | Minimum price across all offers |
| `price_avg` | decimal | Average price across all offers |
| `price_max` | decimal | Maximum price across all offers |
| `currency` | string | ISO 4217 currency code |


## Segment Classification

| Segment | Routes |
|---|---|
| `domestic` | Canadian routes |
| `short_international` | USA routes |
| `long_international` | All other international routes |

## Acceptance Criteria
- Each Bronze JSON is transformed into one snapshot record per route
- All fields mapped to standard snapshot schema
- `days_in_advance` calculated as the difference between `snapshot_at`
and `departure_date`
- `segment` assigned based on destination classification above
- `direct_flights` counted as offers with zero stops
- `connecting_flights` counted as offers with one or more stops
- `price_min`, `price_avg`, `price_max` calculated across all offers
- Null fields explicitly stored as null — not omitted
- Output saved as Parquet to `data/silver/`
