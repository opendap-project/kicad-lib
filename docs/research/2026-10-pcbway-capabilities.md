# PCBWay manufacturing capabilities mapped to the T1

- **Date:** 2026-10-22
- **Status:** Desk research. Nothing in this report is a decision. Section 4 is a proposal for the maintainers: the PCBWay processes that the KLIB-002 rule sets should target. No rule file is written yet.
- **Scope:** PCBWay's published limits for rigid, HDI, flex and rigid-flex boards, stencils, SMT and BGA assembly, parts sourcing, CNC machining, 3D printing, vacuum casting, sheet metal, injection moulding and finishes, checked against what the T1 needs today.
- **Inputs:** BRD-053, BRD-054, BRD-055 (board requirements), CASE-020 to CASE-022 and CASE-028 (case requirements), KLIB-002, board ADR 0002 (HAT signals over a flat cable), board BOM v1.3, the high-speed I/O topology report, hat-standard HAT interface v0, the T1 faceplate interface, T1-031/T1-032/T1-038, FPT-022, and the spec sheets in `parts` for package pitches.
- **Method:** every PCBWay page listed in [Sources](#sources) was fetched on 2026-10-22 (curl through a public resolver; the local resolver could not resolve `www.pcbway.com`, so the WebFetch tool could not reach it). Figures are copied from those pages and cited by source key, for example [P1]. A figure PCBWay does not publish on those pages is marked **UNVERIFIED**. Arithmetic on published figures (for example a pad gap from a pitch and a land width) is shown as such and is not a PCBWay statement.

## 0. Summary

1. **Covered, at the published limit:** the RK3566 (FCCSP565L, 0.4 mm + 0.6 mm ball pitch). PCBWay's advanced factory states 0.4 mm as its BGA pitch limit (0.5 mm conventional) and a 0.2 mm minimum BGA pad [P10]. Assembly is stated down to 0.3 mm pitch on rigid boards and 0.4 mm on flex, with X-ray [P8]. Escaping a 0.4 mm field needs HDI with laser microvias in the pads; PCBWay offers 1+N+1 to 6+N+6 builds, stacked and staggered microvias, copper-filled vias and any-layer HDI [P2, P3, P1, P16].
2. **Covered:** HDI main board with both sides populated, 0201 and 01005 passives, 0.35 mm QFN (RK809), 0.4 mm DF40 and 0.3 mm FH35C connectors, impedance-controlled pairs on rigid (±10 %) and flex (±7 % above 50 Ω), multilayer FPC up to 12 layers on the capability page (16 on the order form) with FR-4, steel, aluminium or PI stiffeners and EMI shielding film, rigid-flex up to 26 layers, X-ray, conformal coating, step stencils, turnkey parts sourcing, CNC aluminium with Type II and Type III anodising in twelve colours, PC/ABS/PMMA parts by CNC, SLA, vacuum casting and injection moulding.
3. **At the edge of the published tolerances:** the FH35C faceplate tail. Hirose asks for 0.2 ± 0.03 mm at the mating area and a 15.6 ± 0.05 mm outline. PCBWay publishes ±1.2 mil (±0.03 mm) thickness for a two-layer FPC up to 12 mil and ±2 mil (±0.05 mm) laser routing [P5], but no tolerance for a stack that includes a PI stiffener (the cell is empty on the page).
4. **Not named on any page (UNVERIFIED, ask in the DFM review):** shielding-can frames, pogo pins (Harwin P70) as SMT parts, flex and rigid-flex assembly limits beyond "contact us" [P8], coverlay opening rules, copper-to-outline clearance on flex, injection-moulding tolerances and textures.
5. **Not covered:** glass. No PCBWay service lists glass, cover-glass cutting or optical bonding. The closest PCBWay alternative is a polished PMMA or PC window (CNC or SLA clear resin). The custom cover glass that T1-038 allows has to come from another supplier.
6. **Proposed rule sets for KLIB-002** (section 4): `pcbway-hdi` (main board), `pcbway-flex` (HAT flat cable and faceplate cable), `pcbway-rigid-flex` (only if a rigid-flex option is chosen) and `pcbway-multilayer` (device-side piece and rigid faceplate boards with impedance control). The vendored kicad-druid PCBWay set stays for simple 2- to 6-layer boards.

## 1. Capability tables

PCBWay publishes two tiers for rigid boards: "Standard PCB" (quick-turn, [P1] first table) and "Advanced PCB" ([P1] second table, [P2]). The advanced table grades each parameter as normal, medium difficulty, high difficulty or non-standard review. The tables below list the normal value first and the limit after it.

### 1.1 Rigid boards (standard and advanced)

| Parameter | Value | Source |
|---|---|---|
| Layers | Standard 1–14; advanced 3–16 normal, 18–24 medium, ≥ 24 high; up to 64 | P1, P2 |
| Board thickness | Standard 0.2–3.2 mm; advanced 0.21–6.0 mm | P1, P2 |
| Minimum multilayer thickness (through-hole build) | 8 layers ≥ 1.20 mm normal, 1.00 mm medium; 10 layers ≥ 1.40 / 1.20 mm | P1 |
| Thickness tolerance | T ≤ 1.0 mm: ±0.10 mm; 1.6 mm: ±0.18 mm | P1 |
| Outer track/space before compensation, 18 µm copper | ≥ 4/5 mil normal; 4/4 mil medium; locally 3.5/3.5 mil from a BGA-area line to a pad | P1 |
| Outer track/space, 35 µm copper | ≥ 5/6 mil normal; 5/5 mil medium | P1 |
| Inner track/space, 18 µm copper | ≥ 4/4 mil normal; 4/3.5 mil medium | P1 |
| Inner track/space, 35 µm copper | ≥ 4/5 mil normal; 4/4 mil medium | P1 |
| Minimum track/space, advanced | 2/2 mil on parts of the board only (H/H oz inner, 1/3 oz outer) | P2 |
| Track width tolerance | ±20 % normal; ±10 % medium | P1 |
| Mechanical drill | Standard 0.15–6.0 mm; advanced 0.20–6.5 mm normal | P1 |
| Hole size versus board thickness | 0.20 mm up to 1.6 mm thick; 0.25 mm up to 2.0 mm | P1 |
| Aspect ratio (through) | ≤ 8 normal; 20:1 maximum (advanced) | P1, P2 |
| Via annular ring (outer, 18–35 µm) | ≥ 5 mil normal; 4 mil medium; 3 mil minimum (advanced) | P1, P2 |
| Hole to hole, vias ≤ 0.45 mm | ≥ 11 mil | P1 |
| Hole to inner conductor (8 layers) | ≥ 9 mil normal; 7 mil medium; 6 mil high | P1 |
| Hole to conductor (advanced) | 6 mil inner and outer | P2 |
| Copper weights | Outer 1–8 oz, inner 1–4 oz (standard); 1/3 oz base minimum (advanced) | P1, P2 |
| Minimum dielectric | 2 mil (advanced); 50 µm for impedance stack-ups | P2, P12 |
| Impedance tolerance | ±10 %; ±5 Ω at 50 Ω and below | P1, P2 |
| Plugged vias | 0.15 mm (CNC) and 0.10 mm (laser blind/buried) to 0.7 mm | P2 |
| Via-in-pad | Offered; BGA via-in-pad is resin-filled with a plated cap; options "via in pad", "via filled with resin", "all vias filled with resin and capped", "via filled with copper", back drill, custom stack-up | P11, P15, P16 |
| Solder mask | Opening ≥ 2 mil normal, 1 mil only in BGA areas; bridge 4 mil (green, 1 oz); 3 mil minimum (advanced, green), 4 mil (black); IC pads keep a mask bridge from 8 mil pad spacing | P1, P2 |
| BGA pad | Prototype factory ≥ 0.25 mm, pad-to-trace 0.15 mm; advanced factory ≥ 0.2 mm (0.15 mm sample limit), BGA to line 3 mil (2.5 mil prototype limit) | P10 |
| BGA pad by finish | Immersion gold ≥ 11 mil normal, 8 mil medium | P1 |
| BGA pitch | Advanced factory: 0.4 mm limit, 0.5 mm conventional; prototype factory: 0.35 mm pad centre to centre | P2, P10 |
| Line to board edge (milled) | 0.20 mm | P1 |
| Outline tolerance | ±0.2 mm standard; ±0.1 mm advanced | P1, P2 |
| Surface finishes | HASL, lead-free HASL, ENIG, OSP, hard gold, immersion silver, immersion tin, ENEPIG | P1 |
| ENIG thickness | Ni 100–150 µin, Au 1–8 µin normal | P1 |
| Hard gold (gold finger) | Ni 120–150 µin, Au 1–30 µin normal | P1 |
| Materials | FR-4 Tg 140/150/170 (Shengyi S1141, S1000-H, S1000-2/2M), halogen-free, high-speed classes 1–5 G (for example S1165, FR408HR, TU-862), 5–10 G, 10–25 G, > 25 G; Rogers and PTFE | P2, P16 |
| Silkscreen | Line ≥ 0.15 mm, height ≥ 0.8 mm | P1 |
| Acceptance | IPC Class 2 normal; Class 3 on request | P1, P16 |

### 1.2 HDI

| Parameter | Value | Source |
|---|---|---|
| Via types | Blind, buried, through | P3 |
| Builds | 1+N+1, 2+N+2 … 6+N+6 (≥ 6 orders reviewed); the roadmap lists 7+N+7 with stacked and staggered vias; any-layer HDI is "high difficulty" | P1, P2, P3 |
| Layers | Up to 60 (reviewed above 30) | P3 |
| Finished copper | 18–70 µm | P3 |
| Minimum track/space | 0.065/0.065 mm | P3 |
| Thickness | 0.1–8.0 mm (reviewed below 0.2 mm) | P3 |
| Laser drill | 4 mil standard; 3 mil reviewed (single 106 prepreg); 8 mil maximum, dielectric ≤ 0.15 mm | P3 |
| Laser hole (roadmap) | 0.076 mm finished | P2 |
| Mechanical drill | 0.15 mm | P3 |
| Aspect ratio | 14:1 maximum | P3 |
| Resin-filled vias | 0.254–6.5 mm | P3 |
| Solder mask bridge | 4 mil green, 5 mil other colours (≤ 1 oz) | P3 |
| Hole filling | Plating line with "HDI hole filling capability" | P3 |
| Published examples | 8 layers, 3rd order, 1.0 ± 0.1 mm, laser 0.1 mm, mechanical 0.20 mm, 55/55 µm, ENIG + OSP; 10 layers, 2nd order, 1.3 mm, 65/65 µm, ENEPIG; 14 layers any-layer (6th order), 1.6 mm, laser 0.15 mm, 75/75 µm | P3 |
| Availability | HDI from 4 layers | P17 |

PCBWay does not publish a microvia land size or a microvia aspect ratio for rigid HDI (**UNVERIFIED**). The rigid-flex page gives 1:1 for blind holes [P6].

### 1.3 Flex (FPC)

| Parameter | Value | Source |
|---|---|---|
| Layers | 1–12 (capability page); 1–16 (order form) | P5, P13 |
| Base | Polyimide (adhesive and adhesiveless), PET, high-frequency SF230 (DK ≤ 3.6) | P5, P13 |
| Thickness without stiffener | 4–40 mil; order steps 0.025–0.34 mm, ≥ 0.35 mm, ≥ 0.4 mm | P5, P13 |
| Standard stack-ups | 2 layers 0.1–0.38 mm; 4 layers 0.2–0.33 mm; 6 layers 0.3–0.42 mm; 8–16 layers 0.45–0.91 mm; air-gap 2/4/6/8 layers 0.16/0.24/0.37/0.5 mm | P14 |
| PI dielectric | 12.5–125 µm; DK 3.5 with adhesive, 3.3 adhesiveless | P14 |
| Thickness tolerance | Single layer ±1.0 mil; two layers (≤ 12 mil) ±1.2 mil; multilayer ≤ 12 mil ±1.2 mil; 12–32 mil ±8 %; with PI stiffener: no value published (**UNVERIFIED**) | P5 |
| Track/space | 2/2 mil inner and outer (page); ≥ 0.06 mm (order form) | P5, P13 |
| Hole / pad | Mechanical 4 mil (page); ≥ 0.15 / 0.35 mm (order form) | P5, P13 |
| Impedance tolerance | ±4 Ω (≤ 50 Ω); ±7 % (> 50 Ω) | P5 |
| Coverlay | Yellow, white, black, transparent; minimum coverlay bridge 8 mil | P5, P13 |
| Solder mask on flex | Green, black | P5 |
| Bend radius | Single layer 3–6 × thickness; two layers 7–10 ×; multilayer 10–15 × | P5 |
| Copper | Finished outer 9–88 µm; inner 12, 18, 35 µm | P13 |
| Stiffeners | PI 0.05–0.25 mm; FR-4 0.2–1.5 mm (0.1 mm unusual); black FR-4 0.2–1.5 mm; stainless steel 0.1–0.5 mm; aluminium 0.2–1.5 mm; top, bottom or both | P13 |
| Tapes | 3M 467, Tesa 8853/8854, 3M 9495LE (3M parts "not for reflow"); conductive tape HT-A1134 | P13 |
| EMI shielding film | HCF-6000G, PC800; top, bottom or both | P13 |
| Other options | Via filled with copper, air-gap FPC, impedance control, edge plating, castellated holes | P13 |
| Finishes | ENIG, ENEPIG (default Ni 200 µin, Pd 2 µin, Au 2 µin), hard gold, immersion silver, immersion tin, OSP, soft gold | P5, P13 |
| Size | Minimum 0.0788 × 0.1576 in; maximum 8.668 × 27.5 in (about 220 × 698 mm) | P5 |
| Routing accuracy | Laser ±2 mil; punching ±2–6 mil | P5 |

### 1.4 Rigid-flex

| Parameter | Value | Source |
|---|---|---|
| Layers | Up to 26 | P4, P6 |
| Published builds | 1R+2F+1R (0.35 mm), 2R+2F+2R, 4R+2F+4R (1.0 mm), 4R+4F+4R HDI (1.70 mm), (2+1+2F+1+2) HDI 8 layers | P4, P6 |
| Thickness | 0.25–6.0 mm | P6 |
| Track/space | 0.065/0.065 mm; 3 mil standard, 2 mil special | P6 |
| Hole / pad | 0.10 / 0.35 mm; drilled 6 mil standard | P6 |
| Via ring | 6 mil standard, 5 mil special | P6 |
| Aspect ratio | Through 8:1 standard, 10:1 for holes ≥ 0.30 mm; blind 1:1 | P6 |
| Registration | ±3 mil; ±2 mil with LDI | P6 |
| Outline tolerance | ±0.10 mm standard, ±0.05 mm special | P6 |
| Impedance tolerance | ±7.5 % | P6 |
| Copper | Flex part 0.5–2 oz; rigid part 1–4 oz | P6 |
| Finishes | ENIG, electrolytic gold, immersion silver, HASL, immersion tin, OSP, Ni-Pd-Au | P6 |

### 1.5 Assembly, stencils and parts

| Parameter | Value | Source |
|---|---|---|
| Passives | 01005, 0201, 0402 and up | P8, P9 |
| BGA pitch | 0.3 mm on rigid boards, 0.4 mm on flex, with X-ray [P8]; 0.25 mm [P9]; the BGA page shows "0.25 mm" and "0.3 mm" side by side [P7]. Take 0.3 mm (rigid) and 0.4 mm (flex) as the conservative published figures | P7, P8, P9 |
| BGA types | PBGA, CBGA, micro BGA, fine-pitch BGA, stacked BGA, PoP | P7, P18 |
| Fine pitch | 0.25 mm leaded parts; "small chip packages 0.2 mm pitch" | P8, P18 |
| Sides | Single or double-sided placement; SMT, THT and mixed | P8, P18 |
| Inspection | 3D SPI, AOI, X-ray (100 % X-ray of BGA on samples), flying probe, ICT, functional test | P8, P18, P19 |
| Optional services | Conformal coating, press-fit, box build, cable and harness assembly, firmware loading | P19 |
| Flex and rigid-flex assembly | Offered; limits not published ("contact service") | P8, P19 |
| Board size | 10 × 10 mm minimum [P8] or 50 × 100 mm [P9]; smaller or non-rectangular boards are panelised with rails; rails required when copper is closer than 3.5 mm to the edge | P8, P9, P20 |
| Stencils | Laser-cut stainless steel, framed or frameless; 0.08–0.3 mm (order form), 0.1–0.2 mm (page); step stencil option; electropolishing; nano coating on request | P8, P13, P21 |
| Parts sourcing | Turnkey, consigned (kitted) or combination; sources named: Digi-Key, Mouser, Arrow, Avnet | P8, P15 |
| Component packaging | Reels, cut tape, tubes, trays, loose parts | P8 |

### 1.6 Mechanics and finishes

| Service | Value | Source |
|---|---|---|
| CNC materials | Aluminium 6061-T6/T651, 6063-T5/T6, 6082, 7075-T6/T651, 5052, 2A12; ABS, PC, PMMA, POM, nylon, PEEK and others | P22 |
| CNC tolerances | Parts to 300 mm: ±0.125 mm, angularity ±0.5°; "±0.005–0.01 in depending on specs" | P22 |
| CNC size | 2 mm to 1,000 mm; minimum diameter 0.3 mm | P22 |
| CNC finishes | As-milled (Ra 125 µin), smooth machining (Ra 1.6 µm), bead blast, brushed, anodised, bead blast + anodised colour, hard anodising (Type III), powder coat, plating, PVD, laser engraving, chem film, electropolishing | P22, P23 |
| Anodising colours (aluminium) | Natural, black, grey, gold, rose gold, red, blue, champagne, brown, purple, green, orange | P23 |
| Anodising thickness (sheet metal page) | Type II 8–12 µm clear, 4–8 µm colour; "black, clear or any RAL or Pantone"; Type III for wear | P26 |
| Painting on polymers | Spray painting in any Pantone colour on ABS, PC, PP, nylon, POM, PMMA and others; bead blast also on ABS and PC | P23 |
| SLA | Up to 2100 × 800 × 700 mm; minimum wall 0.8 mm; ±0.2 mm below 100 mm, ±0.2 % above; Ra 3–10 µm; clear resin UTR-8100, polishable | P24 |
| SLS | Nylon 12 and PA12 GF; minimum wall 1 mm; ±0.25 mm below 100 mm; threads and inserts as secondary options | P25 |
| MJF | HP PA12, HP PA12 40 % GF; ±0.25 % of length (100 mm) | P27 |
| SLM (metal) | AlSi10Mg, stainless steel, titanium TC4, tool steel; minimum wall 1 mm; ±0.3 mm below 100 mm | P27, P28 |
| FDM | Includes PC, PC-FR and carbon-filled grades (PA6-CF, PLA-CF, PETG-CF, ASA-CF, PPS-CF) | P27 |
| Vacuum casting | Silicone moulds, two-component polyurethanes; listed materials ABS, POM, nylon, PC, PE, PP, PS, TPU, rubber | P29 |
| Sheet metal | Laser cutting 0.5–10 mm, bending 0.5–6 mm; cut ±0.2 mm, bend ±1.0°, bend to edge ±0.254 mm; aluminium 5052/6061, stainless 301/304/316, copper, brass | P26 |
| Injection moulding | Plastic injection, LSR, overmoulding and insert moulding; PC, ABS, PC-ABS, PMMA, TPE, TPU, LSR and others. Tolerances, minimum wall and texture grades: **UNVERIFIED** (not on the page) | P30 |
| Glass | Not offered on any fetched page | — |

## 2. T1 needs against PCBWay prototype services

Verdicts: **Covered** (inside a published normal or medium value), **Limit** (at a published limit), **Review** (offered, but the figure that matters is not published), **Not covered**.

### 2.1 Main board

| Need | T1 figure | PCBWay | Verdict |
|---|---|---|---|
| Smallest-pitch BGA: RK3566 | FCCSP565L, 15.5 × 14.4 mm, 0.4 mm + 0.6 mm ball pitch (`parts/Rockchip/RK3566.md`, from the RK3566 brief); land pattern and ball map **UNVERIFIED** | Fab: 0.4 mm limit, 0.5 mm conventional, pad ≥ 0.2 mm [P10]. Assembly: 0.3 mm rigid with X-ray [P8] | **Limit** (fab), Covered (assembly) |
| 0.4 mm field escape | 0.25 mm pad with a 0.10 mm laser via keeps a 0.075 mm (3 mil) ring, the published minimum [P2, P3]; the gap between such pads is 0.15 mm, too narrow for a 0.065 mm track with 0.065 mm spaces (arithmetic) | Via-in-pad, copper-filled stacked or staggered microvias, 1+N+1 to 6+N+6 and any-layer [P2, P3, P16] | Covered; the build order depends on the ball map (**UNVERIFIED**) |
| LPDDR4X (Samsung K4UBE3D4AB-MGCL), eMMC (KLMBG2JETD-B041) | Package and pitch **UNVERIFIED** in the parts sheets | Covered if ≥ 0.4 mm | Open until the package drawings exist |
| Fuel gauge MAX17055 (WLP) | Ball count and pitch **UNVERIFIED** | Same | Open. Note (2026-10-22): the T1 moved to a 2S battery ([board ADR 0014](https://github.com/opendap-project/board/blob/main/docs/adr/0014-two-cell-battery.md)); the gauge is now the BQ28Z610-R1 in a 12-pin SON (DRZ, 2.5 × 4 mm), no WLP |
| RK809-5 PMIC | QFN68, 0.35 mm pitch | Fine pitch 0.25 mm [P8]. A 0.35 mm pitch leaves less than the 8 mil pad spacing that keeps a mask bridge [P2], so the row gets one gang opening (arithmetic, depends on the land width) | Covered |
| RP2354A, CS43198, LP5521 and other 0.4–0.5 mm QFN/SON | 0.4 mm pitch, 0.20 mm lands (RP2354A) | Same as above; 0.2 mm spacing sits at the 8 mil threshold | Covered |
| DF40C-100DP / -50DP headers | 0.4 mm pitch, 0.23 mm lands (gap 0.17 mm, 6.7 mil) | Fine pitch assembly [P8]; gap below the 8 mil mask-bridge threshold, so gang opening per row | Covered |
| FH35C-51S connector | 0.3 mm pitch, two staggered rows at 0.6 mm, 0.3 mm lands (gap 0.3 mm) | Fine pitch 0.25 mm [P8]; mask bridge possible | Covered |
| Smallest passives | 0201 (HAT AC-coupling caps, line 70); 0402 RF network | 01005 and up [P8] | Covered |
| Differential pairs on the board | USB 3 and USB 2: 90 Ω; PCIe: 85–100 Ω (**UNVERIFIED** target); MIPI DSI and CSI-2: 100 Ω (HAT interface v0) | ±10 % [P1]; custom stack-up; minimum dielectric 50 µm [P12]; high-speed laminates in the 1–5 G and 5–10 G classes [P2] | Covered. Whether ±10 % meets each standard's budget belongs to the board SI work |
| Both sides populated | BRD-054 | Double-sided placement [P8] | Covered |
| Shielding cans | Two-piece frame and cover, DNP first (BOM line 90, part open) | Not named. A frame on tape is an ordinary SMT part; a clipped cover is a manual step (box build) | **Review** |
| Assembly variants (BRD-053) | Prototypes populate every option | DNP is handled by the BOM and centroid files; nothing specific published | Covered |
| BGA inspection | RK3566, LPDDR4X, eMMC | X-ray [P8, P19] | Covered |
| Conformal coating | Not required by any T1 requirement today | Offered [P19] | Covered if needed |
| Board size for assembly | Main body ideal 54 mm wide (T1-032) | Below 50 × 100 mm, panelise with rails [P9, P20] | Covered |

### 2.2 HAT flat cable (board ADR 0002)

| Need | T1 figure | PCBWay | Verdict |
|---|---|---|---|
| Conductor count | DF40 100-contact signal + 50-contact power connector at each end; 12 differential pairs in a ground–signal–signal–ground row (HAT interface v0) | FPC up to 12 layers (page) or 16 (order form) [P5, P13] | Covered |
| Impedance | 90 Ω (USB), 100 Ω (MIPI), PCIe open; "90 Ω diff" in BOM line 102 | ±7 % above 50 Ω on flex [P5] (90 ± 6.3 Ω, 100 ± 7 Ω, arithmetic); ±7.5 % on rigid-flex [P6]; air-gap and SF230 high-frequency options [P13, P14] | Covered |
| Shielding | Not specified | EMI shielding film top, bottom or both [P13] | Covered if needed (the film changes the impedance stack-up) |
| Length | Not defined yet | Up to about 698 mm [P5] | Covered |
| Thickness and bend | Not defined yet | 4 layers 0.2–0.33 mm, minimum bend radius 10–15 × thickness (about 2.0–5.0 mm, arithmetic) [P5, P14] | Covered once the routing in the case is drawn |
| DF40C receptacles on the FPC | 0.4 mm pitch, 0.20 mm lands (gap 0.20 mm, 7.9 mil); Hirose asks for a stiffener under the receptacle | Coverlay bridge minimum 8 mil [P5]: gang opening per row or LPI mask on flex; FR-4 0.2–1.5 mm or stainless 0.1–0.5 mm stiffener [P13]; flex assembly on request [P8] | Covered, flex assembly is **Review** |
| Copper for power | HAT_5V ×12, HAT_3V3 ×6, GND ×22 contacts on the 50-pin | Finished outer copper up to 88 µm, inner up to 35 µm [P13] | Covered |
| Rigid-flex alternative | Not the current plan (BOM line 66 has a DF40 pair at both ends) | 2–26 layers, HDI rigid-flex [P4, P6] | Available as an option only |

### 2.3 Faceplate cable and faceplate board

| Need | T1 figure | PCBWay | Verdict |
|---|---|---|---|
| FH35C mating tail thickness | 0.2 ± 0.03 mm at the mating area, with a stiffener film (Hirose FH35C catalog p. 2, p. 5) | Two-layer FPC 0.1–0.2 mm, PI stiffener 0.05–0.25 mm [P13]; ±1.2 mil for two layers ≤ 12 mil [P5]; no tolerance published with the PI stiffener | **Limit / Review** |
| FH35C tail outline | F = 15.6 ± 0.05 mm (51 contacts) | Laser routing ±2 mil (±0.05 mm) [P5] | **Limit** |
| FH35C back-side copper | Remove copper on the back of the mating area (Hirose p. 6) | Design rule, no fab limit | Covered |
| DSI pairs on the cable | 100 Ω, up to 4 lanes + clock (faceplate interface) | ±7 % on flex [P5] | Covered |
| Faceplate flex with FH12 connectors | "Faceplate flex" carries FH12-20S and FH12-6S (0.5 mm) (BOM lines 84, 85) | FPC with FR-4 or PI stiffeners under the connectors [P13]; flex assembly on request [P8] | Covered, flex assembly is **Review** |
| Faceplate as rigid board or rigid-flex | Not decided | Rigid multilayer [P1] or rigid-flex 1R+2F+1R and up [P4, P6] | Covered |

### 2.4 HAT device-side piece

| Need | T1 figure | PCBWay | Verdict |
|---|---|---|---|
| Board | DF40C headers (0.4 mm), about 128 Harwin P70 pogo pins, TPD4E05U06 ESD (0.5 mm USON), 12 differential pairs | Rigid multilayer with impedance control [P1] | Covered |
| Pogo pin placement | Harwin P70-1000045R: SMT, Ø 1.54 mm barrel, Ø 2.00 mm flange, 3.50 mm free height, tape and reel (`parts/Harwin/P70-1000045R.md`) | Reels accepted [P8]; pogo pins not named; pick-up and height limits not published | **Review** |
| Contact pads on the HAT side | Flat pads against pogo pins (hat-standard, finish not chosen) | ENIG, hard gold (Ni 120–150 µin, Au 1–30 µin normal), ENEPIG [P1] | Covered |

### 2.5 Case and mechanics

| Need | T1 figure | PCBWay | Verdict |
|---|---|---|---|
| First cases in polymer | PC or ABS (CASE-020) | CNC ABS, PC [P22]; SLA, MJF, SLS [P24, P25, P27]; vacuum casting PC/ABS-like [P29]; injection PC, ABS, PC-ABS [P30] | Covered |
| Graphite colour with a grip texture | CASE-021 | Spray painting in any Pantone colour, bead blast on ABS and PC [P23]; mould textures **UNVERIFIED** | Covered (paint, blast); mould texture **Review** |
| Anodised aluminium | CASE-022 | CNC 6061/6063/7075 [P22]; anodising in twelve colours including grey and black, Type III hard anodising [P23] | Covered |
| Crystal clear | CASE-022 | CNC PMMA, PC; SLA clear UTR-8100, polishable [P22, P24] | Covered |
| Carbon | CASE-022 | Carbon-filled FDM grades only [P27]; carbon-fibre laminate not listed | **Review** |
| Seals for IP65 (T1-017, Draft) | Not designed | LSR moulding, TPU, TPE [P30] | Covered |
| Cover glass and optical bonding | Custom optically bonded lens (BOM line 83); the only allowed custom part (T1-038, FPT-022) | No glass, cover-glass or bonding service | **Not covered.** Closest PCBWay option: a polished PMMA or PC window (CNC or SLA) for fit prototypes |
| Dimensions | At most 62.5 × 95 × 25 mm (T1-031) | Inside every listed build volume | Covered |
| Sheet metal parts | None defined | 0.5 mm minimum sheet [P26] | Covered if needed; too thick for custom shielding cans, so catalog cans stay |

## 3. Constraints the rule sets must carry

These follow from the figures above and from the part sheets. They are design-rule facts, not PCBWay statements.

1. **Mask bridge threshold.** Pads closer than 8 mil (0.203 mm) do not keep a solder-mask bridge [P2]: RK809 (0.35 mm), DF40 headers and receptacles, and some 0.4 mm QFNs get one opening per row.
2. **0.4 mm BGA.** Pad ≥ 0.2 mm [P10], ring ≥ 3 mil around a 0.10 mm laser via [P2, P3], hence a 0.25 mm pad when the via sits in the pad. Mask opening 1 mil in the BGA area [P1].
3. **Through-hole aspect ratio** limits a 0.20 mm hole to 1.6 mm of board [P1]; the main board is far thinner, so this does not bind.
4. **Coverlay** bridge 8 mil (0.2 mm) on flex [P5]; coverlay opening and copper-to-outline rules on flex are not published (**UNVERIFIED**), so the flex rule set keeps the rigid 0.20 mm edge clearance until PCBWay's DFM answers.
5. **Flex bends** at 10–15 × thickness for multilayer [P5]; stiffened areas (connectors) must not bend.

## 4. Proposed PCBWay processes for the KLIB-002 rule sets (proposal)

One rule set per process, in `design-rules/<fab>-<process>/`, each with a test board that triggers every rule (KLIB-002). Values marked "default" are the published normal values; "floor" is the published limit, used only in named areas (rule areas or net classes).

### 4.1 `pcbway-hdi`: main board

Target: advanced HDI, 2+N+2 with copper-filled stacked microvias as the starting point, 8 or 10 layers, FR-4 Tg 170 (S1000-2M), ENIG. The build order (1+N+1, 2+N+2, 3+N+3 or any-layer) is set by the RK3566 ball map, which is **UNVERIFIED**; the rule set should parameterise it. PCBWay publishes an 8-layer, 3rd-order, 1.0 mm example [P3].

| Rule | Default | Floor | Source |
|---|---|---|---|
| Track/space (outer and inner, ≤ 18 µm base) | 0.075 / 0.075 mm (3/3 mil order option) | 0.065 / 0.065 mm in the BGA escape area | P3, P16 |
| Laser microvia drill / land | 0.10 / 0.25 mm | 0.075 mm drill (reviewed) | P2, P3 |
| Laser via dielectric | ≤ 0.15 mm (8 mil via maximum) | — | P3 |
| Microvia stacking | Stacked and staggered, copper-filled | — | P2, P16 |
| Mechanical via drill / land | 0.20 / 0.45 mm (5 mil ring) | 0.15 / 0.35 mm (4 mil ring) | P1, P3 |
| Via-in-pad (mechanical) | Resin-filled and plated over | — | P11 |
| Hole to hole (vias ≤ 0.45 mm) | 0.28 mm (11 mil) | — | P1 |
| Hole to inner copper (8 layers) | 0.23 mm (9 mil) | 0.15 mm (6 mil) | P1, P2 |
| BGA pad | 0.25 mm | 0.20 mm | P10 |
| BGA pitch | 0.4 mm allowed only for the RK3566 footprint | 0.4 mm | P10 |
| Solder-mask expansion | 0.05 mm | 0.025 mm in BGA areas | P1 |
| Solder-mask web | 0.10 mm (4 mil) | 0.075 mm (3 mil, green) | P2, P3 |
| Copper to milled edge | 0.20 mm | — | P1 |
| Silkscreen | 0.15 mm line, 0.8 mm height | — | P1 |
| Impedance | ±10 %, dielectric ≥ 50 µm | — | P1, P12 |
| Thickness tolerance | ±0.10 mm (T ≤ 1.0 mm) | — | P1 |

### 4.2 `pcbway-flex`: HAT flat cable and faceplate cable

Target: adhesiveless polyimide FPC, ENIG, 2 layers for the faceplate cable (FH35C tail 0.2 mm with a PI stiffener) and 4 layers for the HAT flat cable (0.2–0.33 mm, air-gap stack-up as an option), FR-4 or stainless stiffeners under the DF40 receptacles. The layer counts are proposals; the HAT stack-up comes from the signal-integrity test coupon (HAT interface v0, §7).

| Rule | Default | Floor | Source |
|---|---|---|---|
| Track/space | 0.075 / 0.075 mm (3/3 mil, published examples) | 0.06 mm | P5, P13 |
| Via drill / land | 0.15 / 0.35 mm | 0.10 mm drill (4 mil) | P5, P13 |
| Coverlay web | 0.20 mm (8 mil); gang opening below | — | P5 |
| Copper to outline | 0.20 mm (rigid value, **UNVERIFIED** for flex) | — | P1 |
| Outline tolerance | ±0.05 mm (laser) | — | P5 |
| Thickness tolerance | ±0.03 mm (two layers ≤ 12 mil) | — | P5 |
| Impedance | ±7 % (> 50 Ω) | — | P5 |
| Stiffeners | PI 0.05–0.25 mm; FR-4 0.2–1.5 mm; stainless 0.1–0.5 mm | — | P13 |
| Bend radius (keep-out for components and vias) | 10–15 × thickness (multilayer); 7–10 × (two layers) | — | P5 |
| Copper | Outer finished 9–88 µm; inner 12–35 µm | — | P13 |

### 4.3 `pcbway-rigid-flex`: only if a rigid-flex option is chosen

Candidates: the faceplate (rigid area under the FH12 connectors with a flex tail to the FH35C), or the device-side piece and the HAT flat cable as one part, which would remove one DF40 pair (a change to BOM line 66 that only the maintainers can make).

| Rule | Default | Floor | Source |
|---|---|---|---|
| Track/space | 0.075 / 0.075 mm (3 mil) | 0.065 mm (2 mil special) | P6 |
| Via drill / land | 0.15 / 0.35 mm (6 mil drill, 6 mil ring) | 0.10 / 0.35 mm | P6 |
| Aspect ratio | 8:1 through; 1:1 blind | 10:1 (holes ≥ 0.30 mm) | P6 |
| Registration allowance | ±3 mil | ±2 mil (LDI) | P6 |
| Outline tolerance | ±0.10 mm | ±0.05 mm | P6 |
| Impedance | ±7.5 % | — | P6 |
| Copper | Flex 0.5–2 oz, rigid 1–4 oz | — | P6 |

### 4.4 `pcbway-multilayer`: device-side piece and rigid faceplate boards

Target: advanced multilayer with through vias only, 4 or 6 layers, impedance control, ENIG (hard gold where a contact surface needs it). The vendored kicad-druid PCBWay set does not encode the impedance or the 0.4 mm DF40 gang-opening rules; this set adds them on top of PCBWay's normal values.

| Rule | Default | Floor | Source |
|---|---|---|---|
| Outer track/space, 18 µm base | 0.10 / 0.125 mm (4/5 mil) | 0.10 / 0.10 mm (4/4 mil) | P1 |
| Inner track/space, 18 µm base | 0.10 / 0.10 mm | 0.10 / 0.09 mm | P1 |
| Via drill / land | 0.20 / 0.45 mm | 0.15 / 0.35 mm | P1 |
| Hole to inner copper (4 / 6 layers) | 0.18 / 0.20 mm (7 / 8 mil) | 0.15 / 0.165 mm (6 / 6.5 mil) | P1 |
| Solder-mask expansion / web | 0.05 / 0.10 mm | 0.025 / 0.075 mm | P1, P2 |
| Copper to milled edge | 0.20 mm | — | P1 |
| Impedance | ±10 % | — | P1 |
| Minimum thickness | 4 layers 0.60 mm, 6 layers 0.9 mm | 0.40 / 0.70 mm | P1 |

### 4.5 Unchanged

The vendored `vendor/kicad-druid/` PCBWay set stays for simple 2- to 6-layer boards (test fixtures, HAT reference boards without impedance control).

## 5. Questions for PCBWay's DFM review

1. Microvia land and aspect ratio for rigid HDI, and whether copper-filled stacked microvias in 0.25 mm pads on a 0.4 mm grid are a normal or a reviewed build.
2. Which BGA assembly pitch applies on rigid boards: 0.25 mm [P9] or 0.3 mm [P8]; and the prototype-factory figure of 0.35 mm pad centre to centre [P10] against the 0.4 mm advanced limit.
3. Thickness tolerance of a two-layer FPC with a PI stiffener at the FH35C mating area (target 0.2 ± 0.03 mm).
4. Coverlay opening rules and copper-to-outline clearance on flex.
5. Flex and rigid-flex assembly limits (fine pitch, connectors on a stiffened area, panelisation).
6. Shielding-can frames and Harwin P70 pogo pins as SMT parts: nozzle pick-up, placement height, X-ray or AOI coverage.
7. Injection-moulding tolerances, minimum wall and texture grades for a PC or PC-ABS housing.

## Sources

All pages fetched on 2026-10-22.

| Key | Page |
|---|---|
| P1 | PCB Capabilities (standard and advanced tables): <https://www.pcbway.com/capabilities.html> |
| P2 | Advanced PCB Capabilities: <https://www.pcbway.com/advanced-pcb-capabilities.html> |
| P3 | HDI PCB: <https://www.pcbway.com/hdi-pcb.html> |
| P4 | Flex and rigid-flex overview: <https://www.pcbway.com/fpc-rigid-flex-pcb.html> |
| P5 | Flexible PCB: <https://www.pcbway.com/fpc-rigid-flex-pcb/flex-pcb.html> |
| P6 | Rigid-flex PCB: <https://www.pcbway.com/fpc-rigid-flex-pcb/rigid-flex-pcb.html> |
| P7 | BGA Assembly Capabilities: <https://www.pcbway.com/pcb_prototype/BGA_Assembly_Capabilities.html> |
| P8 | Assembly capabilities: <https://www.pcbway.com/assembly-capabilities.html> |
| P9 | PCB assembly capabilities: <https://www.pcbway.com/pcb_prototype/PCB_assembly_Capabilities.html> |
| P10 | PCB BGA (fab capability): <https://www.pcbway.com/pcb_prototype/PCB_BGA.html> |
| P11 | Via-in-Pad: <https://www.pcbway.com/pcb_prototype/PCB_Via_in_Pad.html> |
| P12 | Impedance Control: <https://www.pcbway.com/pcb_prototype/Impedance_Control.html> |
| P13 | FPC order form (options and stencil): <https://www.pcbway.com/flexible.aspx> |
| P14 | Stack-up for FPC: <https://www.pcbway.com/pcb_prototype/Stack_up_for_FPC.html> |
| P15 | PCB Assembly: <https://www.pcbway.com/pcb-assembly.html> |
| P16 | Advanced PCB order form (options): <https://www.pcbway.com/HighQualityOrderOnline.aspx> |
| P17 | Assembly order form, PCB section (track/space options, HDI from 4 layers): <https://www.pcbway.com/quotesmt.aspx> |
| P18 | SMT Assembly Capabilities: <https://www.pcbway.com/pcb_prototype/SMT_Assembly_Capabilities.html> |
| P19 | Assembly order form, assembly options: <https://www.pcbway.com/quotesmt.aspx> |
| P20 | PCB Assembly Special Reminders: <https://www.pcbway.com/assembly-special-remind.html> |
| P21 | SMT stencil: <https://www.pcbway.com/pcb_prototype/SMT_stencil_and_Laser_Stencil.html> |
| P22 | CNC machining: <https://www.pcbway.com/rapid-prototyping/cnc-machining/> |
| P23 | Surface finishing: <https://www.pcbway.com/rapid-prototyping/Surface-Finishing.html> |
| P24 | SLA: <https://www.pcbway.com/rapid-prototyping/3D-Printing/3D-Printing-SLA.html> |
| P25 | SLS: <https://www.pcbway.com/rapid-prototyping/3D-Printing/3D-Printing-SLS.html> |
| P26 | Sheet metal: <https://www.pcbway.com/rapid-prototyping/sheet-metal/> |
| P27 | 3D printing overview (tolerances, materials): <https://www.pcbway.com/rapid-prototyping/3d-printing/> |
| P28 | SLM: <https://www.pcbway.com/rapid-prototyping/3D-Printing/3D-Printing-SLM.html> |
| P29 | Vacuum casting: <https://www.pcbway.com/rapid-prototyping/3D-Printing/3D-Printing-VC.html> |
| P30 | Injection moulding: <https://www.pcbway.com/rapid-prototyping/injection-molding/> |
