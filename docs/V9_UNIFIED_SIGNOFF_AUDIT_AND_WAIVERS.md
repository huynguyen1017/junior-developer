# ENGR 852 · V4→V9 Unified Sign-Off Audit, Evidence Provenance & Technical Waivers (`v7.0`)

## 1. Executive Summary & Architectural Provenance (`V4 → V9`)

| Milestone | Key Engineering Change | Verified Evidence Artifact (on `main` @ `fcc7d39`) | Evidence Class |
| :--- | :--- | :--- | :--- |
| **V1–V2 (8-Bit Overflow Discovery)** | Reproduced `Accumulate[7:0]` saturation at `8'hFF` (`255`) when `256` pixels exceed 8-bit unsigned capacity, causing `BestDist < 8'hFF` to fail and leaving `motionX`/`motionY` unupdated (`xx`). | `evidence/v9_signoff/waveforms/V9_fig7_orig8bit_row1_nWave.png`, `V9_fig8_orig8bit_complete_nWave.png` | `IMPORTED_REFERENCE` / `NATIVE_EXECUTION` |
| **V3–V4 (16-Bit Non-Saturating Datapath)** | Upgraded `Accumulate[15:0]` (`pe.v`), `BestDist[15:0]` (`comp.v`), and `top.v` interconnects to 16 bits (`max = 65,535 > 65,280 = 16'hFF00`). Verified across 3 self-checking VCS testbenches (`0000`, `0100`, `FF00`). | `evidence/v9_signoff/logs/vcs_3tb_regression.log` | `IMPORTED_REFERENCE` |
| **V5 (Memory-Macro-Free Port Architecture)** | Removed internal ROM/SRAM macro instantiations from `top.v`, exposing external `AddressR`, `AddressS1`, `AddressS2` buses (`ZERO_SYNTHESIZED_MEMORIES`). | `evidence/v9_signoff/reports/top_qor.rpt` (`8,230` leaf cells, `449` flip-flops, `0` SRAM macros) | `IMPORTED_REFERENCE` |
| **V6–V7 (SAED14nm FinFET Place, CTS & Route)** | Synthesized and routed in Synopsys Fusion Compiler (`W-2024.09-SP2`) targeting `520 MHz` (`1.923 ns` period) within a `125.07 µm × 62.80 µm` (`7,854.40 µm²`) core (`3,416.18 µm²` cell area). | `evidence/v9_signoff/reports/top_utilization.rpt`, `check_routes.rpt` | `IMPORTED_REFERENCE` |
| **V8–V9 (ICV DRC, Connectivity LVS & 3-Corner PrimeTime STA)** | Standalone Synopsys IC Validator (`W-2024.09-3`) `top.LAYOUT_ERRORS` (`0 / 242` DRC errors) and 3-corner PrimeTime (`W-2024.09-SP2`) STA (`FAST`, `TYPICAL`, `SLOW`). | `evidence/v9_signoff/icv/top.LAYOUT_ERRORS`, `evidence/v9_signoff/pt_signoff/*` | `IMPORTED_REFERENCE` |

---

## 2. Explicit Technical Audit of V9 Sign-Off Evidence Gaps & Engineering Waivers

In accordance with **Section I** of the v7.0 Evidence-Integrity Specification, the completed `main` branch (`fcc7d39`) remains **100% untouched**, while the following four technical nuances inside `evidence/v9_signoff/` and `deliverables/ENGR852_V9_Final_Submission_and_Evidence_Bundle.zip` are explicitly documented and disclosed:

### 2.1 PrimeTime 3-Corner STA Coverage Analysis (`21%` Tested Reg-to-Reg vs `79%` Untested Clock-Gating / Constant / Async Arcs)
- **Observed Evidence (`evidence/v9_signoff/pt_signoff/FAST_analysis_coverage.rpt`, `TYPICAL_analysis_coverage.rpt`, `SLOW_analysis_coverage.rpt`)**:
  - `setup`: `5,508` total checks → `1,182` met (`21%`), `0` violated (`0%`), **`4,326` untested (`79%`)**
  - `hold`: `5,508` total checks → `1,182` met (`21%`), `0` violated (`0%`), **`4,326` untested (`79%`)**
  - `out_setup` / `out_hold`: `53` total checks → `51` met (`96%`), `0` violated (`0%`), `2` untested (`4%`)
- **Root-Cause Explanation**:
  - All `449` sequential flip-flops in the 16-PE systolic pipeline have active clock/data pins checked across `1,182` constrained timing endpoints (`0` setup violations, `0` hold violations; worst setup slack `+0.71 ns` FAST, `+0.54 ns` TYPICAL, `+0.22 ns` SLOW; worst hold slack `>= +0.00 ns`).
  - The `4,326` untested checks correspond to unasserted secondary library arcs on multi-input SAED14nm sequential/logic primitives (such as unused scan-enable/test pins, tied control pins, and unexercised conditional path arcs when default SDC constraints are applied without scan-mode case analysis).
  - **Disclosure**: Headline QoR tables must report both the **`0` violated paths (`1,182 / 1,182` tested endpoints met)** and the **`21%` (`1,182 / 5,508`) total arc coverage** rather than implying 100% arc coverage.

### 2.2 PrimeTime `SLOW_violators.rpt` Electrical DRV Waivers (`max_capacitance` & `min_capacitance`)
- **Observed Evidence (`evidence/v9_signoff/pt_signoff/SLOW_violators.rpt`)**:
  1. **`max_capacitance` violation (1 net/pin in SLOW corner)**:
     - Pin `phfnr_buf_2159/X`: Required max capacitance = `16.72 fF`, Actual load capacitance = `17.66 fF`, **Slack = `-0.94 fF` (`VIOLATED`)**.
  2. **`min_capacitance` violations (5 pins in SLOW corner)**:
     - `A1239/X`: Required `0.15 fF`, Actual `0.13 fF`, Slack **`-0.02 fF` (`VIOLATED`)**
     - `v9_cts_ropt_h_inst_17420/X`: Required `0.15 fF`, Actual `0.13 fF`, Slack **`-0.02 fF` (`VIOLATED`)**
     - `v9_cts_copt_gre_h_inst_16725/X`: Required `0.15 fF`, Actual `0.14 fF`, Slack **`-0.01 fF` (`VIOLATED`)**
     - `ctmi_10111/X`: Required `0.15 fF`, Actual `0.14 fF`, Slack **`-0.01 fF` (`VIOLATED`)**
     - `phfnr_buf_2195/X`: Required `0.15 fF`, Actual `0.15 fF`, Slack **`0.00 fF` (`VIOLATED` rounding threshold)**
- **Engineering Assessment & Waiver**:
  - In the `SLOW` (`ss0p72v125c`) corner, `phfnr_buf_2159/X` exceeds its nominal `16.72 fF` library max-capacitance table bound by `0.94 fF` (`5.6%`), yet the path still meets setup timing with **`+0.22 ns` positive setup slack** and `0` max-transition violations. In a production tape-out spin, upsizing `phfnr_buf_2159` by one fin-strength step (`X2 → X4`) or splitting the fanout resolves the `-0.94 fF` excursion.
  - The 5 `min_capacitance` flags (`-0.01` to `-0.02 fF` on short local nets between adjacent standard cells) are benign library table lower-bound warnings where actual wire+pin load (`0.13–0.15 fF`) is slightly below the characterization table floor (`0.15 fF`), while hold timing is cleanly met (`>= +0.00 ns`).

### 2.3 Fusion Compiler `check_lvs.rpt` vs. Standalone Foundry Schematic-vs-Layout LVS
- **Observed Evidence (`evidence/v9_signoff/reports/check_lvs.rpt`)**:
  - `check_lvs` inside Synopsys Fusion Compiler checks physical netlist connectivity across `8,644` nets (`0` electrical shorts, `0` opens, `0` floating routes).
- **Disclosure**:
  - `check_lvs.rpt` is **Fusion Compiler's internal layout connectivity / open-short verification**, whereas `evidence/v9_signoff/icv/top.LAYOUT_ERRORS` is **standalone Synopsys IC Validator (`W-2024.09-3`) physical DRC (`LAYOUT ERRORS RESULTS: CLEAN`)**. Neither should be misrepresented as a standalone third-party Calibre/ICV device-extraction SPICE netlist LVS run.

### 2.4 V9 Submission Bundle (`deliverables/ENGR852_V9_Final_Submission_and_Evidence_Bundle.zip`) Contents
- **Observed Evidence**:
  - The 58-file ZIP archive (`7,162,885` bytes) packages all Verilog RTL (`8-bit` & `16-bit`), 3 self-checking testbenches, SDC constraints, TCL flow scripts, PrimeTime 3-corner reports, IC Validator `top.LAYOUT_ERRORS`, Fusion Compiler QoR/utilization/LVS reports, high-resolution waveform & layout PNGs, and the final DOCX/PDF/PPTX deliverables.
  - Raw proprietary/multi-hundred-megabyte PDK database binaries (`.ndm`, `.gds`, `.fsdb`, `.spef`, `.def`) remain on the SFSU `mahmoodi.rcc.at.sfsu.edu` server (`~/me_asic_new_v1`) rather than inside the GitHub-hosted ZIP archive.
