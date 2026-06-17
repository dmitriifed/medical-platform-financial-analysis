# Bug Fix Log

## BUG-001 · run.bat — wrong venv path
**File:** `run.bat`
**Date:** 2026-04-08

**Problem:** `run.bat` checked for `.venv` and called `.venv\Scripts\python.exe`, but the local virtual environment is named `venv`. Script exited silently with no output.

**Fix:** Replaced all `.venv` references with `venv`.

---

## BUG-002 · Chart 7.5 — NameError: `doc_rev` not defined
**File:** `notebooks/quick_viz_4.ipynb` — Cell 72 (Chart 7.5 · Pareto — Doctors → Revenue)
**Date:** 2026-04-08

**Problem:** Cell 72 used `doc_rev` which was defined in a separate cell (Cell 71) marked `%%script false` (disabled). Running Cell 72 in isolation raised `NameError: name 'doc_rev' is not defined`.

**Fix:** Rewrote Cell 72 to be self-contained — added imports, data load from `crm_stage_finished.xlsx`, and `doc_rev` computation directly inside the cell. Replaced `mpl_show` / `plotly_capture` helpers with `plt.show()` / `pf.show()` to remove dependency on setup cells.

---

## BUG-003 · quick_viz_4.ipynb — truncated/corrupted file
**File:** `notebooks/quick_viz_4.ipynb`
**Date:** 2026-04-08

**Problem:** The notebook file was truncated mid-cell during a write operation (cut off at char 83489, line 1747). The JSON was malformed — source array, cell object, cells array, and notebook object were all left unclosed. `json.loads()` raised `JSONDecodeError: Expecting ',' delimiter`.

**Fix:** Appended the missing source lines for Chart 7.5, then closed the JSON structure (`source` array → cell object → cells array → notebook metadata object). Verified with `json.loads()` before writing — result: 73 cells, JSON valid.