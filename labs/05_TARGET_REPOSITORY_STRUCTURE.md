# Target Repository Structure

## 1. Principle

Students do not receive the final architecture on day one.

MarketPulse starts with one Python file and evolves only when a new requirement creates a clear reason to separate responsibilities.

The 18-hour CORE deliberately avoids advanced Python packaging.

The goal is to understand:

- where data comes from;
- where provider-specific logic belongs;
- where shared analytics belong;
- how terminal and dashboard presentation reuse the same application logic;
- how the repository evolves through Git history.

## 2. Starter repository

Initial structure:

```text
esilv-marketpulse/
├── README.md
├── TEAM_TEMPLATE.md
├── CONTRIBUTING.md
├── .gitignore
├── requirements.txt
├── config/
│   └── settings.yml
├── data/
│   └── sample/
│       ├── instruments.json
│       └── prices.csv
├── docs/
│   ├── 00_MARKETPULSE_FUNCTIONAL_CONTRACT.md
│   ├── 01_STUDENT_ONBOARDING.md
│   ├── 02_MARKETPULSE_USE_CASE.md
│   ├── 03_GITHUB_TEAM_WORKFLOW.md
│   ├── 04_CHECKPOINTS_AND_EVIDENCE.md
│   ├── 05_TARGET_REPOSITORY_STRUCTURE.md
│   ├── 06_TD_SEQUENCE_AND_LEARNING_PATH.md
│   ├── 07_TD_TRANSVERSE_REVIEW_AND_REBALANCING.md
│   ├── 08_TD_REMEDIATION_PLAN.md
│   ├── 09_YAHOO_FINANCE_INSTRUCTOR_REFERENCE.md
│   ├── 10_BLOOMBERG_INSTRUCTOR_REFERENCE.md
│   ├── 11_BLOOMBERG_PROVIDER_SCAFFOLD.md
│   ├── 12_MARKETPULSE_APPLICATION_SNAPSHOT_CONTRACT.md
│   ├── 13_MARKETPULSE_LIBRARIES_AND_DEPENDENCIES.md
│   ├── 14_TEACHING_READINESS_AND_DRY_RUN_PLAN.md
│   ├── 15_INSTRUCTOR_CONTINGENCY_AND_RECOVERY_PLAYBOOK.md
│   ├── 16_TEACHING_BASELINE_RELEASE.md
│   └── labs/
├── evidence/
│   └── README.md
└── src/
    └── main.py
```

This structure is intentionally small.

## 3. Frozen CORE architecture

The CORE architecture for the 18 hours is now fixed as:

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

Not every file exists on day one.

The structure appears progressively as the business requirements evolve.

## 4. Progressive evolution

### TD01 to TD06 - Starter and Git foundations

```text
src/
└── main.py
```

At this stage, students focus on:

- local CSV / JSON data;
- Python fundamentals;
- Git history;
- branches;
- Pull Requests;
- code review.

No additional Python architecture is required.

### TD07 - Shared analytics appear

```text
src/
├── main.py
└── analytics.py
```

`analytics.py` becomes the home of reusable comparison logic such as:

- date alignment;
- period return;
- base-100 normalization;
- relative performance.

Provider-specific identifiers do not belong in this file.

### TD08 - Yahoo Finance provider appears

```text
src/
├── main.py
├── analytics.py
└── providers/
    ├── __init__.py
    └── yahoo_provider.py
```

`yahoo_provider.py` owns Yahoo-specific acquisition and normalization.

The rest of MarketPulse continues to use canonical rows.

### TD09 - Bloomberg mapping is documented

TD09 does not require a new Python module yet.

The main deliverable is:

```text
docs/BLOOMBERG_FIELD_MAPPING.md
```

### TD10 - Bloomberg provider appears

```text
src/
├── main.py
├── analytics.py
└── providers/
    ├── __init__.py
    ├── yahoo_provider.py
    └── bloomberg_provider.py
```

`bloomberg_provider.py` owns Bloomberg-specific acquisition and normalization.

The shared analytics remain unchanged.

### TD11 - Dashboard entry point appears

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

The dashboard is deliberately a single CORE entry point.

This avoids introducing package and import complexity that is not required by the module.

### TD12 - Release structure is validated

TD12 does not introduce a new application layer.

It validates the integrated structure already built through TD11.

## 5. Target CORE repository

A possible final CORE repository is:

```text
esilv-marketpulse/
├── README.md
├── TEAM.md
├── TEAM_TEMPLATE.md
├── CONTRIBUTING.md
├── requirements.txt
├── .gitignore
├── config/
│   └── settings.yml
├── data/
│   └── sample/
│       ├── instruments.json
│       └── prices.csv
├── src/
│   ├── main.py
│   ├── analytics.py
│   ├── dashboard.py
│   └── providers/
│       ├── __init__.py
│       ├── yahoo_provider.py
│       └── bloomberg_provider.py
├── docs/
│   ├── labs/
│   └── ...
└── evidence/
    ├── checkpoint-a/
    ├── checkpoint-b/
    └── checkpoint-c/
```

The exact content of student repositories may vary slightly, but the CORE Python paths above are the common reference.

## 6. Responsibility map

```text
src/main.py
=
application orchestration
+
build_market_snapshot(...)
+
terminal presentation

src/analytics.py
=
shared comparison logic

src/providers/yahoo_provider.py
=
Yahoo-specific acquisition
+
Yahoo-to-canonical normalization

src/providers/bloomberg_provider.py
=
Bloomberg-specific acquisition
+
Bloomberg-to-canonical normalization

src/dashboard.py
=
Dash presentation
+
snapshot consumption
```

The shared application result is defined in:

```text
docs/12_MARKETPULSE_APPLICATION_SNAPSHOT_CONTRACT.md
```

For the flat CORE structure, `build_market_snapshot(...)` lives in `src/main.py`.

The architectural rule is:

```text
provider-specific code
        |
        v
canonical rows
        |
        v
shared analytics
        |
        v
application snapshot
        |
        +----------------+
        |                |
        v                v
terminal output      Dash output
```

## 7. CORE execution paths

The intended CORE entry points are:

```bash
python src/main.py
python src/dashboard.py
```

The dashboard entry point is introduced only in TD11.

Before TD11, only the terminal entry point is required.

## 8. Configuration status

`config/settings.yml` is part of the repository as a human-readable configuration contract.

Parsing YAML is not required by the 18-hour CORE.

Students should not add PyYAML solely to satisfy the existence of this file.

If the teaching team later decides to wire YAML into the application, that is a separate explicit extension.

## 9. Important CORE exclusions

The common target does not require:

```text
src/marketpulse/
tests/
Dockerfile
.github/workflows/
Kubernetes
complex packaging
advanced CI/CD
```

These are outside the common 18-hour scope unless explicitly introduced as optional material.

## 10. Optional professional evolution

After the CORE sequence, a team may explore a more formal package structure such as:

```text
src/
└── marketpulse/
    ├── __init__.py
    ├── app.py
    ├── analytics.py
    ├── providers/
    └── dashboard/
```

This is an architectural extension, not a mandatory TD requirement.

Students must not be penalized for keeping the frozen CORE structure.

## 11. Market comparison flow

MarketPulse ultimately handles:

```text
Instrument
+
Benchmark
   |
   v
same period
+
same interval
   |
   v
performance comparison
```

The common contract remains:

```text
lookback = 1mo
interval = 1d
```

unless the instructor explicitly revises the common configuration.

## 12. Final criterion

The goal is not to reproduce a directory tree mechanically.

A successful team should be able to explain:

- why `analytics.py` was introduced;
- why providers are separated;
- why provider-specific identifiers do not leak into analytics;
- why terminal and Dash presentation share the same calculations;
- how Git history reflects the repository evolution;
- how another student can clone and run the project.
