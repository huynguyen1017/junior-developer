# 100-Transition Native Verdi Stability Report (`v8.3`)

**Completed:** `2026-11-12T22:37:07.730260+00:00`  
**Test Runner:** `practice_from_scratch/scripts/test_v8_3_native_verdi_lifecycle_and_100_transitions.py`  
**Staging Server:** `http://127.0.0.1:8789`

## Observed Metrics

| Metric | Observed Value | Requirement |
|---|---:|---|
| Total Transitions | `100` | `100` |
| Successful Transitions | `100` | `100` |
| Failed Transitions | `0` | `0` |
| Incorrect Figure Captures | `0` | `0` |
| Modal-Blocked Events | `0` | `0` |
| Initial → Final Verdi Windows | `1 -> 1` | No window leak |
| Initial → Final SSH/Verdi Procs | `1 -> 1` | No process leak |
| Orphaned Resources | `0` | `0` |
| Test Runner Max RSS | `64,208,896` bytes (`61.23 MiB`) | Bounded |
| Average Transition Latency | `3,016.11 ms` | Responsive |
| Max Transition Latency | `5,532.27 ms` | Bounded |
| Total Loop Duration | `303.78 s` | Completed cleanly |

## Transition Mix Verified

The 100-transition sequence cycled across all 6 figure modes (`fig7`, `fig8`, `fig9`, `fig10`, `fig11`, `layout`), enforcing monotonic `selection_generation_id`, `.rc` signal preservation (`wvSaveSignal -win $target_w $engr852_rc_file`), automatic X11 `WM_DELETE_WINDOW` resolution for any job-owned `"Question"` modal dialog, and strict separation of `layout` (`v9_closure/top.dlib`) from Verdi nWave FSDB waveforms.
