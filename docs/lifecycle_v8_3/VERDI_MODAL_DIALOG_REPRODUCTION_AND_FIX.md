# Verdi Modal Dialog Reproduction and Fix (`0xe0063a "Question"`)

## 1. Reproduction Trigger

- **Command**: Opening an `nWave` view, modifying signals via `wvAddSignal`, and closing that `nWave` tab without calling `wvSaveSignal -win $target_w {<file.rc>}` while `resaveSignals = TRUE` is active in `work_93/novas.rc`.
- **Observed Window**: `0xe0063a "Question"`, `WM_TRANSIENT_FOR=0xe00006`, `_NET_WM_STATE_MODAL`, `_NET_WM_PID=3832600`.
- **Meaning in Verdi `W-2024.09-1`**:
  - Clicking **Yes** closes the unsaved `nWave` tab without saving `.rc`.
  - Clicking **Cancel** aborts closing the tab.
  - Sending ICCCM `WM_DELETE_WINDOW` to `0xe0063a` closes only the dialog window while leaving `0xe00006` alive.

## 2. Two-Part Permanent Fix Implemented

1. **Root-Cause Prevention in Tcl Wrapper (`engr852_native_verdi_bridge.py`)**:
   - `build_defect_d_safe_tcl_wrapper()` now executes:
     `wvSaveSignal -win $target_w $engr852_rc_file`
     verified against Synopsys Verdi `W-2024.09-1` `verdi_tcl.db`.
   - This clears the dirty `*` flag on the automation-owned `nWave` tab so closing/switching never triggers `"Remember to save signals to a signal file. Do you want to continue?"`.
2. **`NativeModalDialogDetector` & `NativeModalRecoveryAgent` (`engr852_verdi_lifecycle_manager.py`)**:
   - `detect_verdi_modal_dialogs()` inspects `xwininfo -root -tree`, `xwininfo -id <wid>` (`Map State: IsViewable`), and `xprop -id <wid>` (`_NET_WM_PID`, `WM_TRANSIENT_FOR`, `_NET_WM_STATE_MODAL`).
   - Positively matches `0xe0063a` to owning job `native_fig10_1794514078_573ac4` (`VERIFIED_EVIDENCE`).
   - Saves `waveform_configuration.rc` and all 8 lifecycle files first, then sends ICCCM `WM_DELETE_WINDOW` via `/opt/X11/lib/libX11.6.dylib` (`ctypes`) to `0xe0063a` **only** — keeping `0xe00006` intact.
   - Unknown or `USER_MANAGED` dialogs escalate to `MODAL_BLOCKED` (`NATIVE_GUI_CONFIRMATION_REQUIRED`) without auto-dismissing.
