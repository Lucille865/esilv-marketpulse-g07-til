BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

import json
from pathlib import Path


SAMPLE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample"
    / "bloomberg_reference_sample.json"
)


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    with open(SAMPLE_PATH, encoding="utf-8-sig") as file:
        data = json.load(file)

    def find_series(obj):
        if isinstance(obj, dict):
            if obj.get("provider_identifier") == identifier:
                return obj

            for value in obj.values():
                result = find_series(value)
                if result is not None:
                    return result

        elif isinstance(obj, list):
            for item in obj:
                result = find_series(item)
                if result is not None:
                    return result

        return None

    series = find_series(data)

    if series is None:
        raise ValueError(f"Bloomberg identifier not found: {identifier}")

    return series


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Convert approved Bloomberg sample data into canonical rows."""

    if raw_data["canonical_ticker"] != canonical_ticker:
        raise ValueError("Canonical ticker mismatch")

    rows = []

    for observation in raw_data["observations"]:
        row = {
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        }

        rows.append(row)

    return rows

def fetch_bloomberg_prices(canonical_ticker):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]

    raw_data = fetch_raw_bloomberg_history(identifier)

    rows = normalize_bloomberg_history(
        raw_data,
        canonical_ticker
    )

    return rows
