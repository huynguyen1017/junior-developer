#!/usr/bin/env python3
"""
Renders a high-resolution recruiter showcase banner for the v3.0 Full-Stack ASIC Web IDE
(`evidence/screenshots/interactive_asic_academy_recruiter_showcase.png`).
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path("/Users/huynguyen/Developer/portfolio/motion-estimator-asic-lab-notebook-2026")
OUT_PNG = REPO_ROOT / "evidence" / "screenshots" / "interactive_asic_academy_recruiter_showcase.png"
OUT_PNG.parent.mkdir(parents=True, exist_ok=True)


def load_font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = [
            "/System/Library/Fonts/SFNSMono.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/Library/Fonts/Courier New.ttf",
        ]
    elif bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    else:
        candidates = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def main():
    W, H = 1600, 960
    img = Image.new("RGB", (W, H), (6, 9, 19))
    draw = ImageDraw.Draw(img)

    f_title = load_font(22, bold=True)
    f_sub = load_font(14, bold=False)
    f_tab = load_font(14, bold=True)
    f_h2 = load_font(18, bold=True)
    f_body = load_font(14, bold=False)
    f_mono = load_font(13, mono=True)
    f_small = load_font(12, bold=True)

    # Top Studio Header
    draw.rectangle([0, 0, W, 68], fill=(10, 15, 30), outline=(45, 58, 84))
    draw.rounded_rectangle([18, 14, 58, 54], radius=10, fill=(59, 130, 246))
    draw.text((27, 23), "ME", font=f_h2, fill=(255, 255, 255))
    draw.text((72, 14), "ENGR 852 · 520 MHz 14nm FinFET ASIC Web IDE & Lab Studio (v3.0 FULL-STACK IDE)", font=f_title, fill=(248, 250, 252))
    draw.text((72, 42), "In-Browser MacBook Air Terminal · Multi-File Verilog/TCL Code Editor · AI Auto-Debugger · 100-Page Manual · 500-Q Mastery", font=f_sub, fill=(148, 163, 184))

    # Right header pills
    draw.rounded_rectangle([1130, 18, 1360, 50], radius=16, fill=(6, 78, 59), outline=(16, 185, 129))
    draw.text((1146, 26), "ORDER GUARD: PAGE 1 VERIFIED ✓", font=f_small, fill=(110, 231, 183))
    draw.rounded_rectangle([1372, 18, 1582, 50], radius=10, fill=(37, 99, 235), outline=(99, 102, 241))
    draw.text((1388, 26), "▶ Run Page in Web Terminal", font=f_small, fill=(255, 255, 255))

    # 7-Tab Ribbon Bar
    draw.rectangle([0, 68, W, 116], fill=(12, 18, 34), outline=(45, 58, 84))
    tabs = [
        ("💻 1. Practice Lab IDE & MacBook Terminal", True),
        ("🚀 2. Launchpad & Step 0 Doctor", False),
        ("📚 3. 100-Page Curriculum (V1→V9)", False),
        ("🎛️ 4. Hardware & 14nm STA Simulators", False),
        ("📈 5. Verdi Waveforms & Layout", False),
        ("🎓 6. 500-Q Quiz & Midterm (Q1–Q10)", False),
        ("🌿 7. GitHub & Portfolio", False),
    ]
    tx = 16
    for label, active in tabs:
        tw = len(label) * 7 + 26
        if active:
            draw.rounded_rectangle([tx, 76, tx + tw, 108], radius=8, fill=(37, 99, 235), outline=(99, 102, 241))
            draw.text((tx + 12, 84), label, font=f_small, fill=(255, 255, 255))
        else:
            draw.rounded_rectangle([tx, 76, tx + tw, 108], radius=8, fill=(17, 26, 46), outline=(51, 65, 85))
            draw.text((tx + 12, 84), label, font=f_small, fill=(148, 163, 184))
        tx += tw + 8

    # Split-Pane Workspace
    # Left Column: Guided Page 1-100 Lab Manual + Sub-Commands + Quiz (x: 20..760)
    draw.rounded_rectangle([20, 132, 765, 938], radius=14, fill=(15, 23, 42), outline=(59, 130, 246))
    draw.text((38, 148), "Page 1 / 100 · V1-PREP · Master Roadmap & Isolated Workspace Setup", font=f_h2, fill=(255, 255, 255))
    draw.rounded_rectangle([38, 180, 745, 234], radius=8, fill=(8, 47, 37), outline=(16, 185, 129))
    draw.text((50, 190), "🌱 Beginner Guide: Click '▶ Paste & Run One-Liner in Web Terminal' to execute directly", font=f_body, fill=(167, 243, 208))
    draw.text((50, 210), "inside the embedded MacBook Air Terminal on the right — or copy to your external Terminal!", font=f_body, fill=(203, 213, 225))

    # One-Liner Box on Left
    draw.rounded_rectangle([38, 246, 745, 368], radius=10, fill=(5, 8, 17), outline=(59, 130, 246))
    draw.text((50, 256), "⚡ COMBINED COPY-PASTE ONE-LINER (PAGE 1)", font=f_small, fill=(147, 197, 253))
    draw.rounded_rectangle([430, 252, 620, 278], radius=6, fill=(16, 185, 129))
    draw.text((442, 258), "▶ Run in Web Terminal", font=f_small, fill=(255, 255, 255))
    draw.rounded_rectangle([628, 252, 735, 278], radius=6, fill=(37, 99, 235))
    draw.text((638, 258), "⌨️ Paste Prompt", font=f_small, fill=(255, 255, 255))
    draw.text((50, 290), 'snap_step "page001_master_roadmap" "mkdir -p ~/Developer/motion-estimator-14nm-asic-manual', font=f_mono, fill=(147, 197, 253))
    draw.text((50, 312), '&& cd ~/Developer/motion-estimator-14nm-asic-manual && mkdir -p rtl/8bit rtl/16bit tb/16bit', font=f_mono, fill=(147, 197, 253))
    draw.text((50, 334), 'constraints scripts docs deliverables && pwd && ls -la"', font=f_mono, fill=(147, 197, 253))

    # Left Sub-Tabs
    subtabs = ["🔬 1. Sub-Commands Lab", "📘 2. Theory & Video", "✅ 3. Verifier Diff", "🎯 4. Page 5-Q Quiz"]
    sx = 38
    for idx, st in enumerate(subtabs):
        stw = 170
        draw.rounded_rectangle([sx, 382, sx + stw, 412], radius=7, fill=(37, 99, 235) if idx == 0 else (17, 26, 46), outline=(99, 102, 241) if idx == 0 else (51, 65, 85))
        draw.text((sx + 10, 390), st, font=f_small, fill=(255, 255, 255) if idx == 0 else (148, 163, 184))
        sx += stw + 7

    # Sub-command cards
    sc_items = [
        ("#1: mkdir -p ~/Developer/motion-estimator-14nm-asic-manual", "Creates 100% isolated practice workspace on MacBook Air without touching main repo."),
        ("#2: mkdir -p rtl/8bit rtl/16bit tb/8bit tb/16bit constraints scripts", "Builds clean directory hierarchy for 8-bit baseline trap (V2) vs 16-bit fix (V3)."),
        ("#3: open -a XQuartz && ssh -Y 926784856@mahmoodi.rcc.at.sfsu.edu", "Verifies X11 socket :0 and tunnels Synopsys Verdi / Fusion Compiler GUI over SSH."),
        ("#4: source scripts/synopsys_setup.tcl && which vcs verdi fc_shell icv pt_shell", "Loads all 5 Synopsys EDA binaries & SAED14nm FinFET libraries in ~/me_asic_new_v1."),
    ]
    sy = 426
    for cmd_t, desc_t in sc_items:
        draw.rounded_rectangle([38, sy, 745, sy + 114], radius=9, fill=(8, 14, 30), outline=(30, 41, 59))
        draw.text((52, sy + 12), cmd_t, font=f_mono, fill=(251, 191, 36))
        draw.rounded_rectangle([585, sy + 8, 732, sy + 34], radius=6, fill=(37, 99, 235))
        draw.text((596, sy + 14), "▶ Run Sub-Command", font=f_small, fill=(255, 255, 255))
        draw.text((52, sy + 46), desc_t, font=f_body, fill=(226, 232, 240))
        draw.text((52, sy + 72), "ENGR 852 Link: Ch. 10 Systolic Motion Estimator & SAED14nm ASIC Sign-Off Flow", font=f_sub, fill=(167, 243, 208))
        sy += 124

    # Right Column Top: Embedded MacBook Air Terminal (x: 785..1580, y: 132..545)
    draw.rounded_rectangle([785, 132, 1580, 545], radius=14, fill=(5, 8, 17), outline=(99, 102, 241))
    draw.rounded_rectangle([785, 132, 1580, 172], radius=14, fill=(30, 41, 59))
    draw.ellipse([802, 146, 814, 158], fill=(255, 95, 86))
    draw.ellipse([822, 146, 834, 158], fill=(255, 189, 46))
    draw.ellipse([842, 146, 854, 158], fill=(39, 201, 63))
    draw.text((870, 144), "huynguyen@MacBook-Air — zsh — ~/Developer/motion-estimator-14nm-asic-manual", font=f_mono, fill=(226, 232, 240))
    draw.rounded_rectangle([1440, 140, 1568, 164], radius=10, fill=(6, 78, 59), outline=(16, 185, 129))
    draw.text((1452, 145), "✓ EXIT 0 (0.24s)", font=f_small, fill=(110, 231, 183))

    term_lines = [
        "huynguyen@MacBook-Air motion-estimator-14nm-asic-manual % snap_step \"page001_master_roadmap\" \"...\"",
        "/Users/huynguyen/Developer/motion-estimator-14nm-asic-manual",
        "drwxr-xr-x  11 huynguyen  staff  352 Nov  9 13:46 .",
        "drwxr-xr-x   4 huynguyen  staff  128 Nov  9 13:46 rtl",
        "drwxr-xr-x   4 huynguyen  staff  128 Nov  9 13:46 tb",
        "drwxr-xr-x   3 huynguyen  staff   96 Nov  9 13:46 constraints",
        "================================================================================",
        "[✓ EXPECTED OUTCOME VERIFIED — PAGE 1 PASS]",
        "    Matched Markers : motion-estimator-14nm-asic-manual, rtl, tb, scripts",
        "    Interactive Lab : UNLOCKED on http://127.0.0.1:8788 (Sub-Commands + 5-Q Quiz)",
        "================================================================================",
        ">>> [AUTO-BRIDGE] Synced log + screenshot + live feedback to Web IDE (:8788) & GitHub!",
    ]
    ty = 186
    for tl in term_lines:
        col = (110, 231, 183) if "VERIFIED" in tl or "AUTO-BRIDGE" in tl else (226, 232, 240)
        draw.text((802, ty), tl, font=f_mono, fill=col)
        ty += 22

    # Terminal Prompt Input Bar
    draw.rectangle([786, 462, 1579, 506], fill=(11, 19, 37), outline=(51, 65, 85))
    draw.text((800, 476), "huynguyen@MacBook-Air %", font=f_mono, fill=(52, 211, 153))
    draw.rounded_rectangle([995, 469, 1345, 499], radius=6, fill=(5, 8, 17), outline=(99, 102, 241))
    draw.text((1005, 476), "Paste Page One-Liner or type command...", font=f_mono, fill=(148, 163, 184))
    draw.rounded_rectangle([1355, 469, 1475, 499], radius=6, fill=(16, 185, 129))
    draw.text((1367, 477), "▶ Execute (Enter)", font=f_small, fill=(255, 255, 255))
    draw.rounded_rectangle([1483, 469, 1570, 499], radius=6, fill=(124, 58, 237))
    draw.text((1493, 477), "🤖 AI Debug", font=f_small, fill=(255, 255, 255))

    # Right Column Bottom: Multi-File Verilog/TCL Code Editor + AI Auto-Debugger (x: 785..1580, y: 560..938)
    draw.rounded_rectangle([785, 560, 1580, 938], radius=14, fill=(15, 23, 42), outline=(51, 65, 85))
    draw.rounded_rectangle([802, 574, 1055, 604], radius=7, fill=(124, 58, 237))
    draw.text((814, 582), "🤖 1. AI Auto-Debugger & Doctor", font=f_small, fill=(255, 255, 255))
    draw.rounded_rectangle([1065, 574, 1340, 604], radius=7, fill=(37, 99, 235))
    draw.text((1077, 582), "📝 2. Verilog / TCL Code Editor (pe.v)", font=f_small, fill=(255, 255, 255))
    draw.rounded_rectangle([1350, 574, 1565, 604], radius=7, fill=(17, 26, 46), outline=(51, 65, 85))
    draw.text((1362, 582), "📸 3. Captured PNG & Log", font=f_small, fill=(148, 163, 184))

    # Split preview inside bottom right: AI Debugger + Verilog Editor
    draw.rounded_rectangle([802, 616, 1564, 756], radius=10, fill=(8, 14, 30), outline=(16, 185, 129))
    draw.text((818, 628), "✓ AI VERIFIER & AUTO-DEBUGGER: ALL EXPECTED MARKERS MATCHED (EXIT CODE 0)", font=f_small, fill=(110, 231, 183))
    draw.text((818, 652), "AI Diagnosis: Isolated workspace ~/Developer/motion-estimator-14nm-asic-manual verified.", font=f_body, fill=(226, 232, 240))
    draw.text((818, 676), "1-Click Self-Healing Repair Command Ready if any marker fails on MacBook Air or mahmoodi!", font=f_body, fill=(147, 197, 253))
    draw.rounded_rectangle([818, 704, 1140, 738], radius=7, fill=(16, 185, 129))
    draw.text((832, 714), "🛠️ Inject & Run AI Auto-Fix in Web Terminal", font=f_small, fill=(255, 255, 255))

    draw.rounded_rectangle([802, 768, 1564, 924], radius=10, fill=(5, 8, 17), outline=(59, 130, 246))
    draw.text((818, 778), "📄 rtl/16bit/pe.v (16-Bit Processing Element — Editable in Browser IDE + 1-Click Compile & Sim)", font=f_small, fill=(147, 197, 253))
    code_lines = [
        "module PE (input wire clock, input wire [7:0] R, S1, S2, input wire S1S2mux, newDist,",
        "           output reg [15:0] Accumulate, output reg [7:0] Rpipe);",
        "    wire [7:0] S_sel = S1S2mux ? S1 : S2;",
        "    wire [7:0] abs_diff = (R > S_sel) ? (R - S_sel) : (S_sel - R);",
        "    always @(posedge clock) Accumulate <= newDist ? {8'd0, abs_diff} : Accumulate + {8'd0, abs_diff};",
    ]
    cy = 804
    for cl in code_lines:
        draw.text((818, cy), cl, font=f_mono, fill=(226, 232, 240))
        cy += 21

    img.save(OUT_PNG, "PNG")
    print(f"Saved v3 showcase banner -> {OUT_PNG}")


if __name__ == "__main__":
    main()
