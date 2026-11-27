# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Live connectivity:
not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `<clé_date_du_json>` | Mapped to canonical `YYYY-MM-DD` string |
| ticker | application mapping | AAPL or SP500 |
| open | `<clé_open_du_json>` | Converted to `float` (verify if present for `SPX Index`) |
| high | `<clé_high_du_json>` | Converted to `float` (verify if present for `SPX Index`) |
| low | `<clé_low_du_json>` | Converted to `float` (verify if present for `SPX Index`) |
| close | `<clé_close_du_json>` | Converted to `float` |
| volume | `<clé_volume_du_json>` | Converted to `int` (note if missing/null for `SPX Index`) |


## TD10 handoff

- Access mode:
- Instrument identifier:
- Benchmark identifier:
- Date representation:
- Input structure:
- Missing fields:
- Special normalization notes: