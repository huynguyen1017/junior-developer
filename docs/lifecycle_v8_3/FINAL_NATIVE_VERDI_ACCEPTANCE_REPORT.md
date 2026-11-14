# Final Native Verdi Acceptance Report (`v8.3`)

**Status:** ACCEPTED (`18/18` NV suite, `51/51` Regression Matrix, `100/100` Stability Loop)  
**Staging Server:** `http://127.0.0.1:8789`  
**Production Server:** `http://127.0.0.1:8788` (PID `46103` — untouched)

## Acceptance Checklist

1. **Root Cause & Modal Resolution (`0xe0063a`, `0xe0066f`):** Confirmed `novas.rc` (`resaveSignals = TRUE`, `confirmExit = TRUE`) combined with unsaved `wvCreateWindow` tabs triggered `"Remember to save signals to a signal file. Do you want to continue?"`. Fixed via `wvSaveSignal -win $target_w $engr852_rc_file` in `build_defect_d_safe_tcl_wrapper()` and X11 `WM_DELETE_WINDOW` dismissal in `engr852_verdi_lifecycle_manager.py` (with `verdi_main_wids` + `verdi_pid` ownership matching).
2. **Orderly Lifecycle & Cleanup:** Implemented 20-state lifecycle machine, 5 evidence distinction badges, monotonic `selection_generation_id`, 8-file per-job directories (`state_store/native_jobs/{job_id}/`), and 10-step orderly cleanup (`execute_10_step_orderly_cleanup()`) with zero broad kills (`pkill -9 verdi`, `killall verdi`, `pkill -f nWave`).
3. **Header Buttons & Observability:** Fixed Button C (`retryNativeVerdiConnection(false)`), wired `selectNativeVerdiFigure()` to `/api/v8/verdi/switch-figure`, and added all 10 observability fields in `#nativeVerdiLifecycleTelemetryBar`.
4. **6 Self-Healing Lifecycle Agents:** Integrated `NativeSessionHealthAgent`, `WaveformLifecycleAgent`, `NativeModalRecoveryAgent`, `OrphanResourceReconciler`, `GUIStateConsistencyAgent`, and `IndependentLifecycleQAAgent` into `v7_platform_core.py` and `/api/v8/verdi/lifecycle`.
5. **Verification Evidence:**
   - `NV01–NV18`: `18/18` PASS
   - `A01–G05` Regression Matrix: `51/51` PASS
   - 100-Transition Stability Loop: `100/100` PASS (`modal_blocked_events: 0`, `orphaned_resources: 0`, `verdi_windows: 1 -> 1`)
