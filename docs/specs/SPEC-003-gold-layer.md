# SPEC-003: Gold Layer — Coverage Analysis & Anomaly Detection

## Overview
Apply coverage analysis and anomaly detection to normalized snapshots.
The output is a set of metrics per route and segment with anomaly flags
that enable teams to identify when the search engine is behaving
unexpectedly.

---

## Anomaly Detection Rules

| Rule | Field | Condition | Flag |
|---|---|---|---|
| Low coverage | `total_offers` | < 3 | `is_coverage_anomaly` = True |
| Low competition | `unique_carriers` | < 2 | `is_coverage_anomaly` = True |
| Price spread | `price_max` / `price_min` | > 5 | `is_price_anomaly` = True |

---

## Acceptance Criteria (BDD — Gherkin Format)

---

**Scenario 1: Low Coverage — Few Offers**
```gherkin
Given a normalized snapshot from the Silver layer
When total_offers is 2
Then is_coverage_anomaly must be True
```

---

**Scenario 2: Low Coverage — Few Carriers**
```gherkin
Given a normalized snapshot from the Silver layer
When unique_carriers is 1
Then is_coverage_anomaly must be True
```

---

**Scenario 3: Price Spread Anomaly**
```gherkin
Given a normalized snapshot from the Silver layer
When price_min is 100.00
And price_max is 600.00
Then is_price_anomaly must be True
```

---

**Scenario 4: No Anomaly**
```gherkin
Given a normalized snapshot from the Silver layer
When total_offers is 10
And unique_carriers is 4
And price_min is 200.00
And price_max is 800.00
Then is_coverage_anomaly must be False
And is_price_anomaly must be False
```

---

**Scenario 5: Price Anomaly — Null Price**
```gherkin
Given a normalized snapshot from the Silver layer
When price_min is null
Then is_price_anomaly must be False
```

---

## Acceptance Criteria

- `is_coverage_anomaly` is True when `total_offers` < 3 or
`unique_carriers` < 2
- `is_price_anomaly` is True when `price_max` / `price_min` > 5
- `is_price_anomaly` is False when `price_min` is null or zero
- Every snapshot receives both anomaly flags — True or False
- Output saved as Parquet to `data/gold/`
- Results persisted to PostgreSQL table `search_snapshots`
- All anomaly rules covered by automated tests
