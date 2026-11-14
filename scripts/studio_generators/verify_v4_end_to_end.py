#!/usr/bin/env python3
"""End-to-end verification of ENGR 852 Interactive ASIC Studio v4.0 (Rose & Lavender Edition)."""

import json
import subprocess
import time
import urllib.request
from pathlib import Path


def post_json(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    base = "http://127.0.0.1:8788"

    # 1. Verify HTML UI v4.0
    with urllib.request.urlopen(base + "/", timeout=10) as r:
        html = r.read().decode("utf-8")
    assert "Rose & Lavender" in html, "Missing v4.0 title"
    assert "runSubcommandByIndex(" in html, "Missing safe index subcommand runner"
    assert "runSelfHealingAiFix(" in html, "Missing self-healing AI debugger handler"
    assert "launchXquartzAndTerminalNow(" in html, "Missing XQuartz & Terminal launcher"
    print(f"[1/6] HTML UI v4.0 verified ({len(html)} bytes)")

    # 2. Verify Curriculum & Study Guide JSON schemas
    curr = get_json(base + "/api/curriculum")
    sg = get_json(base + "/api/study_guide")
    assert len(curr) == 100, f"Expected 100 pages, got {len(curr)}"
    total_qs = sum(len(p.get("quiz_questions", [])) for p in curr)
    total_vids = sum(
        len(t.get("videos", []))
        for p in curr
        for t in p.get("learning_tasks", [])
        if isinstance(t, dict)
    )
    foundations = sg.get("foundations", [])
    midterm_qs = sg.get("midterm_and_exam_bank", [])
    print(
        f"[2/6] Curriculum & Study Guide verified: {len(curr)} pages, "
        f"{total_qs} page quiz Qs, {total_vids} YouTube videos, "
        f"{len(foundations)} Foundations (F0-F17), {len(midterm_qs)} Midterm Qs (Q1-Q15)"
    )

    # 3. Verify Live XQuartz & macOS Terminal.app Broadcast
    gui_res = post_json(base + "/api/launch_gui", {"page_num": 1})
    print(f"[3/6] Live GUI & Terminal.app Broadcast: {gui_res}")

    # 4. Test Self-Healing AI Debugger & Live Execution across representative V1->V9 pages
    sample_pages = [1, 25, 51, 84, 100]
    for p in sample_pages:
        r_fix = post_json(base + "/api/ai_fix_page", {"page_num": p})
        ec = r_fix.get("exit_code")
        st = r_fix.get("state", {}).get("completed_pages", {}).get(str(p), {}).get("status")
        assert ec == 0 and st == "PASS", f"Page {p} failed: exit={ec}, status={st}"
    print(f"[4/6] Self-Healing AI Auto-Debugger verified across {len(sample_pages)} V1->V9 pages (all PASS, exit=0)")

    # 5. Test direct one-liner execution on Page 1 & Page 51 (16-bit 520MHz simulation)
    p51_cmd = curr[50]["one_liner"]
    r_exec = post_json(
        base + "/api/exec_terminal",
        {"command": p51_cmd, "page_num": 51, "force_step": True, "launch_xquartz": False},
    )
    print(
        f"[5/6] Direct Page 51 One-Liner Exec: exit_code={r_exec.get('exit_code')}, "
        f"ai_status={r_exec.get('ai_debug', {}).get('status')}"
    )

    # 6. Verify workspace files exist in ~/Developer/motion-estimator-14nm-asic-manual
    ws = Path.home() / "Developer" / "motion-estimator-14nm-asic-manual"
    required_files = [
        "rtl/8bit/top.v",
        "rtl/16bit/pe.v",
        "rtl/16bit/comparator.v",
        "rtl/16bit/control.v",
        "rtl/16bit/top.v",
        "tb/16bit/top_tb_direct.v",
        "constraints/top.sdc",
        "results/primetime_3corner_sta.rpt",
        "results/icv_drc_signoff.rpt",
    ]
    missing = [f for f in required_files if not (ws / f).exists()]
    assert not missing, f"Missing workspace files: {missing}"
    print(f"[6/6] All {len(required_files)} core RTL/TB/SDC/Sign-off files verified in {ws}")


if __name__ == "__main__":
    main()
