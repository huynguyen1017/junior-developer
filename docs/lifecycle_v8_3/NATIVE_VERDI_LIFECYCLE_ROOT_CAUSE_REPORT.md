# Native Verdi Lifecycle Root Cause Report (v8.3)

## 1. Confirmed Incident & Live Forensic Evidence

During live read-only inspection of XQuartz (`DISPLAY=/var/run/com.apple.launchd.SQD4ShgIqM/org.xquartz:0`) and `mahmoodi.rcc.at.sfsu.edu`:

- **Local macOS SSH Process**: `PID 13276` (`job_id=a177c6d2df05495d`, `fig_id=fig10`) running `ssh -Y ... 926784856@mahmoodi.rcc.at.sfsu.edu tcsh -fc 'source /packages/synopsys/setup/synopsys_setup.tcl; cd /home/926784856/ENGR852_Project/22_v9_clean_verdi_waveforms/work_93; exec verdi -dbdir ../simv_reg.daidir -ssf motion_v5_16bit_top_regression.fsdb -play /tmp/engr852_verdi_wrapper_a177c6d2df05495d.tcl'`.
- **Remote Verdi Process**: `PID 3832600` (parent `sshd PID 3832592`, UID `825408680`).
- **Main Verdi X11 Window**: `0xe00006` (`<Verdi-Apex:nTraceMain:1> ... motion_v5_16bit_top_regression.fsdb`, `1900x1040+0+22`, `WM_CLASS=("Novas", "novas")`, `_NET_WM_PID=3832600`).
- **Centered Modal Dialog X11 Window**: `0xe0063a` (`"Question"`, `324x125+778+415`, `WM_CLASS=("Novas", "novas")`, `_NET_WM_STATE=_NET_WM_STATE_MODAL`, `WM_TRANSIENT_FOR=0xe00006`, `_NET_WM_PID=3832600`), displaying `"Remember to save signals to a signal file. Do you want to continue? [Yes] [Cancel]"`.

## 2. Why Multiple `nWave` Tabs Existed in One Verdi Process

1. In `work_93/`, `novas.conf` and `novas.rc` reference `verdiLog/novas_autosave.ses`, which restores two saved waveform views (`*<nWave:2>` and `*<nWave:3>`).
2. `build_defect_d_safe_tcl_wrapper()` in `engr852_native_verdi_bridge.py` executed `set target_w [wvCreateWindow]`, opening `<nWave:4>` inside the **same** Verdi process (`PID 3832600`) rather than spawning a second Verdi process.

## 3. Exact Root Cause of the Modal Dialog & Automation Blockage

1. `work_93/novas.rc` has `resaveSignals = TRUE` and `confirmExit = TRUE`.
2. `build_defect_d_safe_tcl_wrapper()` added 17 signals with `wvAddSignal -win $target_w {...}` but **never called** `wvSaveSignal -win $target_w {<file.rc>}`, leaving the `nWave` tab dirty (`*`).
3. When `<nWave:4>` was closed, Synopsys Verdi `W-2024.09-1` saw `signalModified == true && resaveSignals == TRUE` and raised `0xe0063a "Question"`.
4. `verdi_windows_detailed()` in `engr852_native_verdi_bridge.py` filtered `xwininfo -root -tree` strictly for `"Verdi-Apex"` or `"Verdi-Elite"`, completely ignoring `"Question"` (`0xe0063a`).
5. Button C (`Retry / Reconnect`) in `index.html` line 1763 called `triggerXquartzExternalWindowPlot(true)` (force new launch) instead of `retryNativeVerdiConnection(false)`.
6. Figure switching in `index.html` did not coordinate with a backend lifecycle manager or monotonic `selection_generation_id`.
