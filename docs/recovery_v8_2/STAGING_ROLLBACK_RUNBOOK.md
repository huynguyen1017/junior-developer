# JUNIOR DEVELOPER v8.2 — Staging Rollback Runbook

## 1. Instant Non-Destructive Rollback Procedure

All pre-v8.2 staging files were snapshotted prior to modification at:
`/Users/huynguyen/Developer/ENGR852_Stability_Recovery_20261111/backups/pre_v8_2_snapshot/`

To restore the exact pre-v8.2 staging state on port `8789` without touching Production port `8788` (PID `46103`):

```bash
cp -p /Users/huynguyen/Developer/ENGR852_Stability_Recovery_20261111/backups/pre_v8_2_snapshot/engr852_native_verdi_bridge.py \
  /Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged/practice_from_scratch/scripts/engr852_native_verdi_bridge.py

cp -p /Users/huynguyen/Developer/ENGR852_Stability_Recovery_20261111/backups/pre_v8_2_snapshot/v7_platform_core.py \
  /Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged/practice_from_scratch/web_console/v7_platform_core.py

cp -p /Users/huynguyen/Developer/ENGR852_Stability_Recovery_20261111/backups/pre_v8_2_snapshot/server.py \
  /Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged/practice_from_scratch/web_console/server.py

bash /Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged/practice_from_scratch/scripts/manage_staging_8789.sh restart
bash /Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged/practice_from_scratch/scripts/manage_staging_8789.sh status
```
