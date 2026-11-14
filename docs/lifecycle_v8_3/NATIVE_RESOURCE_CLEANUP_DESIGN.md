# Native Resource Cleanup Design (`NativeResourceCleanupManager`)

## 1. Orderly 10-Step Release Sequence

Implemented in `execute_10_step_orderly_cleanup()` (`practice_from_scratch/scripts/engr852_verdi_lifecycle_manager.py`):
1. **Stop new actions for old selection**: Increment monotonic `selection_generation_id`.
2. **Preserve verified evidence**: Persist all 8 job files and redacted PNGs.
3. **Release viewer subscription**: Detach browser stream without touching XQuartz.
4. **Stop job capture worker**: Stop only job-owned workers (none active in on-demand XWD mode).
5. **Release unused GUI views**: Detect job-owned transient modals and dismiss safely via `WM_DELETE_WINDOW`.
6. **Handle signal-file preservation**: Confirm `waveform_configuration.rc` is saved.
7. **Check remaining session users**: Preserve shared FSDB-family sessions, `USER_MANAGED` sessions, and `layout` transitions.
8. **Terminate exclusively owned process**: Only when `terminate_process=True` and `_verify_pid_is_job_owned_ssh(ssh_pid, job_id)` confirms `ssh` + `verdi` + `job_id`.
9. **Reconcile OS/X11 state**: Update `cleanup_state` (`REUSED_BY_COMPATIBLE_FIGURE`, `PRESERVED_FOR_USER`, or `CLEANUP_COMPLETE`).
10. **Emit cleanup report**: Write `cleanup_report.json`.

## 2. Forbidden Cleanup Methods

Broad kills (`pkill -9 verdi`, `killall verdi`, `pkill -f nWave`, global SSH kills, XQuartz restarts, GlobalProtect disconnects) are strictly prohibited and absent from all code paths.
