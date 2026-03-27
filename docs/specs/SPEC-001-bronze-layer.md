# SPEC-001: Bronze Layer — Raw Data Ingestion

## Overview
Store raw API responses exactly as received from Amadeus.
No transformations. No modifications.

## Acceptance Criteria

**Given:** A flight search request for each defined route,
departure_date, adults=1, cabin_class=economy
**When:** The extraction service calls the Amadeus flight search endpoint
**Then:**
- Raw JSON from Amadeus is saved to `data/bronze/`
- Files are named with timestamp: `YYYYMMDD_HHMMSS_amadeus.json`
- No field is modified, added, or removed
- Extraction timestamp is logged

## File Naming Convention
```
data/bronze/
    20260324_100000_amadeus.json
    20260324_100010_amadeus.json
```

## Failure Criteria
- API returns error → log error, do not save empty file
- API timeout → log timeout, retry once
