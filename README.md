# ESILV MarketPulse — Team g07-til

<p align="center">
  <img
    src="https://www.itii-pdl.com/wp-content/uploads/2024/11/logo_esilv_couleur.jpg?ver=1733410620"
    alt="ESILV - De Vinci Higher Education"
    width="100"
  />
</p>

[![Course: MESIFI472326](https://img.shields.io/badge/course-MESIFI472326-1f6feb.svg)](docs/06_TD_SEQUENCE_AND_LEARNING_PATH.md)
[![ESILV A4](https://img.shields.io/badge/ESILV-A4-111827.svg)](docs/00_MARKETPULSE_FUNCTIONAL_CONTRACT.md)
[![Team](https://img.shields.io/badge/team-g07--til-0969da.svg)](https://github.com/Lucille865/esilv-marketpulse-g07-til)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)](https://www.python.org/)
[![TD](https://img.shields.io/badge/TD-18h-orange.svg)](docs/06_TD_SEQUENCE_AND_LEARNING_PATH.md)
[![Mode](https://img.shields.io/badge/mode-APPROVED__SAMPLE-2ea44f.svg)](docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md)

**MarketPulse** is our team implementation for the **ESILV A4 - Python, Git, Linux** module (`esilv-marketpulse-g07-til`).

> Acquire market data from provider stages, normalize it to one canonical contract, compare one instrument with its benchmark, then expose the same application snapshot through both the terminal and a Dash dashboard.

### ⚡ Languages and Tools

<p align="center">
  <a href="https://www.python.org/" target="_blank" rel="noreferrer" title="Python">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/>
  </a>
  <a href="https://git-scm.com/" target="_blank" rel="noreferrer" title="Git">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="git" width="40" height="40"/>
  </a>
  <a href="https://github.com/" target="_blank" rel="noreferrer" title="GitHub">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" alt="github" width="40" height="40"/>
  </a>
  <a href="https://www.kernel.org/" target="_blank" rel="noreferrer" title="Linux">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/>
  </a>
  <a href="https://www.gnu.org/software/bash/" target="_blank" rel="noreferrer" title="Bash">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-original.svg" alt="bash" width="40" height="40"/>
  </a>
  <a href="https://finance.yahoo.com/" target="_blank" rel="noreferrer" title="Yahoo Finance / yfinance">
    <img src="https://logos-world.net/wp-content/uploads/2020/10/Yahoo-Emblem.png" alt="yahoo" width="40" height="40"/>
  </a>
  <a href="https://dash.plotly.com/" target="_blank" rel="noreferrer" title="Dash">
    <img src="https://img.shields.io/badge/Dash-008DE5?logo=plotly&amp;logoColor=white" alt="dash" height="40"/>
  </a>
  <a href="https://plotly.com/python/" target="_blank" rel="noreferrer" title="Plotly">
    <img src="https://cdn.simpleicons.org/plotly/3F4F75" alt="plotly" width="40" height="40"/>
  </a>
  <a href="https://www.bloomberg.com/professional/" target="_blank" rel="noreferrer" title="Bloomberg">
    <img src="https://img.shields.io/badge/Bloomberg-000000?logo=bloomberg&amp;logoColor=white" alt="bloomberg" height="40"/>
  </a>
</p>

## Table of contents

- [What MarketPulse does](#what-marketpulse-does)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Data providers](#data-providers)
- [Canonical data contract](#canonical-data-contract)
- [Metrics](#metrics)
- [Testing](#testing)
- [Git workflow](#git-workflow)
- [Documentation](#documentation)
- [Team](#team)

## What MarketPulse does

MarketPulse compares the performance of a financial instrument against a reference benchmark over the same historical window and frequency, using a single shared application snapshot (`build_market_snapshot()` in `src/main.py`) consumed identically by the terminal CLI and the Dash web interface.

Team configuration:

```text
Instrument : AAPL - Apple Inc.
Benchmark  : SP500 - S&P 500
Lookback   : 1 month
Interval   : Daily
Provider   : Bloomberg stage - APPROVED_SAMPLE (with Yahoo Finance / yfinance support)
```

## Architecture

The application follows a simple pipeline, and every interface reads the same output:

```text
 ┌───────────────┐   ┌───────────────┐   ┌───────────────┐   ┌───────────────────────┐
 │  Providers    │ → │ Normalization │ → │  Comparison   │ → │ build_market_snapshot │
 │ Bloomberg /   │   │ canonical     │   │ instrument vs │   │ (single source of     │
 │ Yahoo Finance │   │ contract      │   │ benchmark     │   │ truth)                │
 └───────────────┘   └───────────────┘   └───────────────┘   └───────────┬───────────┘
                                                                         │
                                                       ┌─────────────────┴───────────────┐
                                                       ▼                                 ▼
                                                 Terminal CLI                    Dash dashboard
```

Design principles:

1. **One contract**: all providers are normalized to the same schema before any computation.
2. **One snapshot**: the CLI and the dashboard never recompute metrics independently.
3. **Replaceable providers**: switching from `APPROVED_SAMPLE` to Yahoo Finance requires no change downstream.

## Project structure

```text
esilv-marketpulse-g07-til/
├── README.md
├── requirements.txt
├── docs/
│   ├── 00_MARKETPULSE_FUNCTIONAL_CONTRACT.md
│   ├── 06_TD_SEQUENCE_AND_LEARNING_PATH.md
│   └── 10_BLOOMBERG_INSTRUCTOR_REFERENCE.md
├── src/
│   ├── main.py            # build_market_snapshot() + CLI entry point
│   └── ...                # providers, normalization, metrics, dashboard
├── tests/
└── data/                  # approved sample data (Bloomberg stage)
```

> Adjust this tree to match the actual content of the repository.

## Installation

### Prerequisites

- Python 3.x
- Git
- A Linux / macOS shell (or WSL on Windows)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Lucille865/esilv-marketpulse-g07-til.git
cd esilv-marketpulse-g07-til

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

### Terminal (CLI)

```bash
python src/main.py
```

Prints the snapshot for `AAPL` vs `SP500` (1 month, daily): normalized series summary and comparison metrics.

### Dash dashboard

```bash
python src/main.py --dash
```

Then open <http://127.0.0.1:8050> in your browser.

> The exact flags depend on the CLI implemented in `src/main.py`. Update the commands above if needed.

### Programmatic access

```python
from src.main import build_market_snapshot

snapshot = build_market_snapshot()
print(snapshot)
```

## Data providers

| Provider | Mode | Description |
|---|---|---|
| Bloomberg stage | `APPROVED_SAMPLE` | Approved sample extract used for reproducible, offline runs (see [instructor reference](docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md)). |
| Yahoo Finance | `yfinance` | Live public data, useful for development and comparison. |

No Bloomberg Terminal access is required: the `APPROVED_SAMPLE` mode ships a validated sample dataset.

## Canonical data contract

Every provider output is normalized to the same structure before analysis:

| Field | Description |
|---|---|
| `date` | Trading date (daily frequency) |
| `symbol` | Instrument or benchmark identifier (`AAPL`, `SP500`) |
| `close` | Closing price |
| `provider` | Source of the data |

The full specification lives in [`docs/00_MARKETPULSE_FUNCTIONAL_CONTRACT.md`](docs/00_MARKETPULSE_FUNCTIONAL_CONTRACT.md).

## Metrics

Computed over the common historical window for the instrument and the benchmark:

- Cumulative return over the lookback period
- Daily returns
- Relative performance (instrument minus benchmark)
- Rebased series (base 100) for chart comparison

## Testing

```bash
pytest tests/
```

## Git workflow

- `main`: stable, validated version
- One feature branch per task: `feature/<short-description>`
- Small, atomic commits with explicit messages (e.g. `feat: add yfinance provider`)
- Merge through Pull Request, reviewed by at least one teammate

## Documentation

| Document | Purpose |
|---|---|
| [Functional contract](docs/00_MARKETPULSE_FUNCTIONAL_CONTRACT.md) | What the application must deliver |
| [TD sequence & learning path](docs/06_TD_SEQUENCE_AND_LEARNING_PATH.md) | Course progression (18h) |
| [Bloomberg instructor reference](docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md) | `APPROVED_SAMPLE` mode details |

## Team

**Team g07-til** — ESILV A4, course MESIFI472326.

| Member | GitHub |
|---|---|
| Lucille | [@Lucille865](https://github.com/Lucille865) |
| Ines | |
| Tom | |

## License

Academic project — ESILV, De Vinci Higher Education.
