import csv
import json
from pathlib import Path

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

DATA_DIR = Path("data/sample")


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


def display_market_summary(asset, prices, show_currency=True):
    currency = f" {asset['currency']}" if show_currency else ""
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{currency}")
    print(f"Last close   : {get_last_close(prices):.2f}{currency}")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    inst_prices = filter_prices(prices, instrument["ticker"])
    bench_prices = filter_prices(prices, benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        inst_prices,
        bench_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base = calculate_base_100(aligned_instrument)
    benchmark_base = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===\n")
    print("Market configuration")
    print("Period   : 1 month")
    print("Interval : Daily\n")

    print("Instrument")
    display_market_summary(instrument, aligned_instrument)
    print(f"Period return : {instrument_return:.2f}%\n")

    print("Benchmark")
    display_market_summary(benchmark, aligned_benchmark, False)
    print(f"Period return : {benchmark_return:.2f}%\n")

    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']} : "
          f"{relative_performance:+.2f} percentage points\n")

    print("Base 100")
    print(f"{instrument['ticker']} : "
          f"{instrument_base[0]['value']:.2f} -> "
          f"{instrument_base[-1]['value']:.2f}")

    print(f"{benchmark['ticker']} : "
          f"{benchmark_base[0]['value']:.2f} -> "
          f"{benchmark_base[-1]['value']:.2f}")


if __name__ == "__main__":
    main()
