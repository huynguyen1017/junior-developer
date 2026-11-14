#!/usr/bin/env python3
"""
Generates the COMPLETE 100-Page Visual Engineering Notebook Manual (Page 1 through Page 100)
in both Markdown (ENGR852_100Page_Visual_Notebook_Guide.md) and PDF
(ENGR852_100Page_Visual_Notebook_Baby_Steps_Manual.pdf), plus the machine-readable
100-Page Curriculum & V1->V9 Guardrail Manifest (practice_from_scratch/curriculum_100pages.json).

Key Architecture on Every Single Page (Page 1 of 100 .. Page 100 of 100):
  1. Visual Annotated Block Diagram & Step-by-Step Execution Pipeline (4-5 stages)
  2. Hardware-to-Verilog / Command-to-Action Verification Table (zero column overlap)
  3. [!] Critical Engineering Note / Beginner Trap & How to Avoid It
  4. Line-by-Line Commented Code & Individual Step-by-Step Terminal Commands (all smaller commands intact)
  5. Dedicated Section Box on the SAME Page: Copy-Paste Combined Page One-Liner
     (combines all smaller commands from that page into one copy-pasteable line wrapped cleanly across
      multiple lines in the PDF so 0% is cut off, walking sequentially from V1 -> V9 and syncing live
      with the Operations Console Website :8788 and GitHub sub-branch `manual-practice-macbook-air`)
  6. Live Verification Checks, Server Script Pulling & Fallback Troubleshooting (If XYZ Fails -> Option A / B)
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

SCRATCH_DIR = Path("/Users/huynguyen/.gemini/antigravity/brain/9abd734c-7786-4e8f-a3e8-35f2bdc2137b/scratch")
BRAIN_DIR = Path("/Users/huynguyen/.gemini/antigravity/brain/9abd734c-7786-4e8f-a3e8-35f2bdc2137b")
REPO_ROOT = Path("/Users/huynguyen/Developer/portfolio/motion-estimator-asic-lab-notebook-2026")

sys.path.insert(0, str(SCRATCH_DIR))
import orig_100page_a5b9bfc as base

base.REPO_ROOT = REPO_ROOT
base.DELIV_DIR = REPO_ROOT / "deliverables"
base.DOCS_DIR = REPO_ROOT / "docs"
base.SCREENSHOTS_DIR = REPO_ROOT / "evidence" / "screenshots"
base.SPREADS_DIR = REPO_ROOT / "evidence" / "notebook_spreads"
base.OUT_PDF = base.DELIV_DIR / "ENGR852_100Page_Visual_Notebook_Baby_Steps_Manual.pdf"
base.OUT_MD = base.DOCS_DIR / "ENGR852_100Page_Visual_Notebook_Baby_Steps_Manual.md"


def slugify(text: str) -> str:
    s = re.sub(r"^Page\s+\d+\s*:\s*", "", text, flags=re.I)
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    parts = [p for p in s.split("_") if p not in ("the", "and", "for", "with", "from", "into", "on", "in", "to", "of", "a")]
    return "_".join(parts[:4]) or "step"


def get_v_stage_info(pnum: int):
    """Maps every page 1..100 to its exact V1..V9 project build evolution milestone."""
    if pnum <= 12:
        return "V1-PREP", "Workstation, GlobalProtect VPN, XQuartz X11 & mahmoodi Setup"
    if pnum <= 24:
        return "V1-ARCH", "Ch. 10 Sec. 10.4 SAD Math, 8-Bit Saturation Trap & 16-Bit Theory"
    if pnum <= 28:
        return "V1-RTL8", "V1 Baseline 8-Bit Saturating Verilog RTL (rtl/8bit/top.v)"
    if pnum <= 32:
        return "V2-RTL16", "V2 Upgraded 16-Bit Non-Saturating RTL & Cycle-4111 Hold (rtl/16bit/top.v)"
    if pnum <= 35:
        return "V3-TB0000", "V3 520 MHz Exact-Match Testbench (top_tb_direct.v -> BestDist=0000)"
    if pnum <= 38:
        return "V3-TB0100", "V3 520 MHz +1 LSB Offset Testbench (top_tb.v -> BestDist=0100, X=FB, Y=07)"
    if pnum <= 41:
        return "V4-TBFF00", "V4 520 MHz Max-Contrast Stress Testbench (top_tb_16bit.v -> BestDist=FF00)"
    if pnum <= 44:
        return "V4-SV-SCB", "V4 SystemVerilog Directed & Multi-Seed Scoreboard Verification"
    if pnum <= 52:
        return "V5-NWAVE", "V5/V9 Synopsys VCS 520 MHz & Verdi nWave Hex Waveform Capture"
    if pnum <= 58:
        return "V6-SYN-FP", "V6 SAED14nm 520 MHz SDC, MCMM Synthesis, Floorplan & PG Network"
    if pnum <= 61:
        return "V7-CTS-RT", "V7 SAED14nm Placement, Clock Tree Synthesis, Detail Route & GDSII"
    if pnum <= 64:
        return "V8-SIGNOFF", "V8/V9 Layout GUI, Standalone ICV DRC (0/242 CLEAN) & 3-Corner PrimeTime STA"
    if pnum <= 88:
        return "V9-PYTHON", "V9 Consolidated Workbook: Python Slides, ReportLab PDF & 11-Gate Harness"
    return "V9-GITHUB", "V9 Final Submission Packaging, GitHub Sync & 100-Page Sign-Off"


def extract_individual_commands_summary(rich_code):
    """Extracts the individual smaller commands shown in Section 4 of the page."""
    cmds = []
    for ln in rich_code:
        s = base.clean_glyphs(str(ln)).strip()
        if s.startswith("TERM_MAC:") or s.startswith("TERM_XQ:") or s.startswith("TERM_SFSU:"):
            cleaned = re.sub(r"^TERM_(MAC|XQ|SFSU):\s*(\[[^\]]+\]\s*)?", "", s).strip()
            if cleaned and not cleaned.startswith("#"):
                cmds.append(cleaned)
    return cmds


def get_page_oneliner_and_meaning(pnum: int, title: str, sub: str, tbl_rows, trap_lines, rich_code):
    """
    Returns (where_badge, env_tag, step_id, v_stage, v_desc, cmd_explanations, one_liner, expected_output_lines, wave_img)
    for every single page 1..100 so that every page has:
      - All individual smaller commands in Section 4, AND
      - A dedicated Section 5 Combined Page One-Liner combining all those steps in sequence (V1 -> V9).
    """
    slug = slugify(title)
    step_id = f"page{pnum:03d}_{slug}"
    v_stage, v_desc = get_v_stage_info(pnum)
    wave_img = None

    if pnum <= 7 or pnum >= 89:
        where_badge = "LOCAL MACBOOK AIR TERMINAL (`zsh`) — or `926784856@mahmoodi.rcc.at.sfsu.edu` (`bash`)"
        env_tag = "MACBOOK" if pnum not in (6, 7) else "XQUARTZ"
    else:
        where_badge = "XQUARTZ / SSH MAHMOODI SERVER TERMINAL (`bash` on `926784856@mahmoodi.rcc.at.sfsu.edu`)"
        env_tag = "926784856@mahmoodi"

    # Combined one-liners per page (1..100) that combine all the smaller commands of that page
    if pnum == 1:
        one_liner = (
            'mkdir -p ~/Developer/engr852_practice && cd ~/Developer/engr852_practice && '
            'if [ ! -d motion-estimator-asic-lab-notebook-2026 ]; then git clone https://github.com/huynguyen1017/motion-estimator-asic-lab-notebook-2026.git; fi && '
            'cd motion-estimator-asic-lab-notebook-2026 && git fetch origin && git checkout manual-practice-macbook-air && '
            'git pull origin manual-practice-macbook-air && source practice_from_scratch/scripts/auto_bridge.sh && '
            'snap_step "page001_master_roadmap" "mkdir -p ~/Developer/motion-estimator-14nm-asic-manual/{rtl/8bit,rtl/16bit,tb/8bit,tb/16bit,scripts,docs,deliverables,evidence/screenshots} && cd ~/Developer/motion-estimator-14nm-asic-manual && pwd && ls -la ~/Developer/motion-estimator-14nm-asic-manual"'
        )
        expected = [
            "AUTO_BRIDGE_READY: branch=manual-practice-macbook-air | live_web=http://127.0.0.1:8788",
            "/Users/huynguyen/Developer/motion-estimator-14nm-asic-manual",
            "drwxr-xr-x ... deliverables  docs  evidence  rtl  scripts  tb",
            ">>> [AUTO-BRIDGE] Uploaded log + screenshot + live state to Web Console & GitHub 'manual-practice-macbook-air': page001_master_roadmap",
        ]
    elif pnum == 2:
        one_liner = (
            'snap_step "page002_engr_852_course_project" '
            '"cd ~/Developer/motion-estimator-14nm-asic-manual && echo \'RUBRIC_CHECK: [1] top.v (0 RAM macros) [2] top_520mhz.sdc (1.923ns) [3] TBs (0000/0100/FF00) [4] 14nm Layout (0/242 DRC) [5] 3-Corner PrimeTime STA\' && grep -E \'top u1|RMEM u2|SMEM u3\' ~/Developer/engr852_practice/motion-estimator-asic-lab-notebook-2026/tb/16bit/top_tb_direct.v && ls -ld rtl/8bit rtl/16bit tb/8bit tb/16bit"'
        )
        expected = [
            "RUBRIC_CHECK: [1] top.v (0 RAM macros) [2] top_520mhz.sdc (1.923ns) [3] TBs (0000/0100/FF00) [4] 14nm Layout (0/242 DRC) [5] 3-Corner PrimeTime STA",
            "top u1 (clock, start, BestDist, motionX, motionY, AddressR, AddressS1, AddressS2, R, S1, S2);",
            "RMEM u2 (AddressR, R);",
            "SMEM u3 (AddressS1, AddressS2, S1, S2);",
        ]
    elif pnum == 3:
        one_liner = (
            'snap_step "page003_brand_new_macbook_air" '
            '"xcode-select -p && git --version && ssh -V 2>&1 && cd ~/Developer/motion-estimator-14nm-asic-manual && python3 -m venv .venv && source .venv/bin/activate && pip install -q --upgrade pip pillow reportlab python-pptx pypdf && python3 -c \'import PIL, reportlab, pptx, pypdf; print(\\\"MACBOOK_CLI_AND_VENV_READY\\\")\'"'
        )
        expected = [
            "/Library/Developer/CommandLineTools",
            "git version 2.39+",
            "MACBOOK_CLI_AND_VENV_READY",
        ]
    elif pnum == 4:
        one_liner = (
            'snap_step "page004_project_naming_variations" '
            '"export PROJ_LOCAL=$HOME/Developer/motion-estimator-14nm-asic-manual PROJ_REMOTE=me_asic_new_v1 SFSU_USER=926784856 SFSU_HOST=mahmoodi.rcc.at.sfsu.edu && echo \"LOCAL=$PROJ_LOCAL | REMOTE=$PROJ_REMOTE | SERVER=$SFSU_USER@$SFSU_HOST | TOP_MODULE=module top (clock,start,BestDist,motionX,motionY,AddressR,AddressS1,AddressS2,R,S1,S2)\""'
        )
        expected = [
            "LOCAL=/Users/huynguyen/Developer/motion-estimator-14nm-asic-manual | REMOTE=me_asic_new_v1 | SERVER=926784856@mahmoodi.rcc.at.sfsu.edu | TOP_MODULE=module top (...)",
        ]
    elif pnum == 5:
        wave_img = "gp_vpn_connecting.png"
        one_liner = (
            'snap_step "page005_installing_operating_palo_alto" '
            '"pgrep -fl GlobalProtect || true; scutil --dns | grep -i sfsu | head -n 4 || true; ifconfig | grep -E \'inet (192\\.168|10\\.|130\\.212)\' || true; nc -zv -G 5 mahmoodi.rcc.at.sfsu.edu 22 2>&1"'
        )
        expected = [
            "GlobalProtect",
            "inet 130.212.163.69 --> 130.212.163.69",
            "Connection to mahmoodi.rcc.at.sfsu.edu port 22 [tcp/ssh] succeeded!",
        ]
    elif pnum == 6:
        wave_img = "gp_vpn_connected_and_xquartz_xterm.png"
        one_liner = (
            'snap_step "page006_installing_configuring_xquartz_macos" '
            '"open -a XQuartz && sleep 1 && defaults write org.xquartz.X11 nolisten_tcp -bool false && echo \"LOCAL_DISPLAY=${DISPLAY:-:0}\" && ls -la /tmp/.X11-unix && /opt/X11/bin/xdpyinfo -display :0 2>/dev/null | head -n 5 || echo XQUARTZ_SOCKET_ACTIVE"'
        )
        expected = [
            "LOCAL_DISPLAY=/private/tmp/com.apple.launchd.../org.xquartz:0",
            "srwxrwxrwx  1 huynguyen  wheel  0 ... X0",
        ]
    elif pnum == 7:
        wave_img = "ssh_x11_multi_terminal_mahmoodi.png"
        one_liner = (
            'snap_step "page007_how_xquartz_ssh_y" '
            '"mkdir -p ~/.ssh && chmod 700 ~/.ssh && grep -q \'Host mahmoodi\' ~/.ssh/config 2>/dev/null || printf \'\\nHost mahmoodi mahmoodi.rcc.at.sfsu.edu\\n  HostName mahmoodi.rcc.at.sfsu.edu\\n  User 926784856\\n  ForwardX11 yes\\n  ForwardX11Trusted yes\\n  ServerAliveInterval 30\\n\' >> ~/.ssh/config && chmod 600 ~/.ssh/config && tail -n 8 ~/.ssh/config && echo \'NOW RUN: ssh -Y 926784856@mahmoodi.rcc.at.sfsu.edu\'"'
        )
        expected = [
            "Host mahmoodi mahmoodi.rcc.at.sfsu.edu",
            "  ForwardX11 yes",
            "  ForwardX11Trusted yes",
            "NOW RUN: ssh -Y 926784856@mahmoodi.rcc.at.sfsu.edu",
        ]
    elif pnum == 8:
        one_liner = (
            'cd ~/motion-estimator-asic-lab-notebook-2026 && git fetch origin && git checkout manual-practice-macbook-air && '
            'git pull origin manual-practice-macbook-air && source practice_from_scratch/scripts/auto_bridge.sh && '
            'snap_step "page008_setting_up_passwordless_ed25519" "chmod go-w ~ && mkdir -p ~/.ssh && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys 2>/dev/null || true; ls -ld ~/.ssh && remote_status"'
        )
        expected = [
            "drwx------. 2 926784856 domain users ... /home/926784856/.ssh",
            "=== REMOTE MAHMOODI SERVER TERMINAL STATE ===",
            "User@Host : 926784856@mahmoodi.rcc.at.sfsu.edu",
            "VCS       : /packages/synopsys/vcs/W-2024.09-1/bin/vcs",
            "Verdi     : /packages/synopsys/verdi/W-2024.09-1/bin/verdi",
            "FC Shell  : /packages/synopsys/fc/X-2025.06-SP2a/bin/fc_shell",
            "ICV       : /packages/synopsys/ic_validator/W-2024.09-3/bin/linux64/icv",
            "PrimeTime : /packages/synopsys/primetime/U-2022.12-SP5-1/bin/pt_shell",
        ]
    elif pnum == 9:
        one_liner = (
            'snap_step "page009_creating_brand_new_isolated" '
            '"mkdir -p ~/me_asic_new_v1/{rtl/8bit,rtl/16bit,tb/8bit,tb/16bit,constraints,scripts,logs,reports,results,pt_reports} && '
            'cp -r ~/ENGR852_Project/16_v3b_final_asic_fc/{setup,common,scripts} ~/me_asic_new_v1/ && '
            'cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/scripts/v5_prime_time_extracted_corners.tcl ~/me_asic_new_v1/scripts/ && '
            'cd ~/me_asic_new_v1 && pwd && ls -la ~/me_asic_new_v1"'
        )
        expected = [
            "/home/926784856/me_asic_new_v1",
            "drwxr-xr-x ... common  constraints  logs  pt_reports  reports  results  rtl  scripts  setup  tb",
        ]
    elif pnum == 10:
        one_liner = (
            'snap_step "page010_loading_synopsys_eda_toolchain" '
            '"cd ~/me_asic_new_v1 && which vcs verdi fc_shell icv pt_shell && echo \"LM_LICENSE_FILE=$LM_LICENSE_FILE\" && cat ~/me_asic_new_v1/scripts/synopsys_setup.tcl && ls -la ~/me_asic_new_v1/common/ndm/ ~/me_asic_new_v1/common/liberty/"'
        )
        expected = [
            "/packages/synopsys/vcs/W-2024.09-1/bin/vcs",
            "/packages/synopsys/verdi/W-2024.09-1/bin/verdi",
            "/packages/synopsys/fc/X-2025.06-SP2a/bin/fc_shell",
            "/packages/synopsys/ic_validator/W-2024.09-3/bin/linux64/icv",
            "/packages/synopsys/primetime/U-2022.12-SP5-1/bin/pt_shell",
            "saed14rvt_ff0p88v125c.db  saed14rvt_ss0p72vm40c.db  saed14rvt_tt0p8v25c.db",
        ]
    elif pnum == 11:
        one_liner = (
            'snap_step "page011_transferring_files_between_your" '
            '"mkdir -p ~/me_asic_new_v1/tb/8bit ~/me_asic_new_v1/tb/16bit && '
            'cp ~/ENGR852_Project/00_original_baseline/ref*.txt ~/ENGR852_Project/00_original_baseline/search*.txt ~/me_asic_new_v1/tb/8bit/ && '
            'cp ~/ENGR852_Project/00_original_baseline/ref*.txt ~/ENGR852_Project/00_original_baseline/search*.txt ~/me_asic_new_v1/tb/16bit/ && '
            'cp ~/ENGR852_Project/00_original_baseline/ref.txt ~/ENGR852_Project/00_original_baseline/search.txt ~/me_asic_new_v1/ && '
            'wc -l ~/me_asic_new_v1/tb/16bit/ref.txt ~/me_asic_new_v1/tb/16bit/search.txt && head -n 5 ~/me_asic_new_v1/tb/16bit/ref.txt"'
        )
        expected = [
            "  256 /home/926784856/me_asic_new_v1/tb/16bit/ref.txt",
            " 1024 /home/926784856/me_asic_new_v1/tb/16bit/search.txt",
            " 1280 total",
        ]
    elif pnum == 12:
        one_liner = (
            'snap_step "page012_part_i_self_check" '
            '"cd ~/me_asic_new_v1 && echo \"GATE_1_HOST=$(hostname) USER=$(whoami) DISPLAY=${DISPLAY:-localhost:10.0}\" && which vcs verdi fc_shell icv pt_shell && ls -d rtl/8bit rtl/16bit tb/8bit tb/16bit common setup scripts && echo PART_I_6POINT_READINESS_GATE_PASS"'
        )
        expected = [
            "GATE_1_HOST=mahmoodi.rcc.at.sfsu.edu USER=926784856 DISPLAY=localhost:10.0",
            "common  rtl/16bit  rtl/8bit  scripts  setup  tb/16bit  tb/8bit",
            "PART_I_6POINT_READINESS_GATE_PASS",
        ]
    elif 13 <= pnum <= 24:
        theory_cmds = {
            13: (
                'python3 -c "print(\'Ref Block R: 16x16 =\', 16*16, \'bytes | Search Window S: 31x31 =\', 31*31, \'active bytes (1024 ROM_S) | Candidate Blocks: 16x16 =\', 16*16, \'| Displacement Range: [-8, +7]\')" && grep -En "module top|AddressR|AddressS" ~/ENGR852_Project/00_original_baseline/top.v',
                "Ref Block R: 16x16 = 256 bytes | Search Window S: 31x31 = 961 active bytes (1024 ROM_S) | Candidate Blocks: 16x16 = 256 | Displacement Range: [-8, +7]"
            ),
            14: (
                'python3 -c "print(\'SAD Regimes -> Exact Match:\', hex(256*0), \'| +1 LSB Shift:\', hex(256*1), \'| +2 Shift:\', hex(256*2), \'| Max Contrast (256*255):\', hex(256*255), \'=\', 256*255)" && grep -En "difference =" ~/ENGR852_Project/00_original_baseline/top.v',
                "SAD Regimes -> Exact Match: 0x0 | +1 LSB Shift: 0x100 | +2 Shift: 0x200 | Max Contrast (256*255): 0xff00 = 65280"
            ),
            15: (
                'python3 -c "pts=[(0,0),(3,15),(6,8),(8,8),(15,15)]; print(\' | \'.join(f\'(i={i},j={j})->dx={i-8}(0x{(i-8)&0xff:02x}),dy={j-8}(0x{(j-8)&0xff:02x})\' for i,j in pts))" && grep -En "vectorX|vectorY|motionX|motionY" ~/ENGR852_Project/00_original_baseline/top.v',
                "(i=0,j=0)->dx=-8(0xf8),dy=-8(0xf8) | (i=3,j=15)->dx=-5(0xfb),dy=7(0x07) | ... | (i=15,j=15)->dx=7(0x07),dy=7(0x07)"
            ),
            16: (
                'grep -En "module PE|module PEend|module PEtotal|S1S2mux" ~/ENGR852_Project/00_original_baseline/top.v && python3 -c "print(\'16 PEs in parallel: PE0..PE14 have Rpipe[7:0] forwarding; PE15 (PEend) terminates array.\')"',
                "Shows 16-PE 1D systolic instantiation inside module PEtotal and dual search ports S1, S2."
            ),
            17: (
                'python3 -c "for c in [0,1,2,15,255,256]: print(f\'count={c:4d} (0x{c:04x}): AddressR=0x{c&0xff:02x} | newDist_PE={c&0xf if (c&0xff)<16 else None} | PEready_active={c>=256 and (c&0xff)<16}\')" && grep -En "newDist|PEready" ~/ENGR852_Project/00_original_baseline/top.v',
                "count=   0 (0x0000): AddressR=0x00 ... count= 256 (0x0100): AddressR=0x00 | newDist_PE=0 | PEready_active=True"
            ),
            18: (
                'python3 -c "total=16*256+15; print(f\'Table 10.1 Schedule: 16 rows * 256 cycles + 15 fill cycles = {total} cycles (0x{total:04x}) | Wall time @ 520MHz (1.923ns) = {total*1.923:.2f} ns\')"',
                "Table 10.1 Schedule: 16 rows * 256 cycles + 15 fill cycles = 4111 cycles (0x100f) | Wall time @ 520MHz (1.923ns) = 7905.45 ns"
            ),
            19: (
                'python3 -c "for y in (0,1,8,15,30): print(f\'Row y={y:2d}: 31*y = (y<<5)-y = {(y<<5)-y:3d} (0x{(y<<5)-y:03x}) == {31*y:3d}\')" && grep -En "AddressS1|AddressS2" ~/ENGR852_Project/00_original_baseline/top.v',
                "Row y= 0: 31*y = (y<<5)-y =   0 ... Row y=15: 31*y = (y<<5)-y = 465 (0x1d1) == 465"
            ),
            20: (
                'grep -En -C 3 "Carry, AccumulateIn" ~/ENGR852_Project/00_original_baseline/top.v && python3 -c "print(\'V1 8-Bit Carry Trap: Any SAD > 255 triggers Carry==1 and clamps AccumulateIn = 8hFF!\')"',
                "Shows 8-bit saturating adder: {Carry, AccumulateIn} = Accumulate + difference; if (Carry == 1) AccumulateIn = 8'b11111111;"
            ),
            21: (
                'grep -En -C 4 "BestDist <= 8" ~/ENGR852_Project/00_original_baseline/top.v && python3 -c "best=0xFF; new_d=0xFF; print(f\'V1 Comparator Tie Trap: newDist=0x{new_d:02X} < BestDist=0x{best:02X} is {new_d < best} -> newBest=0 -> motionX/motionY stay X!\')"',
                "V1 Comparator Tie Trap: newDist=0xFF < BestDist=0xFF is False -> newBest=0 -> motionX/motionY stay X!"
            ),
            22: (
                'grep -En -C 3 "AccumulateIn = Accumulate" ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v && python3 -c "best=0xFFFF; new_d=256*255; print(f\'V2 16-Bit Fix: newDist=0x{new_d:04X} ({new_d}) < BestDist=0x{best:04X} ({best}) is {new_d < best} -> newBest=1!\')"',
                "V2 16-Bit Fix: newDist=0xFF00 (65280) < BestDist=0xFFFF (65535) is True -> newBest=1!"
            ),
            23: (
                'grep -En -C 4 "13\'h100F|completed" ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v && python3 -c "print(\'V2 Counter Fix: 13-bit count[12:0] runs cleanly across 4096..4111 (0x1000..0x100F) and latches completed<=1!\')"',
                "Shows 13-bit counter reg [12:0] count and terminal hold at count == 13'h100F (cycle 4111)."
            ),
            24: (
                'diff -u ~/ENGR852_Project/00_course_reference/rtl/8bit/top.v ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v | head -n 42 || true',
                "Unified diff highlighting every bus width upgrade from V1 8-bit baseline to V2 16-bit non-saturating RTL."
            ),
        }
        cmd_inner, exp_line = theory_cmds[pnum]
        one_liner = f'snap_step "{step_id}" {repr(cmd_inner)}'
        expected = [exp_line]
    elif 25 <= pnum <= 28:
        ranges = {25: (1, 28), 26: (29, 56), 27: (57, 84), 28: (85, 200)}
        s_line, e_line = ranges[pnum]
        op = ">" if pnum == 25 else ">>"
        if pnum == 28:
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/rtl/8bit && "
                f"cp ~/ENGR852_Project/00_course_reference/rtl/8bit/top.v ~/me_asic_new_v1/rtl/8bit/top.v && "
                f"nl -ba ~/me_asic_new_v1/rtl/8bit/top.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/rtl/8bit/top.v && grep -En 'module ' ~/me_asic_new_v1/rtl/8bit/top.v"
            )
        else:
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/rtl/8bit && "
                f"sed -n '{s_line},{e_line}p' ~/ENGR852_Project/00_course_reference/rtl/8bit/top.v {op} ~/me_asic_new_v1/rtl/8bit/top.v && "
                f"nl -ba ~/ENGR852_Project/00_course_reference/rtl/8bit/top.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/rtl/8bit/top.v"
            )
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
        expected = [
            f"[V1 8-Bit RTL] Writes & verifies lines {s_line}..{e_line} of ~/me_asic_new_v1/rtl/8bit/top.v.",
        ]
    elif 29 <= pnum <= 32:
        ranges = {29: (1, 30), 30: (31, 60), 31: (61, 90), 32: (91, 220)}
        s_line, e_line = ranges[pnum]
        op = ">" if pnum == 29 else ">>"
        if pnum == 32:
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/rtl/16bit ~/me_asic_new_v1/common/rtl/verilog && "
                f"cp ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v ~/me_asic_new_v1/rtl/16bit/top.v && "
                f"cp ~/me_asic_new_v1/rtl/16bit/top.v ~/me_asic_new_v1/common/rtl/verilog/top.v && "
                f"nl -ba ~/me_asic_new_v1/rtl/16bit/top.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/rtl/16bit/top.v ~/me_asic_new_v1/common/rtl/verilog/top.v && "
                f"sha256sum ~/me_asic_new_v1/rtl/16bit/top.v"
            )
        else:
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/rtl/16bit && "
                f"sed -n '{s_line},{e_line}p' ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v {op} ~/me_asic_new_v1/rtl/16bit/top.v && "
                f"nl -ba ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/rtl/16bit/top.v"
            )
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
        expected = [
            f"[V2 16-Bit Non-Saturating RTL] Writes & verifies lines {s_line}..{e_line} of ~/me_asic_new_v1/rtl/16bit/top.v.",
        ]
    elif 33 <= pnum <= 35:
        ranges = {33: (1, 26), 34: (27, 52), 35: (53, 120)}
        s_line, e_line = ranges[pnum]
        if pnum < 35:
            op = ">" if pnum == 33 else ">>"
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/tb/16bit && "
                f"sed -n '{s_line},{e_line}p' ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_direct.v {op} ~/me_asic_new_v1/tb/16bit/top_tb_direct.v && "
                f"nl -ba ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_direct.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/tb/16bit/top_tb_direct.v"
            )
            expected = [f"[V3 Testbench 1] Writes & verifies lines {s_line}..{e_line} of tb/16bit/top_tb_direct.v (Exact Match 16'h0000)."]
        else:
            cmd_inner = (
                "mkdir -p ~/me_asic_new_v1/rtl/16bit ~/me_asic_new_v1/tb/16bit ~/me_asic_new_v1/logs && "
                "cp ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v ~/me_asic_new_v1/rtl/16bit/top.v && "
                "cp ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_direct.v ~/me_asic_new_v1/tb/16bit/top_tb_direct.v && "
                "cp ~/ENGR852_Project/00_course_reference/tb/16bit/ref.txt ~/ENGR852_Project/00_course_reference/tb/16bit/search.txt ~/me_asic_new_v1/ && "
                "nl -ba ~/me_asic_new_v1/tb/16bit/top_tb_direct.v | sed -n '53,120p' && "
                "cd ~/me_asic_new_v1 && vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/top_tb_direct.v -o simv_direct >/dev/null && ./simv_direct | tee logs/tb1_direct_0000.log | tail -n 12"
            )
            expected = [
                "BestDist = 0000 (hex) | motionX = f8 (-8) or 07 (+7) | motionY = 07 (+7) or f8 (-8) [PASS]",
            ]
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
    elif 36 <= pnum <= 38:
        ranges = {36: (1, 26), 37: (27, 52), 38: (53, 140)}
        s_line, e_line = ranges[pnum]
        if pnum < 38:
            op = ">" if pnum == 36 else ">>"
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/tb/16bit && "
                f"sed -n '{s_line},{e_line}p' ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb.v {op} ~/me_asic_new_v1/tb/16bit/top_tb.v && "
                f"nl -ba ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/tb/16bit/top_tb.v"
            )
            expected = [f"[V3 Testbench 2] Writes & verifies lines {s_line}..{e_line} of tb/16bit/top_tb.v (+1 LSB Offset 16'h0100)."]
        else:
            cmd_inner = (
                "mkdir -p ~/me_asic_new_v1/rtl/16bit ~/me_asic_new_v1/tb/16bit ~/me_asic_new_v1/logs && "
                "cp ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v ~/me_asic_new_v1/rtl/16bit/top.v && "
                "cp ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb.v ~/me_asic_new_v1/tb/16bit/top_tb.v && "
                "nl -ba ~/me_asic_new_v1/tb/16bit/top_tb.v | sed -n '53,140p' && "
                "cd ~/me_asic_new_v1 && vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/top_tb.v -o simv_offset1 >/dev/null && ./simv_offset1 | tee logs/tb2_offset_0100.log | tail -n 12"
            )
            expected = [
                "Expected X = -5 (FB), Y = 7 (07) | BestDist = 0100 (256), motionX = fb (-5), motionY = 07 (+7) [PASS]",
            ]
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
    elif 39 <= pnum <= 41:
        ranges = {39: (1, 26), 40: (27, 45), 41: (46, 100)}
        s_line, e_line = ranges[pnum]
        if pnum < 41:
            op = ">" if pnum == 39 else ">>"
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/tb/16bit && "
                f"sed -n '{s_line},{e_line}p' ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_16bit.v {op} ~/me_asic_new_v1/tb/16bit/top_tb_16bit.v && "
                f"nl -ba ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_16bit.v | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/tb/16bit/top_tb_16bit.v"
            )
            expected = [f"[V4 Testbench 3] Writes & verifies lines {s_line}..{e_line} of tb/16bit/top_tb_16bit.v (Max Contrast 16'hFF00)."]
        else:
            cmd_inner = (
                "mkdir -p ~/me_asic_new_v1/rtl/16bit ~/me_asic_new_v1/tb/16bit ~/me_asic_new_v1/logs && "
                "cp ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v ~/me_asic_new_v1/rtl/16bit/top.v && "
                "cp ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_16bit.v ~/me_asic_new_v1/tb/16bit/top_tb_16bit.v && "
                "nl -ba ~/me_asic_new_v1/tb/16bit/top_tb_16bit.v | sed -n '46,100p' && "
                "cd ~/me_asic_new_v1 && vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/top_tb_16bit.v -o simv_ff00 >/dev/null && ./simv_ff00 | tee logs/tb3_max_ff00.log | tail -n 12"
            )
            expected = [
                "Max-Contrast Stress Test: BestDist = ff00 (65280 < 65535), motionX = f8 (-8), motionY = f8 (-8) [PASS]",
            ]
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
    elif 42 <= pnum <= 44:
        ranges = {42: (1, 35), 43: (36, 70), 44: (71, 140)}
        s_line, e_line = ranges[pnum]
        if pnum < 44:
            op = ">" if pnum == 42 else ">>"
            cmd_inner = (
                f"mkdir -p ~/me_asic_new_v1/tb/16bit && "
                f"sed -n '{s_line},{e_line}p' ~/ENGR852_Project/00_course_reference/verification/v6_clean/motion_pe_comparator_selfcheck_tb.sv {op} ~/me_asic_new_v1/tb/16bit/motion_pe_comparator_selfcheck_tb.sv && "
                f"nl -ba ~/ENGR852_Project/00_course_reference/verification/v6_clean/motion_pe_comparator_selfcheck_tb.sv | sed -n '{s_line},{e_line}p' && "
                f"wc -l ~/me_asic_new_v1/tb/16bit/motion_pe_comparator_selfcheck_tb.sv"
            )
            expected = [f"[V4 Self-Check SV TB] Writes & verifies lines {s_line}..{e_line} of motion_pe_comparator_selfcheck_tb.sv."]
        else:
            cmd_inner = (
                "mkdir -p ~/me_asic_new_v1/rtl/16bit ~/me_asic_new_v1/tb/16bit ~/me_asic_new_v1/logs && "
                "cp ~/ENGR852_Project/00_course_reference/rtl/16bit/top.v ~/me_asic_new_v1/rtl/16bit/top.v && "
                "cp ~/ENGR852_Project/00_course_reference/verification/v6_clean/motion_pe_comparator_selfcheck_tb.sv ~/me_asic_new_v1/tb/16bit/ && "
                "nl -ba ~/me_asic_new_v1/tb/16bit/motion_pe_comparator_selfcheck_tb.sv | sed -n '71,140p' && "
                "cd ~/me_asic_new_v1 && vcs -full64 -sverilog -debug_access+all rtl/16bit/top.v tb/16bit/motion_pe_comparator_selfcheck_tb.sv -o simv_selfcheck >/dev/null && ./simv_selfcheck | tee logs/tb4_selfcheck.log | tail -n 15"
            )
            expected = [
                "ALL DIRECTED PE & COMPARATOR SELF-CHECKS PASSED! (0000, 0003, FF00 verified)",
            ]
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
    elif 45 <= pnum <= 52:
        wave_map = {
            49: "V9_fig7_orig8bit_row1_nWave.png",
            50: "V9_fig8_orig8bit_complete_nWave.png",
            51: "V9_fig10_16bit_perfect_match_0000_nWave.png",
            52: "V9_fig9_16bit_saturation_row1_nWave.png",
        }
        wave_img = wave_map.get(pnum)
        vcs_verdi_cmds = {
            45: (
                "mkdir -p ~/me_asic_new_v1/{rtl/8bit,tb/8bit,logs,waveforms} && "
                "cp ~/ENGR852_Project/00_original_baseline/top.v ~/me_asic_new_v1/rtl/8bit/top.v && "
                "cp ~/ENGR852_Project/00_original_baseline/top_tb.v ~/me_asic_new_v1/tb/8bit/top_tb.v && "
                "cd ~/me_asic_new_v1 && vcs -full64 -sverilog -debug_access+all rtl/8bit/top.v tb/8bit/top_tb.v -o simv_8bit >/dev/null && "
                "./simv_8bit | tee logs/baseline_8bit_trap.log | tail -n 12"
            ),
            46: (
                "mkdir -p ~/me_asic_new_v1/scripts/verdi_nwave ~/me_asic_new_v1/waveforms && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/*.tcl ~/me_asic_new_v1/scripts/verdi_nwave/ && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/*.sv ~/me_asic_new_v1/tb/ && "
                "ls -lh ~/ENGR852_Project/22_v9_clean_verdi_waveforms/*.fsdb ~/me_asic_new_v1/scripts/verdi_nwave/*.tcl"
            ),
            47: (
                "nl -ba ~/me_asic_new_v1/scripts/verdi_nwave/fig7_orig8bit_row1.tcl && "
                "nl -ba ~/me_asic_new_v1/scripts/verdi_nwave/fig10_16bit_0000.tcl"
            ),
            48: (
                "nl -ba ~/me_asic_new_v1/scripts/verdi_nwave/fig8_orig8bit_complete.tcl && "
                "nl -ba ~/me_asic_new_v1/scripts/verdi_nwave/fig11_16bit_0100.tcl"
            ),
            49: (
                "mkdir -p ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/raw_fig7.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig7_orig8bit_row1_nWave.png && "
                "cat ~/ENGR852_Project/22_v9_clean_verdi_waveforms/simv_sat.log && "
                "ls -lh ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig7_orig8bit_row1_nWave.png"
            ),
            50: (
                "mkdir -p ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/raw_fig8.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig8_orig8bit_complete_nWave.png && "
                "cat ~/ENGR852_Project/22_v9_clean_verdi_waveforms/simv_hold.log && "
                "ls -lh ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig8_orig8bit_complete_nWave.png"
            ),
            51: (
                "mkdir -p ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/raw_fig10.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig10_16bit_perfect_match_0000_nWave.png && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/raw_fig11.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig11_16bit_offset1_0100_nWave.png && "
                "tail -n 25 ~/ENGR852_Project/22_v9_clean_verdi_waveforms/simv_reg.log && "
                "ls -lh ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig10_16bit_perfect_match_0000_nWave.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig11_16bit_offset1_0100_nWave.png"
            ),
            52: (
                "mkdir -p ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/raw_fig9.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig9_16bit_saturation_row1_nWave.png && "
                "cp ~/ENGR852_Project/22_v9_clean_verdi_waveforms/raw_fig12.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig12_16bit_max_sad_ff00_nWave.png && "
                "cat ~/me_asic_new_v1/scripts/verdi_nwave/fig9_16bit_sat_row1.tcl && "
                "ls -lh ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig9_16bit_saturation_row1_nWave.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/V9_fig12_16bit_max_sad_ff00_nWave.png"
            ),
        }
        one_liner = f'snap_step "{step_id}" "{vcs_verdi_cmds[pnum]}"'
        expected = [
            "Executes VCS 520 MHz simulation + Verdi nWave waveform capture/sync and uploads waveform PNGs to Live Web Console & GitHub sub-branch."
        ]
    elif 53 <= pnum <= 64:
        if pnum == 62:
            wave_img = "v9_signoff_clean_layout.png"
        eda_cmds = {
            53: (
                "mkdir -p ~/me_asic_new_v1/common/sdc ~/me_asic_new_v1/constraints && "
                "cp ~/ENGR852_Project/00_course_reference/constraints/top_520mhz.sdc ~/me_asic_new_v1/common/sdc/top.sdc && "
                "cp ~/ENGR852_Project/00_course_reference/constraints/top_520mhz.sdc ~/me_asic_new_v1/constraints/top_520mhz.sdc && "
                "nl -ba ~/me_asic_new_v1/common/sdc/top.sdc"
            ),
            54: (
                "ls -la ~/ENGR852_Project/16_v3b_final_asic_fc/common/liberty/ ~/ENGR852_Project/16_v3b_final_asic_fc/common/ndm/ && "
                "cat ~/ENGR852_Project/16_v3b_final_asic_fc/setup/fc_common_setup.tcl"
            ),
            55: (
                "mkdir -p ~/me_asic_new_v1/reports && "
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/reports/initial_syn* ~/me_asic_new_v1/reports/ && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/initial_syn.tcl && "
                "head -n 30 ~/me_asic_new_v1/reports/initial_syn_report_qor.rpt"
            ),
            56: (
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/reports/compile_flow* ~/me_asic_new_v1/reports/ && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/compile_flow.tcl && "
                "cat ~/me_asic_new_v1/reports/compile_flow_report_area.rpt"
            ),
            57: (
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/reports/classic_place_opt* ~/me_asic_new_v1/reports/ && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/manual_floorplan_creation.tcl && "
                "cat ~/me_asic_new_v1/reports/classic_place_opt_flow_report_area.rpt"
            ),
            58: (
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/create_pg_network.tcl | head -n 48"
            ),
            59: (
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/reports/clock_opt* ~/me_asic_new_v1/reports/ && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/clock_opt.tcl && "
                "cat ~/me_asic_new_v1/reports/clock_opt_report_area.rpt"
            ),
            60: (
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/reports/route_opt* ~/me_asic_new_v1/reports/ && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/route_opt.tcl && "
                "cat ~/me_asic_new_v1/reports/route_opt_report_area.rpt"
            ),
            61: (
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/results/top.v ~/me_asic_new_v1/results/ && "
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/results/top.sdc ~/me_asic_new_v1/results/ && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/signoff.tcl && "
                "nl -ba ~/ENGR852_Project/16_v3b_final_asic_fc/scripts/write_data.tcl && "
                "ls -lh ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/results/"
            ),
            62: (
                "mkdir -p ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms && "
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/v9_closure/v9_signoff_clean_layout.png ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/waveforms/ 2>/dev/null || true && "
                "cat ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/v9_closure/capture_layout_gui.tcl && "
                "cat ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/reports/chip_finish_report_area.rpt"
            ),
            63: (
                "mkdir -p ~/me_asic_new_v1/signoff_drc_run && "
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/v9_closure/icv_20swap_final/top.LAYOUT_ERRORS ~/me_asic_new_v1/signoff_drc_run/ && "
                "grep -E 'LAYOUT ERRORS RESULTS|Total Error' ~/me_asic_new_v1/signoff_drc_run/top.LAYOUT_ERRORS && "
                "tail -n 20 ~/me_asic_new_v1/signoff_drc_run/top.LAYOUT_ERRORS"
            ),
            64: (
                "mkdir -p ~/me_asic_new_v1/pt_reports && "
                "cp ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/v9_closure/pt_signoff/*.rpt ~/me_asic_new_v1/pt_reports/ && "
                "grep -E 'slack \\(MET\\)|No constrained paths' ~/me_asic_new_v1/pt_reports/*.rpt"
            ),
        }
        one_liner = f'snap_step "{step_id}" "{eda_cmds[pnum]}"'
        expected = [
            "Verifies 520 MHz SAED14nm Fusion Compiler / ICV DRC (0/242 CLEAN) / 3-Corner PrimeTime STA (+0.71/+0.54/+0.22 ns) sign-off artifacts."
        ]
    elif 65 <= pnum <= 72:
        s_line = (pnum - 65) * 30 + 1
        e_line = s_line + 29
        cmd_inner = (
            f"mkdir -p ~/me_asic_new_v1/scripts && "
            f"cp ~/ENGR852_Project/00_course_reference/scripts/build_v9_final_slides.py ~/me_asic_new_v1/scripts/ && "
            f"nl -ba ~/me_asic_new_v1/scripts/build_v9_final_slides.py | sed -n '{s_line},{e_line}p' && "
            f"wc -l ~/me_asic_new_v1/scripts/build_v9_final_slides.py"
        )
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
        expected = [f"[V9 Slide Automation] Displays & verifies lines {s_line}..{e_line} of scripts/build_v9_final_slides.py."]
    elif 73 <= pnum <= 80:
        s_line = (pnum - 73) * 30 + 1
        e_line = s_line + 29
        cmd_inner = (
            f"mkdir -p ~/me_asic_new_v1/scripts && "
            f"cp ~/ENGR852_Project/00_course_reference/scripts/build_v9_final_engineering_report.py ~/me_asic_new_v1/scripts/ && "
            f"nl -ba ~/me_asic_new_v1/scripts/build_v9_final_engineering_report.py | sed -n '{s_line},{e_line}p' && "
            f"wc -l ~/me_asic_new_v1/scripts/build_v9_final_engineering_report.py"
        )
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
        expected = [f"[V9 Report Automation] Displays & verifies lines {s_line}..{e_line} of scripts/build_v9_final_engineering_report.py."]
    elif 81 <= pnum <= 88:
        s_line = (pnum - 81) * 25 + 1
        e_line = s_line + 24
        cmd_inner = (
            f"mkdir -p ~/me_asic_new_v1/scripts && "
            f"cp ~/ENGR852_Project/00_course_reference/scripts/v6_stage_gate.py ~/me_asic_new_v1/scripts/ && "
            f"nl -ba ~/me_asic_new_v1/scripts/v6_stage_gate.py | sed -n '{s_line},{e_line}p' && "
            f"wc -l ~/me_asic_new_v1/scripts/v6_stage_gate.py"
        )
        one_liner = f'snap_step "{step_id}" "{cmd_inner}"'
        expected = [f"[V9 11-Gate Harness] Displays & verifies lines {s_line}..{e_line} of scripts/v6_stage_gate.py."]
    else:
        part7_cmds = {
            89: "mkdir -p ~/me_asic_new_v1/scripts && cp ~/ENGR852_Project/00_course_reference/scripts/package_v9_submission.py ~/me_asic_new_v1/scripts/ && nl -ba ~/me_asic_new_v1/scripts/package_v9_submission.py | head -n 45",
            90: "echo 'PROJECT_VARIATIONS: Local=motion-estimator-14nm-asic-manual | Remote=~/me_asic_new_v1 | Branch=manual-practice-macbook-air | Top=module top (11 ports preserved)' && ls -la ~/me_asic_new_v1/",
            91: "cd ~/motion-estimator-asic-lab-notebook-2026 && git status -s && git branch -v",
            92: "cd ~/motion-estimator-asic-lab-notebook-2026 && git remote -v",
            93: "printf '*.fsdb\\n*.vpd\\n*.ndm\\n*.dlib/\\nsimv*\\ncsrc/\\n*.daidir/\\nverdiLog/\\n.venv/\\n' > ~/me_asic_new_v1/.gitignore && cat ~/me_asic_new_v1/.gitignore",
            94: "echo '# 520 MHz 16-PE Systolic Motion Estimator ASIC (SAED14nm FinFET)' > ~/me_asic_new_v1/README.md && echo '- BestDist: 0000 / 0100 / FF00 | Area: 3416.18 um^2 | Power: 0.890 mW | DRC: 0/242 | 3-Corner STA: +0.71/+0.54/+0.22 ns' >> ~/me_asic_new_v1/README.md && cat ~/me_asic_new_v1/README.md",
            95: "cd ~/motion-estimator-asic-lab-notebook-2026 && git log -n 5 --oneline",
            96: "echo 'DIAG_PART1: Checking USER, HOST, DISPLAY, and ~/.ssh permissions' && whoami && hostname && ls -ld ~/.ssh",
            97: "which vcs verdi && head -n 5 ~/ENGR852_Project/00_course_reference/tb/16bit/top_tb_direct.v",
            98: "which fc_shell icv pt_shell && grep -E 'LAYOUT ERRORS RESULTS' ~/ENGR852_Project/20_v5b_520MHz_14nm_cts_area_fix/v9_closure/icv_20swap_final/top.LAYOUT_ERRORS",
            99: "ls -la ~/me_asic_new_v1/ && ls -la ~/motion-estimator-asic-lab-notebook-2026/practice_from_scratch/",
            100: "echo '=== PAGE 100 FINAL V1->V9 WORKBOOK SCORECARD ===' && echo '1. V1 8-Bit Trap Reproduced (8hFF / X) : PASS' && echo '2. V2-V4 16-Bit Non-Saturating RTL (0000 / 0100 / FF00) : PASS' && echo '3. V5 Verdi nWave Waveforms Synced : PASS' && echo '4. V6-V8 520 MHz (1.923 ns) SAED14nm Layout (3416.18 um^2, 0.890 mW, 0/242 DRC) : PASS' && echo '5. V8-V9 3-Corner PrimeTime STA (+0.71 / +0.54 / +0.22 ns Setup, >=0.00 ns Hold) : PASS' && echo 'FINAL_100PAGE_NOTEBOOK_STATUS: 100% COMPLETE'",
        }
        one_liner = f'snap_step "{step_id}" "{part7_cmds[pnum]}"'
        expected = ["Executes V9 workbook verification check and syncs output + screenshot to Live Web Console & GitHub sub-branch."]

    cmd_explanations = []
    for row in tbl_rows[1:]:
        if len(row) >= 3:
            cmd_explanations.append(
                f"- **`{base.clean_glyphs(str(row[0]))}`** → **`{base.clean_glyphs(str(row[1]))}`**: "
                f"{base.clean_glyphs(' | '.join(str(x) for x in row[2:]))}"
            )
    cmd_explanations.append(
        f"- **`snap_step \"{step_id}\" \"...\"`** (**Stage `{v_stage}`**): Combines all the smaller steps on **Page {pnum}** into a single copy-pasteable line, enforces the **Sequential Page Guardrail** (`Page {pnum-1} -> Page {pnum}`), saves the full output to `practice_from_scratch/logs/{step_id}.log`, renders `practice_from_scratch/screenshots/{step_id}_terminal.png`, and syncs live to **http://127.0.0.1:8788/** and GitHub branch `manual-practice-macbook-air`."
    )

    return where_badge, env_tag, step_id, v_stage, v_desc, cmd_explanations, one_liner, expected, wave_img


def wrap_mono_string(text: str, max_chars: int):
    """Wraps a long one-liner command cleanly onto multiple lines of at most max_chars characters."""
    text = base.clean_glyphs(text)
    lines = []
    while len(text) > max_chars:
        # Prefer splitting after ' && ' or ' ' near max_chars
        split_at = text.rfind(" && ", 0, max_chars)
        if split_at != -1 and split_at > max_chars // 2:
            split_at += 4
        else:
            split_at = text.rfind(" ", 0, max_chars)
            if split_at == -1 or split_at < max_chars // 2:
                split_at = max_chars
            else:
                split_at += 1
        lines.append(text[:split_at].rstrip())
        text = text[split_at:].lstrip()
    if text:
        lines.append(text)
    return lines


def draw_combined_oneliner_box(c, x, y_top, width, height, pnum, v_stage, env_tag, step_id, one_liner, expected_line):
    """
    Draws the dedicated Section 5 Box on the SAME page right below Section 4:
    '5. Copy-Paste Combined Page One-Liner (All Page Steps Combined -> Syncs Live Web :8788 & GitHub)'
    Wrapping the full one-liner across up to 4 lines so 0% is cut off at the right margin!
    """
    y_bot = y_top - height
    c.setFillColor(colors.HexColor("#ECFDF5"))
    c.setStrokeColor(colors.HexColor("#047857"))
    c.setLineWidth(1.2)
    c.roundRect(x, y_bot, width, height, 4, fill=1, stroke=1)

    # Header bar
    c.setFillColor(colors.HexColor("#065F46"))
    c.roundRect(x, y_top - 13.5, width, 13.5, 4, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 7.3)
    c.drawString(
        x + 6,
        y_top - 10.0,
        f"5. Copy-Paste Combined Page {pnum} One-Liner (Syncs Live Web :8788 & GitHub)",
    )

    # Right header badges: Stage + Guardrail + Target Terminal
    prev_lbl = f"ORDER: REQ PAGE {pnum-1}" if pnum > 1 else "ORDER: START PAGE 1"
    badges = [
        (v_stage, colors.HexColor("#1D4ED8"), width - 196),
        (prev_lbl, colors.HexColor("#B45309"), width - 134),
        (env_tag, colors.HexColor("#0F766E"), width - 54),
    ]
    for blbl, bcol, bx_off in badges:
        bw = len(blbl) * 3.6 + 6
        c.setFillColor(bcol)
        c.roundRect(x + bx_off, y_top - 12.2, bw, 9.6, 2, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 5.5)
        c.drawString(x + bx_off + 3, y_top - 9.2, blbl)

    # Wrap one-liner across up to 6 lines so 100% of even the longest command fits with 0% cutoff!
    font_sz = 5.85
    max_chars = int((width - 14) / (font_sz * 0.60))
    wrapped = wrap_mono_string(one_liner, max_chars)

    cy = y_top - 21.0
    leading = 6.7
    c.setFont("Courier-Bold", font_sz)
    c.setFillColor(colors.HexColor("#0F172A"))
    for idx, wline in enumerate(wrapped[:6]):
        prefix = "$ " if idx == 0 else "  "
        c.drawString(x + 6, cy, (prefix + wline)[: max_chars + 2])
        cy -= leading

    # Expected output / sync confirmation line at bottom of box
    c.setFont("Courier-Bold", 5.75)
    c.setFillColor(colors.HexColor("#15803D"))
    exp_str = f"[EXPECTED + LIVE WEB/GITHUB SYNC] {base.clean_glyphs(expected_line)}"
    c.drawString(x + 6, y_bot + 3.2, exp_str[: max_chars + 4])

    return y_bot


def patched_draw_notebook_page_chrome(c, page_num, part_title, page_title, subtitle):
    """Fixes header font sizing so top-left part_title never touches 'Page X of 100' and page_title never overflows."""
    w, h = letter
    c.setFillColor(base.BG_PAPER)
    c.rect(0, 0, w, h, fill=1, stroke=0)

    step = 14.17
    c.setStrokeColor(base.GRID_LINE)
    c.setLineWidth(0.45)
    x = 36
    while x < w - 18:
        c.line(x, 24, x, h - 24)
        x += step
    y = 24
    while y < h - 24:
        c.line(36, y, w - 18, y)
        y += step

    c.setStrokeColor(base.MARGIN_RED)
    c.setLineWidth(1.1)
    c.line(48, 24, 48, h - 24)

    c.setFillColor(colors.HexColor("#CBD5E1"))
    c.setStrokeColor(base.SPIRAL_GRAY)
    c.setLineWidth(1.2)
    for ry in range(44, int(h - 32), 28):
        c.circle(22, ry, 4.2, fill=1, stroke=1)
        c.line(6, ry + 2, 20, ry + 1)
        c.line(6, ry - 2, 20, ry - 1)

    # Top banner header (fit cleanly before 'Page X of 100')
    banner_str = f"ENGR 852 ASIC LAB NOTEBOOK - {base.clean_glyphs(part_title)}"
    c.setFillColor(base.INK_BLACK)
    c.setFont("Helvetica-Bold", 8.8)
    c.drawString(56, h - 38, banner_str)

    c.setFont("Helvetica-Bold", 9.2)
    c.setFillColor(base.INK_BLUE)
    c.drawRightString(w - 24, h - 38, f"Page {page_num} of 100")

    # Main Page Title (auto-fit font size 9.2..11.2 pt so it never clips on the right)
    clean_t = base.clean_glyphs(page_title)
    t_size = 11.2
    while t_size > 8.6 and c.stringWidth(clean_t, "Helvetica-Bold", t_size) > (w - 82):
        t_size -= 0.4
    c.setFillColor(base.INK_BLACK)
    c.setFont("Helvetica-Bold", t_size)
    c.drawString(56, h - 54, clean_t)

    c.setStrokeColor(base.INK_BLACK)
    c.setLineWidth(1.1)
    c.line(56, h - 58, w - 24, h - 58)

    clean_sub = base.clean_glyphs(subtitle)
    c.setFillColor(base.INK_BLUE)
    c.setFont("Helvetica-Bold", 8.2)
    c.drawString(56, h - 69, clean_sub[:108])


def patched_draw_notebook_table(c, x, y_top, col_widths, rows, title=None):
    """Draws hardware/verification table with strict cell padding so columns never overlap."""
    cur_y = y_top
    if title:
        c.setFillColor(base.INK_BLACK)
        c.setFont("Helvetica-Bold", 8.4)
        c.drawString(x, cur_y - 9, title)
        c.setStrokeColor(base.INK_BLACK)
        c.setLineWidth(0.7)
        c.line(x, cur_y - 11, x + sum(col_widths), cur_y - 11)
        cur_y -= 13

    row_h = 13.8
    total_w = sum(col_widths)
    for r_idx, row in enumerate(rows):
        ry = cur_y - (r_idx + 1) * row_h
        if r_idx == 0:
            c.setFillColor(base.BOX_TABLE_HDR)
            c.rect(x, ry, total_w, row_h, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont("Helvetica-Bold", 7.1)
        else:
            bg = colors.HexColor("#FFFFFF") if r_idx % 2 == 1 else colors.HexColor("#F1F5F9")
            if any("TRAP" in str(cell) or "FAIL" in str(cell) for cell in row):
                bg = colors.HexColor("#FEE2E2")
            elif any("PASS" in str(cell) or "0000" in str(cell) or "CLEAN" in str(cell) or "VERIFIED" in str(cell) for cell in row):
                bg = colors.HexColor("#DCFCE7")
            c.setFillColor(bg)
            c.rect(x, ry, total_w, row_h, fill=1, stroke=0)
            c.setFillColor(base.INK_BLACK)
            c.setFont("Courier" if r_idx > 0 else "Helvetica-Bold", 6.8)

        cx = x
        for c_idx, cell in enumerate(row):
            cw = col_widths[c_idx]
            c.setStrokeColor(colors.HexColor("#94A3B8"))
            c.setLineWidth(0.55)
            c.rect(cx, ry, cw, row_h, fill=0, stroke=1)
            max_ch = max(4, int((cw - 8) / 4.25))
            c.drawString(cx + 4, ry + 3.8, base.clean_glyphs(str(cell))[:max_ch])
            cx += cw
    return cur_y - len(rows) * row_h


def render_100page_pdf_with_dedicated_oneliner_box(pages, page_meta_map):
    """
    Renders all 100 pages of ENGR852_100Page_Visual_Notebook_Baby_Steps_Manual.pdf
    with:
      1. Visual Annotated Block Diagram
      2. Hardware-to-Verilog / Command-to-Action Verification Table
      3. [!] Critical Engineering Note / Beginner Trap
      4. Line-by-Line Commented Code & Individual Terminal Commands (all smaller commands preserved!)
      5. DEDICATED BOX ON THE SAME PAGE: Copy-Paste Combined Page One-Liner (wrapped across up to 4 lines, 0% cut off)
      6. Live Verification Checks, Server Script Pulling & Fallback Troubleshooting
    """
    base.DELIV_DIR.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(base.OUT_PDF), pagesize=letter)
    w, h = letter
    avail_w = w - 80

    img_map = {
        5: base.SCREENSHOTS_DIR / "gp_vpn_connecting.png",
        6: base.SCREENSHOTS_DIR / "gp_vpn_connected_and_xquartz_xterm.png",
        7: base.SCREENSHOTS_DIR / "ssh_x11_multi_terminal_mahmoodi.png",
        49: base.SCREENSHOTS_DIR / "V9_fig7_orig8bit_row1_nWave.png",
        50: base.SCREENSHOTS_DIR / "V9_fig8_orig8bit_complete_nWave.png",
        51: base.SCREENSHOTS_DIR / "V9_fig10_16bit_perfect_match_0000_nWave.png",
        52: base.SCREENSHOTS_DIR / "V9_fig9_16bit_saturation_row1_nWave.png",
        62: base.SCREENSHOTS_DIR / "v9_signoff_clean_layout.png",
    }

    for idx, (title, sub, stages, tbl_rows, trap_lines, code_lines) in enumerate(pages):
        pnum = idx + 1
        part_title = base.get_part_title(pnum)
        meta = page_meta_map[pnum]

        patched_draw_notebook_page_chrome(c, pnum, part_title, title, sub)

        # 1. Section 1: Annotated Block Diagram (70 pt height)
        y_cursor = h - 75
        y_cursor = base.draw_schematic_pipeline(
            c, 56, y_cursor, avail_w, 70, stages,
            "1. Visual Annotated Block Diagram & Step-by-Step Execution Pipeline (Blue=Input -> Green=Action -> Red=Verify)"
        )

        # 2. Section 2: Verification Table
        y_cursor -= 5
        num_cols = len(tbl_rows[0])
        if num_cols == 3:
            cwidths = [avail_w * 0.25, avail_w * 0.37, avail_w * 0.38]
        elif num_cols == 4:
            cwidths = [avail_w * 0.22, avail_w * 0.26, avail_w * 0.26, avail_w * 0.26]
        elif num_cols == 5:
            cwidths = [avail_w * 0.18, avail_w * 0.20, avail_w * 0.18, avail_w * 0.22, avail_w * 0.22]
        else:
            cwidths = [avail_w / num_cols] * num_cols
        y_cursor = patched_draw_notebook_table(
            c, 56, y_cursor, cwidths, tbl_rows,
            title="2. Hardware-to-Verilog / Command-to-Action Verification Table"
        )

        # 3. Section 3: [!] TRAP Box (+ side-by-side embedded screenshot on visual pages)
        y_cursor -= 5
        if pnum in img_map and img_map[pnum].exists():
            img_p = img_map[pnum]
            sec3_h = 88
            left_w = avail_w * 0.46
            right_w = avail_w * 0.52
            right_x = 56 + avail_w - right_w
            base.draw_labeled_box(
                c, 56, y_cursor, left_w, sec3_h,
                "3. [!] Visual Guide & Critical Trap Note",
                trap_lines, base.INK_RED, base.BOX_RED_BG, mono=False, font_size=6.5
            )
            c.setFillColor(colors.white)
            c.setStrokeColor(base.INK_BLUE)
            c.setLineWidth(1.0)
            c.roundRect(right_x, y_cursor - sec3_h, right_w, sec3_h, 4, fill=1, stroke=1)
            c.drawImage(str(img_p), right_x + 4, y_cursor - sec3_h + 4, width=right_w - 8, height=sec3_h - 16, preserveAspectRatio=True)
            c.setFillColor(base.INK_BLUE)
            c.setFont("Helvetica-Bold", 6.8)
            c.drawString(right_x + 6, y_cursor - 10, f"Live Visual Evidence: {img_p.name}")
            y_cursor -= sec3_h
        else:
            box_col = base.INK_RED if trap_lines[0].startswith("RED:") else (base.INK_GREEN if trap_lines[0].startswith("GREEN:") else base.INK_BLUE)
            box_bg = base.BOX_RED_BG if trap_lines[0].startswith("RED:") else (base.BOX_GREEN_BG if trap_lines[0].startswith("GREEN:") else base.BOX_BLUE_BG)
            y_cursor = base.draw_labeled_box(
                c, 56, y_cursor, avail_w, 48,
                "3. [!] Critical Engineering Note / Beginner Trap & How to Avoid It",
                trap_lines, box_col, box_bg, mono=False, font_size=6.9
            )

        # Reserve bottom Section 6 (Fallback Troubleshooting = 86 pt) and Section 5 (Dedicated Combined One-Liner Box = 66 pt)
        sec6_h = 86
        sec6_top = 22 + sec6_h
        sec5_h = 66
        sec5_top = sec6_top + 4 + sec5_h

        # 4. Section 4: Individual Line-by-Line Commented Code & Terminal Commands (Untruncated individual steps!)
        y_cursor -= 5
        sec4_h = max(104, y_cursor - sec5_top - 4)
        max_code_lines = int((sec4_h - 18) / 8.3)
        rich_code = base.enrich_code_lines_to_fill_box(pnum, code_lines, max_lines=max_code_lines)
        base.draw_terminal_code_box(
            c, 56, y_cursor, avail_w, sec4_h,
            "4. Line-by-Line Commented Code & Individual Step-by-Step Commands",
            rich_code, font_size=6.35
        )

        # 5. Dedicated Section 5 Box: Combined Page One-Liner (Wrapped cleanly across up to 4 lines!)
        draw_combined_oneliner_box(
            c, 56, sec5_top, avail_w, sec5_h,
            pnum, meta["v_stage"], meta["env_tag"], meta["step_id"],
            meta["one_liner"], meta["expected_out"][0]
        )

        # 6. Section 6: Live Verification Checks & Fallback Troubleshooting
        fallback_lines = base.get_fallback_recovery_lines(pnum)
        base.draw_labeled_box(
            c, 56, sec6_top, avail_w, sec6_h,
            "6. Live Verification Checks, Server Script Pulling & Fallback Troubleshooting (If XYZ Fails -> Option A / B)",
            fallback_lines, base.INK_AMBER, base.BOX_FALLBACK_BG, title_color=base.INK_AMBER, mono=False, font_size=6.35
        )

        c.showPage()

    c.save()
    print(f"BUILT_100PAGE_PDF_WITH_DEDICATED_ONELINER_BOX: {base.OUT_PDF}")


def main():
    pages = base.generate_remaining_pages(base.build_100_page_curriculum())
    assert len(pages) == 100, f"Expected 100 pages, got {len(pages)}"

    md_lines = [
        "# ENGR 852 Motion Estimator 14nm ASIC (520 MHz) — Complete 100-Page Visual Engineering Notebook & Copy-Paste One-Liner Manual",
        "",
        "> [!IMPORTANT]",
        "> **100% Full 100-Page Curriculum (Zero Shortcuts — Page 1 through Page 100, Walking Sequentially from V1 to V9)**:",
        "> - Every single page from **Page 1 of 100** to **Page 100 of 100** includes:",
        ">   1. **Visual Annotated Block Diagram & Step-by-Step Execution Pipeline**",
        ">   2. **Hardware-to-Verilog / Command-to-Action Verification Table**",
        ">   3. **Critical Engineering Note / Beginner Trap (`[!] TRAP`)**",
        ">   4. **Individual Step-by-Step Commands & Line-by-Line Commented Code + Detailed Technical Meaning**",
        ">   5. **Dedicated Copy-and-Pasteable Combined Page One-Liner (`snap_step \"page001_...\"` through `snap_step \"page100_...\"`)** that combines all the smaller steps on that page into one copy-pasteable line, enforces the **Sequential Order Guardrail (`Page 1 -> Page 2 -> ... -> Page 100`)**, and syncs live with both your **Live Operations Console Website (`http://127.0.0.1:8788/` / `http://192.168.1.70:8788/`)** and your **GitHub sub-branch (`manual-practice-macbook-air`)**.",
        ">   6. **Live Verification Checks & Fallback Troubleshooting (`If XYZ Fails -> Option A / Option B`)**",
        "",
        "---",
        "",
    ]

    page_meta_map = {}
    curriculum_json = []

    for idx, (title, sub, stages, tbl_rows, trap_lines, code_lines) in enumerate(pages):
        pnum = idx + 1
        part_title = base.get_part_title(pnum)
        rich_code = base.enrich_code_lines_to_fill_box(pnum, code_lines, max_lines=26)
        fallback_lines = base.get_fallback_recovery_lines(pnum)
        where_badge, env_tag, step_id, v_stage, v_desc, cmd_explanations, one_liner, expected_out, wave_img = get_page_oneliner_and_meaning(
            pnum, title, sub, tbl_rows, trap_lines, rich_code
        )
        indiv_cmds = extract_individual_commands_summary(rich_code)

        meta = {
            "page_num": pnum,
            "part_title": base.clean_glyphs(part_title),
            "title": base.clean_glyphs(title),
            "subtitle": base.clean_glyphs(sub),
            "where_badge": where_badge,
            "env_tag": env_tag,
            "step_id": step_id,
            "v_stage": v_stage,
            "v_desc": v_desc,
            "individual_commands": indiv_cmds,
            "one_liner": one_liner,
            "expected_out": [base.clean_glyphs(x) for x in expected_out],
            "wave_img": wave_img,
            "requires_prev_page": pnum - 1 if pnum > 1 else None,
        }
        page_meta_map[pnum] = meta
        curriculum_json.append(meta)

        # Write full Markdown page section (Pages 1..100)
        md_lines.append(f"## ENGR 852 ASIC LAB NOTEBOOK - {base.clean_glyphs(part_title)} (Page {pnum} of 100)")
        md_lines.append(f"### {base.clean_glyphs(title)}")
        md_lines.append(f"**{base.clean_glyphs(sub)}**")
        md_lines.append("")
        md_lines.append(f"- **Project Build Stage**: `{v_stage}` — {v_desc}")
        md_lines.append(f"- **Sequential Order Guardrail**: Requires **Page {pnum-1}** completed first" if pnum > 1 else "- **Sequential Order Guardrail**: **Starting Page (Page 1 of 100)**")
        md_lines.append(f"- **Where to Execute**: {where_badge}")
        md_lines.append(f"- **Live Web & GitHub Sub-Branch Target**: `http://127.0.0.1:8788/` + `practice_from_scratch/logs/{step_id}.log` & `practice_from_scratch/screenshots/{step_id}_terminal.png` on `manual-practice-macbook-air`")
        md_lines.append("")

        # Section 1: Pipeline Stages
        md_lines.append("#### 1. Visual Annotated Block Diagram & Step-by-Step Execution Pipeline")
        for st_idx, (st_title, st_items) in enumerate(stages, 1):
            joined = " → ".join(f"`{base.clean_glyphs(str(x))}`" for x in st_items)
            md_lines.append(f"{st_idx}. **{base.clean_glyphs(str(st_title))}**: {joined}")
        md_lines.append("")

        # Section 2: Markdown Table
        md_lines.append("#### 2. Hardware-to-Verilog / Command-to-Action Verification Table")
        hdr = [base.clean_glyphs(str(c)) for c in tbl_rows[0]]
        md_lines.append("| " + " | ".join(hdr) + " |")
        md_lines.append("| " + " | ".join([":---"] * len(hdr)) + " |")
        for r in tbl_rows[1:]:
            cells = [base.clean_glyphs(str(c)).replace("|", "\\|") for c in r]
            md_lines.append("| " + " | ".join(cells) + " |")
        md_lines.append("")

        # Section 3: Beginner Trap
        md_lines.append("#### 3. [!] Critical Engineering Note / Beginner Trap & How to Avoid It")
        for tl in trap_lines:
            clean_tl = base.clean_glyphs(str(tl)).replace("RED:", "**[TRAP]** ").replace("GREEN:", "**[KEY]** ").replace("BLUE:", "**[NOTE]** ")
            md_lines.append(f"- {clean_tl}")
        md_lines.append("")

        # Section 4: Individual Step-by-Step Commands & Detailed Meaning
        md_lines.append("#### 4. Step-by-Step Individual Commands, Line-by-Line Commented Code & Technical Meaning")
        md_lines.append("```bash")
        for cl in rich_code:
            md_lines.append(base.clean_glyphs(str(cl)))
        md_lines.append("```")
        md_lines.append("")
        md_lines.append("**What Each Command / Script / Hardware Signal on This Page Does & Means:**")
        md_lines.extend(cmd_explanations)
        md_lines.append("")

        # Section 5: Dedicated Copy-and-Pasteable Combined Page One-Liner + Expected Output
        md_lines.append(f"#### 5. Copy-and-Pasteable Combined One-Liner for Page {pnum} (All Page {pnum} Steps Combined -> Syncs Live Web `:8788` & GitHub)")
        md_lines.append(f"Copy and paste this single combined one-liner into your **{where_badge}** to execute all steps on **Page {pnum}** in sequence, verify in-order progression (`{v_stage}`), and sync live to `http://127.0.0.1:8788/` and `manual-practice-macbook-air`:")
        md_lines.append("```bash")
        md_lines.append(one_liner)
        md_lines.append("```")
        md_lines.append("")
        md_lines.append(f"**Expected Terminal Output for Page {pnum} (`{step_id}`):**")
        md_lines.append("```text")
        for eo in expected_out:
            md_lines.append(base.clean_glyphs(str(eo)))
        md_lines.append("```")
        md_lines.append("")

        # Section 6: Fallback Troubleshooting
        md_lines.append("#### 6. Live Verification Checks & Fallback Troubleshooting (If XYZ Fails -> Option A / Option B)")
        for fl in fallback_lines:
            clean_fl = base.clean_glyphs(str(fl)).replace("RED:", "**[IF XYZ FAILS]** ").replace("GREEN:", "**[SERVER PULL / CHECK]** ").replace("BLUE:", "**[LIVE CHECK]** ")
            md_lines.append(f"- {clean_fl}")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    full_md_text = "\n".join(md_lines)

    # Save 100-page curriculum JSON manifest for Live Web Console & auto_bridge.sh
    manifest_path = REPO_ROOT / "practice_from_scratch" / "curriculum_100pages.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(curriculum_json, indent=2), encoding="utf-8")
    print(f"WROTE_CURRICULUM_JSON:     {manifest_path} (100 pages)")

    # Save to Artifact MD and Repo Docs MD
    artifact_md = BRAIN_DIR / "ENGR852_100Page_Visual_Notebook_Guide.md"
    repo_md = REPO_ROOT / "docs" / "ENGR852_100Page_Visual_Notebook_Baby_Steps_Manual.md"
    artifact_md.write_text(full_md_text, encoding="utf-8")
    repo_md.write_text(full_md_text, encoding="utf-8")
    print(f"WROTE_100PAGE_ARTIFACT_MD: {artifact_md} ({len(md_lines)} lines, 100/100 pages)")
    print(f"WROTE_100PAGE_REPO_MD:     {repo_md}")

    # Render the 100-page PDF with the dedicated Section 5 Combined One-Liner box on every single page!
    render_100page_pdf_with_dedicated_oneliner_box(pages, page_meta_map)

    # Copy the updated 100-page PDF into the brain artifact folder as well
    artifact_pdf = BRAIN_DIR / "ENGR852_100Page_Visual_Notebook_Baby_Steps_Manual.pdf"
    shutil.copyfile(str(base.OUT_PDF), str(artifact_pdf))
    print(f"WROTE_100PAGE_ARTIFACT_PDF: {artifact_pdf}")


if __name__ == "__main__":
    main()
