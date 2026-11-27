# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Reference availability:
Not yet located in the repository.

Live connectivity:
not demonstrated

## Instrument input inspection

- Provider identifier: AAPL US Equity
- Canonical ticker: AAPL
- Access mode: APPROVED_SAMPLE
- Source: data/sample/bloomberg_reference_sample.json

### Available fields

- observation_date
- open_value
- high_value
- low_value
- close_value
- volume_value

These fields are teaching wrapper keys, not Bloomberg LIVE field mnemonics.

## Benchmark input inspection

- Provider identifier: SPX Index
- Canonical ticker: SP500
- Access mode: APPROVED_SAMPLE
- Source: data/sample/bloomberg_reference_sample.json

### Available fields

- observation_date
- open_value
- high_value
- low_value
- close_value
- volume_value

These fields are teaching wrapper keys, not Bloomberg LIVE field mnemonics.

The Bloomberg provider identifier is SPX Index,
but the MarketPulse canonical ticker remains SP500.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | observation_date | Teaching wrapper key - target format YYYY-MM-DD |
| ticker | Application mapping | AAPL or SP500 |
| open | open_value | Teaching wrapper key - float |
| high | high_value | Teaching wrapper key - float |
| low | low_value | Teaching wrapper key - float |
| close | close_value | Teaching wrapper key - float |
| volume | volume_value | Teaching wrapper key - target type int |

## Mapping notes

- Teaching wrapper keys are not Bloomberg LIVE field mnemonics.
- Provider-specific identifiers must remain outside analytics.py.
- The canonical tickers must remain AAPL and SP500.
- The target structure is compatible with the existing MarketPulse analytics.
- The mapping is based on the TD09 instructions and the provided JSON files.
- The instructor reference document could not be located or consulted.
- Live Bloomberg connectivity has not been demonstrated.
- Special normalization rules and missing-value handling remain to be verified.

## Canonical ticker preservation

Bloomberg provider identifiers must be mapped to MarketPulse canonical tickers.

- AAPL US Equity -> AAPL
- SPX Index -> SP500

The normalized rows must preserve the existing MarketPulse canonical structure.

Conceptual example for the benchmark:

```json
{
    "date": "...",
    "ticker": "SP500",
    "open": ...,
    "high": ...,
    "low": ...,
    "close": ...,
    "volume": ...
}
```

Provider-specific identifiers must not enter the analytics layer.

TD09 documents the normalization contract.
The normalization implementation will be completed in TD10.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity
- Benchmark identifier: SPX Index
- Date representation: YYYY-MM-DD
- Input structure: JSON containing instrument and benchmark series with historical observations.
- Missing fields: No missing or null values detected in the inspected observations.

### Special normalization notes

- Map AAPL US Equity to AAPL.
- Map SPX Index to SP500.
- Map observation_date to date.
- Map open_value to open.
- Map high_value to high.
- Map low_value to low.
- Map close_value to close.
- Map volume_value to volume.
- Preserve the existing MarketPulse canonical row structure.
- Preserve the existing analytics functions.
- Teaching wrapper keys are not Bloomberg LIVE field mnemonics.
- Live Bloomberg connectivity has not been demonstrated.
- The instructor reference document could not be consulted.

Expected canonical reference:
data/sample/bloomberg_reference_expected.json
