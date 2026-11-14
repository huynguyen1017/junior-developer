# JUNIOR DEVELOPER v8.2 — Native Verdi End-to-End Report (`P0 NATIVE VERDI REPAIR DIRECTIVE`)

## 1. Forensic Analysis of the `<nWave:4>` 3-Signal Failure & `TclPlay` Quirks

Inspection of `/Users/huynguyen/.local/share/engr852-native-gui/fig10_chatrecovery_20261111/verdi_native_process.log` and live Synopsys Verdi `W-2024.09-1` `-play` logs on `mahmoodi` revealed the exact root causes of the `<nWave:4>` 3-signal truncation:

1. **Unbraced `[12:0]` in double-quoted `puts` (`TclPlay: invalid command name "12:0", error line=41`)**:
   - Signals 1 (`clock`) and 2 (`start`) had scalar paths without brackets, so `puts "ENGR852_SIGNAL_ADDED ..."` succeeded.
   - Signal 3 (`count[12:0]`) was added by `wvAddSignal`, and then the immediately following `puts "ENGR852_SIGNAL_ADDED ... sig=/motion_v5_16bit_top_regression_tb/dut/ctl_u/count[12:0] rc=0"` caused Tcl to evaluate `[12:0]` as a command substitution inside double quotes, aborting the Tcl script before signals 4–17 (`S1S2mux[15:0]` .. `completed`) or `ENGR852_NWAVE_VERIFIED` could run.
2. **Remote `tcsh` `!` History Expansion (`![info: Event not found.`)**:
   - Uploading Tcl scripts containing `if {![info exists _Verdi_1]}` via remote `tcsh` inline command arguments triggered `tcsh` history expansion (`![info`) before the file was written.
3. **Synopsys Verdi `TclPlay` Engine Requirements**:
   - Synopsys Verdi `W-2024.09-1`'s `-play` engine (`TclPlay`) overrides Tcl `puts` with a 1-argument GUI console logger (`puts string`; 2-argument `puts $fileId string` throws `wrong # args: should be "puts string"`) and requires `wvOpenFile`, `wvAddSignal`, `wvZoom`, and `wvScrollUp` to execute as flat top-level commands rather than nested inside `foreach` or `catch`.

## 2. Verified Repair in `engr852_native_verdi_bridge.py`

1. **Flat Top-Level Braced Tcl Wrapper (`build_defect_d_safe_tcl_wrapper`)**:
   - Uses `if {[info exists _Verdi_1] == 0}` (zero `!` characters) and uploads the wrapper via `stdin` (`cat > /tmp/engr852_verdi_wrapper_${job}.tcl`) so remote `tcsh` never parses the Tcl body.
   - Emits flat top-level `wvOpenFile -win $target_w {{{fsdb_name}}}`, `wvAddSignal -win $target_w {{{sp}}}` (for all 17 signals), `wvZoom -win $target_w {zoom_start} {zoom_end}`, and `wvScrollUp -win $target_w 15` with Tcl brace-quoted paths (`{{{sp}}}`) and 1-argument `puts` statements.
   - Tested directly in `tclsh` (`V82-01`) and live in Synopsys Verdi `W-2024.09-1` (`V82-07`): all 17 `fig10` signals execute with exit code `0`.
2. **Fail-Closed Per-Signal Verification (`build_signal_verification_records` & `capture_and_verify`)**:
   - `added_ok` is `True` if and only if `ENGR852_SIGNAL_ADDED` is logged for that signal's resolved FSDB path and `ENGR852_NWAVE_VERIFIED` succeeded (`V82-02`).
   - During live capture (`capture_and_verify`), when XQuartz pixel rail verification passes (`rail_ok=True`), the bridge also inspects remote `verdiLog/verdi.cmd` on `mahmoodi` to confirm all 17 `wvAddSignal` commands executed in Verdi before recording `ENGR852_SIGNAL_ADDED` and `ENGR852_NWAVE_VERIFIED`.
3. **Strict Window Reuse Gate (`launch` & `_find_verified_process_log_for_window`)**:
   - `launch(attach_existing=True)` checks whether the existing X11 window has a verified `verdi_native_process.log` containing `ENGR852_NWAVE_VERIFIED` and all required signals before attaching.

## 3. Live End-to-End Synopsys Verdi Verification (`job_id = a177c6d2df05495d`)

- **Job ID**: `a177c6d2df05495d` (and prior live verification run `9c53742601244f76`)
- **X11 Window ID**: `0xe00006` (`<Verdi-Apex:nTraceMain:1> motion_v5_16bit_top_regression_tb ... - .../motion_v5_16bit_top_regression.fsdb`, `1900×1040`)
- **Status / State**: `WAVEFORM_SIGNALS_VERIFIED` / `connection_state: WAVEFORM_VERIFIED` / `controller_state: COMPLETE`
- **Evidence Class**: `REAL_APPLICATION_CAPTURE`
- **Redacted Artifact**: `/Users/huynguyen/.local/share/engr852-native-gui/a177c6d2df05495d/verdi_window_redacted.png`
- **Redacted Artifact SHA-256**: `fdc58c0d1e0eaed42ed25720e4ef11e9c011248ad9fbe4cc01eae972b47e8f22`
- **Pixel Metrics**: `19` populated waveform rail bands (`nwave_detected_rail_bands: 19`), `154` active green trace scanlines (`nwave_green_scanlines: 154`), `791` label rows, `455` yellow timeline axis samples
- **Verified Signals (`17/17` `added_ok: true`, `verified_nwave_handle: "_nWave4"`)**:
  1. `clock` (`/motion_v5_16bit_top_regression_tb/clock`, 1-bit BIN)
  2. `start` (`/motion_v5_16bit_top_regression_tb/start`, 1-bit BIN)
  3. `count[12:0]` (`/motion_v5_16bit_top_regression_tb/dut/ctl_u/count[12:0]`, 13-bit HEX: `fe`, `ff`, `100` .. `10f` .. `113`)
  4. `S1S2mux[15:0]` (`/motion_v5_16bit_top_regression_tb/dut/S1S2mux[15:0]`, 16-bit HEX)
  5. `newDist[15:0]` (`/motion_v5_16bit_top_regression_tb/dut/newDist[15:0]`, 16-bit HEX)
  6. `CompStart` (`/motion_v5_16bit_top_regression_tb/dut/CompStart`, 1-bit BIN)
  7. `PEready[15:0]` (`/motion_v5_16bit_top_regression_tb/dut/PEready[15:0]`, 16-bit HEX)
  8. `VectorX[3:0]` (`/motion_v5_16bit_top_regression_tb/dut/VectorX[3:0]`, 4-bit HEX)
  9. `VectorY[3:0]` (`/motion_v5_16bit_top_regression_tb/dut/VectorY[3:0]`, 4-bit HEX)
  10. `AddressR[7:0]` (`/motion_v5_16bit_top_regression_tb/AddressR[7:0]`, 8-bit HEX)
  11. `AddressS1[9:0]` (`/motion_v5_16bit_top_regression_tb/AddressS1[9:0]`, 10-bit HEX)
  12. `AddressS2[9:0]` (`/motion_v5_16bit_top_regression_tb/AddressS2[9:0]`, 10-bit HEX)
  13. `newBest` (`/motion_v5_16bit_top_regression_tb/dut/comp_u/newBest`, 1-bit BIN)
  14. `BestDist[15:0]` (`/motion_v5_16bit_top_regression_tb/BestDist[15:0]`, 16-bit HEX: `ffff -> 0100 -> 0000`)
  15. `motionX[3:0]` (`/motion_v5_16bit_top_regression_tb/motionX[3:0]`, 4-bit HEX: `0 -> 8 (-8) -> 7 (+7)`)
  16. `motionY[3:0]` (`/motion_v5_16bit_top_regression_tb/motionY[3:0]`, 4-bit HEX: `0 -> 8 (-8)`)
  17. `completed` (`/motion_v5_16bit_top_regression_tb/completed`, 1-bit BIN)
