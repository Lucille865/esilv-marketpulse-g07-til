import json
from pathlib import Path
from typing import Any

BLOOMBERG_IDENTIFIERS: dict[str, str] = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

REFERENCE_SAMPLE = Path("data/sample/bloomberg_reference_sample.json")


def load_bloomberg_reference_sample(path: str | Path = REFERENCE_SAMPLE) -> dict[str, Any]:
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def find_reference_series(payload: dict[str, Any], provider_identifier: str) -> dict[str, Any]:
    for series in payload["series"]:
        if series["provider_identifier"] == provider_identifier:
            return series
    raise ValueError(f"Approved Bloomberg-stage series not found: {provider_identifier}")


def normalize_reference_series(series: dict[str, Any]) -> list[dict[str, Any]]:
    canonical_ticker = series["canonical_ticker"]
    rows: list[dict[str, Any]] = []
    for observation in series["observations"]:
        rows.append({
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(observation["volume_value"]),
        })
    return rows


def fetch_approved_sample_prices(
    provider_identifier: str,
    path: str | Path = REFERENCE_SAMPLE,
) -> list[dict[str, Any]]:
    payload = load_bloomberg_reference_sample(path)
    series = find_reference_series(payload, provider_identifier)
    return normalize_reference_series(series)


def fetch_raw_bloomberg_history(identifier, start_date, end_date):
    # The instructor supplies or demonstrates the environment-specific implementation.
    raise NotImplementedError("LIVE Bloomberg acquisition is not available in APPROVED_SAMPLE mode.")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    if isinstance(raw_data, dict) and "observations" in raw_data:
        rows = []
        for observation in raw_data["observations"]:
            rows.append({
                "date": observation["observation_date"],
                "ticker": canonical_ticker,
                "open": float(observation["open_value"]),
                "high": float(observation["high_value"]),
                "low": float(observation["low_value"]),
                "close": float(observation["close_value"]),
                "volume": int(observation["volume_value"]),
            })
        return rows
    raise NotImplementedError("LIVE normalization requires documented LIVE fields from TD09.")
