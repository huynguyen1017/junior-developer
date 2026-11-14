# Verdi Lifecycle State Machine (v8.3)

## 1. 20 Supported Lifecycle States

`NOT_STARTED`, `DISCOVERING`, `REUSING_EXISTING_SESSION`, `LAUNCHING`, `LOADING_FSDB`, `LOADING_SIGNAL_LAYOUT`, `PLOTTING_SIGNALS`, `VERIFYING_WAVEFORMS`, `READY`, `SWITCH_REQUESTED`, `SAVING_SIGNAL_LAYOUT`, `RELEASING_OLD_VIEW`, `ATTACHING_NEW_VIEW`, `MODAL_BLOCKED`, `RECOVERING`, `SUSPENDED`, `CLEANUP_PENDING`, `CLEANUP_COMPLETE`, `FAILED`, `USER_ACTION_REQUIRED`.

## 2. 5 Evidence Distinction Badges

`LIVE_APPLICATION_VERIFIED`, `LIVE_WAVEFORMS_VERIFIED`, `HISTORICAL_CAPTURE_AVAILABLE`, `SIGNALS_CONFIGURED_ONLY`, `NATIVE_SESSION_BLOCKED`.

## 3. Race-Condition & Modal Guards

- Monotonic `selection_generation_id` prevents stale backend responses or captures from overwriting newer figure selections.
- `MODAL_BLOCKED` halts conflicting launches until `NativeModalRecoveryAgent` or an authorized user resolves the dialog.
- `_LIFECYCLE_LOCK` serializes state transitions.
