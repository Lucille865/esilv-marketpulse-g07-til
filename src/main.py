import csv
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)
from src.providers.bloomberg_provider import (
    BLOOMBERG_IDENTIFIERS,
    fetch_approved_sample_prices,
)

DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
ACCESS_MODE = "APPROVED_SAMPLE"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def build_market_snapshot(access_mode: str = ACCESS_MODE) -> dict:
    """Build the canonical MarketPulse application snapshot shared by terminal and Dash."""
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    if access_mode == "APPROVED_SAMPLE":
        instrument_prices = fetch_approved_sample_prices(
            BLOOMBERG_IDENTIFIERS[instrument["ticker"]]
        )
        benchmark_prices = fetch_approved_sample_prices(
            BLOOMBERG_IDENTIFIERS[benchmark["ticker"]]
        )
        provider_label = "Bloomberg stage - APPROVED_SAMPLE"
    else:
        raise NotImplementedError(
            f"Unsupported Bloomberg access mode: {access_mode}"
        )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    return {
        "provider": provider_label,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "access_mode": access_mode,
        "instrument": {
            "ticker": instrument["ticker"],
            "name": instrument["name"],
        },
        "benchmark": {
            "ticker": benchmark["ticker"],
            "name": benchmark["name"],
        },
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative_performance,
        "instrument_base_100": instrument_base_100,
        "benchmark_base_100": benchmark_base_100,
    }


def print_market_snapshot(snapshot: dict) -> None:
    """Render the shared MarketPulse snapshot to the terminal."""
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    inst_base = snapshot["instrument_base_100"]
    bench_base = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print("Bloomberg stage" if snapshot.get("access_mode") == "APPROVED_SAMPLE" else snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot.get("access_mode", "APPROVED_SAMPLE"))
    print()
    print("Market configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")
    print()
    print("Aligned window")
    print(f"Start date   : {inst_base[0]['date']}")
    print(f"End date     : {inst_base[-1]['date']}")
    print(f"Observations : {len(inst_base)}")
    print()
    print("Performance")
    print(f"{instrument['ticker']} return      : {snapshot['instrument_return']:+.2f}%")
    print(f"{benchmark['ticker']} return    : {snapshot['benchmark_return']:+.2f}%")
    print(f"Relative perf    : {snapshot['relative_performance']:+.2f} pp")
    print()
    print("Base 100")
    print(f"{instrument['ticker']} ({inst_base[0]['date']} -> {inst_base[-1]['date']}): {inst_base[0]['value']:.2f} -> {inst_base[-1]['value']:.2f}")
    print(f"{benchmark['ticker']} ({bench_base[0]['date']} -> {bench_base[-1]['date']}): {bench_base[0]['value']:.2f} -> {bench_base[-1]['value']:.2f}")


def main():
    snapshot = build_market_snapshot()
    print_market_snapshot(snapshot)


if __name__ == "__main__":
    main()