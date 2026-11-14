# Signal Layout Preservation Policy (v8.3)

## 1. Signal Configuration Classification

- **`USER_MANAGED`**: Manually created or modified by a user. Never discarded automatically.
- **`AUTOMATION_TEMPORARY`**: Generated for an automated figure run. Preserved in `native_jobs/{job_id}/waveform_configuration.rc` and may be released per policy.
- **`VERIFIED_EVIDENCE`**: Associated with a captured, validated engineering result (`WAVEFORM_SIGNALS_VERIFIED`). Evidence, SHA-256 hashes, and `.rc` layout are always persisted before release.
- **`UNKNOWN_OWNER`**: Cannot be attributed to a known job. Never automatically closed or discarded.

## 2. Per-Job Artifact Directory (`native_jobs/{job_id}/`)

Every job maintains 8 synchronized files in `practice_from_scratch/state_store/native_jobs/{job_id}/` (and `~/.local/share/engr852-native-gui/{job_id}/`):
1. `session_manifest.json`
2. `waveform_configuration.rc` (Synopsys `Magic 271485` / `Revision Verdi_W-2024.09-1` format)
3. `source_fsdb_manifest.json`
4. `source_tcl_manifest.json`
5. `capture_manifest.json`
6. `native_stdout.log`
7. `native_stderr.log`
8. `cleanup_report.json`
