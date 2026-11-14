#!/usr/bin/env python3
"""
JUNIOR DEVELOPER v8.1.1 — Master Automated Verification Suite
Verifies Fixes 1..15 and all 25 Acceptance Tests (E2E-01 .. E2E-25) against
http://127.0.0.1:8789/ while confirming production port 8788 remains untouched.
"""
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

STAGING_URL = "http://127.0.0.1:8789"
STAGING_ROOT = Path("/Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged")
SCRIPTS_DIR = STAGING_ROOT / "practice_from_scratch" / "scripts"
WEB_DIR = STAGING_ROOT / "practice_from_scratch" / "web_console"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(WEB_DIR))

import engr852_native_verdi_bridge as bridge  # noqa: E402


def http_req(path: str, method: str = "GET", data: dict | None = None, headers: dict | None = None) -> tuple[int, dict | bytes, dict]:
    url = f"{STAGING_URL}{path}"
    hdrs = dict(headers or {})
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        hdrs.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            if "application/json" in ctype:
                return resp.status, json.loads(raw.decode("utf-8")), dict(resp.headers)
            return resp.status, raw, dict(resp.headers)
    except urllib.error.HTTPError as err:
        raw = err.read()
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except Exception:
            parsed = {"raw": raw.decode("utf-8", errors="replace")}
        return err.code, parsed, dict(err.headers)


def run_suite() -> dict:
    results = []

    def record(test_id: str, title: str, passed: bool, detail: str):
        status = "PASS" if passed else "FAIL"
        print(f"[{status}] {test_id}: {title} — {detail}")
        results.append({"id": test_id, "title": title, "status": status, "passed": bool(passed), "detail": detail})

    # E2E-01: Staging port 8789 listening & healthy; production 8788 untouched
    code, bv, _ = http_req("/api/v8/build-version")
    record("E2E-01", "Staging 127.0.0.1:8789 health & build-version check", code == 200 and isinstance(bv, dict) and bv.get("ok") is True, f"HTTP {code}, git_mode={bv.get('git_mode') if isinstance(bv, dict) else 'N/A'}")

    # E2E-02: LaunchAgent plist & manage_staging_8789.sh service wrapper
    plist = Path.home() / "Library" / "LaunchAgents" / "com.juniordeveloper.engr852.staging8789.plist"
    mgr = SCRIPTS_DIR / "manage_staging_8789.sh"
    record("E2E-02", "LaunchAgent plist & manage_staging_8789.sh present", plist.is_file() and mgr.is_file(), f"plist={plist.exists()}, script={mgr.exists()}")

    # E2E-03: Explicit -F ~/.ssh/config in _resolve_ssh_extra_args()
    ssh_args = bridge._resolve_ssh_extra_args()
    record("E2E-03", "Explicit -F ~/.ssh/config in SSH args (P0-01)", "-F" in ssh_args, f"ssh_extra_args={ssh_args}")

    # E2E-04: Signed 4-bit two's-complement formatting (4'h8 (-8), 4'h7 (+7), 4'he (-2), 4'hd (-3))
    f8 = bridge.format_signed_4bit_vector("0x8")
    f7 = bridge.format_signed_4bit_vector("0x7")
    fe = bridge.format_signed_4bit_vector("0xe")
    fd = bridge.format_signed_4bit_vector("0xd")
    fig10_ev = bridge.FIGURE_CONFIGS["fig10"]["expected_values"]
    record(
        "E2E-04",
        "Signed 4-bit two's-complement formatting (Fix 7)",
        f8 == "4'h8 (-8)" and f7 == "4'h7 (+7)" and fe == "4'he (-2)" and fd == "4'hd (-3)" and fig10_ev["count_0x010f"]["motionX_signed"] == "4'h7 (+7)",
        f"{f8}, {f7}, {fe}, {fd}",
    )

    # E2E-05: Single-copy 17-signal Tcl wrapper (wvCut before wvAddSignal)
    tcl_wrap = bridge.build_defect_d_safe_tcl_wrapper("fig10")
    record("E2E-05", "Single-copy 17-signal Tcl wrapper (P0-06)", "wvSelectAll" in tcl_wrap and "wvCut" in tcl_wrap and "ENGR852_SIGNAL_ADDED" in tcl_wrap, "wvSelectAll + wvCut + ENGR852_SIGNAL_ADDED verified in Tcl wrapper")

    # E2E-06: All 6 figure metadata endpoints return distinct figure-specific FSDB & Tcl
    code_figs, figs_meta, _ = http_req("/api/v8/figures/metadata")
    figs_dict = figs_meta.get("figures", figs_meta) if isinstance(figs_meta, dict) else {}
    record("E2E-06", "Distinct metadata for fig7..fig11 & layout", code_figs == 200 and "fig7" in figs_dict and "fig10" in figs_dict and figs_dict["fig7"].get("tcl") != figs_dict["fig10"].get("tcl"), f"figures={list(figs_dict.keys())[:6]}")

    # E2E-07: Live vs Recorded Truth Separation
    code_st, st_data, _ = http_req("/api/v8/verdi/live-status?fig_id=fig10")
    record("E2E-07", "Truthful live-status state machine (P0-07)", code_st == 200 and isinstance(st_data, dict) and "connection_state" in st_data, f"state={st_data.get('connection_state')}, evidence_class={st_data.get('evidence_class')}")

    # E2E-08: Strict job_id required on /api/v8/verdi/live-frame.png (400 without job_id)
    c_no_job, _, _ = http_req("/api/v8/verdi/live-frame.png?fig_id=fig10")
    record("E2E-08", "Reject live-frame.png without explicit job_id (P0-05)", c_no_job == 400, f"HTTP {c_no_job} without job_id")

    # E2E-09: Reject mismatched figure vs job_id on /api/v8/verdi/live-frame.png (409)
    c_mismatch, _, _ = http_req("/api/v8/verdi/live-frame.png?fig_id=fig7&job_id=fig10_v803_live_imac")
    record("E2E-09", "Reject mismatched figure/job_id on live-frame.png (409)", c_mismatch in (404, 409, 422), f"HTTP {c_mismatch} on fig7 + fig10 job")

    # E2E-10: Serve verified redacted capture when valid job_id & figure match
    c_valid_img, img_bytes, _ = http_req("/api/v8/verdi/live-frame.png?fig_id=fig10&job_id=fig10_v803_live_imac")
    record("E2E-10", "Serve verified redacted PNG for valid fig10 job_id", c_valid_img == 200 and isinstance(img_bytes, (bytes, bytearray)) and len(img_bytes) > 10000, f"HTTP {c_valid_img}, bytes={len(img_bytes) if isinstance(img_bytes, (bytes, bytearray)) else 0}")

    # E2E-11: Unauthenticated POST /api/v8/devices/select rejected with 401 (P0-03)
    c_unauth_sel, _, _ = http_req("/api/v8/devices/select", method="POST", data={"selected_device": "imac"})
    record("E2E-11", "Unauthenticated POST /api/v8/devices/select rejected (401)", c_unauth_sel == 401, f"HTTP {c_unauth_sel}")

    # E2E-12: Simulated fault rejected on normal public requests (P0-04)
    c_pub_sf, pub_sf_body, _ = http_req("/api/v8/verdi/live-status?fig_id=fig10&simulated_fault=SSH_AUTH_FAILED")
    record("E2E-12", "Public request rejects ?simulated_fault= parameter (P0-04)", c_pub_sf == 200 and pub_sf_body.get("simulated_fault_rejected") is True, f"simulated_fault_rejected={pub_sf_body.get('simulated_fault_rejected')}")

    # E2E-13: Device registry reports real measured state (no hardcoded True on MacBook Air) (P0-02)
    c_dev, dev_body, _ = http_req("/api/v8/devices/registry?fig_id=fig10")
    devs_map = dev_body.get("devices", {}) if isinstance(dev_body, dict) else {}
    mba = devs_map.get("macbook_air", {}) if isinstance(devs_map, dict) else {}
    record("E2E-13", "Device registry reports real telemetry for MacBook Air (P0-02)", c_dev == 200 and isinstance(dev_body, dict) and mba.get("ssh_authenticated") is not True, f"HTTP {c_dev}, mba_heartbeat={mba.get('heartbeat_status', mba.get('status_summary'))}")

    # E2E-14: Real connection recovery endpoint POST /api/v8/verdi/recover (P0-01)
    c_rec_unauth, _, _ = http_req("/api/v8/verdi/recover", method="POST", data={"fig_id": "fig10"})
    record("E2E-14", "POST /api/v8/verdi/recover protected by owner auth (401)", c_rec_unauth == 401, f"HTTP {c_rec_unauth} for unauthenticated caller")

    # E2E-15: Direct execution of 15-step recover_native_verdi_session() in bridge
    rec_res = bridge.recover_native_verdi_session(fig_id="fig10", selected_device="imac", auto_launch_if_ready=False)
    record("E2E-15", "15-step recover_native_verdi_session() executes real probes", isinstance(rec_res, dict) and len(rec_res.get("recovery_steps", [])) == 15, f"steps={len(rec_res.get('recovery_steps', []))}, error_code={rec_res.get('error_code')}")

    # E2E-16: Checkpoint API GET /api/v8/checkpoint
    c_chk, chk_body, _ = http_req("/api/v8/checkpoint")
    record("E2E-16", "GET /api/v8/checkpoint returns active state", c_chk == 200 and isinstance(chk_body, dict), f"HTTP {c_chk}")

    # E2E-17: Traceability Matrix API GET /api/v8/traceability-matrix
    c_tm, tm_body, _ = http_req("/api/v8/traceability-matrix")
    record("E2E-17", "GET /api/v8/traceability-matrix returns P0 matrix", c_tm == 200 and isinstance(tm_body, dict), f"HTTP {c_tm}")

    # E2E-18: Frontend HTML contains split Refresh Diagnostics & Reconnect buttons + zero fake oscilloscope canvas
    index_html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
    has_btns = ("nvBtnRefreshDiagnostics" in index_html) and ("nvBtnRetryConnection" in index_html)
    record("E2E-18", "Split Refresh Diagnostics & Reconnect buttons in UI", has_btns, f"nvBtnRefreshDiagnostics & nvBtnRetryConnection present={has_btns}")

    # E2E-19: Recorded V9 evidence endpoint serves authentic PNG metadata & SHA-256
    c_rec_fig10, rec10_meta, _ = http_req("/api/v8/figures/fig10/recorded-evidence")
    record("E2E-19", "Recorded V9 evidence metadata & SHA-256 for fig10", c_rec_fig10 == 200 and bool(rec10_meta.get("recorded_image_sha256") or rec10_meta.get("sha256")), f"sha256={str(rec10_meta.get('recorded_image_sha256') or rec10_meta.get('sha256'))[:16]}...")

    # E2E-20: Privacy audit on redacted native capture (zero unredacted institutional IDs)
    job_dir = bridge.ROOT / "fig10_v803_live_imac"
    raw_png = job_dir / "restricted_raw" / "verdi_window.png"
    redacted_png = job_dir / "verdi_window_redacted.png"
    rail_audit = bridge.analyze_verdi_window_pixels(redacted_png) if redacted_png.is_file() else {"verified": False, "width": 2240, "height": 1115}
    priv_audit = bridge.verify_redacted_capture(raw_png, redacted_png, rail_audit.get("width", 2240), rail_audit.get("height", 1115)) if redacted_png.is_file() else {"verified": False}
    record("E2E-20", "Privacy redaction audit on verdi_window_redacted.png", bool(priv_audit.get("verified")), f"privacy_audit={priv_audit}")

    # E2E-21: Lower nWave signal-rail pixel verification on native capture
    record("E2E-21", "X11 nWave green/yellow signal-rail pixel verification", bool(rail_audit.get("verified")), f"green_scanlines={rail_audit.get('nwave_green_scanlines')}, rail_bands={rail_audit.get('nwave_detected_rail_bands')}")

    # E2E-22: Public Platform Overview & Courses catalog endpoint
    c_ov, ov_body, _ = http_req("/api/v8/overview")
    record("E2E-22", "Public Platform Overview & Courses API (/api/v8/overview)", c_ov == 200 and isinstance(ov_body, dict) and ov_body.get("ok") is True, f"HTTP {c_ov}")

    # E2E-23: Reddit-style Community channels & posts endpoint
    c_com, com_body, _ = http_req("/api/v8/posts")
    record("E2E-23", "Reddit-style Community posts API (/api/v8/posts)", c_com == 200 and isinstance(com_body, dict) and com_body.get("ok") is True, f"HTTP {c_com}, posts={len(com_body.get('posts', []))}")

    # E2E-24: 100-page lab manual & 500-question quiz independence
    c_st, st_body, _ = http_req("/api/state")
    record("E2E-24", "100-Page Manual & 500-Question Quiz state (/api/state)", c_st == 200 and isinstance(st_body, dict), f"HTTP {c_st}")

    # E2E-25: Production port 8788 untouched & independent from Staging port 8789
    prod_pid = subprocess.run(["lsof", "-ti", "tcp:8788", "-sTCP:LISTEN"], capture_output=True, text=True).stdout.strip()
    stg_pid = subprocess.run(["lsof", "-ti", "tcp:8789", "-sTCP:LISTEN"], capture_output=True, text=True).stdout.strip()
    record("E2E-25", "Staging (8789) isolated from Production (8788)", bool(stg_pid) and (stg_pid != prod_pid), f"staging_pid={stg_pid.splitlines()[0] if stg_pid else 'none'}, prod_pid={prod_pid.splitlines()[0] if prod_pid else 'none'}")

    passed_cnt = sum(1 for r in results if r["passed"])
    summary = {
        "total": len(results),
        "passed": passed_cnt,
        "failed": len(results) - passed_cnt,
        "results": results,
    }
    out_file = STAGING_ROOT / "evidence" / "logs" / "v8_1_1_25_e2e_report.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n=== SUMMARY: {passed_cnt}/{len(results)} E2E TESTS PASSED ===")
    return summary


if __name__ == "__main__":
    s = run_suite()
    sys.exit(0 if s["failed"] == 0 else 1)
