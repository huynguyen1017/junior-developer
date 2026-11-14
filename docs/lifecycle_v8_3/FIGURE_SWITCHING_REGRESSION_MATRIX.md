# Figure Switching Regression Matrix (`v8.3`)

**Generated:** `2026-11-12T22:37:07.730260+00:00`  
**Source Matrix JSON:** `docs/lifecycle_v8_3/FIGURE_SWITCHING_REGRESSION_MATRIX.json`  
**Staging Target:** `http://127.0.0.1:8789` (Production `127.0.0.1:8788` untouched)

## Summary

| Suite | Passed | Total | Status |
|---|---:|---:|---|
| `NV01–NV18` Native Verdi Bridge Failure & Verification | 18 | 18 | PASS |
| `A01–G05` Lifecycle, Modal, Cleanup & Production Safety | 51 | 51 | PASS |
| 100-Transition Stability Loop | 100 | 100 | PASS |

## Group Breakdown (`51/51`)

| Group | Passed | Total | Coverage |
|---|---:|---:|---|
| `A — Native launch` | 6 | 6 | Live launch, attach-existing, missing FSDB/Tcl/X11/SSH failure states |
| `B — Figure switching` | 10 | 10 | `fig7` ↔ `fig8` ↔ `fig9` ↔ `fig10` ↔ `fig11` ↔ `layout`, monotonic `selection_generation_id`, `.rc` backup |
| `C — Modal dialog` | 8 | 8 | `0xe0063a` / `0xe0066f` `"Question"` detection, `WM_DELETE_WINDOW` dismissal, non-Verdi isolation |
| `D — Refresh and reconnect` | 8 | 8 | Button A (`Launch / Verify`), Button B (`Refresh Capture`), Button C (`Retry / Reconnect`), live status telemetry |
| `E — Cleanup` | 10 | 10 | 10-step orderly cleanup, 8-file job directory, zero `pkill -9 verdi` / `killall verdi` / `pkill -f nWave` |
| `F — Physical layout` | 4 | 4 | `layout` mapped to `v9_closure/top.dlib` (`LAYOUT_TOOL_SEPARATE_FROM_VERDI_NWAVE`), Verdi preserved |
| `G — Production safety` | 5 | 5 | Port `8788` PID `46103` untouched, GlobalProtect VPN & unrelated SSH/XQuartz untouched |
