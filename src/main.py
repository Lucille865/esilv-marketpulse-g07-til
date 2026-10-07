import csv
import json
from pathlib import Path

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


# --- Chargement des données ---

def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# --- Traitement & Extraction ---

def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


# --- Fonctions d'affichage ---

def display_configuration():
    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()


def display_market_summary(asset, prices, show_currency=True):
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    currency_suffix = f" {asset['currency']}" if show_currency and "currency" in asset else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close  : {first_close:.2f}{currency_suffix}")
    print(f"Last close   : {last_close:.2f}{currency_suffix}")


# --- Orchestration du flux ---

def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    display_configuration()

    print("Instrument")
    display_market_summary(instrument, instrument_prices, show_currency=True)
    print()
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)


if __name__ == "__main__":
    main()
