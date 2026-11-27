import csv
import json
from pathlib import Path

# TD07
from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)

# TD08
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices

# TD10
from providers.bloomberg_provider import ACCESS_MODE, fetch_bloomberg_prices

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


# TD07
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


# TD10 
def build_market_snapshot(provider="bloomberg"):
    instruments = load_instruments()

    #Lucille's merge
    instrument = instruments["instrument"]

    #Tom's merge 
    benchmark = instruments["benchmark"]

    if provider == "yahoo":
        # TD08
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
        provider_label = "Yahoo Finance via yfinance"
        access_mode = "REMOTE"
    else:
        # TD10
        instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
        benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])
        provider_label = f"Bloomberg stage - {ACCESS_MODE}"
        access_mode = ACCESS_MODE

    # TD07
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:  # TD10
        raise ValueError("No common dates between instrument and benchmark")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )
    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    # TD10
    return {
        "provider": provider_label,
        "access_mode": access_mode,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
    }


#main
def main():
    snapshot = build_market_snapshot()  # TD10

    # TD10 
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_prices = snapshot["instrument_prices"]
    benchmark_prices = snapshot["benchmark_prices"]
    instrument_return = snapshot["instrument_return"]
    benchmark_return = snapshot["benchmark_return"]
    relative_performance = snapshot["relative_performance"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print()

    instrument_latest = instrument_prices[-1]
    benchmark_latest = benchmark_prices[-1]

    print("=== MarketPulse ===")
    print()
    # TD08 / TD10
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")  # TD10
    print(snapshot["access_mode"])  # TD10
    print()
    display_configuration()
    print()
    print("Instrument")
    print(f"{instrument['ticker']} - {instrument['name']}")
    print(f"Last price: {instrument_latest['close']:.2f} {instrument['currency']}")  # TD08
    print(f"Start date   : {get_first_date(instrument_prices)}")  # TD08
    print(f"End date     : {get_last_date(instrument_prices)}")  # TD08
    display_market_summary(instrument, instrument_prices, show_currency=True)
    print(f"Period return : {instrument_return:.2f}%")  # TD07
    print()
    print("Benchmark")
    print(f"{benchmark['ticker']} - {benchmark['name']}")
    print(f"Last level: {benchmark_latest['close']:.2f}")  # TD08
    print(f"Start date   : {get_first_date(benchmark_prices)}")  # TD08
    print(f"End date     : {get_last_date(benchmark_prices)}")  # TD08
    print(f"Period return : {benchmark_return:.2f}%")  # TD07
    print()
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()
    print("Observations")
    print(f"{instrument['ticker']}: {len(instrument_prices)}")
    print(f"{benchmark['ticker']}: {len(benchmark_prices)}")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)

    # TD07 
    print()
    print("Relative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']} : {relative_performance:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{instrument['ticker']} : {instrument_base_100[0]['value']:.2f} -> {instrument_base_100[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} : {benchmark_base_100[0]['value']:.2f} -> {benchmark_base_100[-1]['value']:.2f}")


if __name__ == "__main__":
    main()