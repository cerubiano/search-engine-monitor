# PRD — Search Engine Performance Monitor

## 1. Overview

Search Engine Performance Monitor is a data pipeline that extracts,
normalizes, and analyzes flight search results from the Amadeus API
across a defined set of routes and search parameters. The platform
measures coverage, price stability, and result quality over time,
enabling teams to detect anomalies and understand how search behavior
varies across routes and market segments.

---

## 2. Problem Statement

Flight search engines return results that vary significantly depending
on the route, search parameters, and time of query. Without a structured
monitoring system, it is difficult to determine whether that variation
is expected or represents a problem — such as low coverage on key
routes, unusual price fluctuations, or degraded result quality.

Three core challenges:

- **Visibility:** Teams need a centralized view of how search results
behave across routes and market segments to support informed decisions.
- **Detection:** Identifying when results deviate from expected patterns
requires a systematic and repeatable monitoring process.
- **Measurement:** Understanding the impact of parameter changes on
result quality and coverage requires structured and comparable data
over time.

---

## 3. Scope

### In Scope

- Flight search data extraction from Amadeus API
- A defined set of routes across domestic and international segments
- Analysis of coverage, price stability, and result quality per route
and segment
- Anomaly detection based on coverage and price thresholds
- Dashboard to visualize results over time

### Out of Scope

- Additional providers beyond Amadeus
- Real-time pricing
- Booking and post-booking services
- Cross-provider comparison

---

## 4. Users

| User | Need |
|---|---|
| Data Analyst | Monitor search result behavior across routes and segments to detect anomalies |
| Integration Engineer | Validate that search parameters are returning complete and stable results |
| Team Lead | Make data-driven decisions about which routes or segments require attention |

---

## 5. Core Features

**F1 — Data Extraction**
Connect to Amadeus flight search endpoint and extract raw search results
for a defined set of routes and search parameters. Raw responses stored
in Bronze layer.

**F2 — Data Normalization**
Transform raw responses into a standard schema. Output stored in Silver
layer.

**F3 — Coverage Analysis**
Measure the number of offers, unique carriers, and proportion of direct
vs connecting flights per route and segment.

**F4 — Price Stability Analysis**
Measure minimum, average, and maximum price per route. Track price
variation according to days in advance of departure.

**F5 — Anomaly Detection**
Identify routes where coverage or price deviates from expected patterns
based on defined thresholds.

**F6 — Reporting Dashboard**
Visualize coverage, price stability, quality scores, and anomalies in
an interactive Tableau Public dashboard.

---

## 6. Success Criteria

- Search results extracted from Amadeus for all defined routes and
segments
- Coverage metrics generated per route, per segment, and per search
parameter
- Price stability metrics generated per route and per days in advance
- Anomalies detected and logged when results deviate from defined
thresholds
- Quality score reused from Project 1 scoring logic
- Dashboard publicly accessible via Tableau Public URL
- All analysis rules covered by automated tests
- Code documented and reproducible from README