import csv
import json
from pathlib import Path
from src.analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from src.providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices

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

def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]

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

    
#main
print()
def main():
    instruments = load_instruments()
    #prices = load_prices()
    #normalized_prices = [
    #normalize_price_row(row)
    #for row in prices
    #]

    #Lucille's merge
    instrument = instruments["instrument"]
    print(instrument)

    #Tom's merge 
    benchmark = instruments["benchmark"]
    print(benchmark)

    #instrument_prices = filter_prices(normalized_prices, instrument["ticker"])
    #benchmark_prices = filter_prices(normalized_prices, benchmark["ticker"])

    instrument_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[instrument["ticker"]],
        canonical_ticker=instrument["ticker"],
        period="1mo",
        interval="1d",
    )

    benchmark_prices = fetch_yahoo_prices(
        symbol=YAHOO_SYMBOLS[benchmark["ticker"]],
        canonical_ticker=benchmark["ticker"],
        period="1mo",
        interval="1d",
    )

    aligned_instrument, aligned_benchmark = align_series(
    instrument_prices,
    benchmark_prices,
    )

    instrument_return = calculate_period_return(
        aligned_instrument
    )

    benchmark_return = calculate_period_return(
        aligned_benchmark
    )

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]


    print("=== MarketPulse ===")
    print()
    display_configuration()
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_latest['close']} {instrument['currency']}")
    print(f"Start date   : {get_first_date(aligned_instrument)}")
    print(f"End date     : {get_last_date(aligned_instrument)}")
    display_market_summary(instrument, instrument_prices, show_currency=True)
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']}")
    print(f"Start date   : {get_first_date(aligned_instrument)}")
    print(f"End date     : {get_last_date(aligned_instrument)}")
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Observations")
    print(f"{instrument['ticker']}: {len(instrument_prices)}")
    print(f"{benchmark['ticker']}: {len(benchmark_prices)}")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)

    print("Provider")
    print("Yahoo Finance via yfinance")
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {LOOKBACK_LABEL}")
    print(f"Interval   : {INTERVAL_LABEL}")


if __name__ == "__main__":
    main()

