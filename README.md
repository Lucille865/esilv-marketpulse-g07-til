# ESILV MarketPulse

<p align="center">
  <img
    src="https://www.itii-pdl.com/wp-content/uploads/2024/11/logo_esilv_couleur.jpg?ver=1733410620"
    alt="ESILV - De Vinci Higher Education"
    width="100"
  />
</p>

![Course](https://img.shields.io/badge/course-MESIFI472326-1f6feb.svg)
![ESILV A4](https://img.shields.io/badge/ESILV-A4-111827.svg)
![Python](https://img.shields.io/badge/Python-3.x-3776AB.svg)
![Labs](https://img.shields.io/badge/labs-12-2ea44f.svg)
![TD](https://img.shields.io/badge/TD-18h-orange.svg)
![Access Mode](https://img.shields.io/badge/Bloomberg-APPROVED__SAMPLE-blue.svg)

**MarketPulse** is a multi-source financial market data
application developed as part of the ESILV A4 Python, Git
and Linux module.

> Acquire market data from several provider stages, normalize
> it to one canonical contract, compare one instrument with
> its benchmark, then expose the same application result
> through the terminal and a Dash dashboard.

---

## Languages and Tools

<p align="center">
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original.svg" alt="Git" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/github/github-original.svg" alt="GitHub" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="Linux" width="40" height="40"/>
  <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bash/bash-original.svg" alt="Bash" width="40" height="40"/>
  <img src="https://logos-world.net/wp-content/uploads/2020/10/Yahoo-Emblem.png" alt="Yahoo Finance" width="40" height="40"/>
  <img src="https://img.shields.io/badge/Dash-008DE5?logo=plotly&amp;logoColor=white" alt="Dash" height="40"/>
  <img src="https://cdn.simpleicons.org/plotly/3F4F75" alt="Plotly" width="40" height="40"/>
  <img src="https://img.shields.io/badge/Bloomberg-000000?logo=bloomberg&amp;logoColor=white" alt="Bloomberg" height="40"/>
</p>

---

## 1. Project Overview

MarketPulse compares the financial performance of an instrument
against a market benchmark over a common historical period.

The application provides two interfaces:

- A terminal-based application.
- A web dashboard built with Dash and Plotly.

The central business question is:

> Is the selected instrument outperforming or underperforming
> its benchmark over the same period and frequency?

The project was progressively developed through 12 practical
labs covering Python, Linux, Git, financial data acquisition,
normalization, analytics and graphical presentation.

---

## 2. Market Configuration

| Parameter | Value |
|---|---|
| Instrument | AAPL - Apple Inc. |
| Benchmark | SP500 - S&P 500 |
| Historical window | 1 month |
| Interval | Daily |
| Final provider | Bloomberg stage |
| Access mode | APPROVED_SAMPLE |

### Provider progression

```text
CSV / JSON
    |
    v
Yahoo Finance
    |
    v
Bloomberg stage
    |
    v
Canonical Market Data
    |
    v
Shared Analytics
    |
    v
Application Snapshot
    |
    +----------------+
    |                |
    v                v
Terminal            Dash
```

---

## 3. Data Providers

MarketPulse includes three data acquisition paths:

### Local CSV / JSON

The initial implementation uses local educational datasets
to provide deterministic and reproducible financial data.

### Yahoo Finance

The Yahoo Finance provider retrieves financial data using
the yfinance Python library.

Provider identifiers:

| Canonical ticker | Yahoo Finance identifier |
|---|---|
| AAPL | AAPL |
| SP500 | ^GSPC |

### Bloomberg Stage

The Bloomberg provider supports the normalization of
approved Bloomberg-stage input.

Provider identifiers:

| Canonical ticker | Bloomberg identifier |
|---|---|
| AAPL | AAPL US Equity |
| SP500 | SPX Index |

The final implementation uses:

```text
Provider: Bloomberg stage
Access mode: APPROVED_SAMPLE
Live connectivity: not demonstrated
```

The sample data is available in:

```text
data/sample/bloomberg_reference_sample.json
```

The expected canonical reference is available in:

```text
data/sample/bloomberg_reference_expected.json
```

The mapping contract is documented in:

[Chapter 9 - Bloomberg Field Mapping](docs/BLOOMBERG_FIELD_MAPPING.md)

---

## 4. Bloomberg Access Modes

The Bloomberg stage supports two authorized teaching modes:

### LIVE

The instructor-approved Bloomberg environment successfully
returns financial data.

### APPROVED_SAMPLE

The instructor-provided fallback dataset is used to validate
the provider boundary and the normalization contract.

The final version of MarketPulse uses APPROVED_SAMPLE.

```text
APPROVED_SAMPLE != LIVE Bloomberg connectivity
```

No LIVE Bloomberg connection has been established or claimed.

The teaching wrapper keys used in the sample JSON are not
Bloomberg LIVE field mnemonics.

---

## 5. Financial Analytics

MarketPulse implements three core financial indicators.

### Period Return

Measures the performance of an asset between the first
and last observations of the selected period.

```text
Period Return = (Final Price / Initial Price - 1) * 100
```

### Relative Performance

Measures the difference between the instrument return
and the benchmark return.

```text
Relative Performance = Instrument Return - Benchmark Return
```

The result is expressed in percentage points.

### Base-100 Normalization

Allows the instrument and benchmark to be compared
independently of their original price levels.

```text
Base 100 = Current Price / Initial Price * 100
```

Both series start at 100.

All financial calculations are implemented in analytics.py
and reused by both application interfaces.

---

## 6. Application Architecture

```text
src/
├── main.py
├── analytics.py
├── dashboard.py
└── providers/
    ├── __init__.py
    ├── yahoo_provider.py
    └── bloomberg_provider.py
```

### Responsibilities

| Component | Responsibility |
|---|---|
| providers/ | Data acquisition and normalization |
| analytics.py | Time series alignment and financial calculations |
| main.py | Application orchestration and shared snapshot |
| dashboard.py | Dash graphical presentation |

### Canonical Data Structure

All providers produce the same canonical row structure:

```text
date
ticker
open
high
low
close
volume
```

Provider-specific identifiers remain inside their respective
provider boundaries.

The analytical layer only receives canonical data.

### Shared Application Snapshot

Both interfaces consume the same application result through:

```python
build_market_snapshot()
```

The snapshot contains:

```text
provider
access_mode
lookback
interval
instrument
benchmark
instrument_return
benchmark_return
relative_performance
instrument_base_100
benchmark_base_100
```

The application follows the design principle:

```text
Acquire once
Normalize once
Calculate once
Present many times
```

The dashboard does not directly call financial providers
and does not duplicate analytical calculations.

---

## 7. Requirements

The application requires:

- Python 3 (Python 3.12 used during development)
- Git
- A web browser
- Internet access for dependency installation

Direct Python dependencies:

```text
yfinance
dash
plotly
```

All required dependencies are recorded in requirements.txt.

No Bloomberg-specific Python package is required for the
APPROVED_SAMPLE implementation.

---

## 8. Installation

Clone the team repository:

```bash
git clone https://github.com/Lucille865/esilv-marketpulse-g07-til.git
```

Enter the project directory:

```bash
cd esilv-marketpulse-g07-til
```

Install the required Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Verify the installed dependencies:

```bash
python -m pip check
```

All application commands must be executed from the
repository root.

---

## 9. Run the Terminal Application

Execute:

```bash
python src/main.py
```

The terminal displays:

- Data provider.
- Access mode.
- Instrument and benchmark.
- Historical window.
- Observation frequency.
- Instrument return.
- Benchmark return.
- Relative performance.
- Final base-100 values.

---

## 10. Run the Dashboard

Execute:

```bash
python src/dashboard.py
```

Open the following address in a web browser:

```text
http://127.0.0.1:8050/
```

The dashboard displays:

- Market configuration.
- Provider and access mode.
- Instrument and benchmark.
- Instrument return.
- Benchmark return.
- Relative performance.
- Instrument vs Benchmark base-100 chart.

The dashboard is a presentation layer built with Dash
and Plotly.

It consumes the shared application snapshot without
recomputing financial results.

To stop the server, press:

```text
Ctrl + C
```

---

## 11. Reference Financial Results

The Bloomberg educational sample produces approximately
the following financial results:

| Indicator | Result |
|---|---:|
| AAPL period return | +6.48% |
| SP500 period return | +2.15% |
| Relative performance | +4.33 percentage points |
| AAPL initial base 100 | 100.00 |
| SP500 initial base 100 | 100.00 |
| AAPL final base 100 | 106.48 |
| SP500 final base 100 | 102.15 |

AAPL outperforms the S&P 500 benchmark over the
selected sample period.

The terminal and dashboard consume the same financial
results.

These values come from educational sample data and
must not be interpreted as live market prices.

---

## 12. Environment Constraints

The final implementation uses the APPROVED_SAMPLE
Bloomberg access mode.

Therefore:

- No Bloomberg account is required.
- No Bloomberg API credential is required.
- No professional Bloomberg terminal is required.
- No live Bloomberg connection is required.

Internet access is generally required to install Python
dependencies and use the Yahoo Finance provider.

The local Bloomberg sample can be processed without
live market connectivity once the dependencies are installed.

---

## 13. Reproducibility

MarketPulse is intended to be reproducible from a clean
repository checkout.

The standard execution sequence is:

```bash
git clone https://github.com/Lucille865/esilv-marketpulse-g07-til.git
cd esilv-marketpulse-g07-til
python -m pip install -r requirements.txt
python src/main.py
python src/dashboard.py
```

A successful reproducibility test requires:

- Access to the team repository.
- A compatible Python environment.
- Successful dependency installation.
- Availability of the provided sample data.
- Successful terminal execution.
- Successful dashboard execution.

The application does not depend on a personal workstation
path or LIVE Bloomberg access.

---

## 14. Git Collaboration Workflow

The team follows a collaborative Git and GitHub workflow:

```text
Working branch
      |
      v
Commit
      |
      v
Push
      |
      v
Pull Request
      |
      v
Review
      |
      v
Merge into main
```

Team members develop and validate their contributions
before integrating them into the shared main branch.

---

## 15. Learning Path

### Wave 1 - Foundations - 3h

- TD01 - Bootstrap + Linux
- TD02 - Python + CSV / JSON

### Wave 2 - Git and Collaboration - 6h

- TD03 - Git Local Workflow
- TD04 - Branches + Merge
- TD05 - Remote Branch + Pull Request
- TD06 - Code Review

### Wave 3 - Comparison and Yahoo Finance - 3h

- TD07 - Data Normalization + Comparison
- TD08 - Yahoo Finance

### Wave 4 - Professional Integration - 6h

- TD09 - Bloomberg Introduction
- TD10 - Bloomberg Provider
- TD11 - Dash Dashboard
- TD12 - Integration + Release

---

## 16. Documentation and Evidence

The repository contains the practical session reports,
reference materials and implementation documentation.

```text
Rendu-TP/
labs/
docs/
```

Individual practical session reports are available under:

```text
Rendu-TP/
```

The reports document the implementation steps, terminal
outputs, dashboard screenshots and Git contributions.

The Bloomberg mapping contract is available at:

```text
docs/BLOOMBERG_FIELD_MAPPING.md
```

Screenshots complement Git history and application execution.
They do not replace functional validation.

---

## 17. Security

Sensitive information must never be committed to GitHub.

Examples include:

- Passwords.
- API keys.
- Access tokens.
- SSH private keys.
- Bloomberg credentials.
- Cloud credentials.
- Billing information.
- Session secrets.

Temporary Python files, local environment files and
development artifacts are excluded through .gitignore.

Provider evidence must never be fabricated.

---

## 18. Project Scope

The CORE application focuses on:

- Python programming.
- Financial data acquisition.
- Canonical normalization.
- Shared financial analytics.
- Git collaboration.
- Dash visualization.
- Reproducibility.

The project does not require:

- Docker.
- Kubernetes.
- GitHub Actions.
- Advanced CI/CD.
- Complex deployment infrastructure.
- Advanced quantitative finance.

---

## Academic Information

**Course:** MESIFI472326 - Python, Git, Linux

**School:** ESILV - A4

**Project:** MarketPulse - Multi-Source Financial Market Data Dashboard

**Repository:** Lucille865/esilv-marketpulse-g07-til

**Practical sessions:** TD01 - TD12

**Final provider:** Bloomberg stage - APPROVED_SAMPLE

---

ESILV MarketPulse - Financial Data Analysis and Visualization