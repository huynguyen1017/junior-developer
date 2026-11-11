#!/usr/bin/env python3
"""
JUNIOR DEVELOPER v8.0.1 & v8.0.2 — Real Headless Browser Playwright E2E Verification Suite (15 Checks)
Executes against staging http://127.0.0.1:8789 and captures browser screenshots into the artifacts directory.
"""

import json
import os
import pathlib
import sys
import time
from playwright.sync_api import sync_playwright

BASE_URL = os.environ.get("JDEV8_TEST_BASE_URL", "http://127.0.0.1:8789")
ARTIFACT_DIR = pathlib.Path("/Users/huynguyen/.gemini/antigravity/brain/9abd734c-7786-4e8f-a3e8-35f2bdc2137b")
CHROME_EXECUTABLE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    results = []
    page_errors = []

    def record(test_id, title, passed, details):
        results.append({
            "test_id": test_id,
            "title": title,
            "passed": bool(passed),
            "details": details,
        })
        mark = "PASS" if passed else "FAIL"
        print(f"[{mark}] {test_id} — {title}: {details}", flush=True)

    with sync_playwright() as p:
        launch_kwargs = {"headless": True}
        if pathlib.Path(CHROME_EXECUTABLE).is_file():
            launch_kwargs["executable_path"] = CHROME_EXECUTABLE
        browser = p.chromium.launch(**launch_kwargs)
        context = browser.new_context(viewport={"width": 1600, "height": 1050})
        page = context.new_page()
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))

        # E2E-01: Load landing page & verify brand identity
        page.goto(BASE_URL + "/", wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(1200)
        body_text = page.locator("body").inner_text()
        record(
            "E2E-01",
            "Landing page loads JUNIOR DEVELOPER brand & 'Learn. Build. Connect.' with 0 pageerrors",
            "JUNIOR DEVELOPER" in body_text and "Learn. Build. Connect." in body_text and len(page_errors) == 0,
            f"brand_present={'JUNIOR DEVELOPER' in body_text}, page_errors={len(page_errors)}",
        )

        # E2E-02: Verify RTL & Testbench editors auto-populate from starter project (P1-2)
        page.wait_for_function(
            "() => (document.getElementById('jdevRtlEditor')?.value || '').trim().length > 20 && (document.getElementById('jdevTbEditor')?.value || '').trim().length > 20",
            timeout=10000,
        )
        rtl_val = page.locator("#jdevRtlEditor").input_value()
        tb_val = page.locator("#jdevTbEditor").input_value()
        rtl_hash_txt = page.locator("#jdevRtlHashLabel").inner_text()
        tb_hash_txt = page.locator("#jdevTbHashLabel").inner_text()
        record(
            "E2E-02",
            "RTL & Testbench editors populate automatically with starter sources and SHA-256 hashes (P1-2)",
            len(rtl_val) > 50 and len(tb_val) > 50 and "SHA-256:" in rtl_hash_txt and "SHA-256:" in tb_hash_txt,
            f"rtl_len={len(rtl_val)}, tb_len={len(tb_val)}, rtl_hash='{rtl_hash_txt}'",
        )

        # E2E-03: Click 'Run Verilog + VCD + Yosys' and verify typed VCD waveform canvas + Schema 8.0.1 + 7 states (P1-1, P1-3, P1-7)
        page.evaluate("jdevRunOpenSourceVerilog()")
        page.wait_for_function(
            "() => { const t = document.getElementById('jdevRunOutputPre')?.textContent || ''; return t.includes('OPEN-SOURCE EDA SANDBOX RUN') || t.includes('error'); }",
            timeout=20000,
        )
        run_pre = page.locator("#jdevRunOutputPre").inner_text()
        run_badge = page.locator("#jdevProjectRunBadge").inner_text()
        verif_bar = page.locator("#jdevVerificationStatesBar").inner_text()
        cursor_readout = page.locator("#jdevVcdCursorReadout").inner_text()
        canvas_non_blank = page.evaluate("""() => {
            const c = document.getElementById('jdevVcdWaveformCanvas');
            if (!c) return false;
            const ctx = c.getContext('2d');
            const data = ctx.getImageData(0, 0, c.width, c.height).data;
            let nonBg = 0;
            for (let i = 0; i < data.length; i += 16) {
                if (data[i] > 30 || data[i+1] > 30 || data[i+2] > 50) nonBg++;
            }
            return nonBg > 100;
        }""")
        page.screenshot(
            path=str(ARTIFACT_DIR / "jdev_v801_e2e_verilog_vcd_verified.png"),
            full_page=False,
        )
        record(
            "E2E-03",
            "Open-source Verilog run succeeds without sig.slice crash, renders VCD canvas & 7 verification states",
            "sig.slice is not a function" not in run_pre
            and "FUNCTIONALLY_VERIFIED" in run_badge
            and "ILLUSTRATIVE_HEURISTIC_ESTIMATE" in verif_bar
            and canvas_non_blank,
            f"badge='{run_badge}', canvas_non_blank={canvas_non_blank}, cursor='{cursor_readout[:60]}'",
        )

        # E2E-04: VCD Waveform Zoom, Pan & Cursor Click Inspection (P1-1)
        page.evaluate("jdevZoomPanVcd(1.5, 0)")
        page.evaluate("jdevZoomPanVcd(1.0, 0.2)")
        vcd_box = page.locator("#jdevVcdWaveformCanvas").bounding_box()
        if vcd_box:
            page.mouse.click(vcd_box["x"] + vcd_box["width"] * 0.6, vcd_box["y"] + vcd_box["height"] * 0.5)
        zoomed_readout = page.locator("#jdevVcdCursorReadout").inner_text()
        page.evaluate("jdevResetVcdViewport()")
        record(
            "E2E-04",
            "VCD canvas supports interactive zoom (1.5x), pan, and click-to-inspect cursor time/values",
            "Zoom 1.5x" in zoomed_readout and "=" in zoomed_readout,
            f"zoomed_readout='{zoomed_readout[:80]}'",
        )

        # E2E-05: User Edits Preserved Across Save & Run (P1-2)
        edited_rtl = rtl_val + "\n// E2E_USER_EDIT_MARKER_2026\n"
        page.locator("#jdevRtlEditor").fill(edited_rtl)
        page.evaluate("jdevSaveCurrentProjectSources()")
        page.wait_for_function(
            "() => (document.getElementById('jdevProjectRunBadge')?.textContent || '').includes('SOURCES SAVED')",
            timeout=10000,
        )
        new_rtl_hash = page.locator("#jdevRtlHashLabel").inner_text()
        page.evaluate("jdevRunOpenSourceVerilog()")
        page.wait_for_function(
            "() => (document.getElementById('jdevProjectRunBadge')?.textContent || '').includes('FUNCTIONALLY_VERIFIED')",
            timeout=20000,
        )
        preserved_rtl = page.locator("#jdevRtlEditor").input_value()
        record(
            "E2E-05",
            "Saving modified RTL updates SHA-256 hash and preserves user edits across runs",
            new_rtl_hash != rtl_hash_txt and "E2E_USER_EDIT_MARKER_2026" in preserved_rtl,
            f"old_hash='{rtl_hash_txt}', new_hash='{new_rtl_hash}', marker_preserved={'E2E_USER_EDIT_MARKER_2026' in preserved_rtl}",
        )

        # E2E-06: Empty Editor Submission Rejected with 400 (P1-2)
        page.locator("#jdevRtlEditor").fill("")
        page.evaluate("jdevRunOpenSourceVerilog()")
        page.wait_for_function(
            "() => (document.getElementById('jdevRunOutputPre')?.textContent || '').includes('400_EMPTY_RTL_SOURCE')",
            timeout=10000,
        )
        empty_err_pre = page.locator("#jdevRunOutputPre").inner_text()
        record(
            "E2E-06",
            "Empty RTL editor submission is rejected with 400_EMPTY_RTL_SOURCE (never silently substitutes starter code)",
            "400_EMPTY_RTL_SOURCE" in empty_err_pre,
            f"output='{empty_err_pre.splitlines()[0] if empty_err_pre else ''}'",
        )

        # Restore starter project sources
        page.evaluate("jdevResetCurrentProject()")
        page.wait_for_function(
            "() => (document.getElementById('jdevRtlEditor')?.value || '').trim().length > 50",
            timeout=10000,
        )

        # E2E-07: Malicious Verilog ($readmemh) Blocked in Browser (P0-3)
        page.locator("#jdevTbEditor").fill(
            'module bad_tb; reg [7:0] m [0:3]; initial $readmemh("/Users/huynguyen/.ssh/id_rsa", m); endmodule'
        )
        page.evaluate("jdevRunOpenSourceVerilog()")
        page.wait_for_function(
            "() => (document.getElementById('jdevRunOutputPre')?.textContent || '').includes('400_UNSAFE_VERILOG_SOURCE')",
            timeout=10000,
        )
        unsafe_pre = page.locator("#jdevRunOutputPre").inner_text()
        record(
            "E2E-07",
            "Browser submission of $readmemh host file read is blocked with 400_UNSAFE_VERILOG_SOURCE",
            "400_UNSAFE_VERILOG_SOURCE" in unsafe_pre,
            f"badge='{page.locator('#jdevProjectRunBadge').inner_text()}'",
        )

        # E2E-08: Assertion-Free Simulation Classified as SIMULATION_COMPLETED (P1-4)
        clean_alu_rtl = """module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  assign y = (op == 2'b00) ? (a + b) : (a - b);
  assign overflow = (y > 16'h00FF);
endmodule"""
        no_assert_tb = """`timescale 1ns/1ps
module tb_no_assert;
  reg [7:0] a = 8'h10, b = 8'h20;
  reg [1:0] op = 2'b00;
  wire [15:0] y;
  wire ovf;
  alu8 dut(.a(a), .b(b), .op(op), .y(y), .overflow(ovf));
  initial begin
    $dumpfile("simulation.vcd");
    $dumpvars(0, tb_no_assert);
    #10 a = 8'h30; b = 8'h40;
    #10 op = 2'b01;
    #10 a = 8'h90; b = 8'h10;
    #10 $display("Simulation finished without self-check assertions.");
    $finish;
  end
endmodule"""
        page.locator("#jdevRtlEditor").fill(clean_alu_rtl)
        page.locator("#jdevTbEditor").fill(no_assert_tb)
        page.evaluate("jdevRunOpenSourceVerilog()")
        page.wait_for_function(
            "() => (document.getElementById('jdevProjectRunBadge')?.textContent || '').includes('SIMULATION_COMPLETED')",
            timeout=20000,
        )
        na_badge = page.locator("#jdevProjectRunBadge").inner_text()
        na_bar = page.locator("#jdevVerificationStatesBar").inner_text()
        record(
            "E2E-08",
            "Simulation without self-checking assertions displays SIMULATION_COMPLETED & UNVERIFIED_NO_SELF_CHECKING_ASSERTIONS",
            "SIMULATION_COMPLETED" in na_badge and "UNVERIFIED_NO_SELF_CHECKING_ASSERTIONS" in na_bar,
            f"badge='{na_badge}'",
        )

        # E2E-09: Synthesis Failure Surfaced as SYNTHESIS_FAILED (P1-4)
        bad_synth_rtl = """module alu8(input [7:0] a, input [7:0] b, input [1:0] op, output [15:0] y, output overflow);
  assign y = a + b;
  assign overflow = 1'b0;
  `ifndef __ICARUS__
  yosys_only_syntax_error bad_cell;
  `endif
endmodule"""
        page.locator("#jdevRtlEditor").fill(bad_synth_rtl)
        page.evaluate("jdevRunOpenSourceVerilog()")
        page.wait_for_function(
            "() => (document.getElementById('jdevProjectRunBadge')?.textContent || '').includes('SYNTHESIS_FAILED')",
            timeout=20000,
        )
        sf_badge = page.locator("#jdevProjectRunBadge").inner_text()
        sf_bar = page.locator("#jdevVerificationStatesBar").inner_text()
        record(
            "E2E-09",
            "Yosys synthesis failure is surfaced as SYNTHESIS_FAILED in badge and 7-state bar",
            "SYNTHESIS_FAILED" in sf_badge and "Synthesis: SYNTHESIS_FAILED" in sf_bar,
            f"badge='{sf_badge}'",
        )

        # Restore starter project
        page.evaluate("jdevResetCurrentProject()")
        page.wait_for_timeout(600)

        # E2E-10: Register/Migrate Guest -> Student Account in Browser
        ts = int(time.time()) % 100000
        handle = f"e2e_stud_{ts}"
        page.locator("#jdevRegHandle").fill(handle)
        page.locator("#jdevRegEmail").fill(f"{handle}@sfsu.edu")
        page.locator("#jdevRegDisplayName").fill("E2E Browser Student")
        page.locator("#jdevRegPassword").fill("StrongBrowserPass!2026")
        page.evaluate("jdevRegisterAccount(true)")
        page.wait_for_function(
            "() => (document.getElementById('jdevSessionRolePill')?.textContent || '').trim() === 'STUDENT'",
            timeout=10000,
        )
        role_pill = page.locator("#jdevSessionRolePill").inner_text()
        record(
            "E2E-10",
            "Guest-to-Student account migration succeeds in browser and updates role pill to STUDENT",
            role_pill.strip() == "STUDENT",
            f"role_pill='{role_pill}', handle='{handle}'",
        )

        # E2E-11: Junior Connect Post Creation & XSS Protection (P1-5)
        page.evaluate("switchTab('tab-jdev-connect')")
        page.wait_for_timeout(300)
        page.locator("#jdevPostTitleInput").fill(f"XSS Audit Post {ts} <script>window.__XSS_FIRED=1</script>")
        page.locator("#jdevPostBodyInput").fill("Testing HTML escaping in community feed <img src=x onerror=window.__XSS_FIRED=1>")
        page.evaluate("jdevCreatePost()")
        page.wait_for_timeout(1000)
        xss_fired = page.evaluate("() => Boolean(window.__XSS_FIRED)")
        feed_txt = page.locator("#jdevPostsFeedBox").inner_text()
        record(
            "E2E-11",
            "Community post creation renders safely with XSS payload neutralized",
            (f"XSS Audit Post {ts}" in feed_txt) and (not xss_fired),
            f"post_visible={f'XSS Audit Post {ts}' in feed_txt}, xss_fired={xss_fired}",
        )

        # E2E-12: Junior Messenger Conversation Creation & Real-Time Message Send (P1-5)
        page.evaluate("switchTab('tab-jdev-messenger')")
        page.wait_for_timeout(300)
        page.locator("#jdevNewRoomTitleInput").fill(f"RTL Verification Study Group {ts}")
        page.evaluate("jdevCreateConversation('group')")
        page.wait_for_timeout(800)
        page.locator("#jdevMessageInput").fill(f"Verified 16-bit BestDist=0x0000 in study room {ts}!")
        page.evaluate("jdevSendMessage()")
        page.wait_for_timeout(800)
        msg_stream_txt = page.locator("#jdevMessagesStreamBox").inner_text()
        record(
            "E2E-12",
            "Junior Messenger group creation & message delivery render in real time",
            f"Verified 16-bit BestDist=0x0000 in study room {ts}!" in msg_stream_txt,
            f"conv_title='{page.locator('#jdevActiveConvTitle').inner_text()}'",
        )

        # E2E-13: Scoped AI Mentor Consultation
        page.evaluate("switchTab('tab-jdev-home')")
        page.wait_for_timeout(300)
        page.locator("#jdevAiPromptInput").fill("Why does 8-bit PE saturation fail on Row 1?")
        page.evaluate("jdevRunAiMentor()")
        page.wait_for_function(
            "() => !(document.getElementById('jdevAiResponseBox')?.textContent || '').includes('Consulting scoped AI Agent')",
            timeout=10000,
        )
        ai_txt = page.locator("#jdevAiResponseBox").inner_text()
        record(
            "E2E-13",
            "Scoped AI Mentor returns grounded hardware verification explanation",
            len(ai_txt) > 40 and ("SAD" in ai_txt or "16-bit" in ai_txt or "8-bit" in ai_txt or "BestDist" in ai_txt),
            f"response_len={len(ai_txt)}",
        )

        # E2E-14: v8.0.2 Fake Canvas Oscilloscope Removed & Native Verdi Viewer Truthful BLOCKED State
        fake_canvas_exists = page.evaluate("() => document.getElementById('popupOscilloscopeCanvas') !== null")
        page.evaluate("openLivePopupExecutionModal()")
        page.wait_for_timeout(1200)
        conn_badge_txt = page.locator("#nativeVerdiConnectionStateBadge").inner_text()
        blocked_banner_visible = page.locator("#nativeVerdiBlockedBanner").is_visible()
        fake_invocations = page.evaluate("() => window.__FAKE_OSCILLOSCOPE_INVOCATIONS || 0")
        page.locator("#livePopupExecutionModal").screenshot(
            path=str(ARTIFACT_DIR / "jdev_v802_native_verdi_viewer_modal.png")
        )
        record(
            "E2E-14",
            "Fake #popupOscilloscopeCanvas is removed, __FAKE_OSCILLOSCOPE_INVOCATIONS===0, and modal shows truthful BLOCKED state",
            (not fake_canvas_exists)
            and fake_invocations == 0
            and ("BLOCKED" in conn_badge_txt)
            and blocked_banner_visible,
            f"fake_canvas_exists={fake_canvas_exists}, fake_invocations={fake_invocations}, conn_badge='{conn_badge_txt}', blocked_banner={blocked_banner_visible}",
        )

        # E2E-15: v8.0.2 Distinct Recorded V9 Figure Captures (fig7..fig11, layout) & Student Permission Gate
        seen_hashes = {}
        seen_urls = {}
        for fid in ("fig7", "fig8", "fig9", "fig10", "fig11", "layout"):
            page.evaluate(f"async () => {{ await selectNativeVerdiFigure('{fid}', true); }}")
            page.wait_for_timeout(200)
            if fid == "fig10":
                page.locator("#livePopupExecutionModal").screenshot(
                    path=str(ARTIFACT_DIR / "jdev_v802_recorded_v9_fig10_modal.png")
                )
            prov_text = page.locator("#nativeVerdiProvenanceBox").inner_text()
            img_src = page.evaluate("() => document.getElementById('nativeVerdiWindowPreviewImg')?.getAttribute('src') || ''")
            seen_urls[fid] = img_src
            for line in prov_text.splitlines():
                if "SHA-256" in line:
                    seen_hashes[fid] = line.strip()
                    break

        # Student clicks 'Launch / Refresh Native Verdi' -> must NOT fake PASS; must show Owner/Companion permission block
        page.evaluate("triggerXquartzExternalWindowPlot(false)")
        page.wait_for_timeout(800)
        after_launch_badge = page.locator("#nativeVerdiConnectionStateBadge").inner_text()
        after_launch_banner = page.locator("#nativeVerdiBlockedBanner").inner_text()
        fake_invocations_after = page.evaluate("() => window.__FAKE_OSCILLOSCOPE_INVOCATIONS || 0")

        distinct_urls_ok = len(set(seen_urls.values())) == 6 and "v9_signoff_clean_layout.png" in seen_urls.get("layout", "")
        record(
            "E2E-15",
            "All 6 figures (fig7..fig11, layout) render distinct recorded V9 captures & student native Verdi launch is blocked (403)",
            distinct_urls_ok
            and fake_invocations_after == 0
            and ("BLOCKED" in after_launch_badge or "403" in after_launch_banner or "Owner" in after_launch_banner),
            f"distinct_urls={len(set(seen_urls.values()))}/6, layout_img='{seen_urls.get('layout')}', after_badge='{after_launch_badge}'",
        )

        browser.close()

    passed_all = sum(1 for r in results if r["passed"])
    print(f"\n=== BROWSER E2E SUMMARY: {passed_all}/{len(results)} CHECKS PASSED (page_errors={len(page_errors)}) ===")
    if passed_all != len(results) or len(page_errors) > 0:
        if page_errors:
            print("Page errors:", page_errors)
        sys.exit(1)


if __name__ == "__main__":
    main()
