#!/usr/bin/env python3
"""
Upgrades scripts/build_100page_visual_notebook_sop.py so that:
- Every single page (Pages 1..100) fills 100% of Box 4 (all rows down to the bottom border of Box 4)
  and 100% of Box 5 (all rows down to the bottom border of Box 5) with ZERO empty white space and ZERO right-edge clipping!
"""

from pathlib import Path

REPO_ROOT = Path("/Users/huynguyen/Developer/portfolio/motion-estimator-asic-lab-notebook-2026")
TARGET_SCRIPT = REPO_ROOT / "scripts" / "build_100page_visual_notebook_sop.py"

# Read the original curriculum portion (up to "def render_100page_pdf_and_md():" or "# ====")
raw_text = TARGET_SCRIPT.read_text(encoding="utf-8")
split_key = "# ==============================================================================\n# ENHANCED FULL-PAGE DENSE RENDERING ENGINE"
if split_key in raw_text:
    prefix = raw_text.split(split_key)[0]
else:
    prefix = raw_text.split("def render_100page_pdf_and_md():")[0]

addition = r'''# ==============================================================================
# ENHANCED FULL-PAGE DENSE RENDERING ENGINE (ZERO WASTED WHITE SPACE)
# Includes:
# - High-Contrast Terminal Execution Badges: [MACBOOK], [XQUARTZ], [926784856@mahmoodi], [OUTPUT]
# - Full 100%-Height Line-by-Line Commented Code & Script Walkthroughs per page (Zero Empty Space)
# - Section 5: Self-Healing Verification & Fallback Recovery Matrix (Plan A / Plan B / Plan C)
# - Real Pre-Given Server Script Pulling & Customization Instructions
# ==============================================================================

BADGE_MAC_BG = colors.HexColor("#1E3A8A")
BADGE_MAC_ROW = colors.HexColor("#DBEAFE")
BADGE_XQ_BG = colors.HexColor("#0F766E")
BADGE_XQ_ROW = colors.HexColor("#CCFBF1")
BADGE_SFSU_BG = colors.HexColor("#B45309")
BADGE_SFSU_ROW = colors.HexColor("#FEF3C7")
BADGE_OUT_BG = colors.HexColor("#15803D")
BADGE_OUT_ROW = colors.HexColor("#DCFCE7")
BOX_FALLBACK_BG = colors.HexColor("#FFFBEB")
INK_AMBER = colors.HexColor("#92400E")


def clean_glyphs(text):
    return str(text).replace("★", "[!]").replace("—", " - ").replace("–", "-")


def get_page_specific_eda_script_lines(pnum):
    """Returns real, line-by-line commented Synopsys TCL / Makefile / SDC / Shell commands for Pages 45..64."""
    tcl_dir = REPO_ROOT / "scripts" / "synopsys_tcl"

    def read_tcl_with_comments(fname, start=0, count=22, header_comment=""):
        p = tcl_dir / fname
        lines = []
        if header_comment:
            lines.append(header_comment)
        if p.exists():
            raw = [ln.rstrip() for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]
            subset = raw[start:start + count]
            for i, ln in enumerate(subset):
                lines.append(f"{start + i + 1:02d}: {ln}")
        return lines

    mapping = {
        45: [
            "TERM_SFSU: [926784856@mahmoodi ~]$ cp -r ~/ENGR852_Project/16_v3b_final_asic_fc/scripts ~/me_asic_new_v1/",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cd ~/me_asic_new_v1 && tcsh",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ source ./scripts/synopsys_setup.tcl",
            "# --- Pre-Given Course Makefile (Makefile.starter) + 520 MHz VCS Compilation ---",
            *read_tcl_with_comments("Makefile.starter", 0, 16),
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ vcs -full64 -sverilog -debug_access+all -kdb \\",
            "TERM_SFSU:   rtl/16bit/top.v tb/16bit/top_tb_direct.v -o simv_direct -l logs/vcs_direct.log",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ./simv_direct -l logs/simv_direct.log",
            "OUT_OK:    BestDist = 0000 (hex) = 0 (dec) | motionX = f8 (-8) | motionY = 07 (+7) [PASS]",
        ],
        46: [
            "TERM_XQ:   [student@MacBook ~ %] open -a XQuartz && echo $DISPLAY",
            "OUT_OK:    /private/tmp/com.apple.launchd.xxxx/org.xquartz:0  (Local X11 Server Active)",
            "TERM_XQ:   [student@MacBook ~ %] ssh -Y -o ForwardX11Trusted=yes 926784856@mahmoodi.rcc.at.sfsu.edu",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cd ~/me_asic_new_v1 && tcsh",
            "# --- Inside scripts/synopsys_setup.tcl (Pre-Given Server Setup Script) ---",
            *read_tcl_with_comments("synopsys_setup.tcl", 0, 14),
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ source ./scripts/synopsys_setup.tcl",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ verdi -ssf waves_16bit_direct.fsdb &",
            "OUT_OK:    Verdi GUI & nWave window pop up on your MacBook screen via XQuartz!",
        ],
        47: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ verdi -ssf waves_16bit_tb.fsdb &",
            "# --- Step-by-Step Verdi nWave Signal Selection & Hex Radix Formatting ---",
            "01: # In nWave Menu: Click 'Signal' -> 'Get Signals...' (or press keyboard shortcut 'g')",
            "02: # Left Pane (Signal Hierarchy): Click 'top_tb' -> Click 'u1 (top)' -> Click 'u1 (Control)'",
            "03: # Add Top Ports:   clock, start, BestDist[15:0], motionX[7:0], motionY[7:0]",
            "04: # Add Memory Bus:  AddressR[7:0], R[7:0], AddressS1[9:0], S1[7:0], AddressS2[9:0], S2[7:0]",
            "05: # Add Control Bus: u1.u1.count[12:0], u1.u1.completed, u1.CompStart, u1.PEready[15:0]",
            "06: # Add PE Array:    u1.u3.PE0.Accumulate[15:0] ... u1.u18.PE15.Accumulate[15:0]",
            "07: # Add Comparator:  u1.u2.newDist[15:0], u1.u2.newBest, u1.u2.vectorX[3:0], u1.u2.vectorY[3:0]",
            "08: # Click 'Append' -> Click 'OK' (All 22 signals appear in the black nWave canvas)",
            "09: # Press Ctrl+A (Select All Signals) -> Right-Click -> 'Radix' -> 'Hexadecimal'",
            "10: # Right-Click 'Signal' column header -> 'Signal Display Options' -> Enable 'Full Hierarchy Name'",
            "TERM_SFSU: # Save signal list so you never have to re-click signals manually:",
            "11: # In nWave Menu: Click 'File' -> 'Save Signal...' -> Save as 'scripts/me_signals.rc'",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ verdi -ssf waves_16bit_tb.fsdb -sswr scripts/me_signals.rc &",
            "OUT_OK:    All 22 hierarchical signals load automatically in Hexadecimal radix!",
        ],
        48: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ verdi -ssf waves_16bit_direct.fsdb -sswr scripts/me_signals.rc &",
            "# --- Step-by-Step Verdi nWave Zooming & Time Cursor Measurement ---",
            "01: # Keyboard Shortcut 'f' (Zoom Full): Shows full simulation 0.00 ns .. 7,905.45 ns",
            "02: # Notice at full 7,905 ns scale, 4,111 clock cycles are compressed into solid colored bands.",
            "03: # Keyboard Shortcut 'z' (Zoom In) or Left-Click-Drag across 480 ns .. 530 ns:",
            "04: #   -> Reveals Row-1 completion window (count = 13'h00F9 .. 13'h0110) with readable hex boxes!",
            "05: # Left-Click at t = 494.21 ns (count = 13'h0100): Yellow Primary Cursor (Marker A) snaps to edge",
            "06: # Middle-Click at t = 523.06 ns (count = 13'h010F): White Delta Cursor (Marker B) snaps to edge",
            "07: # Top Ruler displays: Cursor = 494.211 ns | Marker = 523.056 ns | Delta = 28.845 ns (15 cycles)",
            "08: # Jump to Terminal Cycle 4111: Click 'Search' -> 'By Value' -> Signal: count -> Value: 13'h100F",
            "09: # Press 'z' 3 times around t = 7,905.45 ns to inspect final BestDist, motionX, motionY, completed=1",
            "TERM_MAC:  [student@MacBook ~ %] # Press Cmd+Shift+4 on MacBook to capture crisp PNG of nWave window!",
            "OUT_OK:    Full-screen waveform PNG captured with top ruler, scrollbar, and hex register transitions!",
        ],
        49: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ vcs -full64 -sverilog -debug_access+all rtl/8bit/top.v tb/8bit/top_tb.v -o simv_8b",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ./simv_8b -l logs/simv_8bit_row1.log",
            "# --- Waveform Verification: V9_fig7_orig8bit_row1_nWave.png (count = 0x00F9..0x0110) ---",
            "01: # At count = 12'h00FF (t = 492.29 ns): PE0 finishes accumulating 256th pixel of candidate (0,0)",
            "02: # Because true SAD D(0,0) > 255, 8-bit PE0 saturates: PE0.Accumulate[7:0] clamps at 8'hFF (255)!",
            "03: # At count = 12'h0100 (t = 494.21 ns): CompStart asserts (0 -> 1) and PEready[0] asserts (16'h0001)",
            "04: # Comparator tests strict inequality: if (newDist < BestDist) -> (8'hFF < 8'hFF) == FALSE (0)!",
            "05: # Consequently, u1.u2.newBest remains 1'b0 across all 16 PEs in Row 1 (count = 0x0100..0x010F)!",
            "OUT_OK:    Verified 8-bit saturation & strict '<' tie behavior in Verdi nWave at 520 MHz!",
        ],
        50: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -E 'BestDist|motionX|motionY' logs/simv_8bit_row1.log",
            "# --- Waveform Verification: V9_fig8_orig8bit_complete_nWave.png (count = 0x100F, t = 7,905.45 ns) ---",
            "01: # In 8-bit random+1 offset testbench (top_tb.v), candidate (-5,+7) has true SAD = 256 (9'h100).",
            "02: # In 8-bit PE, 256 triggers Carry == 1 -> clamps to 8'hFF, tying earlier saturated blocks!",
            "03: # In 8-bit max-contrast testbench (all pixels |0x00 - 0xFF| = 255), all 256 blocks saturate to 8'hFF.",
            "04: # At count = 12'h100F (t = 7,905.45 ns): BestDist stays 8'hFF and motionX/Y never update (or tie)!",
            "05: # Furthermore, without the 13-bit counter fix, 12-bit count[11:0] wraps to 12'h000 at cycle 4096!",
            "OUT_OK:    Proved why 16-bit non-saturating datapath + 13-bit terminal hold is architecturally required!",
        ],
        51: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/top_tb_direct.v -o simv_16b_0000",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ./simv_16b_0000 -l logs/simv_16b_0000.log",
            "# --- Waveform Verification: V9_fig10_16bit_perfect_match_0000_nWave.png ---",
            "01: # At count < 256: CompStart == 0 initializes BestDist[15:0] <= 16'hFFFF (65,535).",
            "02: # At count = 13'h0100 (PE0 ready): D(0,0) = 16'h0909 < 16'hFFFF -> newBest=1, BestDist <= 16'h0909.",
            "03: # At count = 13'h0101 (PE1 ready): D(1,0) = 16'h07C7 < 16'h0909 -> newBest=1, BestDist <= 16'h07C7.",
            "04: # At count = 13'h010F (PE15 ready): Exact match D(15,0) = 16'h0000 < BestDist -> newBest=1!",
            "05: # Comparator latches BestDist <= 16'h0000, motionX <= 8'h07 (+7), motionY <= 8'hF8 (-8)!",
            "OUT_OK:    BestDist = 16'h0000 verified in both VCS log and Verdi nWave (answers teammate Q3)!",
        ],
        52: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/top_tb_16bit.v -o simv_16b_ff00",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ./simv_16b_ff00 -l logs/simv_16b_ff00.log",
            "# --- Waveform Verification: V9_fig9_16bit_saturation_row1_nWave.png ---",
            "01: # Stimulus: All reference pixels R = 8'h00, all search pixels S = 8'hFF -> |R - S| = 255 per cycle.",
            "02: # Across 256 pixels: PE0.Accumulate[15:0] counts 0x00FF, 0x01FE, 0x02FD ... up to 16'hFF00 (65,280).",
            "03: # At count = 13'h0100 (t = 494.21 ns): PEready[0] = 1, newDist = 16'hFF00, BestDist = 16'hFFFF.",
            "04: # Because 16'hFF00 (65,280) < 16'hFFFF (65,535) is TRUE, newBest = 1 asserts on the first block!",
            "05: # Comparator latches BestDist <= 16'hFF00, motionX <= 8'hF8 (-8), motionY <= 8'hF8 (-8)!",
            "OUT_OK:    BestDist = 16'hFF00 verified for max-distortion stress test (answers teammate Q1 & Q2)!",
        ],
        53: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/common/sdc/top.sdc ./common/sdc/top.sdc",
            "# --- Complete Line-by-Line Commented 520 MHz SDC File (constraints/top_520mhz.sdc) ---",
            "01: # Course Project Specification: Clock = 520 MHz (1.923 ns), I/O Delay = 0.5 ns, Uncertainty = 0.2 ns",
            "02: create_clock -name clock -period 1.923 [get_ports clock]   ;# 1000 / 1.923 = 520.02 MHz",
            "03: set_clock_uncertainty 0.2 [get_clocks clock]               ;# 200 ps jitter + skew margin",
            "04: # Constrain all 25 data/control input ports (exclude clock port itself!):",
            "05: set_input_delay 0.5 -clock clock [get_ports {start R* S1* S2*}]",
            "06: # Constrain all 60 output ports (BestDist[15:0], motionX[7:0], motionY[7:0], AddressR/S1/S2):",
            "07: set_output_delay 0.5 -clock clock [all_outputs]",
            "08: # Note: Reference (ROM_R) and Search (ROM_S) memories are EXCLUDED from top.v synthesis!",
            "09: # Available internal register-to-register setup budget = 1.923 - 0.200 = 1.723 ns",
            "10: # Available I/O path budget = 1.923 - 0.500 - 0.200 = 1.223 ns",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ cat common/sdc/top.sdc",
            "OUT_OK:    SDC verified: period=1.923, uncertainty=0.2, input_delay=0.5, output_delay=0.5",
        ],
        54: [
            "TERM_SFSU: [926784856@mahmoodi ~]$ cp -r ~/ENGR852_Project/16_v3b_final_asic_fc/{setup,common,scripts} ~/me_asic_new_v1/",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cp rtl/16bit/top.v ~/me_asic_new_v1/common/rtl/verilog/top.v",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cp constraints/top_520mhz.sdc ~/me_asic_new_v1/common/sdc/top.sdc",
            "# --- Inspecting Pre-Given Course Setup Files (setup/fc_common_setup.tcl & setup/mcmm_setup.tcl) ---",
            "01: set DESIGN_NAME       \"top\"                              ;# Must match module top in top.v",
            "02: set DESIGN_LIBRARY    \"top.dlib\"                         ;# NDM container in ./results/top.dlib",
            "03: set VERILOG_PATH      \"./common/rtl/verilog\"             ;# Reads ./common/rtl/verilog/top.v",
            "04: set SDC_FILE          \"./common/sdc/top.sdc\"             ;# Reads 520 MHz (1.923 ns) constraints",
            "05: set DB_FF             \"./common/liberty/saed14rvt_ff0p88v125c.db\" ;# FAST corner (0.88V, 125C)",
            "06: set DB_TT             \"./common/liberty/saed14rvt_tt0p8v25c.db\"   ;# TYPICAL corner (0.80V, 25C)",
            "07: set DB_SS             \"./common/liberty/saed14rvt_ss0p72vm40c.db\" ;# SLOW corner (0.72V, -40C)",
            "08: set REFERENCE_LIBRARY \"./common/ndm/saed14rvt_frame_timing.ndm\"   ;# 14nm FinFET RVT NDM cells",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ls -la common/liberty/ common/ndm/",
            "OUT_OK:    All 3 Liberty .db corners (FF, TT, SS) and SAED14nm NDM reference library verified!",
        ],
        55: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/initial_syn.tcl' | tee logs/01_initial_syn.log",
            "# --- Actual Pre-Given Script 1: scripts/initial_syn.tcl (Lines 1..55) ---",
            *read_tcl_with_comments("initial_syn.tcl", 0, 22),
            "OUT_OK:    Created ./results/top.dlib (block: top/inital_syn) and ./results/top_initial_syn.v!",
        ],
        56: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/compile_flow.tcl' | tee logs/02_compile.log",
            "# --- Actual Pre-Given Script 2: scripts/compile_flow.tcl (MCMM + compile_fusion) ---",
            *read_tcl_with_comments("compile_flow.tcl", 0, 22),
            "OUT_OK:    Completed compile_fusion (initial_map -> logic_opto -> final_opto) with 0 memory macros!",
        ],
        57: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ sed -i 's/-core_utilization 0.6/-core_utilization 0.35/g' scripts/manual_floorplan_creation.tcl",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/manual_floorplan_creation.tcl' | tee logs/03_floorplan.log",
            "# --- Actual Pre-Given Script 3: scripts/manual_floorplan_creation.tcl ---",
            *read_tcl_with_comments("manual_floorplan_creation.tcl", 0, 22),
            "OUT_OK:    Floorplan initialized (2:1 aspect ratio, M3/M4 I/O pins, M5 clock pin, tap/boundary cells)!",
        ],
        58: [
            "# --- Actual Pre-Given Script 4: scripts/create_pg_network.tcl (Called by manual_floorplan_creation.tcl) ---",
            *read_tcl_with_comments("create_pg_network.tcl", 0, 22),
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -E 'check_pg_connectivity|check_pg_drc|Error' logs/03_floorplan.log",
            "OUT_OK:    M1 stdcell rails + M5/M6/M7 PG mesh + M6/M7 core rings compiled with 0 PG DRC errors!",
        ],
        59: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/place_opt.tcl' | tee logs/04_place_opt.log",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/clock_opt.tcl' | tee logs/05_clock_opt.log",
            "# --- Actual Pre-Given Script 5 & 6: scripts/clock_opt.tcl (2x Width/Spacing NDR + VSS Shielding) ---",
            *read_tcl_with_comments("clock_opt.tcl", 8, 22),
            "OUT_OK:    Clock tree synthesized across 449 DFFs with target_skew 0.1 ns and M2..M5 VSS shielding!",
        ],
        60: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/route_opt.tcl' | tee logs/06_route_opt.log",
            "# --- Actual Pre-Given Script 7: scripts/route_opt.tcl (Global, Track, Detail Route + Redundant Vias) ---",
            *read_tcl_with_comments("route_opt.tcl", 8, 22),
            "OUT_OK:    Detail routing + route_opt + add_redundant_vias + check_routes + check_lvs completed cleanly!",
        ],
        61: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f ./scripts/signoff.tcl' | tee logs/07_signoff.log",
            "# --- Actual Pre-Given Script 8 & 9: scripts/signoff.tcl + scripts/write_data.tcl ---",
            *read_tcl_with_comments("signoff.tcl", 6, 15),
            *read_tcl_with_comments("write_data.tcl", 0, 10),
            "OUT_OK:    Exported results/top.v, results/top.sdc, results/top.spef.{min,nom,max}, and results/top.gds!",
        ],
        62: [
            "TERM_XQ:   [student@MacBook ~ %] ssh -Y 926784856@mahmoodi.rcc.at.sfsu.edu",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -gui'",
            "# --- Inside Fusion Compiler GUI Command Console (Inspecting Routed 14nm Layout): ---",
            "01: open_lib ./results/top.dlib",
            "02: open_block top/signoff_v5",
            "03: # In left 'View Settings' panel -> Check Metal Layers M1, M2, M3, M4, M5, M6, M7",
            "04: # Press 'f' to Fit Full Die Area (125.07 um x 62.80 um) in the layout canvas",
            "05: gui_write_window_image -format png -file ./results/v9_signoff_clean_layout.png",
            "OUT_OK:    Saved high-resolution 14nm routed chip layout image ./results/v9_signoff_clean_layout.png!",
        ],
        63: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ cat signoff_drc_run/top.LAYOUT_ERRORS",
            "# --- Verifying Standalone Synopsys IC Validator (ICV) DRC & LVS Sign-Off Reports ---",
            "01: # In scripts/signoff.tcl, Fusion Compiler invokes ICV with SAED14nm 1p9m DRC & Metal Fill runsets:",
            "02: set_app_options -name signoff.check_drc.runset -value ${DRC_RUNSET_FILE}",
            "03: signoff_check_drc    ;# Runs ICV across all 242 SAED14nm FinFET design rules",
            "04: signoff_fix_drc      ;# Automatically repairs any spacing/width/via enclosure issues",
            "05: signoff_check_drc    ;# Re-verifies 0 remaining DRC violations",
            "06: # Run preflight placement audit to verify 0 unplaced cells before/after GDS export:",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -E 'LAYOUT ERRORS RESULTS|Total Error' signoff_drc_run/top.LAYOUT_ERRORS",
            "OUT_OK:    LAYOUT ERRORS RESULTS : CLEAN (0 / 242 rule violations; UNPLACED_FLAT_CELL_COUNT = 0)!",
        ],
        64: [
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; pt_shell -f ./scripts/v5_prime_time_extracted_corners.tcl' | tee logs/08_primetime.log",
            "# --- Actual 3-Corner PrimeTime Script: scripts/v5_prime_time_extracted_corners.tcl ---",
            *read_tcl_with_comments("v5_prime_time_extracted_corners.tcl", 0, 21),
            "OUT_OK:    FAST: Setup +0.71ns / Hold 0.00ns | TYP: +0.54ns / +0.04ns | SLOW: +0.22ns / +0.14ns (0 violations)!",
        ],
    }
    return mapping.get(pnum, [])


def get_page_specific_part7_lines(pnum):
    """Returns rich, page-specific command/script blocks for Pages 89..100."""
    mapping = {
        89: [
            "TERM_MAC:  [student@MacBook ~ %] cd ~/Developer/engr852-14nm-motion-estimator",
            "TERM_MAC:  [student@MacBook ~ %] source .venv/bin/activate",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/package_v9_submission.py",
            "# --- Inside scripts/package_v9_submission.py (Automated Deliverable Bundler) ---",
            "01: # Collects all required rubric folders into a single clean submission archive:",
            "02: #   01_RTL_and_Testbenches/ -> rtl/8bit/top.v, rtl/16bit/top.v, top_tb.v, top_tb_direct.v, ref.txt, search.txt",
            "03: #   02_Simulation_Logs_and_Waveforms/ -> 7 VCS logs + 4 zoomed Verdi nWave PNGs (0000, 0100, FF00, 8-bit)",
            "04: #   03_Synthesis_and_Constraints/ -> top_520mhz.sdc, top.v (gate-level netlist), area/power/timing .rpt",
            "05: #   04_Physical_Design_GDS_DRC_SPEF/ -> v9_signoff_clean_layout.png, top.LAYOUT_ERRORS, 3-corner .spef",
            "06: #   05_PrimeTime_3Corner_PostLayout_STA/ -> FAST, TYPICAL, SLOW setup & hold timing reports",
            "07: #   06_Engineering_Report_and_Slides/ -> Engineering Report PDF + 19-Slide Presentation (.pptx & .pdf)",
            "TERM_MAC:  [student@MacBook ~ %] unzip -l deliverables/ENGR852_Motion_Estimator_Final_Master_Package_V9.zip | head -n 20",
            "OUT_OK:    Created clean, rubric-complete submission .zip with 0 temporary .daidir or lock files!",
        ],
        90: [
            "# --- Customizing Project Naming, Slide Palette, & Report Headers on Your New Laptop ---",
            "TERM_MAC:  [student@MacBook ~ %] export MY_NEW_REPO=\"engr852-520mhz-motion-estimator-asic\"",
            "TERM_MAC:  [student@MacBook ~ %] mkdir -p ~/Developer/$MY_NEW_REPO && cd ~/Developer/$MY_NEW_REPO",
            "01: # Variation 1 (Server Folder): Use ~/me_asic_new_v1 on 926784856@mahmoodi.rcc.at.sfsu.edu",
            "02: # Variation 2 (Testbench Shift): Edit TARGET_DX / TARGET_DY in tb/top_tb.v (e.g. (+3,-4) -> X=03, Y=FC)",
            "03: # Variation 3 (Slide Theme): In scripts/build_v9_final_slides.py, change RGBColor(15, 23, 42) to:",
            "04: #     NAVY_THEME  = RGBColor(12, 35, 64)   # Classic Engineering Navy",
            "05: #     SFSU_PURPLE = RGBColor(35, 17, 97)   # SFSU Gator Purple & Gold",
            "06: #     SLATE_TEAL  = RGBColor(15, 118, 110) # Modern Silicon Teal",
            "07: # Variation 4 (Keep Identical): NEVER rename 'module top' or its 11 ports (clock, start, BestDist, etc.)!",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/build_v9_final_slides.py && python3 scripts/build_v9_final_engineering_report.py",
            "OUT_OK:    Regenerated customized presentation deck (.pptx) and engineering report (.pdf) in 3 seconds!",
        ],
        91: [
            "# --- Git Dataflow Commands: Working Tree -> Staging Index -> Local Repo -> GitHub Remote ---",
            "TERM_MAC:  [student@MacBook ~ %] cd ~/Developer/engr852-14nm-motion-estimator",
            "TERM_MAC:  [student@MacBook ~ %] git init -b main",
            "OUT_OK:    Initialized empty Git repository in .../engr852-14nm-motion-estimator/.git/",
            "TERM_MAC:  [student@MacBook ~ %] git config user.name \"Your Full Name\"",
            "TERM_MAC:  [student@MacBook ~ %] git config user.email \"your_email@sfsu.edu\"",
            "TERM_MAC:  [student@MacBook ~ %] git status -s",
            "01: # '??' means untracked file in Working Tree; 'A ' means staged in Index; 'M ' means modified",
            "02: # Always inspect 'git status' before committing to ensure no >100 MB .fsdb or .ndm files are staged!",
            "TERM_MAC:  [student@MacBook ~ %] git add rtl/ tb/ constraints/ scripts/ verification/ docs/ deliverables/ README.md",
            "TERM_MAC:  [student@MacBook ~ %] git diff --cached --stat",
            "OUT_OK:    All Verilog RTL, testbenches, SDC, TCL scripts, reports, and slides staged cleanly!",
        ],
        92: [
            "# --- Creating a Brand-New GitHub Repository via Browser or GitHub CLI (gh) ---",
            "01: # Option A (Web Browser): Open https://github.com/new on your MacBook Air",
            "02: #   -> Repository name: engr852-520mhz-motion-estimator-asic (or your custom project name)",
            "03: #   -> Description: 520 MHz 16-PE Systolic Motion Estimator ASIC in Synopsys SAED14nm FinFET",
            "04: #   -> Visibility: Public (or Private) -> Leave 'Add a README' UNCHECKED -> Click 'Create repository'",
            "05: # Option B (Command Line via GitHub CLI 'gh' on your MacBook Terminal):",
            "TERM_MAC:  [student@MacBook ~ %] brew install gh && gh auth login",
            "TERM_MAC:  [student@MacBook ~ %] gh repo create engr852-520mhz-motion-estimator-asic --public --source=. --remote=origin",
            "TERM_MAC:  [student@MacBook ~ %] git remote -v",
            "OUT_OK:    origin  git@github.com:<YOUR_USERNAME>/engr852-520mhz-motion-estimator-asic.git (fetch/push)",
        ],
        93: [
            "# --- Configuring GitHub SSH Keys & Critical .gitignore Rules for Synopsys ASIC Projects ---",
            "TERM_MAC:  [student@MacBook ~ %] ssh-keygen -t ed25519 -C \"github-macbook\" -f ~/.ssh/id_ed25519_github -N \"\"",
            "TERM_MAC:  [student@MacBook ~ %] pbcopy < ~/.ssh/id_ed25519_github.pub  # Copies public key to clipboard",
            "01: # Paste key at https://github.com/settings/keys -> Click 'Add SSH key', then test connection:",
            "TERM_MAC:  [student@MacBook ~ %] ssh -T git@github.com",
            "OUT_OK:    Hi <username>! You've successfully authenticated, but GitHub does not provide shell access.",
            "TERM_MAC:  [student@MacBook ~ %] cat << 'EOF' > .gitignore",
            "02: *.fsdb",
            "03: *.vpd",
            "04: *.ndm",
            "05: *.dlib/",
            "06: simv*",
            "07: csrc/",
            "08: *.daidir/",
            "09: verdiLog/",
            "10: .venv/",
            "11: EOF",
            "OUT_OK:    .gitignore created — prevents Synopsys binary databases from exceeding GitHub's 100 MB limit!",
        ],
        94: [
            "# --- Generating a Publication-Grade GitHub README.md With Full Verification Tables ---",
            "TERM_MAC:  [student@MacBook ~ %] head -n 25 README.md",
            "01: # # 520 MHz 16-PE Systolic Motion Estimator ASIC (Synopsys SAED14nm FinFET)",
            "02: # - **Architecture**: 16-PE 1D Systolic Array + 13-Bit Explicit FSM + 16-Bit Non-Saturating SAD",
            "03: # - **Clock Target**: 520.02 MHz (1.923 ns period, 0.5 ns I/O delay, 0.2 ns clock uncertainty)",
            "04: # - **Physical Layout**: 125.07 um x 62.80 um die, 8,230 cells (449 FFs), 0 SRAM/ROM macros",
            "05: # - **DRC / LVS Sign-Off**: 0 / 242 ICV DRC violations (CLEAN), 0 LVS mismatches",
            "06: # - **Post-Layout PrimeTime STA**:",
            "07: #   - FAST (minTLU_125): Setup WNS = +0.71 ns | Hold WNS = 0.00 ns (0 violations)",
            "08: #   - TYPICAL (nomTLU_25): Setup WNS = +0.54 ns | Hold WNS = +0.04 ns (0 violations)",
            "09: #   - SLOW (maxTLU_-40): Setup WNS = +0.22 ns | Hold WNS = +0.14 ns (0 violations)",
            "OUT_OK:    README.md documents architecture, 3 testbench regimes (0000, 0100, FF00), and full sign-off metrics!",
        ],
        95: [
            "# --- Executing the Final Commit, Annotated Release Tag, and Push to GitHub ---",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/v6_stage_gate.py --scope full",
            "OUT_OK:    FINAL_GATE_RESULT: PASS (All 11/11 RTL, Simulation, GDS, DRC, LVS, and 3-Corner STA Gates Verified)",
            "TERM_MAC:  [student@MacBook ~ %] git add -A",
            "TERM_MAC:  [student@MacBook ~ %] git status -s",
            "TERM_MAC:  [student@MacBook ~ %] git commit -m \"Complete 520 MHz SAED14nm Motion Estimator ASIC RTL, P&R & Sign-Off\"",
            "TERM_MAC:  [student@MacBook ~ %] git tag -a v1.0-signoff -m \"Verified 520 MHz SAED14nm Sign-Off Release\"",
            "TERM_MAC:  [student@MacBook ~ %] git push -u origin main --tags",
            "OUT_OK:    Branch 'main' set up to track 'origin/main'; tag 'v1.0-signoff' pushed to GitHub!",
        ],
        96: [
            "# --- Live Diagnostic & Self-Healing Commands for VPN, XQuartz, and SSH Issues ---",
            "TERM_MAC:  [student@MacBook ~ %] # Symptom 1: 'ssh: connect to host mahmoodi.rcc.at.sfsu.edu port 22: Operation timed out'",
            "TERM_MAC:  [student@MacBook ~ %] scutil --dns | grep sfsu.edu && nc -zv mahmoodi.rcc.at.sfsu.edu 22",
            "01: # Fix 1: Click GlobalProtect globe icon in macOS menu bar -> Connect to vpn.sfsu.edu -> Approve Duo push.",
            "TERM_XQ:   [student@MacBook ~ %] # Symptom 2: 'Error: Can't open display:' when running verdi or fc_shell -gui",
            "TERM_XQ:   [student@MacBook ~ %] open -a XQuartz && /opt/X11/bin/xdpyinfo -display :0 | head -n 5",
            "02: # Fix 2: Open XQuartz -> Settings -> Security -> Enable 'Allow connections from network clients' -> Log out/in of macOS!",
            "TERM_SFSU: [926784856@mahmoodi ~]$ # Symptom 3: SSH still asks for password after adding Ed25519 key",
            "TERM_SFSU: [926784856@mahmoodi ~]$ chmod go-w ~ && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys",
            "OUT_OK:    All VPN, XQuartz DISPLAY socket, and SSH key permission issues resolved!",
        ],
        97: [
            "# --- Live Diagnostic & Self-Healing Commands for Synopsys VCS & Verdi Waveform Issues ---",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ # Symptom 1: 'vcs: command not found' or 'verdi: command not found'",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; which vcs verdi'",
            "01: # Symptom 2: Clock frequency in waveform is 500 MHz (2.0 ns) instead of 520 MHz (1.923 ns):",
            "02: # Fix 2: Check top of testbench! Must be `timescale 1ns/10ps (or 1ns/100fs), NOT `timescale 1ns/1ns!",
            "03: # Symptom 3: Verdi says 'Cannot open FSDB file waves.fsdb':",
            "04: # Fix 3: Ensure testbench initial block calls $fsdbDumpfile(\"waves.fsdb\"); $fsdbDumpvars(0, top_tb);",
            "05: #        and compile with vcs -full64 -sverilog -debug_access+all -kdb!",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ls -lh *.fsdb",
            "OUT_OK:    waves.fsdb generated cleanly with full hierarchical signal visibility!",
        ],
        98: [
            "# --- Live Diagnostic & Self-Healing Commands for Fusion Compiler, ICV DRC, & PrimeTime STA ---",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ # Symptom 1: 'Error: Required design library results/top.dlib is locked'",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ rm -f results/top.dlib/**/lock* && ps -u $USER | grep fc_shell",
            "01: # Symptom 2: Pre-given sta_post_layout.tcl fails with 'Cannot find file i2c_master_top.v':",
            "02: # Fix 2: The course template sta_post_layout.tcl had 'i2c_master_top' from Lab 4! Replace with 'top':",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ sed -i 's/i2c_master_top/top/g' scripts/sta_post_layout.tcl",
            "03: # Symptom 3: High routing congestion or DRC errors during route_opt:",
            "04: # Fix 3: Lower floorplan utilization from 0.60 to 0.35..0.52 in scripts/manual_floorplan_creation.tcl!",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; fc_shell -no_log -f scripts/v6_gds_preflight.tcl'",
            "OUT_OK:    UNPLACED_FLAT_CELL_COUNT=0 | PLACEMENT_PREFLIGHT_PASSED!",
        ],
        99: [
            "# --- Master Start-to-Finish Command Cheat Sheet (New MacBook + XQuartz + mahmoodi + GitHub) ---",
            "TERM_XQ:   [student@MacBook ~ %] open -a XQuartz && ssh -Y 926784856@mahmoodi.rcc.at.sfsu.edu",
            "TERM_SFSU: [926784856@mahmoodi ~]$ mkdir -p ~/me_asic_new_v1 && cd ~/me_asic_new_v1",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ cp -r ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/{setup,common,scripts} .",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ source ./scripts/synopsys_setup.tcl",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ vcs -full64 -sverilog -debug_access+all common/rtl/verilog/top.v tb/top_tb_direct.v -o simv && ./simv",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ foreach s (initial_syn compile_flow manual_floorplan_creation place_opt clock_opt route_opt signoff)",
            "TERM_SFSU:   fc_shell -no_log -f ./scripts/${s}.tcl | tee logs/${s}.log",
            "TERM_SFSU: end",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ pt_shell -f ./scripts/v5_prime_time_extracted_corners.tcl | tee logs/pt_3corner.log",
            "OUT_OK:    Complete RTL-to-GDSII + 3-Corner PrimeTime Sign-Off executed from scratch in ~/me_asic_new_v1!",
        ],
        100: [
            "# --- Final 11-Gate Self-Checking Verification Harness Execution & Rubric Sign-Off ---",
            "TERM_MAC:  [student@MacBook ~ %] cd ~/Developer/engr852-14nm-motion-estimator && source .venv/bin/activate",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/v6_stage_gate.py --scope full",
            "OUT_OK:    [PASS] G1: 8-Bit & 16-Bit RTL Synthesizable (0 SRAM/ROM Macros Inside top.v)",
            "OUT_OK:    [PASS] G2: 520 MHz (1.923 ns) VCS Regression (7/7 Self-Checking Testbenches PASS)",
            "OUT_OK:    [PASS] G3: Verdi nWave Waveforms Captured (0000 Exact, 0100 +1 Offset, FF00 Max Contrast)",
            "OUT_OK:    [PASS] G4: Synopsys Fusion Compiler 14nm Routed Layout (125.07 x 62.80 um, 8,230 Cells)",
            "OUT_OK:    [PASS] G5: Merged GDSII Export Verified (results/top.gds, 0 Unplaced Cells / 0 GDS-110)",
            "OUT_OK:    [PASS] G6: Standalone ICV DRC Clean (0 / 242 Violations) & LVS Clean (0 Errors)",
            "OUT_OK:    [PASS] G7: 3-Corner PrimeTime Post-Layout STA (Setup & Hold >= 0.00 ns Across FF/TT/SS)",
            "OUT_OK:    FINAL_GATE_RESULT: PASS — 100% Ready for 90-100% Course Project Grading & Live Demo!",
        ],
    }
    return mapping.get(pnum, [])


def enrich_code_lines_to_fill_box(pnum, raw_code_lines, max_lines=26):
    """Guarantees Section 4 has exactly `max_lines` rich, terminal-tagged lines so Box 4 is 100% full on every page."""
    if 45 <= pnum <= 64:
        custom = get_page_specific_eda_script_lines(pnum)
        if custom:
            raw_code_lines = custom
    elif 89 <= pnum <= 100:
        custom = get_page_specific_part7_lines(pnum)
        if custom:
            raw_code_lines = custom

    enriched = []
    for ln in raw_code_lines:
        s = str(ln)
        if any(s.startswith(p) for p in ("TERM_MAC:", "TERM_XQ:", "TERM_SFSU:", "OUT_OK:")):
            enriched.append(s)
        elif s.startswith("ssh ") or s.startswith("scp ") or s.startswith("rsync ") or s.startswith("xcode-select") or s.startswith("python3 ") or s.startswith("pip ") or s.startswith("git ") or s.startswith("scutil ") or s.startswith("nc "):
            enriched.append("TERM_MAC:  [student@MacBook ~ %] " + s)
        elif s.startswith("open -a XQuartz") or s.startswith("echo $DISPLAY") or s.startswith("xclock"):
            enriched.append("TERM_XQ:   [student@MacBook ~ %] " + s)
        elif s.startswith("source /apps") or s.startswith("which vcs") or s.startswith("vcs ") or s.startswith("fc_shell") or s.startswith("icv ") or s.startswith("pt_shell") or s.startswith("pwd") or s.startswith("ls -la /apps"):
            enriched.append("TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ " + s)
        else:
            enriched.append(s)

    # Rich 25-line bank per Part so every single page fills 100% of Box 4 with zero empty white space
    if pnum <= 12:
        extra = [
            "# --- Step-by-Step Server Workspace Clone & Pre-Given Course Script Setup on mahmoodi ---",
            "TERM_XQ:   [student@MacBook ~ %] open -a XQuartz && /opt/X11/bin/xdpyinfo -display :0 >/dev/null && echo LOCAL_XQUARTZ_OK",
            "OUT_OK:    LOCAL_XQUARTZ_OK (X11 socket /private/tmp/com.apple.launchd.../org.xquartz:0 is active)",
            "TERM_XQ:   [student@MacBook ~ %] ssh -Y -o ForwardX11=yes -o ForwardX11Trusted=yes 926784856@mahmoodi.rcc.at.sfsu.edu",
            "TERM_SFSU: [926784856@mahmoodi ~]$ mkdir -p ~/me_asic_new_v1/{rtl/8bit,rtl/16bit,tb/8bit,tb/16bit,scripts,logs,results,pt_reports}",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cp -r ~/ENGR852_Project/16_v3b_final_asic_fc/{setup,common,scripts} ~/me_asic_new_v1/",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/scripts/v5_prime_time_extracted_corners.tcl ~/me_asic_new_v1/scripts/",
            "TERM_SFSU: [926784856@mahmoodi ~]$ cd ~/me_asic_new_v1 && tcsh",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ source ./scripts/synopsys_setup.tcl",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ echo \"DISPLAY=$DISPLAY\" && which vcs verdi fc_shell icv pt_shell",
            "OUT_OK:    DISPLAY=localhost:10.0 | /packages/synopsys/vcs/W-2024.09-1/bin/vcs (All 5 Synopsys tools ready!)",
            "# --- How scripts/synopsys_setup.tcl Configures Your Synopsys Environment on mahmoodi ---",
            "01: source /packages/synopsys/setup/synthesis.csh       ;# Design Compiler / synthesis libs",
            "02: source /packages/synopsys/setup/vcs_2024.csh        ;# Synopsys VCS W-2024.09-1 simulator",
            "03: source /packages/synopsys/setup/primetime_2022.csh  ;# Synopsys PrimeTime 3-corner sign-off STA",
            "04: source /packages/synopsys/setup/verdi_2024.csh      ;# Synopsys Verdi + nWave waveform GUI",
            "05: source /packages/synopsys/setup/fc.csh              ;# Synopsys Fusion Compiler 14nm P&R",
            "06: source /packages/synopsys/setup/ic_validator_2024.csh ;# Synopsys IC Validator DRC & LVS",
            "TERM_MAC:  [student@MacBook ~ %] rsync -avz 926784856@mahmoodi.rcc.at.sfsu.edu:~/me_asic_new_v1/scripts/ ./scripts/synopsys_tcl/",
            "OUT_OK:    Synced all pre-given course TCL scripts to local MacBook for inspection & Git tracking!",
        ]
    elif pnum <= 24:
        extra = [
            "// --- Interactive Hardware Verification of This Architectural Step on mahmoodi ---",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/top_tb_direct.v -o simv_check && ./simv_check'",
            "OUT_OK:    Cycle 256 (0x0100): CompStart=1, PEready=0x0001 | Cycle 4111 (0x100F): completed=1, BestDist=16'h0000",
            "// --- Comparing 8-Bit Baseline (rtl/8bit/top.v) vs. 16-Bit Non-Saturating Upgrade (rtl/16bit/top.v) ---",
            "01: // In 8-bit PE:  {Carry, AccumulateIn} = Accumulate + difference; if (Carry == 1) AccumulateIn = 8'hFF;",
            "02: // In 16-bit PE: AccumulateIn = Accumulate + {8'd0, difference};  // Exact sum up to 256*255 = 65,280 (16'hFF00)",
            "03: // In 8-bit Control:  reg [11:0] count; // Wraps to 0 at cycle 4096 -> resets BestDist during Row 15!",
            "04: // In 16-bit Control: reg [12:0] count; reg completed; // Holds at count == 13'h100F (cycle 4111)!",
            "05: // In 8-bit Comparator:  if (CompStart == 0) BestDist <= 8'hFF;   // Ties when newDist == 8'hFF!",
            "06: // In 16-bit Comparator: if (CompStart == 0) BestDist <= 16'hFFFF; // 16'hFF00 < 16'hFFFF is always TRUE!",
            "// --- Course Project Syllabus Requirements Checklist (Items 1-5) ---",
            "07: // [x] Clock Period = 1.923 ns (520.02 MHz) | Input Delay = 0.5 ns | Output Delay = 0.5 ns | Uncertainty = 0.2 ns",
            "08: // [x] Exclude Reference (RMEM 256x8) and Search (SMEM 1024x8) memories from top.v synthesis!",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -E 'BestDist|motionX|motionY|PASS' logs/*.log | tail -n 4",
            "OUT_OK:    All SAD D(i,j), motion vector (i-8, j-8), and cycle-4111 hold equations verified in VCS!",
        ]
    elif pnum <= 44:
        extra = [
            "// --- Running This Testbench & Inspecting Waveforms on 926784856@mahmoodi.rcc.at.sfsu.edu ---",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; vcs -full64 -sverilog -debug_access+all -kdb rtl/16bit/top.v tb/16bit/top_tb_direct.v -o simv_direct && ./simv_direct -l logs/tb_direct.log'",
            "OUT_OK:    BestDist = 0000 (hex) | motionX = 07 (+7) or f8 (-8) | motionY = f8 (-8) or 07 (+7) [PASS]",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; vcs -full64 -sverilog -debug_access+all -kdb rtl/16bit/top.v tb/16bit/top_tb.v -o simv_tb && ./simv_tb -l logs/tb_offset1.log'",
            "OUT_OK:    Expected X = -5 (FB), Y = 7 (07) | Actual BestDist = 0100 (256), motionX = fb (-5), motionY = 07 (+7) [PASS]",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ tcsh -c 'source ./scripts/synopsys_setup.tcl; vcs -full64 -sverilog -debug_access+all -kdb rtl/16bit/top.v tb/16bit/top_tb_16bit.v -o simv_ff00 && ./simv_ff00 -l logs/tb_ff00.log'",
            "OUT_OK:    Max-Contrast Stress Test: BestDist = ff00 (65,280 < 65,535), motionX = f8 (-8), motionY = f8 (-8) [PASS]",
            "// --- Using the Pre-Given Starter Makefile (Course Project/Motion Estimator RTL and Testbench/Makefile) ---",
            "01: # You can also run using make by passing RTL and TB overrides on the command line:",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ make -f scripts/synopsys_tcl/Makefile.starter RTL=rtl/16bit/top.v TB=tb/16bit/top_tb.v test",
            "OUT_OK:    Makefile compiled and executed simv cleanly with +ntb_random_seed=1!",
        ]
    elif pnum <= 64:
        extra = [
            "# --- Post-Stage Automated Quality & Error Audit on 926784856@mahmoodi.rcc.at.sfsu.edu ---",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -En '^Error:|^Fatal:|PLACE-004|PLACE-006|CMD-081|GDS-110' logs/*.log || echo ZERO_TOOL_ERRORS",
            "OUT_OK:    ZERO_TOOL_ERRORS (No synthesis, placement, CTS, routing, DRC, or PrimeTime errors detected!)",
            "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ ls -lh results/top.v results/top.sdc results/top.gds results/*.spef",
            "OUT_OK:    Verified non-empty gate-level netlist (top.v), 3-corner SPEFs, and merged 14nm GDSII (top.gds)!",
            "# --- Key Physical Design & Sign-Off Metrics Summary (SAED14nm FinFET @ 520 MHz / 1.923 ns) ---",
            "01: # Die Dimensions:    125.07 um x 62.80 um = 7,854.40 um^2 (Core Area = 6,558.96 um^2, Util = 52.08%)",
            "02: # Leaf Cell Count:   8,230 standard cells (449 D flip-flops; 0 SRAM/ROM memory macros synthesized)",
            "03: # Total Cell Area:   3,416.18 um^2 (16-bit full-precision non-saturating datapath; 1,366.85 um^2 in 8-bit)",
            "04: # Total Power (TT):  0.890 mW at 520 MHz (0.889 mW dynamic switching + 0.00089 mW cell leakage)",
            "05: # ICV Sign-Off DRC:  0 / 242 rule violations (signoff_drc_run/top.LAYOUT_ERRORS -> CLEAN)",
            "06: # PrimeTime 3-Corner: FAST (+0.71/0.00 ns), TYPICAL (+0.54/+0.04 ns), SLOW (+0.22/+0.14 ns) -> 0 violations!",
        ]
    else:
        extra = [
            "# --- End-to-End Local Regeneration & 11-Gate Verification Commands on Your MacBook Air ---",
            "TERM_MAC:  [student@MacBook ~ %] source .venv/bin/activate",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/build_v9_final_slides.py",
            "OUT_OK:    Generated deliverables/ENGR852_V9_Complete_19_Slides.pptx & 3-slide contribution deck!",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/build_v9_final_engineering_report.py",
            "OUT_OK:    Generated deliverables/ENGR852_V9_Motion_Estimator_Final_Engineering_Report.pdf!",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/package_v9_submission.py",
            "OUT_OK:    Bundled complete rubric submission zip: ENGR852_Motion_Estimator_Final_Master_Package_V9.zip",
            "TERM_MAC:  [student@MacBook ~ %] python3 scripts/v6_stage_gate.py --scope full",
            "OUT_OK:    FINAL_GATE_RESULT: PASS (All 11/11 verification gates verified with zero missing artifacts!)",
            "TERM_MAC:  [student@MacBook ~ %] git status -s && git log -n 2 --oneline",
            "OUT_OK:    Working tree clean — ready for git push -u origin main to your GitHub repository!",
        ]

    for item in extra:
        if len(enriched) >= max_lines:
            break
        if item not in enriched:
            enriched.append(item)

    # Append additional unique diagnostic & rubric-verification commands if needed so Box 4 is 100% full with zero repetition
    unique_tail_bank = [
        "# --- Additional Live Diagnostic & Rubric Verification Commands for This Step ---",
        "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ sha256sum common/rtl/verilog/top.v common/sdc/top.sdc",
        "OUT_OK:    Verified exact SHA-256 checksums for synthesizable 16-bit top.v and 520 MHz top.sdc!",
        "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -i 'memory' reports/*.rpt || echo ZERO_SYNTHESIZED_MEMORIES",
        "OUT_OK:    ZERO_SYNTHESIZED_MEMORIES (Confirms RMEM & SMEM are excluded from synthesis per rubric!)",
        "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -E 'slack \\(MET\\)|No constrained paths' pt_reports/*.rpt | head -n 3",
        "OUT_OK:    slack (MET) +0.71 ns (FAST) | slack (MET) +0.54 ns (TYPICAL) | slack (MET) +0.22 ns (SLOW)",
        "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ grep -E 'LAYOUT ERRORS RESULTS' signoff_drc_run/top.LAYOUT_ERRORS",
        "OUT_OK:    LAYOUT ERRORS RESULTS : CLEAN (0 / 242 SAED14nm FinFET DRC violations across M1..M9)",
        "TERM_SFSU: [926784856@mahmoodi me_asic_new_v1]$ df -h . && ps -u $USER",
        "OUT_OK:    Server disk quota healthy and zero hung background EDA processes on mahmoodi!",
        "TERM_MAC:  [student@MacBook ~ %] ls -lh deliverables/*.pdf deliverables/*.pptx deliverables/*.zip",
        "OUT_OK:    Verified Engineering Report PDF, 19-Slide Presentation PPTX, and Master Submission ZIP!",
    ]
    for u_item in unique_tail_bank:
        if len(enriched) >= max_lines:
            break
        if u_item not in enriched:
            enriched.append(u_item)

    return enriched[:max_lines]


def get_fallback_recovery_lines(pnum):
    """Returns Section 5: 8 concise lines (<= 95 chars each) of Live Checks & Plan A/B/C Fallbacks."""
    if pnum <= 12:
        return [
            "BLUE:[LIVE CHECK] In XQuartz xterm: echo $DISPLAY && ssh -Y 926784856@mahmoodi.rcc.at.sfsu.edu 'echo $DISPLAY'",
            "RED:[IF XYZ FAILS #1] 'ssh: Operation timed out' or 'Could not resolve hostname mahmoodi.rcc.at.sfsu.edu':",
            "  -> Option A: Click GlobalProtect menu bar icon -> Portal: vpn.sfsu.edu -> Connect -> Approve Duo Push.",
            "  -> Option B: Flush macOS DNS cache: dscacheutil -flushcache && sudo killall -HUP mDNSResponder.",
            "RED:[IF XYZ FAILS #2] Remote $DISPLAY is empty or Verdi/FC GUI prints 'Error: Can't open display':",
            "  -> Option A: XQuartz -> Settings -> Security -> Enable 'Allow connections from network clients' & relogin.",
            "  -> Option B: Run inside XQuartz xterm (Cmd+N): ssh -Y -o ForwardX11Trusted=yes 926784856@mahmoodi...",
            "GREEN:[PULL SERVER SCRIPTS] cp -r ~/ENGR852_Project/16_v3b_final_asic_fc/{setup,common,scripts} ~/me_asic_new_v1/",
        ]
    if pnum <= 24:
        return [
            "BLUE:[LIVE CHECK] Verify top.v ports & widths: grep -En 'module top|output|input|Accumulate|count' rtl/16bit/top.v",
            "RED:[IF XYZ FAILS #1] Synthesis includes SRAM/ROM macros or area exceeds 10,000 um^2:",
            "  -> Option A: Remove any RMEM/SMEM instantiation from top.v! Keep memories ONLY in tb/top_tb.v.",
            "  -> Option B: Verify top.v outputs AddressR[7:0], AddressS1[9:0], AddressS2[9:0] and inputs R, S1, S2.",
            "RED:[IF XYZ FAILS #2] BestDist wipes to FFFF at cycle 4096 or motionX/motionY remain 'xx':",
            "  -> Option A: Widen Control count to reg [12:0] count and latch completed <= 1'b1 at 13'h100F (4111).",
            "  -> Option B: In 16-bit PE, use AccumulateIn = Accumulate + {8'd0, difference} (no 8'hFF clamp!).",
            "GREEN:[PULL STARTER RTL] cp ~/ENGR852_Project/16_v3b_final_asic_fc/common/rtl/verilog/top.v ~/me_asic_new_v1/rtl/",
        ]
    if pnum <= 44:
        return [
            "BLUE:[LIVE CHECK] Run VCS & check outputs: ./simv -l logs/sim.log && grep -E 'BestDist|motion|PASS' logs/sim.log",
            "RED:[IF XYZ FAILS #1] Waveform clock period is 2.0 ns (500 MHz) instead of 1.923 ns (520 MHz):",
            "  -> Option A: Set line 1 of testbench to `timescale 1ns/10ps (or 1ns/100fs), NOT `timescale 1ns/1ns!",
            "  -> Option B: Use 'always #0.9615 clock = ~clock;' so 2 * 0.9615 ns = 1.9230 ns (520.02 MHz).",
            "RED:[IF XYZ FAILS #2] VCS fails with 'Unresolved module RMEM/SMEM' or '$readmemh cannot open ref.txt':",
            "  -> Option A: Copy ref.txt and search.txt into your run directory: cp tb/ref.txt tb/search.txt .",
            "  -> Option B: Run starter Makefile: make -f scripts/synopsys_tcl/Makefile.starter RTL=... TB=... test",
            "GREEN:[3-REGIME CHECK] top_tb_direct.v -> 16'h0000 | top_tb.v -> 16'h0100 (-5,+7) | top_tb_16bit.v -> 16'hFF00!",
        ]
    if pnum <= 64:
        return [
            "BLUE:[LIVE CHECK] Scan EDA logs for hidden errors: grep -En '^Error:|^Fatal:|PLACE-004|GDS-110' logs/*.log",
            "RED:[IF XYZ FAILS #1] 'fc_shell: command not found' or 'pt_shell: command not found' on mahmoodi:",
            "  -> Option A: Run inside tcsh: tcsh -c 'source ./scripts/synopsys_setup.tcl; which fc_shell icv pt_shell'.",
            "  -> Option B: In interactive tcsh, run: source ./scripts/synopsys_setup.tcl before invoking EDA tools.",
            "RED:[IF XYZ FAILS #2] Pre-given sta_post_layout.tcl fails with 'Cannot find i2c_master_top' or link error:",
            "  -> Option A: Fix tutorial name in script: sed -i 's/i2c_master_top/top/g' scripts/sta_post_layout.tcl.",
            "  -> Option B: Prepend '*' to link_path: set link_path [list * ./common/liberty/saed14rvt_ff0p88v125c.db ...].",
            "GREEN:[RESUME SCRIPT] If SSH drops during P&R, resume cleanly: bash scripts/resume_v3_physical_flow.sh cts",
        ]
    return [
        "BLUE:[LIVE CHECK] Run automated 11-gate verification harness: python3 scripts/v6_stage_gate.py --scope full",
        "RED:[IF XYZ FAILS #1] Python fails with 'ModuleNotFoundError: No module named pptx / reportlab / PIL':",
        "  -> Option A: Activate virtualenv first: source .venv/bin/activate && pip install python-pptx reportlab pillow.",
        "  -> Option B: Invoke venv Python directly: ./.venv/bin/python3 scripts/build_v9_final_slides.py.",
        "RED:[IF XYZ FAILS #2] 'git push' rejected due to >100 MB file limit or remote repository mismatch:",
        "  -> Option A: Add *.fsdb *.gds *.dlib/ to .gitignore and run: git rm --cached *.gds *.fsdb.",
        "  -> Option B: Set your new repo URL: git remote set-url origin https://github.com/<USER>/<NEW_REPO>.git.",
        "GREEN:[RUBRIC COMPLETE] All 5 deliverables (RTL, 520MHz Synthesis, TBs, 14nm Layout/DRC/SPEF, 3-Corner PT) PASS!",
    ]


def draw_terminal_code_box(c, x, y_top, width, height, title, lines, font_size=6.65):
    """Draws Section 4 with standout color-coded Terminal Pill Badges ([MACBOOK], [XQUARTZ], [926784856@mahmoodi], [OUTPUT])."""
    y_bot = y_top - height
    c.setFillColor(BOX_CODE_BG)
    c.setStrokeColor(INK_PURPLE)
    c.setLineWidth(1.1)
    c.roundRect(x, y_bot, width, height, 4, fill=1, stroke=1)

    # Header bar
    c.setFillColor(INK_PURPLE)
    c.roundRect(x, y_top - 15, width, 15, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 8.0)
    c.drawString(x + 7, y_top - 11, title)

    # Legend pills on right side of header bar
    legend = [
        ("MACBOOK", BADGE_MAC_BG, width - 235),
        ("XQUARTZ", BADGE_XQ_BG, width - 178),
        ("926784856@mahmoodi", BADGE_SFSU_BG, width - 122),
        ("OUTPUT", BADGE_OUT_BG, width - 42),
    ]
    for lbl, bcol, lx in legend:
        pw = len(lbl) * 3.8 + 6
        c.setFillColor(bcol)
        c.roundRect(x + lx, y_top - 13.5, pw, 11, 2, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 5.8)
        c.drawString(x + lx + 3, y_top - 10.2, lbl)

    leading = font_size + 2.2
    cy = y_top - 24.0
    for raw_line in lines:
        if cy < y_bot + 4:
            break
        line = clean_glyphs(raw_line)
        badge_lbl = None
        badge_bg = None
        row_bg = None
        text_col = INK_BLACK
        is_bold = False

        if line.startswith("TERM_MAC:"):
            badge_lbl = "MACBOOK"
            badge_bg = BADGE_MAC_BG
            row_bg = BADGE_MAC_ROW
            line = line[len("TERM_MAC:"):].strip()
            is_bold = True
        elif line.startswith("TERM_XQ:"):
            badge_lbl = "XQUARTZ"
            badge_bg = BADGE_XQ_BG
            row_bg = BADGE_XQ_ROW
            line = line[len("TERM_XQ:"):].strip()
            is_bold = True
        elif line.startswith("TERM_SFSU:"):
            badge_lbl = "926784856@mahmoodi"
            badge_bg = BADGE_SFSU_BG
            row_bg = BADGE_SFSU_ROW
            line = line[len("TERM_SFSU:"):].strip()
            is_bold = True
        elif line.startswith("OUT_OK:"):
            badge_lbl = "EXPECTED"
            badge_bg = BADGE_OUT_BG
            row_bg = BADGE_OUT_ROW
            line = line[len("OUT_OK:"):].strip()
            text_col = INK_GREEN
            is_bold = True

        if row_bg is not None:
            c.setFillColor(row_bg)
            c.rect(x + 3, cy - 2.0, width - 6, leading - 0.3, fill=1, stroke=0)

        text_x = x + 6
        if badge_lbl is not None:
            bw = len(badge_lbl) * 3.7 + 7
            c.setFillColor(badge_bg)
            c.roundRect(x + 5, cy - 1.5, bw, leading - 1.2, 2, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 5.7)
            c.drawString(x + 8, cy + 0.3, badge_lbl)
            text_x = x + 8 + bw

        if line.lstrip().startswith("#") or line.lstrip().startswith("//"):
            c.setFillColor(INK_BLUE if "---" in line else colors.HexColor("#334155"))
            c.setFont("Courier-Bold" if "---" in line else "Courier", font_size)
        else:
            c.setFillColor(text_col)
            c.setFont("Courier-Bold" if is_bold else "Courier", font_size)

        max_chars = int((x + width - text_x - 6) / (font_size * 0.60))
        c.drawString(text_x, cy, line[:max_chars])
        cy -= leading

    return y_bot


def render_100page_pdf_and_md():
    DELIV_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    SPREADS_DIR.mkdir(parents=True, exist_ok=True)

    pages = generate_remaining_pages(build_100_page_curriculum())
    c = canvas.Canvas(str(OUT_PDF), pagesize=letter)
    w, h = letter
    avail_w = w - 80

    img_map = {
        5: SCREENSHOTS_DIR / "gp_vpn_connecting.png",
        6: SCREENSHOTS_DIR / "gp_vpn_connected_and_xquartz_xterm.png",
        7: SCREENSHOTS_DIR / "ssh_x11_multi_terminal_mahmoodi.png",
        49: SCREENSHOTS_DIR / "V9_fig7_orig8bit_row1_nWave.png",
        50: SCREENSHOTS_DIR / "V9_fig8_orig8bit_complete_nWave.png",
        51: SCREENSHOTS_DIR / "V9_fig10_16bit_perfect_match_0000_nWave.png",
        52: SCREENSHOTS_DIR / "V9_fig9_16bit_saturation_row1_nWave.png",
        62: SCREENSHOTS_DIR / "v9_signoff_clean_layout.png",
    }

    md_lines = [
        "# ENGR 852 Motion Estimator 14nm ASIC (520 MHz) — 100-Page Visual Engineering Notebook Manual",
        "",
        "Complete high-density baby-steps Standard Operating Procedure (SOP) with zero wasted page space, standout",
        "terminal execution badges (`[MACBOOK]`, `[XQUARTZ]`, `[926784856@mahmoodi]`, `[EXPECTED]`), pre-given server",
        "script pulling instructions, line-by-line commented RTL/TB/TCL/Python code, and Plan A/B/C fallback recovery.",
        "",
    ]

    for idx, (title, sub, stages, tbl_rows, trap_lines, code_lines) in enumerate(pages):
        pnum = idx + 1
        part_title = get_part_title(pnum)
        draw_notebook_page_chrome(c, pnum, part_title, title, sub)

        # 1. Section 1: Annotated Block Diagram / GUI Action Flow (Compact 78 pt height)
        y_cursor = h - 84
        y_cursor = draw_schematic_pipeline(
            c, 56, y_cursor, avail_w, 78, stages,
            "1. Visual Annotated Block Diagram & Step-by-Step Execution Pipeline (Blue=Input -> Green=Action -> Red=Verify)"
        )

        # 2. Section 2: Hardware-to-Verilog / Command Verification Table
        y_cursor -= 6
        num_cols = len(tbl_rows[0])
        if num_cols == 3:
            cwidths = [avail_w * 0.25, avail_w * 0.37, avail_w * 0.38]
        elif num_cols == 4:
            cwidths = [avail_w * 0.22, avail_w * 0.26, avail_w * 0.26, avail_w * 0.26]
        elif num_cols == 5:
            cwidths = [avail_w * 0.18, avail_w * 0.20, avail_w * 0.18, avail_w * 0.22, avail_w * 0.22]
        else:
            cwidths = [avail_w / num_cols] * num_cols
        y_cursor = draw_notebook_table(
            c, 56, y_cursor, cwidths, tbl_rows,
            title="2. Hardware-to-Verilog / Command-to-Action Verification Table"
        )

        # 3. Section 3: [!] TRAP / Key Insight Box (with side-by-side embedded screenshot on visual pages!)
        y_cursor -= 6
        if pnum in img_map and img_map[pnum].exists():
            img_p = img_map[pnum]
            sec3_h = 104
            left_w = avail_w * 0.46
            right_w = avail_w * 0.52
            right_x = 56 + avail_w - right_w
            draw_labeled_box(
                c, 56, y_cursor, left_w, sec3_h,
                "3. [!] Visual Guide & Critical Trap Note",
                trap_lines, INK_RED, BOX_RED_BG, mono=False, font_size=6.8
            )
            c.setFillColor(colors.white)
            c.setStrokeColor(INK_BLUE)
            c.setLineWidth(1.1)
            c.roundRect(right_x, y_cursor - sec3_h, right_w, sec3_h, 4, fill=1, stroke=1)
            c.drawImage(str(img_p), right_x + 4, y_cursor - sec3_h + 4, width=right_w - 8, height=sec3_h - 18, preserveAspectRatio=True)
            c.setFillColor(INK_BLUE)
            c.setFont("Helvetica-Bold", 7.2)
            c.drawString(right_x + 6, y_cursor - 11, f"Live Visual Evidence: {img_p.name}")
            y_cursor -= sec3_h
        else:
            box_col = INK_RED if trap_lines[0].startswith("RED:") else (INK_GREEN if trap_lines[0].startswith("GREEN:") else INK_BLUE)
            box_bg = BOX_RED_BG if trap_lines[0].startswith("RED:") else (BOX_GREEN_BG if trap_lines[0].startswith("GREEN:") else BOX_BLUE_BG)
            y_cursor = draw_labeled_box(
                c, 56, y_cursor, avail_w, 56,
                "3. [!] Critical Engineering Note / Beginner Trap & How to Avoid It",
                trap_lines, box_col, box_bg, mono=False, font_size=7.3
            )

        # Reserve exact height at bottom of page (y_bot = 26) for Section 5 (Fallback Troubleshooting Matrix)
        sec5_h = 104
        sec5_top = 26 + sec5_h

        # 4. Section 4: Complete Line-by-Line Commented Code & Standout Terminal Commands
        y_cursor -= 6
        sec4_h = max(130, y_cursor - sec5_top - 6)
        max_code_lines = int((sec4_h - 20) / 8.85)
        rich_code = enrich_code_lines_to_fill_box(pnum, code_lines, max_lines=max_code_lines)
        y_cursor = draw_terminal_code_box(
            c, 56, y_cursor, avail_w, sec4_h,
            "4. Line-by-Line Commented Code & Terminal Commands",
            rich_code, font_size=6.65
        )

        # 5. Section 5: Self-Healing Verification & Fallback Troubleshooting ("If XYZ Fails -> Option A / B")
        fallback_lines = get_fallback_recovery_lines(pnum)
        draw_labeled_box(
            c, 56, sec5_top, avail_w, sec5_h,
            "5. Live Verification Checks, Server Script Pulling & Fallback Troubleshooting (If XYZ Fails -> Option A / B)",
            fallback_lines, INK_AMBER, BOX_FALLBACK_BG, title_color=INK_AMBER, mono=False, font_size=6.7
        )

        c.showPage()

        # Append enriched content to Markdown manual
        md_lines.append(f"## {title}")
        md_lines.append(f"**{sub}**")
        md_lines.append("")
        for tl in trap_lines:
            md_lines.append(f"- {clean_glyphs(tl)}")
        md_lines.append("")
        md_lines.append("### Line-by-Line Commented Code & Terminal Commands")
        md_lines.append("```bash")
        md_lines.extend([clean_glyphs(cl) for cl in rich_code])
        md_lines.append("```")
        md_lines.append("")
        md_lines.append("### Live Verification & Fallback Troubleshooting (If XYZ Fails -> Option A / Option B)")
        for fl in fallback_lines:
            md_lines.append(f"- {clean_glyphs(fl)}")
        md_lines.append("")

    c.save()
    OUT_MD.write_text("\n".join(md_lines), encoding="utf-8")
    print(f"BUILT_DENSE_100PAGE_PDF: {OUT_PDF}")
    print(f"BUILT_DENSE_100PAGE_MD:  {OUT_MD}")
    return pages


def build_3page_visual_spread_images(pages):
    """Renders 6 high-resolution 3-page side-by-side visual engineering notebook spreads (.png)
    with all 5 sections, embedded screenshots, standout terminal badges, and zero empty white space!"""
    SPREADS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        f_hdr = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 13)
        f_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 14)
        f_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 11)
        f_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 11)
        f_reg = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 10)
        f_mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 10)
        f_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 10)
    except Exception:
        f_hdr = f_title = f_sub = f_bold = f_reg = f_mono = f_badge = ImageFont.load_default()

    spread_groups = [
        ("ENGR852_Visual_Spread_01_XQuartz_VPN_SSH_Setup.png", [5, 6, 7]),
        ("ENGR852_Visual_Spread_02_Server_Isolation_and_Tools.png", [8, 9, 10]),
        ("ENGR852_Visual_Spread_03_Chapter10_SAD_and_MotionVectors.png", [13, 14, 15]),
        ("ENGR852_Visual_Spread_04_8Bit_Trap_vs_16Bit_Datapath.png", [20, 21, 22]),
        ("ENGR852_Visual_Spread_05_Testbenches_0000_0100_FF00.png", [33, 36, 39]),
        ("ENGR852_Visual_Spread_06_14nm_Physical_Design_and_GitHub.png", [62, 64, 95]),
    ]

    img_map = {
        5: SCREENSHOTS_DIR / "gp_vpn_connecting.png",
        6: SCREENSHOTS_DIR / "gp_vpn_connected_and_xquartz_xterm.png",
        7: SCREENSHOTS_DIR / "ssh_x11_multi_terminal_mahmoodi.png",
        62: SCREENSHOTS_DIR / "v9_signoff_clean_layout.png",
    }

    page_w, page_h = 900, 1180
    spread_w = page_w * 3 + 40
    spread_h = page_h + 24

    for fname, pnums in spread_groups:
        img = PILImage.new("RGB", (spread_w, spread_h), (218, 212, 200))
        draw = ImageDraw.Draw(img)

        for col_idx, pnum in enumerate(pnums):
            title, sub, stages, tbl_rows, trap_lines, code_lines = pages[pnum - 1]
            title = clean_glyphs(title)
            sub = clean_glyphs(sub)
            ox = 10 + col_idx * (page_w + 10)
            oy = 12

            # Paper rectangle & graph grid
            draw.rectangle([ox, oy, ox + page_w, oy + page_h], fill=(250, 248, 242), outline=(140, 135, 125), width=2)
            for gx in range(ox + 36, ox + page_w - 10, 18):
                draw.line([(gx, oy + 18), (gx, oy + page_h - 18)], fill=(228, 224, 212), width=1)
            for gy in range(oy + 18, oy + page_h - 18, 18):
                draw.line([(ox + 36, gy), (ox + page_w - 10, gy)], fill=(228, 224, 212), width=1)

            # Red margin line & spiral holes
            draw.line([(ox + 48, oy + 18), (ox + 48, oy + page_h - 18)], fill=(248, 150, 150), width=2)
            for ry in range(oy + 34, oy + page_h - 26, 34):
                draw.ellipse([ox + 14, ry - 5, ox + 24, ry + 5], fill=(190, 198, 210), outline=(90, 100, 115))
                draw.line([(ox + 2, ry), (ox + 16, ry)], fill=(90, 100, 115), width=2)

            # Header
            draw.text((ox + 58, oy + 18), f"ENGR 852 VISUAL NOTEBOOK - PAGE {pnum} OF 100", fill=(29, 78, 216), font=f_hdr)
            draw.text((ox + 58, oy + 36), title[:82], fill=(15, 23, 42), font=f_title)
            draw.line([(ox + 58, oy + 54), (ox + page_w - 16, oy + 54)], fill=(15, 23, 42), width=2)
            draw.text((ox + 58, oy + 58), sub[:96], fill=(21, 128, 61), font=f_sub)

            # 1. Section 1: 4-Stage Pipeline Schematic Boxes
            sy = oy + 80
            draw.rectangle([ox + 58, sy, ox + page_w - 16, sy + 122], fill=(255, 255, 255), outline=(15, 23, 42), width=2)
            draw.text((ox + 66, sy + 5), "1. Annotated Visual Schematic & GUI Action Flow:", fill=(15, 23, 42), font=f_bold)
            bw = 182
            for s_idx, (st_t, st_l) in enumerate(stages[:4]):
                bx = ox + 66 + s_idx * 204
                by = sy + 24
                bcol = [(29, 78, 216), (21, 128, 61), (185, 28, 28), (109, 40, 217)][s_idx % 4]
                bgcol = [(239, 246, 255), (240, 253, 244), (254, 242, 242), (245, 243, 255)][s_idx % 4]
                draw.rectangle([bx, by, bx + bw, by + 90], fill=bgcol, outline=bcol, width=2)
                draw.text((bx + 5, by + 4), clean_glyphs(st_t)[:23], fill=bcol, font=f_bold)
                draw.line([(bx + 4, by + 19), (bx + bw - 4, by + 19)], fill=bcol, width=1)
                for l_i, sl in enumerate(st_l[:4]):
                    draw.text((bx + 5, by + 23 + l_i * 16), clean_glyphs(sl)[:25], fill=(15, 23, 42), font=f_mono)
                if s_idx < 3:
                    ax1, ax2, ay = bx + bw, bx + 204, by + 45
                    draw.line([(ax1, ay), (ax2, ay)], fill=(15, 23, 42), width=2)

            # 2. Section 2: Verification Table
            ty = sy + 130
            draw.text((ox + 58, ty), "2. Step-by-Step Verification & Mapping Table:", fill=(15, 23, 42), font=f_bold)
            ty += 16
            row_h = 22
            ncols = len(tbl_rows[0])
            cw = int((page_w - 74) / ncols)
            for r_i, r_data in enumerate(tbl_rows[:7]):
                ry = ty + r_i * row_h
                rbg = (30, 58, 138) if r_i == 0 else ((255, 255, 255) if r_i % 2 == 1 else (241, 245, 249))
                tcol = (255, 255, 255) if r_i == 0 else (15, 23, 42)
                rfnt = f_bold if r_i == 0 else f_reg
                draw.rectangle([ox + 58, ry, ox + page_w - 16, ry + row_h], fill=rbg, outline=(148, 163, 184), width=1)
                for c_i, cell in enumerate(r_data):
                    cx = ox + 58 + c_i * cw
                    draw.line([(cx, ry), (cx, ry + row_h)], fill=(148, 163, 184), width=1)
                    draw.text((cx + 4, ry + 5), clean_glyphs(cell)[: int(cw / 5.7)], fill=tcol, font=rfnt)

            # 3. Section 3: [!] TRAP Box (+ Embedded Screenshot on Pages 5, 6, 7, 62!)
            ky = ty + min(len(tbl_rows), 7) * row_h + 10
            if pnum in img_map and img_map[pnum].exists():
                sec3_h = 132
                left_w = int((page_w - 74) * 0.48)
                right_w = (page_w - 74) - left_w - 8
                draw.rectangle([ox + 58, ky, ox + 58 + left_w, ky + sec3_h], fill=(254, 242, 242), outline=(185, 28, 28), width=2)
                draw.text((ox + 64, ky + 5), "3. [!] TRAP & Visual Check [!]", fill=(185, 28, 28), font=f_bold)
                for t_i, tl in enumerate(trap_lines[:3]):
                    clean_tl = clean_glyphs(tl.replace("RED:", "").replace("GREEN:", "").replace("BLUE:", ""))
                    draw.text((ox + 64, ky + 24 + t_i * 32), clean_tl[:56], fill=(15, 23, 42), font=f_reg)
                    if len(clean_tl) > 56:
                        draw.text((ox + 64, ky + 38 + t_i * 32), clean_tl[56:112], fill=(15, 23, 42), font=f_reg)
                rx = ox + 58 + left_w + 8
                draw.rectangle([rx, ky, rx + right_w, ky + sec3_h], fill=(255, 255, 255), outline=(29, 78, 216), width=2)
                try:
                    shot = PILImage.open(img_map[pnum]).convert("RGB")
                    shot.thumbnail((right_w - 8, sec3_h - 12))
                    img.paste(shot, (rx + 4, ky + 6))
                except Exception:
                    pass
                ky += sec3_h + 8
            else:
                sec3_h = 80
                draw.rectangle([ox + 58, ky, ox + page_w - 16, ky + sec3_h], fill=(254, 242, 242), outline=(185, 28, 28), width=2)
                draw.text((ox + 66, ky + 5), "3. [!] TRAP / Critical Engineering Note & Why It Happens [!]", fill=(185, 28, 28), font=f_bold)
                for t_i, tl in enumerate(trap_lines[:3]):
                    clean_tl = clean_glyphs(tl.replace("RED:", "").replace("GREEN:", "").replace("BLUE:", ""))
                    draw.text((ox + 66, ky + 24 + t_i * 17), clean_tl[:115], fill=(15, 23, 42), font=f_reg)
                ky += sec3_h + 8

            # Reserve bottom Section 5 (Fallback Troubleshooting Matrix)
            sec5_h = 166
            sec5_y = oy + page_h - 14 - sec5_h

            # 4. Section 4: Line-by-Line Commented Code & Standout Terminal Badges
            cy = ky
            ch = sec5_y - cy - 8
            draw.rectangle([ox + 58, cy, ox + page_w - 16, cy + ch], fill=(248, 250, 252), outline=(109, 40, 217), width=2)
            draw.rectangle([ox + 58, cy, ox + page_w - 16, cy + 20], fill=(109, 40, 217))
            draw.text((ox + 66, cy + 3), "4. Line-by-Line Commented Code & Highlighted Terminal Commands:", fill=(255, 255, 255), font=f_bold)

            max_c_lines = int((ch - 24) / 16)
            rich_code = enrich_code_lines_to_fill_box(pnum, code_lines, max_lines=max_c_lines)
            for c_i, raw_cl in enumerate(rich_code[:max_c_lines]):
                ly = cy + 24 + c_i * 16
                cl = clean_glyphs(raw_cl)
                badge = None
                bcol = None
                rbg = None
                tcol = (15, 23, 42)
                if cl.startswith("TERM_MAC:"):
                    badge, bcol, rbg = "MACBOOK", (30, 58, 138), (219, 234, 254)
                    cl = cl[len("TERM_MAC:"):].strip()
                elif cl.startswith("TERM_XQ:"):
                    badge, bcol, rbg = "XQUARTZ", (15, 118, 110), (204, 251, 241)
                    cl = cl[len("TERM_XQ:"):].strip()
                elif cl.startswith("TERM_SFSU:"):
                    badge, bcol, rbg = "926784856@mahmoodi", (180, 83, 9), (254, 243, 199)
                    cl = cl[len("TERM_SFSU:"):].strip()
                elif cl.startswith("OUT_OK:"):
                    badge, bcol, rbg = "OUTPUT", (21, 128, 61), (220, 252, 231)
                    cl = cl[len("OUT_OK:"):].strip()
                    tcol = (21, 128, 61)

                if rbg:
                    draw.rectangle([ox + 62, ly - 1, ox + page_w - 20, ly + 14], fill=rbg)
                tx = ox + 66
                if badge:
                    bw_p = len(badge) * 6 + 10
                    draw.rectangle([ox + 64, ly, ox + 64 + bw_p, ly + 13], fill=bcol)
                    draw.text((ox + 68, ly + 1), badge, fill=(255, 255, 255), font=f_badge)
                    tx = ox + 68 + bw_p
                max_ch = int((ox + page_w - 22 - tx) / 6.0)
                draw.text((tx, ly), cl[:max_ch], fill=tcol, font=f_mono)

            # 5. Section 5: Live Log Checks & Fallback Troubleshooting (If XYZ Fails -> Option A / B)
            draw.rectangle([ox + 58, sec5_y, ox + page_w - 16, sec5_y + sec5_h], fill=(255, 251, 235), outline=(180, 83, 9), width=2)
            draw.rectangle([ox + 58, sec5_y, ox + page_w - 16, sec5_y + 20], fill=(180, 83, 9))
            draw.text((ox + 66, sec5_y + 3), "5. Live Verification Checks, Server Script Pulling & Fallback Recovery (Plan A / B):", fill=(255, 255, 255), font=f_bold)
            fb_lines = get_fallback_recovery_lines(pnum)
            for f_i, fl in enumerate(fb_lines[:8]):
                fly = sec5_y + 24 + f_i * 17
                clean_fl = clean_glyphs(fl)
                fcol = (15, 23, 42)
                if clean_fl.startswith("RED:"):
                    fcol = (185, 28, 28)
                    clean_fl = clean_fl[4:]
                elif clean_fl.startswith("BLUE:"):
                    fcol = (29, 78, 216)
                    clean_fl = clean_fl[5:]
                elif clean_fl.startswith("GREEN:"):
                    fcol = (21, 128, 61)
                    clean_fl = clean_fl[6:]
                draw.text((ox + 66, fly), clean_fl[:122], fill=fcol, font=f_reg)

        out_path = SPREADS_DIR / fname
        img.save(str(out_path), format="PNG", optimize=True)
        print(f"BUILT_DENSE_SPREAD_PNG: {out_path}")
'''

new_src = prefix + addition + "\n\nif __name__ == \"__main__\":\n    all_pages = render_100page_pdf_and_md()\n    build_3page_visual_spread_images(all_pages)\n"
TARGET_SCRIPT.write_text(new_src, encoding="utf-8")
print("UPDATED_FULL_FILL_SCRIPT_OK")
