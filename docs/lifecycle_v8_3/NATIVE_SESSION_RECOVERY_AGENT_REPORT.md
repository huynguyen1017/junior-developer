# Native Session Recovery Agent Report (v8.3)

Six specialized self-healing lifecycle agents implemented in `run_6_self_healing_lifecycle_agents()` (`practice_from_scratch/scripts/engr852_verdi_lifecycle_manager.py`) and integrated into `/api/v8/agents/status` and `/api/v8/verdi/lifecycle`:

1. **`NativeSessionHealthAgent`**: Monitors live Verdi X11 windows (`0xe00006`) on XQuartz `:0` and verifies process/job association.
2. **`WaveformLifecycleAgent`**: Tracks figure-specific FSDB families (`fig7`/`fig8`, `fig10`/`fig11`, `fig9`), `.rc` auto-save (`wvSaveSignal`), and session reuse policies.
3. **`NativeModalRecoveryAgent`**: Detects X11 transient modal dialogs (`0xe0063a "Question"`), backs up `.rc` & evidence, and safely dismisses job-owned unsaved-signal dialogs via ICCCM `WM_DELETE_WINDOW` without terminating `0xe00006`.
4. **`OrphanResourceReconciler`**: Reconciles persisted job manifests in `~/.local/share/engr852-native-gui/` and `state_store/native_jobs/` against live XQuartz windows.
5. **`GUIStateConsistencyAgent`**: Enforces monotonic `selection_generation_id` and strict separation between `layout` (IC Compiler II) and Verdi `nWave`.
6. **`IndependentLifecycleQAAgent`**: Validates the 20-state lifecycle machine, 5 evidence badges, and zero-broad-kill compliance.
