# Waveform Captures & Verification Test Log Catalog

This catalog indexes **every waveform capture** (`.vcd` dumps, Synopsys Verdi/nWave screenshots, Surfer waveform PNGs, XQuartz/SSH step captures, and per-job `verdi_window_redacted.png` captures) and **every preserved verification/test log** collected from `V1` through `v8.3` (`http://127.0.0.1:8789/`).

---

## 1. Raw VCD Waveform Dumps (`46` `.vcd` files preserved)

| File / Location | Size | Origin / Testbench | Key Signal Observations |
| :--- | ---: | :--- | :--- |
| [`verification/v6_clean/motion_v5_16bit_top_regression.vcd`](verification/v6_clean/motion_v5_16bit_top_regression.vcd) | `25.85 MB` | [`verification/v6_clean/motion_v5_16bit_top_regression_tb.sv`](verification/v6_clean/motion_v5_16bit_top_regression_tb.sv) (`520 MHz`, `1.923 ns` period) | Full 3-case 16-bit regression (`(-8,-8)`, `(-3,+2)` `BestDist=16'h0003`, `(+7,+7)` `BestDist=16'h0000`) including `S1S2mux[15:0]`, `SAD[15:0]`, `count[12:0]`, `motionX`, `motionY`, `completed`. |
| [`verification/v6_clean/motion_verification_520mhz.vcd`](verification/v6_clean/motion_verification_520mhz.vcd) | `17.07 MB` | [`tb/motion_verification_520mhz_tb.v`](tb/motion_verification_520mhz_tb.v) | 520 MHz systolic PE & comparator timing verification waveform dump. |
| [`practice_from_scratch/v8_sandboxes/`](practice_from_scratch/v8_sandboxes/) (`44` `simulation.vcd` files) | `774 B – 24 KB` each | Open-source `iverilog` + `vvp` sandbox verification & E2E runs | Generated live by users/E2E tests inside isolated `0700` project run directories and rendered on the `:8789` real VCD canvas viewer. |

---

## 2. Synopsys Verdi nWave, Surfer & Layout Captures (`evidence/screenshots/` — `45` files)

### A. V9 Sign-Off Verdi `nWave` & SAED14 Physical Layout Figures (`fig7`–`fig12` + `layout`)
| Screenshot | Correspondence | What It Verifies |
| :--- | :--- | :--- |
| [`evidence/screenshots/V9_fig7_orig8bit_row1_nWave.png`](evidence/screenshots/V9_fig7_orig8bit_row1_nWave.png) | `fig7` (Original 8-bit Row 1) | Baseline `rtl/8bit/top.v` early systolic window fill & first candidate SAD computation. |
| [`evidence/screenshots/V9_fig8_orig8bit_complete_nWave.png`](evidence/screenshots/V9_fig8_orig8bit_complete_nWave.png) | `fig8` (Original 8-bit Complete) | Baseline 8-bit `BestDist=8'hFF` clipping trap and completion edge at cycle `4,111`. |
| [`evidence/screenshots/V9_fig9_16bit_saturation_row1_nWave.png`](evidence/screenshots/V9_fig9_16bit_saturation_row1_nWave.png) | `fig9` (16-bit Saturation Stress) | `R=8'h00, S=8'hFF` stress proving full-precision `BestDist = 16'hFF00` (`65,280`) with zero overflow/wrap. |
| [`evidence/screenshots/V9_fig10_16bit_perfect_match_0000_nWave.png`](evidence/screenshots/V9_fig10_16bit_perfect_match_0000_nWave.png) | `fig10` (16-bit Perfect Match `0000`) | 17-signal verified capture (`count=0x010f`, `BestDist=16'h0000`, `motionX=0`, `motionY=0`, `completed=1`). |
| [`evidence/screenshots/V9_fig11_16bit_perturbed_sad3_nWave.png`](evidence/screenshots/V9_fig11_16bit_perturbed_sad3_nWave.png) | `fig11` (16-bit Perturbed `SAD=3`) | Signed two's-complement displacement `motionX = 4'he (-2)`, `motionY = 4'hd (-3)` with `BestDist = 16'h0003`. |
| [`evidence/screenshots/V9_fig12_16bit_corner_complete_nWave.png`](evidence/screenshots/V9_fig12_16bit_corner_complete_nWave.png) | `fig12` (16-bit Upper Corner `(+7,+7)`) | Completion hold at cycle `4,111` (`count=0x100f`, `BestDist=16'h0000`, `motionX=4'h7 (+7)`, `motionY=4'h7 (+7)`). |
| [`evidence/screenshots/v9_signoff_clean_layout.png`](evidence/screenshots/v9_signoff_clean_layout.png) | `layout` (SAED14nm P&R GDSII) | Post-route 14nm FinFET standard-cell layout (`125.07 x 62.80 um`, `0 / 242` ICV DRC clean). |

### B. Earlier Development Waveform & Surfer Captures (`V2`–`V4`)
- `Motion_Verdi_application_only_REDACTED.png`, `Motion_nWave_520MHz_Precision_ACTUAL_traces.png`
- `V2_Direct_Surfer_FullApplication_PrivacySafe.png`, `V2_Direct_Surfer_Waveform_Detailed.png`
- `V2_PESaturation_Surfer_FullApplication_PrivacySafe.png`, `V2_PESaturation_Surfer_Waveform_Detailed.png`
- `V2_Perturbed_Surfer_FullApplication_PrivacySafe.png`, `V2_Perturbed_Surfer_Waveform_Detailed.png`
- `V3_Verdi_original_saturated_window_only.png`, `V3B_Verdi_nWave_2240wide_redacted.png`
- `V4_corrected_SAD_fullprecision_nWave_2240px.png`, `V4_original_completion_region_nWave_768px.png`, `V4_original_controller_progress_nWave_1472px.png`

### C. Live Multi-Mac VPN, XQuartz & MacBook Air Setup Screenshots
- `01-vpn-disconnected.png`, `02-vpn-connected.png`, `03-local-xterm.png`, `08_globalprotect_connecting_redirect.png`, `09_multi_terminal_ssh_broken_pipe_overview.png`, `10_ssh_x_broken_pipe_and_timeout_trace.png`, `11_desktop_commander_remote_bridge_trace.png`, `12_ssh_y_xquartz_ok_and_idle_timeout.png`, `13_xquartz_xterm_ssh_x_broken_pipe.png`
- `actual_macbook_air_3_windows_setup.png`, `actual_macbook_air_dark_terminal.jpg`, `actual_macbook_air_globalprotect_connected.jpg`, `actual_macbook_air_white_xquartz_xterm.png`, `actual_macbook_air_zsh_comment_error.jpg`
- `gp_vpn_connected_and_xquartz_xterm.png`, `gp_vpn_connecting.png`, `ssh_x11_multi_terminal_mahmoodi.png`, `interactive_asic_academy_recruiter_showcase.png`
- `macbook_step01_xquartz_launch.png` through `macbook_step07_stage_gate_and_github.png`

### D. Native Verdi Per-Job Window Captures & Tcl/Process Logs
Over **38 native job directories** under [`practice_from_scratch/state_store/native_jobs/`](practice_from_scratch/state_store/native_jobs/) and [`practice_from_scratch/users/`](practice_from_scratch/users/) preserve:
- `verdi_window_redacted.png` (privacy-redacted X11 `nWave` window captures)
- `verdi_native_process.log` / `native_stdout.log` / `native_stderr.log`
- `capture_manifest.json`, `cleanup_report.json`, `session_manifest.json`, `source_fsdb_manifest.json`, `source_tcl_manifest.json`, `waveform_configuration.rc`
- Live verified jobs including `fig10_v803_live_imac` (`0xe00006`, SHA-256 `0802eb42...`), `a177c6d2df05495d` (`17/17` signals `added_ok=true`, `19` waveform rail bands, `154` trace scanlines, PNG SHA-256 `fdc58c0d...`), and fault-injection jobs `nv01_ssh_timeout_test` through `nv15_layout_separation_test`.

---

## 3. Preserved Verification, Regression & Acceptance Test Logs

### A. Platform & Native Verdi Verification Reports (`v7.0` → `v8.3`)
| Report / Script | Scope | Exact Preserved Result |
| :--- | :--- | :--- |
| [`practice_from_scratch/state_store/acceptance_tests_v7_report.json`](practice_from_scratch/state_store/acceptance_tests_v7_report.json) | `v7.0` 13-test fault-injection & orchestrator suite | **`13 / 13 PASS`** (`all_passed: true`, executed `2026-11-10T09:45:00Z`) |
| [`practice_from_scratch/verification_reports/v7_1_acceptance_results.json`](practice_from_scratch/verification_reports/v7_1_acceptance_results.json) | `v7.1` Native Verdi bridge (`17` fault-injection + `8` live E2E) | **`25 / 25 PASS`** (`all_passed: true`, executed `2026-11-10T20:37:11Z`) |
| [`practice_from_scratch/verification_reports/v8_0_acceptance_results.json`](practice_from_scratch/verification_reports/v8_0_acceptance_results.json) & [`.md`](practice_from_scratch/verification_reports/v8_0_verification_report.md) | `v8.0` JUNIOR DEVELOPER platform security, Seatbelt sandbox, community & auth (`AC01–AC15`) + `v7.1` regression | **`15 / 15 PASS`** (`all_v8_passed: true`) + **`25 / 25 PASS`** (`v7_1_summary`) |
| [`practice_from_scratch/web_console/state_store/v8_1_verification_results.json`](practice_from_scratch/web_console/state_store/v8_1_verification_results.json) | `v8.1` unified platform verification | **`9 / 9 PASS`** (`ok: true`) |
| [`evidence/logs/v8_1_1_25_e2e_report.json`](evidence/logs/v8_1_1_25_e2e_report.json) | Historical `v8.1.1` 25-check E2E snapshot prior to `v8.2` Tcl fix | **`24 / 25 PASS` (`1 FAIL`: `E2E-05`)** — preserved verbatim for auditability; resolved in `v8.2` |
| [`docs/recovery_v8_2/QA_ACCEPTANCE_MATRIX.json`](docs/recovery_v8_2/QA_ACCEPTANCE_MATRIX.json) & [`.md`](docs/recovery_v8_2/QA_ACCEPTANCE_MATRIX.md) | `v8.2` Master Recovery acceptance matrix (`V82-01..07`) & live `17/17` signal verification | **`7 / 7 PASS`**, verdict **`LIVE_WAVEFORM_VERIFICATION_PASS`** (`2026-11-12T20:08:02Z`) |
| [`docs/lifecycle_v8_3/FIGURE_SWITCHING_REGRESSION_MATRIX.json`](docs/lifecycle_v8_3/FIGURE_SWITCHING_REGRESSION_MATRIX.json) & [`100_TRANSITION_STABILITY_REPORT.md`](docs/lifecycle_v8_3/100_TRANSITION_STABILITY_REPORT.md) | `v8.3` Native Verdi lifecycle: `NV01–NV18`, `A01–G05` regression matrix, and 100-transition stress loop across `fig7..fig11` & `layout` | **`18 / 18` NV PASS**, **`51 / 51` Regression PASS**, **`100 / 100` Stability Loop PASS** (`0` failed transitions, `0` modal blocks, `0` orphaned resources, `avg 3,016.11 ms`) |

### B. Synopsys VCS / PrimeTime / ICV / 100-Page Manual Logs
- [`evidence/logs/`](evidence/logs/) (`12` logs & reports): `V5_16bit_regression_results.log` (`V5_TOP_REGRESSION_PASS 3/3`), `V5_native_synopsys_vcs_results.log`, `motion_synthesis_stat.log`, `motion_vcs_precision_12check_terminal_excerpt.log`, `motion_vcs_sad_scoreboard_three_seed_run_20261104.log`, `motion_verification_520mhz.log`, `vcs_top_tb_520mhz.log`, `vcs_top_tb_direct_520mhz.log`, `vcs_v6_clean_suite.log` (`SUMMARY 7 / 7`), `staging_8789_stdout.log`, `staging_8789_stderr.log`, `v8_1_1_25_e2e_report.json`.
- [`evidence/v9_signoff/`](evidence/v9_signoff/): `icv/top.LAYOUT_ERRORS` (`CLEAN`), `pt_signoff/{FAST,TYPICAL,SLOW}_*.rpt`, `reports/v9_eco_clean_*.rpt`, `gds_export_audit.log`.
- [`verification/v6_clean/qa_runs/`](verification/v6_clean/qa_runs/): 7 individual VCS `.run.log` files + `summary.json` + `stage_gate.json`.
- [`practice_from_scratch/logs/`](practice_from_scratch/logs/) (`101` `.log` files) & [`practice_from_scratch/screenshots/`](practice_from_scratch/screenshots/) (`102` `.png` files): complete Page 1–100 terminal execution transcripts and rendered PNGs, plus mirrored snapshot in [`practice_from_scratch/runs/archived_snapshot_20261112T191104Z/`](practice_from_scratch/runs/archived_snapshot_20261112T191104Z/).
