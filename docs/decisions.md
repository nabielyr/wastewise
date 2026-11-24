# Decision Log

Technical decisions for WasteWise, newest at the bottom. Each entry records what was decided and why,
so later phases (and the README) can point back here.

## Template

```
### D-XXX: <short title>
- Date: YYYY-MM-DD
- Phase / step: <e.g. 4.1>
- Decision: <what was decided>
- Reason: <why>
- Alternatives considered: <what else, and why not>
```

---

### D-001: Local Python 3.12 with plain venv
- Date: 2026-11-17
- Phase / step: 0.4
- Decision: Support `requires-python >=3.11`; develop locally on Python 3.12 in a `.venv` created with `python -m venv`.
- Reason: Only Python 3.12 is installed on the dev machine and `uv` is not available. Nothing in the stack needs 3.11 specifically.
- Alternatives considered: Installing Python 3.11 or `uv` (extra setup for no practical gain). CI will test 3.11 and 3.12.

### D-002: Makefile run through mingw32-make on Windows
- Date: 2026-11-17
- Phase / step: 0.9
- Decision: Keep a portable `Makefile` (all commands go through `$(PY) -m ...`, venv path picked by `$(OS)`) and run it with `mingw32-make` on Windows.
- Reason: GNU `make` is not on PATH, but `mingw32-make` from MSYS2 is. The same Makefile works unchanged on Linux CI.
- Alternatives considered: Installing GNU make, or a Python task runner (adds a dependency, diverges from the plan).

### D-003: Normalize line endings to LF
- Date: 2026-11-17
- Phase / step: 0.2
- Decision: Add `.gitattributes` with `* text=auto eol=lf`.
- Reason: Development happens on Windows while CI runs on Linux; consistent endings keep diffs and pre-commit hooks clean.
- Alternatives considered: Relying on each machine's `core.autocrlf` setting (not reproducible).

### D-004: PLAN.md checkboxes for 0.1 to 0.10 ticked retroactively
- Date: 2026-11-22
- Phase / step: 0.11
- Decision: `docs/PLAN.md` was added in step 0.11, so steps 0.1 to 0.10 are ticked in that same commit.
- Reason: The file did not exist earlier, so the "tick in the same commit" rule could only start from 0.11.
- Alternatives considered: None.

### D-005: Anonymous Kaggle download as fallback
- Date: 2026-11-24
- Phase / step: fix after 1.1
- Decision: When no Kaggle credentials are configured, `download.py` downloads the dataset through `python -m kaggle` without logging in. Credentials are only required if that fails.
- Reason: `kannanaikkal/food-demand-forecasting` is public (license DbCL-1.0) and the Kaggle CLI allows logged-out downloads. The Python library only permits anonymous access when it runs as the CLI, so the fallback shells out to it. Verified: the download produces `train.csv`, `fulfilment_center_info.csv`, `meal_info.csv`, `test.csv` (plus `sample_submission.csv`, unused).
- Alternatives considered: Requiring a token for everyone (blocks reproducibility for no benefit on a public dataset).
