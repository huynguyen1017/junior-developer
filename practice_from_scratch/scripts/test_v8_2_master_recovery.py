#!/usr/bin/env python3
"""
JUNIOR DEVELOPER v8.2 — MASTER RECOVERY & P0 NATIVE VERDI REPAIR VERIFICATION SUITE
Strictly separates:
- UNIT_TEST_PASS
- MOCKED_FAILURE_CLASSIFICATION_PASS
- BACKEND_INTEGRATION_PASS
- LIVE_WAVEFORM_VERIFICATION_BLOCKED_BY_SSH_TCP_TIMEOUT (or LIVE_WAVEFORM_VERIFICATION_PASS if live window & SSH are active)
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

STAGING_ROOT = Path("/Users/huynguyen/Developer/portfolio/motion-estimator-v7-native-verdi-staged")
SCRIPTS_DIR = STAGING_ROOT / "practice_from_scratch" / "scripts"
WEB_DIR = STAGING_ROOT / "practice_from_scratch" / "web_console"
DOCS_DIR = STAGING_ROOT / "docs" / "recovery_v8_2"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(WEB_DIR))

import engr852_native_verdi_bridge as bridge

BASE_URL = "http://127.0.0.1:8789"
PROD_URL = "http://127.0.0.1:8788"


def http_req(path: str, method: str = "GET", data: dict | None = None, headers: dict | None = None) -> tuple[int, dict | bytes]:
    url = f"{BASE_URL}{path}"
    hdrs = {"Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        hdrs["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            ctype = resp.headers.get("Content-Type", "")
            if "application/json" in ctype:
                return resp.status, json.loads(raw.decode("utf-8"))
            return resp.status, raw
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw.decode("utf-8"))
        except Exception:
            return e.code, {"raw": raw.decode("utf-8", errors="replace")}


def main() -> int:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    def record(test_id: str, category: str, title: str, passed: bool, verdict_class: str, detail: str):
        rec = {
            "test_id": test_id,
            "category": category,
            "title": title,
            "passed": bool(passed),
            "verdict_class": verdict_class,
            "detail": detail,
            "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        results.append(rec)
        tag = "PASS" if passed else "FAIL"
        print(f"[{tag}] {test_id} ({verdict_class}): {title} — {detail}")

    # 1. UNIT_TEST_PASS: Defect-D Tcl Wrapper Bracket-Quoting & 17-Signal Tclsh Execution
    cfg_fig10 = bridge.resolve_figure_config("fig10")
    tcl_paths_17 = cfg_fig10.get("tcl_signal_paths", [])
    req_sigs_17 = cfg_fig10.get("required_signals", [])
    tcl_text = bridge.build_defect_d_safe_tcl_wrapper("fig10")
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        (td_p / "fig10_16bit_perfect_match.tcl").write_text(
            "wvCreateWindow\n# simulated legacy script referencing $_Verdi_1 and _nWave2\nputs $_Verdi_1\n",
            encoding="utf-8",
        )
        harness = """
proc wvCreateWindow args { return "_nWave4" }
proc wvSetPosition args { return 0 }
proc wvOpenFile args { return 0 }
proc wvSelectGroup args { return 0 }
proc wvSelectAll args { return 0 }
proc wvCut args { return 0 }
proc wvAddSignal {flag win sig} { return 1 }
proc wvSetRadix args { return 0 }
proc wvZoomAll args { return 0 }
proc wvZoom args { return 0 }
proc wvScrollUp args { return 0 }
proc wvSetCursor args { return 0 }
proc wvGetFileTimeRange args { return "0 22000000" }
proc wvGetWindowTimeUnit args { return "100fs" }
proc verdiDockWidgetMaximize args { return 0 }
""" + tcl_text
        h_file = td_p / "run_harness.tcl"
        h_file.write_text(harness, encoding="utf-8")
        proc = subprocess.run(["tclsh", str(h_file)], cwd=str(td_p), capture_output=True, text=True, timeout=10)
        out = proc.stdout + "\n" + proc.stderr
        recs = bridge.build_signal_verification_records(
            req_sigs_17,
            tcl_paths_17,
            {},
            "0xe00006",
            out,
        )
        all_17_ok = proc.returncode == 0 and "ENGR852_NWAVE_VERIFIED win=_nWave4" in out and len(recs) == 17 and all(r["added_ok"] for r in recs)
        record(
            "V82-01",
            "P0_TCL_BRACKET_FIX",
            "Defect-D Tcl wrapper executes all 17 signals in tclsh without [12:0] command substitution error",
            all_17_ok,
            "UNIT_TEST_PASS" if all_17_ok else "FAIL",
            f"rc={proc.returncode}, verified_signals={sum(1 for r in recs if r['added_ok'])}/17, handle={recs[0]['verified_nwave_handle']}",
        )

    # 2. UNIT_TEST_PASS: Fail-Closed Signal Verification Records on Empty / Partial Logs
    sample_reqs = ["clock", "start", "count[12:0]", "BestDist[15:0]"]
    sample_paths = [
        "/motion_v5_16bit_top_regression_tb/clock",
        "/motion_v5_16bit_top_regression_tb/start",
        "/motion_v5_16bit_top_regression_tb/dut/ctl_u/count[12:0]",
        "/motion_v5_16bit_top_regression_tb/BestDist[15:0]",
    ]
    empty_recs = bridge.build_signal_verification_records(sample_reqs, sample_paths, {}, "0xe00006", "")
    partial_log = (
        "ENGR852_SIGNAL_ADDED win=_nWave4 sig=/motion_v5_16bit_top_regression_tb/clock rc=0\n"
        "ENGR852_SIGNAL_ADDED win=_nWave4 sig=/motion_v5_16bit_top_regression_tb/start rc=0\n"
        "TclPlay: invalid command name \"12:0\", error line=41\n"
    )
    partial_recs = bridge.build_signal_verification_records(sample_reqs, sample_paths, {}, "0xe00006", partial_log)
    fail_closed_ok = (
        all(not r["added_ok"] and r["verified_nwave_handle"] == "UNVERIFIED" for r in empty_recs)
        and partial_recs[0]["added_ok"] is True
        and partial_recs[1]["added_ok"] is True
        and partial_recs[2]["added_ok"] is False
        and partial_recs[3]["added_ok"] is False
    )
    record(
        "V82-02",
        "P0_FAIL_CLOSED_SIGNAL_RECORDS",
        "build_signal_verification_records rejects empty and 3-signal partial TclPlay crash logs",
        fail_closed_ok,
        "UNIT_TEST_PASS" if fail_closed_ok else "FAIL",
        f"empty_added_ok={[r['added_ok'] for r in empty_recs]}, partial_added_ok={[r['added_ok'] for r in partial_recs]}",
    )

    # 3. BACKEND_INTEGRATION_PASS: Production 8788 untouched & Staging 8789 online
    prod_code = subprocess.run(
        ["curl", "-s", "--noproxy", "*", "-o", "/dev/null", "-w", "%{http_code}", f"{PROD_URL}/"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    stg_code, _ = http_req("/")
    ports_ok = prod_code == "200" and stg_code == 200
    record(
        "V82-03",
        "SERVICE_ISOLATION",
        "Production 127.0.0.1:8788 untouched (HTTP 200) and Staging 127.0.0.1:8789 online (HTTP 200)",
        ports_ok,
        "BACKEND_INTEGRATION_PASS" if ports_ok else "FAIL",
        f"prod_8788=HTTP {prod_code}, staging_8789=HTTP {stg_code}",
    )

    # 4. BACKEND_INTEGRATION_PASS: 10-Agent Orchestration Status & NetworkHealthAgent Telemetry
    ag_code, ag_body = http_req("/api/v8/agents/status?fig_id=fig10")
    nh_code, nh_body = http_req("/api/v8/network/health?fig_id=fig10")
    nh_file = STAGING_ROOT / "practice_from_scratch" / "state_store" / "network_health" / "latest.json"
    nh_mode = oct(nh_file.stat().st_mode & 0o777) if nh_file.exists() else "missing"
    ag_ok = (
        ag_code == 200
        and isinstance(ag_body, dict)
        and ag_body.get("agent_count") == 10
        and nh_code == 200
        and isinstance(nh_body, dict)
        and nh_body.get("circuit_breaker_state") in ("CLOSED", "HALF_OPEN", "OPEN")
        and nh_file.exists()
        and (nh_file.stat().st_mode & 0o777) == 0o600
    )
    record(
        "V82-04",
        "TEN_AGENT_ORCHESTRATION",
        "GET /api/v8/agents/status (10 agents) & GET /api/v8/network/health (circuit breaker + 0600 latest.json)",
        ag_ok,
        "BACKEND_INTEGRATION_PASS" if ag_ok else "FAIL",
        f"agents={ag_body.get('agent_count')}, circuit_breaker={nh_body.get('circuit_breaker_state')}, mode={nh_mode}",
    )

    # 5. BACKEND_INTEGRATION_PASS: Security & Auth Protection on Live-Status & Native-Jobs
    unauth_jobs_code, _ = http_req("/api/v1/native-jobs", method="POST", data={"fig_id": "fig10"})
    forged_ls_code, _ = http_req("/api/v8/verdi/live-status?fig_id=fig10", headers={"Authorization": "Bearer forged_invalid_token_xyz"})
    sec_ok = unauth_jobs_code in (401, 403) and forged_ls_code in (401, 403)
    record(
        "V82-05",
        "SECURITY_ACCESS_CONTROL",
        "Unauthenticated POST /api/v1/native-jobs and forged Bearer token on GET /api/v8/verdi/live-status rejected",
        sec_ok,
        "BACKEND_INTEGRATION_PASS" if sec_ok else "FAIL",
        f"unauth_post_native_jobs=HTTP {unauth_jobs_code}, forged_live_status=HTTP {forged_ls_code}",
    )

    # 6. BACKEND_INTEGRATION_PASS: Durable Asynchronous POST /api/v1/native-jobs (HTTP 202 Accepted)
    secret_path = Path.home() / ".config" / "engr852" / "owner_private_config.json"
    comp_secret = json.loads(secret_path.read_text(encoding="utf-8")).get("companion_secret", "")
    comp_code, comp_body = http_req(
        "/api/v8/auth/companion",
        method="POST",
        data={"companion_secret": comp_secret, "device_id": "imac"},
        headers={"X-Companion-Secret": comp_secret},
    )
    comp_token = comp_body.get("session_token", "") if isinstance(comp_body, dict) else ""
    csrf_token = comp_body.get("csrf_token", "") if isinstance(comp_body, dict) else ""
    auth_hdrs = {
        "Authorization": f"Bearer {comp_token}",
        "X-CSRF-Token": csrf_token,
        "X-Companion-Secret": comp_secret,
    }
    t0 = time.time()
    nj_code, nj_body = http_req(
        "/api/v1/native-jobs",
        method="POST",
        data={"fig_id": "fig10", "page_num": 51, "force_new_launch": False},
        headers=auth_hdrs,
    )
    latency_ms = round((time.time() - t0) * 1000, 1)
    jid = nj_body.get("job_id", "") if isinstance(nj_body, dict) else ""
    st_code, st_body = http_req(f"/api/v1/native-jobs/{jid}", headers=auth_hdrs) if jid else (404, {})
    ev_code, ev_body = http_req(f"/api/v1/native-jobs/{jid}/events", headers=auth_hdrs) if jid else (404, {})
    async_ok = (
        nj_code == 202
        and bool(jid)
        and nj_body.get("accepted") is True
        and st_code == 200
        and ev_code == 200
    )
    record(
        "V82-06",
        "DURABLE_ASYNC_NATIVE_JOBS",
        "POST /api/v1/native-jobs returns HTTP 202 Accepted with durable job_id, GET status, and GET events",
        async_ok,
        "BACKEND_INTEGRATION_PASS" if async_ok else "FAIL",
        f"HTTP {nj_code} in {latency_ms}ms, job_id={jid}, status_http={st_code}, events_http={ev_code}",
    )

    # 7. LIVE WAVEFORM / TRANSPORT CLASSIFICATION: Inspect real live status without fabricating PASS
    ls_code, ls_body = http_req("/api/v8/verdi/live-status?fig_id=fig10")
    err_code = ls_body.get("error_code", "UNKNOWN") if isinstance(ls_body, dict) else "UNKNOWN"
    summary_st = ls_body.get("summary_status", "UNKNOWN") if isinstance(ls_body, dict) else "UNKNOWN"
    flags = ls_body.get("flags", {}) if isinstance(ls_body, dict) else {}
    verdi_win = ls_body.get("verdi_window_id", "") if isinstance(ls_body, dict) else ""
    if summary_st == "VERDI_GUI_READY" and err_code == "NONE":
        live_verdict = "LIVE_WAVEFORM_VERIFICATION_PASS"
    else:
        live_verdict = f"LIVE_WAVEFORM_VERIFICATION_BLOCKED_BY_{err_code}"
    record(
        "V82-07",
        "TRUTHFUL_LIVE_TRANSPORT_AND_GUI_STATE",
        "Live transport & XQuartz Verdi state classified truthfully without fabricating PASS",
        ls_code == 200 and err_code in ("NONE", "SSH_TCP_TIMEOUT", "VERDI_PROCESS_NOT_RUNNING", "SSH_AUTH_FAILED", "VPN_ROUTE_UNAVAILABLE"),
        live_verdict,
        f"summary_status={summary_st}, error_code={err_code}, verdi_window_id={verdi_win or 'NONE'}, flags={flags}",
    )

    matrix = {
        "schema_version": "8.2.0",
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "staging_url": BASE_URL,
        "production_url_untouched": PROD_URL,
        "total_checks": len(results),
        "passed_checks": sum(1 for r in results if r["passed"]),
        "live_waveform_verdict": live_verdict,
        "results": results,
    }
    (DOCS_DIR / "QA_ACCEPTANCE_MATRIX.json").write_text(json.dumps(matrix, indent=2), encoding="utf-8")
    print(f"\nSaved QA_ACCEPTANCE_MATRIX.json ({matrix['passed_checks']}/{matrix['total_checks']} passed, live_verdict={live_verdict})")
    return 0 if all(r["passed"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
