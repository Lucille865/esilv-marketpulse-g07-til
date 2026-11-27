import json
from pathlib import Path

# TD09 mapping: docs/BLOOMBERG_FIELD_MAPPING.md
ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")

# Canonical MarketPulse ticker -> Bloomberg identifier
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(identifier, sample_path=SAMPLE_PATH):
    """Raw input boundary.

    APPROVED_SAMPLE mode: reads the instructor-approved fixture.
    A LIVE implementation would only replace this function.
    """
    with open(sample_path, encoding="utf-8") as file:
        fixture = json.load(file)

    for series in fixture["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"No approved sample series for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Normalization boundary: teaching wrapper keys -> canonical rows."""
    if raw_data["canonical_ticker"] != canonical_ticker:
        raise ValueError(
            f"Series metadata ticker {raw_data['canonical_ticker']} "
            f"does not match {canonical_ticker}"
        )

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

    if not rows:
        raise ValueError(f"No observations for {canonical_ticker}")

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier)
    return normalize_bloomberg_history(raw_data, canonical_ticker)