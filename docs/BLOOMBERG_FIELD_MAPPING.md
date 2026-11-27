# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

- Source: `data/sample/bloomberg_reference_sample.json`
- Reference: `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` (instructor reference, not present in the team repository; the mapping below follows the fixture's own `schema_note` and the expected canonical file)
- Live connectivity: **not demonstrated**

Fixture metadata observed:

| Key | Value |
|---|---|
| `sample_kind` | `instructor_approved_fallback_fixture` |
| `provider_stage` | `bloomberg` |
| `access_mode` | `approved_sample` |
| `is_live_bloomberg_output` | `false` |
| `provenance` | Illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg historical observations |

This document must not be presented as proof of LIVE Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

Provider identifiers stay at the provider boundary. `analytics.py` only receives the canonical tickers `AAPL` and `SP500`.

### Identifier comparison (optional)

| Canonical | CSV | Yahoo | Bloomberg |
|---|---|---|---|
| AAPL | AAPL | AAPL | AAPL US Equity |
| SP500 | SP500 | ^GSPC | SPX Index |

## Inspected inputs

### Instrument

| Item | Observed value |
|---|---|
| `role` | `instrument` |
| `canonical_ticker` | `AAPL` |
| `provider_identifier` | `AAPL US Equity` |
| Observations | 21 |
| First / last date | 2026-09-01 / 2026-09-30 |
| First / last close | 250 / 266.2 |
| Volume | between 38,000,000 and 44,000,000 |

### Benchmark

| Item | Observed value |
|---|---|
| `role` | `benchmark` |
| `canonical_ticker` | `SP500` |
| `provider_identifier` | `SPX Index` |
| Observations | 21 |
| First / last date | 2026-09-01 / 2026-09-30 |
| First / last close | 6600 / 6742 |
| Volume | `0` on every observation |

Both series contain exactly the same 21 dates.

## Input structure

```text
{
  sample_kind, provider_stage, access_mode,
  is_live_bloomberg_output, provenance, schema_note,
  series: [
    {
      role,
      canonical_ticker,
      provider_identifier,
      observations: [
        {
          observation_date,
          open_value,
          high_value,
          low_value,
          close_value,
          volume_value
        }
      ]
    }
  ]
}
```

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Teaching wrapper key. String `YYYY-MM-DD`, kept as is |
| ticker | application mapping from `series[].canonical_ticker` | `AAPL` or `SP500`. `provider_identifier` is never copied into rows |
| open | `open_value` | Teaching wrapper key. JSON number, convert to `float` |
| high | `high_value` | Teaching wrapper key. JSON number, convert to `float` |
| low | `low_value` | Teaching wrapper key. JSON number, convert to `float` |
| close | `close_value` | Teaching wrapper key. JSON number, convert to `float` |
| volume | `volume_value` | Teaching wrapper key. Convert to `int`. Always `0` for `SPX Index` |

**Important:**

```text
teaching wrapper key
!=
Bloomberg LIVE field mnemonic
```

`observation_date`, `open_value`, `high_value`, `low_value`, `close_value` and `volume_value` are teaching keys defined by the fixture (`schema_note`). No Bloomberg field mnemonic is named in this document, because none was observed in a LIVE session.

## Target canonical rows

Taken from `data/sample/bloomberg_reference_expected.json`:

```python
{
    "date": "2026-09-01",
    "ticker": "AAPL",
    "open": 249.2,
    "high": 251.5,
    "low": 248,
    "close": 250,
    "volume": 38000000,
}

{
    "date": "2026-09-01",
    "ticker": "SP500",
    "open": 6592,
    "high": 6615,
    "low": 6580,
    "close": 6600,
    "volume": 0,
}
```

## TD10 handoff

- Access mode: APPROVED_SAMPLE (live connectivity not demonstrated)
- Instrument identifier: `AAPL US Equity` → canonical `AAPL`
- Benchmark identifier: `SPX Index` → canonical `SP500`
- Date representation: ISO string `YYYY-MM-DD`, no time or timezone, usable directly as `date`
- Input structure: JSON object with a `series` list; select each series by `provider_identifier` (or `role`), then read its `observations` list
- Missing fields: none; `volume_value` is present for `SPX Index` but always `0`
- Special normalization notes:
  - some prices are JSON integers (e.g. `248`, `6600`): convert open/high/low/close to `float`
  - convert `volume_value` to `int`
  - take `ticker` from `canonical_ticker`, never from `provider_identifier`
  - return a flat list of canonical rows (`date, ticker, open, high, low, close, volume`)
  - reuse `align_series()` and the TD07 analytics unchanged; `analytics.py` must not contain `AAPL US Equity` or `SPX Index`
- Expected canonical reference: `data/sample/bloomberg_reference_expected.json` (42 rows: 21 AAPL + 21 SP500)
- Sanity check: the sample reuses the CSV values, so TD10 should reproduce the TD07 results: AAPL +6.48 %, SP500 +2.15 %, relative performance +4.33 percentage points

## Validation

- [x] access mode is explicit
- [x] instrument mapping is documented
- [x] benchmark mapping is documented
- [x] field source is identifiable
- [x] canonical tickers remain AAPL and SP500
- [x] no LIVE field name invented
- [x] APPROVED_SAMPLE wrapper keys are labelled as teaching keys
- [x] missing fields are documented honestly
- [x] no credential appears
- [x] TD10 handoff is present