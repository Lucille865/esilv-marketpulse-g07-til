import csv
import json
from pathlib import Path

DATA_DIR = Path("data/sample")


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as f:
        return json.load(f)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def filter_prices(prices, ticker):
    return [p for p in prices if p["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def display_market_summary(asset, prices, show_currency=True):
    currency = f" {asset['currency']}" if show_currency else ""
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{currency}")
    print(f"Last close   : {get_last_close(prices):.2f}{currency}\n")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    inst_prices = filter_prices(prices, instrument["ticker"])
    bench_prices = filter_prices(prices, benchmark["ticker"])

    # En-tête de configuration
    print("=== MarketPulse ===\n")
    print("Market configuration")
    print("Period   : 1 month")
    print("Interval : Daily\n")

    # Instrument
    print("Instrument")
    display_market_summary(instrument, inst_prices, show_currency=True)

    # Benchmark
    print("Benchmark")
    display_market_summary(benchmark, bench_prices, show_currency=False)


if __name__ == "__main__":
    main()