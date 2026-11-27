import csv
import json
from pathlib import Path

from providers.bloomberg_provider import fetch_bloomberg_prices

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

from providers.yahoo_provider import (
    fetch_yahoo_prices,
    YAHOO_SYMBOLS,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


# --- Data loading ---

def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as f:
        return json.load(f)


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as f:
        return [normalize_price_row(row) for row in csv.DictReader(f)]


def filter_prices(prices, ticker):
    return [p for p in prices if p["ticker"] == ticker]


def get_first_close(prices):
    return prices[0]["close"]


def get_last_close(prices):
    return prices[-1]["close"]


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


# --- Display ---

def display_market_summary(asset, prices, show_currency=True):
    currency = f" {asset['currency']}" if show_currency else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{currency}")
    print(f"Last close   : {get_last_close(prices):.2f}{currency}")


def display_configuration():
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")


# --- Shared application snapshot ---

def build_market_snapshot():
    # Business configuration
    provider = "Bloomberg stage"
    access_mode = "APPROVED_SAMPLE"
    lookback = "1mo"
    interval = "1d"

    # Load instrument and benchmark metadata
    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # Fetch canonical rows
    instrument_prices = fetch_bloomberg_prices(
        instrument["ticker"]
    )

    benchmark_prices = fetch_bloomberg_prices(
        benchmark["ticker"]
    )

    # Reuse existing alignment
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices
    )

    # Reuse existing analytics
    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return
    )

    instrument_base_100 = calculate_base_100(
        aligned_instrument
    )

    benchmark_base_100 = calculate_base_100(
        aligned_benchmark
    )

    # Shared application result
    snapshot = {
        "provider": provider,
        "access_mode": access_mode,
        "lookback": lookback,
        "interval": interval,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }

    return snapshot


# --- Main ---

def main():
    snapshot = build_market_snapshot()

    print("=" * 50)
    print("MARKETPULSE")
    print("=" * 50)

    print("\n--- Provider ---")
    print(snapshot["provider"])

    print("\n--- Access mode ---")
    print(snapshot["access_mode"])

    print("\n--- Market context ---")

    print(
        f"Instrument : {snapshot['instrument']['ticker']} - "
        f"{snapshot['instrument']['name']}"
    )

    print(
        f"Benchmark  : {snapshot['benchmark']['ticker']} - "
        f"{snapshot['benchmark']['name']}"
    )

    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")

    print("\n--- Period returns ---")
    print("AAPL return:", snapshot["instrument_return"])
    print("SP500 return:", snapshot["benchmark_return"])

    print("\n--- Relative performance ---")
    print("AAPL vs SP500:", snapshot["relative_performance"])

    print("\n--- Base 100 ---")

    print(
        "AAPL final value:",
        snapshot["instrument_base_100"][-1]
    )

    print(
        "SP500 final value:",
        snapshot["benchmark_base_100"][-1]
    )

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()