#!/usr/bin/env python3
"""
JUNIOR DEVELOPER v8.0.1 & v8.0.2 — Comprehensive Security, Correctness & Native Verdi Verification Suite
Runs against staging server http://127.0.0.1:8789 without touching production port 8788.
"""

import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("JDEV8_TEST_BASE_URL", "http://127.0.0.1:8789")
REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
OWNER_PRIVATE_CFG = pathlib.Path.home() / ".config" / "engr852" / "owner_private_config.json"
BRIDGE_SCRIPT = REPO_ROOT / "practice_from_scratch" / "scripts" / "engr852_native_verdi_bridge.py"


def load_companion_secret():
    if OWNER_PRIVATE_CFG.is_file():
        try:
            return json.loads(OWNER_PRIVATE_CFG.read_text(encoding="utf-8")).get("companion_secret", "")
        except Exception:
            return ""
    return ""


def api_request(path, method="GET", payload=None, headers=None, timeout=15):
    url = BASE_URL + path
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    data_bytes = None
    if payload is not None:
        data_bytes = json.dumps(payload).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    req = urllib.request.Request(url, data=data_bytes, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                body = json.loads(raw)
            except Exception:
                body = {"_raw": raw}
            return resp.status, body
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw)
        except Exception:
            body = {"_raw": raw}
        return e.code, body


def main():
    results = []

    def record(test_id, title, passed, details):
        results.append({
            "test_id": test_id,
            "title": title,
            "passed": bool(passed),
            "details": details,
        })
        mark = "PASS" if passed else "FAIL"
        print(f"[{mark}] {test_id} — {title}: {details}")

    # 1. Mint a guest session and register two student accounts (studentA, studentB)
    ts = int(time.time()) % 100000
    st, guest_data = api_request("/api/v8/auth/guest", method="POST", payload={})
    guest_token = guest_data.get("session_token", "")
    record(
        "SEC-01",
        "Guest session provisioning",
        st == 200 and bool(guest_token),
        f"status={st}, handle={guest_data.get('user', {}).get('handle')}",
    )

    st_a, reg_a = api_request(
        "/api/v8/auth/register",
        method="POST",
        payload={
            "handle": f"stud_a_{ts}",
            "email": f"stud_a_{ts}@sfsu.edu",
            "display_name": "Student Alpha",
            "password": "StrongPassword!2026",
        },
    )
    token_a = reg_a.get("session_token", "")
    csrf_a = reg_a.get("csrf_token", "")
    hdr_a = {"Authorization": f"Bearer {token_a}", "X-CSRF-Token": csrf_a}

    st_b, reg_b = api_request(
        "/api/v8/auth/register",
        method="POST",
        payload={
            "handle": f"stud_b_{ts}",
            "email": f"stud_b_{ts}@sfsu.edu",
            "display_name": "Student Beta",
            "password": "StrongPassword!2026",
        },
    )
    token_b = reg_b.get("session_token", "")
    csrf_b = reg_b.get("csrf_token", "")
    hdr_b = {"Authorization": f"Bearer {token_b}", "X-CSRF-Token": csrf_b}

    record(
        "SEC-02",
        "Student account registration & CSRF issuance",
        st_a == 200 and st_b == 200 and bool(token_a) and bool(token_b) and bool(csrf_a),
        f"studentA={reg_a.get('user', {}).get('handle')}, studentB={reg_b.get('user', {}).get('handle')}",
    )

    # 2. P0-1: Verify all 19 legacy/host/workspace/GitHub/Verdi POST routes block guest & student sessions with 403
    privileged_post_routes = [
        ("/api/exec_terminal", {"cmd": "id"}),
        ("/api/v7/jobs/execute", {"page_num": 1, "cmd": "id"}),
        ("/api/v7/jobs/control", {"job_id": "test", "action": "cancel"}),
        ("/api/ai_fix_page", {"page": 1}),
        ("/api/heal_all_failed", {}),
        ("/api/github_sync", {}),
        ("/api/verify_all_100", {}),
        ("/api/workspace_file", {"path": "rtl/16bit/top.v", "content": "// test"}),
        ("/api/reset_progress", {}),
        ("/api/user_onboard", {"username": "test"}),
        ("/api/v7/git_sync", {}),
        ("/api/v7/acceptance_tests", {}),
        ("/api/v7/xquartz_check", {}),
        ("/api/v7/custom_curriculum", {"title": "test"}),
        ("/api/custom_project", {"action": "status"}),
        ("/api/native-runs", {"fig_id": "fig10"}),
        ("/api/xquartz_plot", {"fig_id": "fig10"}),
        ("/api/launch_gui", {"tool": "verdi"}),
        ("/api/super_agent/chat", {"action": "run_page", "page": 1}),
    ]
    blocked_count = 0
    failed_routes = []
    for route, body in privileged_post_routes:
        code_student, _ = api_request(route, method="POST", payload=body, headers=hdr_a)
        code_guest, _ = api_request(route, method="POST", payload=body, headers={"Authorization": f"Bearer {guest_token}"})
        if code_student == 403 and code_guest == 403:
            blocked_count += 1
        else:
            failed_routes.append(f"{route}(stud={code_student},guest={code_guest})")
    record(
        "P0-1",
        "All 19 host/workspace/GitHub/EDA POST endpoints reject student & guest tokens with 403",
        blocked_count == len(privileged_post_routes),
        f"blocked={blocked_count}/{len(privileged_post_routes)}, failures={failed_routes}",
    )

    # 3. P1-6: Verify sensitive GET endpoints reject student/guest with 403
    privileged_get_routes = [
        "/api/native-runs",
        "/api/v7/acceptance_tests",
        "/api/v7/events",
        "/api/super_agent/diagnostics",
        "/api/workspace_file?path=rtl/16bit/top.v",
    ]
    get_blocked = 0
    get_failures = []
    for route in privileged_get_routes:
        code_stud, _ = api_request(route, method="GET", headers=hdr_a)
        if code_stud == 403:
            get_blocked += 1
        else:
            get_failures.append(f"{route}->{code_stud}")
    record(
        "P1-6A",
        "Sensitive host/diagnostic/Verdi GET endpoints reject student sessions with 403",
        get_blocked == len(privileged_get_routes),
        f"blocked={get_blocked}/{len(privileged_get_routes)}, failures={get_failures}",
    )

    # 4. P0-2: Companion Authentication Bypass Checks
    # 4a: Calling /api/v8/auth/companion without secret -> 403
    st_comp_nosecret, body_comp_nosecret = api_request("/api/v8/auth/companion", method="POST", payload={})
    # 4b: Calling /api/v8/auth/companion with valid secret BUT with X-Forwarded-For header -> 403
    comp_secret = load_companion_secret()
    st_comp_xff, body_comp_xff = api_request(
        "/api/v8/auth/companion",
        method="POST",
        payload={},
        headers={"X-Companion-Secret": comp_secret, "X-Forwarded-For": "198.51.100.42"},
    )
    # 4c: Calling /api/v8/auth/companion from direct loopback with valid X-Companion-Secret -> 200
    st_comp_ok, body_comp_ok = api_request(
        "/api/v8/auth/companion",
        method="POST",
        payload={"companion_secret": comp_secret},
        headers={"X-Companion-Secret": comp_secret},
    )
    owner_token = body_comp_ok.get("session_token", "")
    owner_hdr = {"Authorization": f"Bearer {owner_token}"}
    record(
        "P0-2",
        "Companion endpoint rejects missing secret & X-Forwarded-For proxy headers (403) and accepts valid secret (200)",
        st_comp_nosecret == 403 and st_comp_xff == 403 and st_comp_ok == 200 and bool(owner_token),
        f"no_secret={st_comp_nosecret}, with_xff={st_comp_xff}, valid_secret={st_comp_ok}, role={body_comp_ok.get('user', {}).get('role')}",
    )

    # 5. P1-6B: Verify GET /api/native-runs works cleanly (200) for verified Owner Companion (fixing AttributeError)
    st_nr_owner, body_nr_owner = api_request("/api/native-runs", method="GET", headers=owner_hdr)
    record(
        "P1-6B",
        "GET /api/native-runs returns 200 JSON for verified Owner Companion session",
        st_nr_owner == 200 and body_nr_owner.get("ok") is True and isinstance(body_nr_owner.get("runs"), list),
        f"status={st_nr_owner}, runs_count={len(body_nr_owner.get('runs', []))}",
    )

    # 6. P0-3: Student Open-Source Verilog Sandbox Security & Kernel Sandbox Enforcement
    st_projs, body_projs = api_request("/api/v8/projects", method="GET", headers=hdr_a)
    projects = body_projs.get("projects", [])
    first_proj_id = projects[0]["project_id"] if projects else ""

    malicious_payloads = [
        ("$readmemh host file read", 'module m; reg [7:0] mem [0:3]; initial $readmemh("/Users/huynguyen/.ssh/id_rsa", mem); endmodule'),
        ("$fopen file access", 'module m; integer fd; initial fd = $fopen("/tmp/pwn", "w"); endmodule'),
        ("$system shell escape", 'module m; initial $system("id"); endmodule'),
        ("`include arbitrary path", '`include "/etc/passwd"\nmodule m; endmodule'),
    ]
    rejected_malicious = 0
    for label, bad_tb in malicious_payloads:
        st_bad, body_bad = api_request(
            f"/api/v8/projects/{first_proj_id}/runs",
            method="POST",
            payload={"rtl_source": "module top(input a, output b); assign b = a; endmodule", "tb_source": bad_tb},
            headers=hdr_a,
        )
        if st_bad == 400 and body_bad.get("code") == "400_UNSAFE_VERILOG_SOURCE":
            rejected_malicious += 1
    record(
        "P0-3A",
        "Malicious Verilog constructs ($readmemh, $fopen, $system, `include) rejected with HTTP 400",
        rejected_malicious == len(malicious_payloads),
        f"rejected={rejected_malicious}/{len(malicious_payloads)}",
    )

    # 7. P1-2: Project source retrieval, SHA-256 hashes, save endpoint, and empty editor rejection
    st_pget, body_pget = api_request(f"/api/v8/projects/{first_proj_id}", method="GET", headers=hdr_a)
    proj_detail = body_pget.get("project", {})
    has_sources = bool(proj_detail.get("rtl_source")) and bool(proj_detail.get("tb_source")) and bool(proj_detail.get("rtl_sha256"))
    st_empty_save, body_empty_save = api_request(
        f"/api/v8/projects/{first_proj_id}",
        method="PUT",
        payload={"rtl_source": "", "tb_source": proj_detail.get("tb_source", "")},
        headers=hdr_a,
    )
    st_empty_run, body_empty_run = api_request(
        f"/api/v8/projects/{first_proj_id}/runs",
        method="POST",
        payload={"rtl_source": "", "tb_source": ""},
        headers=hdr_a,
    )
    record(
        "P1-2",
        "Project detail includes rtl_source/tb_source/SHA-256 and rejects empty editor submissions with HTTP 400",
        has_sources and st_empty_save == 400 and st_empty_run == 400,
        f"has_sources={has_sources}, empty_save={st_empty_save}({body_empty_save.get('code')}), empty_run={st_empty_run}({body_empty_run.get('code')})",
    )

    # 8. P1-1, P1-3, P1-4, P1-7: Execute valid self-checking ALU run and verify Schema 8.0.1 + typed VCD + kernel sandbox
    st_run_ok, body_run_ok = api_request(
        f"/api/v8/projects/{first_proj_id}/runs",
        method="POST",
        payload={
            "rtl_source": proj_detail.get("rtl_source"),
            "tb_source": proj_detail.get("tb_source"),
            "run_yosys": True,
        },
        headers=hdr_a,
        timeout=25,
    )
    run_ok = body_run_ok.get("run", {})
    wf_ok = run_ok.get("waveform_summary", {})
    sigs_ok = wf_ok.get("signals", [])
    typed_sig_ok = (
        isinstance(sigs_ok, list)
        and len(sigs_ok) > 0
        and isinstance(sigs_ok[0], dict)
        and "name" in sigs_ok[0]
        and isinstance(sigs_ok[0].get("samples"), list)
    )
    schema_ok = (
        run_ok.get("schema_version") == "8.0.1"
        and run_ok.get("status") == "FUNCTIONALLY_VERIFIED"
        and run_ok.get("functional_assertion_state") == "ASSERTIONS_PASSED"
        and run_ok.get("synthesis_state") == "SYNTHESIZED"
        and run_ok.get("timing_estimate_state") == "ILLUSTRATIVE_HEURISTIC_ESTIMATE"
        and isinstance(run_ok.get("stages"), dict)
    )
    record(
        "P1-1_P1-3",
        "Self-checking ALU run returns Schema 8.0.1, FUNCTIONALLY_VERIFIED, and typed VCD signals with samples[{t,v}]",
        st_run_ok == 200 and typed_sig_ok and schema_ok,
        f"status={run_ok.get('status')}, schema={run_ok.get('schema_version')}, signals={len(sigs_ok)}, timing_state={run_ok.get('timing_estimate_state')}",
    )

    # 9. P1-4A: Run without self-checking assertions must return SIMULATION_COMPLETED (not FUNCTIONALLY_VERIFIED)
    clean_alu_rtl = """module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  assign y = (op == 2'b00) ? (a + b) : ((op == 2'b01) ? (a - b) : (a * b));
  assign overflow = (y > 16'h00FF);
endmodule
"""
    non_checking_tb = """`timescale 1ns/1ps
module tb_no_assert;
  reg [7:0] a = 8'h10, b = 8'h20;
  reg [1:0] op = 2'b00;
  wire [15:0] y;
  wire ovf;
  alu8 dut(.a(a), .b(b), .op(op), .y(y), .overflow(ovf));
  initial begin
    $dumpfile("simulation.vcd");
    $dumpvars(0, tb_no_assert);
    #10 a = 8'hFF; b = 8'h01;
    #10 op = 2'b01;
    #10 a = 8'h40; b = 8'h20;
    #10 $display("Done running waves without self-check.");
    $finish;
  end
endmodule
"""
    st_no_assert, body_no_assert = api_request(
        f"/api/v8/projects/{first_proj_id}/runs",
        method="POST",
        payload={
            "rtl_source": clean_alu_rtl,
            "tb_source": non_checking_tb,
            "run_yosys": True,
        },
        headers=hdr_a,
        timeout=25,
    )
    run_na = body_no_assert.get("run", {})
    record(
        "P1-4A",
        "Simulation without self-checking assertions is classified as SIMULATION_COMPLETED (not FUNCTIONALLY_VERIFIED)",
        st_no_assert == 200
        and run_na.get("status") == "SIMULATION_COMPLETED"
        and run_na.get("functional_assertion_state") == "UNVERIFIED_NO_SELF_CHECKING_ASSERTIONS",
        f"status={run_na.get('status')}, assertion_state={run_na.get('functional_assertion_state')}",
    )

    # 10. P1-4B: Run where simulation passes but Yosys synthesis fails must return SYNTHESIS_FAILED
    bad_synth_rtl = """module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  real r_val;
  always @(*) r_val = $itor(a) / 3.14159;
  assign y = a + b;
  assign overflow = 1'b0;
endmodule
"""
    st_bs, body_bs = api_request(
        f"/api/v8/projects/{first_proj_id}/runs",
        method="POST",
        payload={
            "rtl_source": bad_synth_rtl,
            "tb_source": non_checking_tb,
            "run_yosys": True,
        },
        headers=hdr_a,
        timeout=25,
    )
    run_bs = body_bs.get("run", {})
    # Note: if Yosys synthesizes `real` by ignoring unused `r_val`, let's force a Yosys synthesis error via an unresolved cell or division of real
    if run_bs.get("synthesis_exit_code") == 0:
        bad_synth_rtl_2 = """module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  assign y = a + b;
  assign overflow = 1'b0;
  `ifndef __ICARUS__
  syntax_error_in_yosys_only invalid_token;
  `endif
endmodule
"""
        st_bs, body_bs = api_request(
            f"/api/v8/projects/{first_proj_id}/runs",
            method="POST",
            payload={
                "rtl_source": bad_synth_rtl_2,
                "tb_source": non_checking_tb,
                "run_yosys": True,
            },
            headers=hdr_a,
            timeout=25,
        )
        run_bs = body_bs.get("run", {})

    record(
        "P1-4B",
        "Simulation passing with Yosys synthesis failure is classified as SYNTHESIS_FAILED (never masked as PASS)",
        st_bs == 200
        and run_bs.get("status") == "SYNTHESIS_FAILED"
        and run_bs.get("synthesis_state") == "SYNTHESIS_FAILED",
        f"status={run_bs.get('status')}, synth_exit={run_bs.get('synthesis_exit_code')}, synth_state={run_bs.get('synthesis_state')}",
    )

    # 11. P1-5: Messenger privacy & user block enforcement + XSS sanitization
    st_dm, body_dm = api_request(
        "/api/v8/messages/conversations",
        method="POST",
        payload={"conversation_type": "dm", "recipient_handle": f"stud_b_{ts}"},
        headers=hdr_a,
    )
    conv_id = body_dm.get("conversation", {}).get("conversation_id", "")
    # Third user (guest) tries to read DM between studentA and studentB -> 403
    st_dm_leak, _ = api_request(
        f"/api/v8/messages/conversations/{conv_id}/messages",
        method="GET",
        headers={"Authorization": f"Bearer {guest_token}"},
    )
    # Student B blocks Student A, then Student A tries to send DM -> 403
    api_request(
        "/api/v8/users/block",
        method="POST",
        payload={"target_handle": f"stud_a_{ts}", "block": True},
        headers=hdr_b,
    )
    st_blocked_msg, _ = api_request(
        f"/api/v8/messages/conversations/{conv_id}/messages",
        method="POST",
        payload={"body": "Hello after block"},
        headers=hdr_a,
    )
    # Unblock for cleanliness
    api_request(
        "/api/v8/users/block",
        method="POST",
        payload={"target_handle": f"stud_a_{ts}", "block": False},
        headers=hdr_b,
    )
    record(
        "P1-5",
        "Private DM read blocked for non-member (403) and blocked user prevented from messaging (403)",
        st_dm == 200 and st_dm_leak == 403 and st_blocked_msg == 403,
        f"dm_create={st_dm}, outsider_read={st_dm_leak}, blocked_send={st_blocked_msg}",
    )

    # 12. v8.0.2: Native Verdi 18-case self-test (NV01-NV18) + Distinct Figure Provenance + Live Status Truthfulness
    proc_nv = subprocess.run(
        [sys.executable, str(BRIDGE_SCRIPT), "self-test"],
        capture_output=True,
        text=True,
        timeout=30,
    )
    out_nv = proc_nv.stdout or ""
    idx_nv = out_nv.find('\n{\n  "suite":')
    nv_json = json.loads(out_nv[idx_nv + 1 :]) if idx_nv >= 0 else json.loads(out_nv)
    record(
        "V802-NV18",
        "engr852_native_verdi_bridge.py 18-case acceptance suite (NV01-NV18)",
        proc_nv.returncode == 0 and nv_json.get("passed") == 18 and nv_json.get("total") == 18,
        f"passed={nv_json.get('passed')}/{nv_json.get('total')}",
    )

    st_figs, body_figs = api_request("/api/v8/figures/recorded-evidence", method="GET")
    figs_map = body_figs.get("figures", {})
    hashes_set = {v.get("sha256") for v in figs_map.values() if v.get("sha256")}
    record(
        "V802-PROV",
        "All 6 V9 figures (fig7..fig11, layout) map to 6 distinct verified screenshots & SHA-256 hashes",
        st_figs == 200 and len(figs_map) == 6 and len(hashes_set) == 6,
        f"figures={list(figs_map.keys())}, unique_sha256_count={len(hashes_set)}",
    )

    st_live, body_live = api_request("/api/v8/verdi/live-status?fig_id=fig10", method="GET")
    live_st = body_live.get("live_status", {})
    record(
        "V802-LIVE",
        "Live Verdi status truthfully reports BLOCKED when no live Verdi X11 window is present",
        st_live == 200
        and live_st.get("verdi_window_found") is False
        and live_st.get("connection_state") == "BLOCKED"
        and isinstance(live_st.get("recorded_evidence"), dict),
        f"connection_state={live_st.get('connection_state')}, verdi_window_found={live_st.get('verdi_window_found')}, xquartz_running={live_st.get('xquartz_running')}",
    )

    passed_all = sum(1 for r in results if r["passed"])
    print(f"\n=== SUMMARY: {passed_all}/{len(results)} CHECKS PASSED ===")
    if passed_all != len(results):
        sys.exit(1)


if __name__ == "__main__":
    main()
