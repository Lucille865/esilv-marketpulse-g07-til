import json
from pathlib import Path
from typing import Any

BLOOMBERG_IDENTIFIERS: dict[str, str] = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

DEFAULT_SAMPLE_PATH = Path("data/sample/bloomberg_reference_sample.json")


def fetch_raw_bloomberg_history(
    identifier: str,
    start_date: str | None = None,
    end_date: str | None = None,
    sample_path: str | Path = DEFAULT_SAMPLE_PATH,
) -> list[dict[str, Any]]:
    """Fetch raw Bloomberg observations for `identifier` from the approved sample."""
    path = Path(sample_path)
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    series_list = payload.get("series", [])
    matched_series = next(
        (s for s in series_list if s.get("provider_identifier") == identifier),
        None,
    )
    if matched_series is None:
        raise KeyError(f"Identifier not found in sample: {identifier}")

    observations = matched_series.get("observations", [])

    filtered: list[dict[str, Any]] = []
    for obs in observations:
        obs_date = str(obs.get("observation_date", ""))
        if start_date is not None and obs_date < start_date:
            continue
        if end_date is not None and obs_date > end_date:
            continue
        filtered.append(obs)

    return filtered

def normalize_bloomberg_history(
    raw_data: list[dict[str, Any]],
    canonical_ticker: str,
    mode: str = "APPROVED_SAMPLE",
) -> list[dict[str, Any]]:
    """Normalize Bloomberg observations into canonical MarketPulse rows."""
    if mode.upper() != "APPROVED_SAMPLE":
        raise NotImplementedError(
            f"Normalization for mode '{mode}' is not implemented; do not assume wrapper keys for LIVE."
        )

    if not canonical_ticker:
        raise ValueError("canonical_ticker must be provided")

    normalized_rows: list[dict[str, Any]] = []

    for observation in raw_data:
        volume_raw = observation.get("volume_value")
        row: dict[str, Any] = {
            "date": str(observation["observation_date"]),
            "ticker": canonical_ticker,
            "open": float(observation["open_value"]),
            "high": float(observation["high_value"]),
            "low": float(observation["low_value"]),
            "close": float(observation["close_value"]),
            "volume": int(volume_raw) if volume_raw is not None else 0,
        }
        normalized_rows.append(row)

    normalized_rows.sort(key=lambda r: r["date"])
    return normalized_rows