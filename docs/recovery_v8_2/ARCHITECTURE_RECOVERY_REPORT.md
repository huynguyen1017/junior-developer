# JUNIOR DEVELOPER v8.2 — Architecture Recovery Report (`MASTER-RECOVERY-v8.2`)

- **Date**: `2026-11-12`
- **Target Staging Environment**: `/Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged` (`http://127.0.0.1:8789`)
- **Production Environment**: `http://127.0.0.1:8788` (PID `46103` — **100% Untouched**)
- **Primary Completed ASIC Project**: `main` branch (`V9` — **100% Untouched**)
- **Preserved Pre-v8.2 Snapshot**: `/Users/huynguyen/Developer/ENGR852_Stability_Recovery_20261111/backups/pre_v8_2_snapshot/`

---

## 1. Executive Summary of Architectural Recovery

1. **Preservation of ChatGPT Connection Stability Hotfix (`2026-11-11`)**:
   - Retained the LaunchAgent supervision (`~/Library/LaunchAgents/com.juniordeveloper.engr852.staging8789.plist`), `manage_staging_8789.sh` lifecycle script, explicit `-F ~/.ssh/config` SSH transport argument resolution, and split **Refresh Diagnostics (Safe)** vs. **Reconnect & Verify SSH/Verdi** UI controls.
2. **Forensic Root-Cause Resolution of the `<nWave:4>` 3-Signal Defect (`P0 NATIVE VERDI REPAIR DIRECTIVE`)**:
   - **Observed Symptom**: In `fig10_chatrecovery_20261111/verdi_native_process.log`, Synopsys Verdi opened `<nWave:4>` and added only `clock`, `start`, and `count[12:0]`, then aborted with:
     ```text
     ENGR852_SIGNAL_ADDED win=2b2c18c0 sig=/motion_v5_16bit_top_regression_tb/clock rc=0
     ENGR852_SIGNAL_ADDED win=2b2c18c0 sig=/motion_v5_16bit_top_regression_tb/start rc=0
     TclPlay: invalid command name "12:0", error line=41
     ```
   - **Root Cause**: `build_defect_d_safe_tcl_wrapper()` previously interpolated `{sp}` directly inside a Tcl double-quoted string (`puts "ENGR852_SIGNAL_ADDED win=$engr852_primary_win sig={sp} rc=0"`). In Tcl, square brackets `[...]` inside double quotes trigger command substitution. As soon as `wvAddSignal` added `/motion_v5_16bit_top_regression_tb/dut/ctl_u/count[12:0]`, Tcl attempted to execute `12:0` as a Tcl command, fatally aborting the TclPlay script before the remaining 14 signals (`S1S2mux[15:0]` through `completed`) or `ENGR852_NWAVE_VERIFIED` could execute.
   - **Secondary Compounding Causes**:
     - Sourced original Tcl scripts referencing `$_Verdi_1` or stale `_nWave2` handles could raise unguarded errors unless `_Verdi_1` was pre-initialized and `source` was wrapped in `catch`.
     - `build_signal_verification_records()` previously defaulted `added_ok=True` when `ENGR852_SIGNAL_ADDED` was absent, and `launch(attach_existing=True)` attached to any open Verdi X11 window without checking whether its `verdi_native_process.log` had actually passed `ENGR852_NWAVE_VERIFIED`.
   - **Architectural Fix**:
     - `build_defect_d_safe_tcl_wrapper()` now assigns each signal path in braces (`set sig_path {{{sp}}}`) and references `$sig_path` inside `wvAddSignal` and `puts`, completely preventing Tcl bracket command substitution across all 17 signals (`verified_signals=17/17` in `tclsh`).
     - `build_signal_verification_records()` is now strictly fail-closed (`added_ok=False`, `verified_nwave_handle="UNVERIFIED"` unless both `ENGR852_SIGNAL_ADDED` and `ENGR852_NWAVE_VERIFIED` are present in the process log).
     - `launch(attach_existing=True)` now inspects `_find_verified_process_log_for_window()` and refuses to attach to a half-populated X11 window, forcing a clean relaunch when prior Tcl execution was incomplete.
3. **Durable Asynchronous Native Verdi Job Orchestration (`/api/v1/native-jobs`)**:
   - Implemented `start_async_native_verdi_job()` in `v7_platform_core.py` and exposed `POST /api/v1/native-jobs` (returning HTTP `202 Accepted` in `< 50 ms`), `GET /api/v1/native-jobs/{job_id}`, `GET /api/v1/native-jobs/{job_id}/events`, `POST /api/v1/native-jobs/{job_id}/capture`, `POST /api/v1/native-jobs/{job_id}/recover`, and `POST /api/v1/native-jobs/{job_id}/cancel` with per-`(user_id, project_id, fig_id)` active job deduplication.
4. **10-Agent Orchestration & Bounded NetworkHealthAgent**:
   - Implemented `get_network_health_telemetry()` with circuit breaker (`CLOSED`, `HALF_OPEN`, `OPEN`), exponential backoff (`10s -> 20s -> 40s -> 60s`), and mode-`0600` redacted telemetry at `practice_from_scratch/web_console/state_store/network_health/latest.json`, alongside `GET /api/v8/agents/status` and `GET /api/v8/network/health`.
