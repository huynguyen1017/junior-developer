# JUNIOR DEVELOPER v8.2 — 10-Agent Orchestration Design (`MASTER-RECOVERY-v8.2`)

- **Endpoint**: `GET /api/v8/agents/status?fig_id=fig10`
- **Network Health Endpoint**: `GET /api/v8/network/health?fig_id=fig10`

## 10-Agent Architecture & Responsibilities

| Order | Agent ID | Primary Responsibility | Bounded Safety & Fail-Closed Contract |
|---|---|---|---|
| 1 | `NetworkHealthAgent` | Probes Local Host -> GlobalProtect `utun` -> DNS -> TCP `:22` -> SSH `BatchMode` -> XQuartz `DISPLAY`. | Circuit breaker (`CLOSED` / `HALF_OPEN` / `OPEN`), exponential backoff (`10s -> 20s -> 40s -> 60s`), `0600` redacted telemetry (`state_store/network_health/latest.json`). Never kills user VPN or modifies routing tables. |
| 2 | `DeviceSessionAgent` | Tracks Device A (`macbook_air`) and Device B (`imac`) companion heartbeats, 60s TTL expiration, pairing/revocation, and capability scoring. | Never hardcodes secondary device readiness; expires stale heartbeats after 60s. |
| 3 | `VerdiExecutionAgent` | Executes non-blocking asynchronous Native Verdi jobs (`POST /api/v1/native-jobs` -> HTTP `202 Accepted`) with per-`(user, project, fig_id)` concurrency deduplication. | Uses braced Tcl signal paths (`set sig_path {{{sp}}}`) so bus brackets `[12:0]` never trigger Tcl command substitution. |
| 4 | `SignalVerificationAgent` | Enforces 3-layer waveform verification: Layer 1 (`fsdb2vcd` variable count), Layer 2 (`ENGR852_SIGNAL_ADDED` + `ENGR852_NWAVE_VERIFIED`), Layer 3 (`nWave` green/yellow pixel scanlines). | Strictly rejects empty logs and 3-signal partial `<nWave:4>` windows (`added_ok=False`, `verified_nwave_handle="UNVERIFIED"`). |
| 5 | `PopupStreamAgent` | Discovers live Novas/Verdi X11 windows, captures window-only `xwd` frames, applies 3-zone privacy redaction, and serves `/api/v8/verdi/live-frame.png`. | Requires explicit `job_id`, rejects figure/job mismatch (`409`), and blocks unredacted captures (`422`). |
| 6 | `UIStateIntegrityAgent` | Synchronizes figure selector, 10-row diagnostic table, signal table, and JSON telemetry. | Never displays `EDUCATIONAL_SIMULATION` or `RECORDED_VERIFIED_CAPTURE` as live `REAL_APPLICATION_CAPTURE`. |
| 7 | `FailureRecoveryAgent` | Runs bounded 15-step non-destructive recovery runbook (`POST /api/v8/verdi/recover` / `POST /api/v1/native-jobs/{job_id}/recover`). | Never touches production port `8788` or active user applications. |
| 8 | `SecurityPrivacyAgent` | Enforces Bearer session/companion auth, CSRF validation on mutating routes, `0600` raw artifact mode, and recursive JSON redaction. | Rejects unauthenticated job launches (`401`) and forged Bearer tokens on `/api/v8/verdi/live-status` (`401`). |
| 9 | `MobileExperienceAgent` | Validates responsive CSS across desktop (`1440x900`), tablet (`768x1024`), and mobile (`390x844`). | Scrollable tables, wrapped status pills, `>=44px` touch targets, no clipped modals. |
| 10 | `ReleaseVerificationAgent` | Maintains `QA_ACCEPTANCE_MATRIX.json` and `STAGING_RELEASE_MANIFEST.json`. | Strictly separates `UNIT_TEST_PASS`, `MOCKED_FAILURE_CLASSIFICATION_PASS`, `BACKEND_INTEGRATION_PASS`, and live waveform verification status. |
