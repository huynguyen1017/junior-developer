# JUNIOR DEVELOPER v8.2 — Cross-Device & Mobile QA Report

## 1. Multi-Device Companion Routing (`Device A: MacBook Air` vs `Device B: iMac`)

- **Device B (`imac` — Primary Authorized Companion Host)**:
  - Evaluated via live local kernel (`ifconfig utun*`, `route -n get`), XQuartz (`xset q`), and SSH (`ssh -F ~/.ssh/config -o BatchMode=yes`) probes.
- **Device A (`macbook_air` — Secondary Client Workstation)**:
  - Evaluated strictly via signed companion heartbeats (`POST /api/v8/devices/heartbeat`) with a 60-second TTL (`E2E-13`).
  - When no heartbeat is active within 60 seconds, Device A reports `heartbeat_status: "UNREGISTERED"` / `"OFFLINE_OR_EXPIRED"` and `can_execute_live_verdi: false`.

## 2. Responsive & Mobile Viewport Verification

| Viewport Class | Resolution | Verified Layout Behavior |
|---|---|---|
| **Desktop Studio** | `1440 × 900` | Dual-column Native Verdi Diagnostic & Signal Table layout with full-width Application Capture Viewer and 1-click **Refresh Diagnostics (Safe)** / **Reconnect & Verify SSH/Verdi** buttons. |
| **Tablet / iPad** | `768 × 1024` | Stacked single-column cards (`grid-template-columns: 1fr`), horizontal scroll wrapper around 10-step diagnostic table and 17-signal verification table. |
| **Mobile Phone** | `390 × 844` | Wrapping action bars (`flex-wrap: wrap`), touch-friendly buttons (`min-height: 44px`), scrollable preformatted JSON telemetry block (`overflow-x: auto`), zero horizontal page overflow. |
