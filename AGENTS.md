# AGENTS.md — car-price-estimator

## State
- Data repo: `used-cars.csv` (3,915 rows + header, ~273 KB) committed at `b462873` on `master` with `.gitignore`. `AGENTS.md` is untracked. No source code, README, manifests, tests, lint/typecheck config, or CI.
- Git 2.56.0 lives at `C:\Program Files\Git\cmd\git.exe` but bare `git` is NOT on PATH in agent sessions — always invoke via the full path (or `$env:Path += ';C:\Program Files\Git\cmd'` first). No `gh` CLI installed.
- `.venv/` exists and is git-ignored; only `pip` installed. Install deps (pandas/scikit-learn/etc.) as needed.

## Data
- Header: `brand,model,year,mileage_miles,fuel_type,transmission,accident_reported,clean_title,price_usd`
- `price_usd` is the target; all others are features.
- `transmission` and `model` are messy free text (e.g. `F`, `2`, `A/T`, `5-Speed A/T`, `Transmission w/Dual Shift Mode`). Normalize before grouping/encoding.
- `accident_reported` is `Yes`/`No`; `clean_title` is `Yes`/`Unknown` — keep `Unknown` as its own category, not null. `fuel_type` also has an `Unknown` level.
- Always re-read the header/first rows before writing parsing code; there is no schema doc.

## Environment
- Windows + PowerShell 5.1: `&&` is not supported as a statement separator — chain with `;` instead.
- Python 3.14 via the `py` launcher (`py --version` works). Bare `python`/`python3` resolve first to a broken Windows Store stub, so use `py -c`, `py -m venv`, or `.venv/Scripts/python.exe` — never assume `python` works.
- Venv: created with `py -m venv .venv`; activate with `.\.venv\Scripts\Activate.ps1` from the project root.
- `.gitignore` covers `.venv/` and `__pycache__/`.
- No build/test/lint commands exist. Verify work by running small scripts, not by guessing at a suite.
