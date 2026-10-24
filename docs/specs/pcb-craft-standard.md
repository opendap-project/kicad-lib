# OpenDAP PCB craft standard

- **Status:** Draft. Requirement KLIB-003 (must, confirmed by the maintainers on 2026-10-24): every OpenDAP board follows this standard. The rules and their values were chosen by Claude under the maintainers' delegation, from the sources cited; the proposals in [§8](#8-colour-and-finish) wait for the maintainers.
- **Date:** 2026-10-24
- **Applies to:** every OpenDAP board: the T1 main board, faceplates, HATs and their reference designs, and any later device.
- **Levels:** each rule carries the lowest quality level at which it is mandatory ([RFC 0010](https://github.com/opendap-project/rfcs/blob/main/text/0010-quality-levels.md)): Q0 bench-safe, Q1 prototype, Q2 pre-compliance, Q3 compliant product, Q4 reference. A build passes every rule at or below its target level; the rest is debt, listed, never dropped.
- **Enforcement:** **DRC**, the rule set [`design-rules/opendap-craft/`](../../design-rules/opendap-craft/); **CHK**, `odapkit craft check` in [toolkit-hardware](https://github.com/opendap-project/toolkit-hardware) (`tools/pcb-craft-check.py`); **Review**, the design review, by a person, against this document.

## Contents

1. [Why](#1-why)
2. [How the standard is applied](#2-how-the-standard-is-applied)
3. [Silkscreen and footprints](#3-silkscreen-and-footprints)
4. [Board markings](#4-board-markings)
5. [Placement](#5-placement)
6. [Routing and copper](#6-routing-and-copper)
7. [Documentation layers](#7-documentation-layers)
8. [Colour and finish](#8-colour-and-finish)
9. [Schematics](#9-schematics)
10. [Practices studied, and the decisions taken](#10-practices-studied-and-the-decisions-taken)
11. [Enforcement summary](#11-enforcement-summary)
12. [Open items](#12-open-items)
13. [Sources](#13-sources)

## 1. Why

The maintainers asked (2026-10-24) that OpenDAP's boards be made with visible care for engineering, quality and appearance, beyond function. An OpenDAP board is also documentation: the boards are open, their files are published, and owners of the DIY edition handle them. A board that reads clearly is easier to assemble, inspect, probe, repair and modify.

The standard turns that into rules a tool or a reviewer can check: one typeface and a closed set of sizes, fixed orientations, a placement grid, closed sets of track widths and vias, required markings and documentation layers. Most of it follows published conventions (KLC, IPC-7351 through KLC, fab capability pages); where a value is OpenDAP's own choice, the rule says so.

Andy Hertzfeld records Steve Jobs, in July 1981, rejecting a Macintosh board layout because the memory chips' lines were "too close together", and saying that "a great carpenter isn't going to use lousy wood for the back of a cabinet, even though nobody's going to see it" [FOLK-PCB]. The point taken here is narrower and practical: an open board's inside is seen, by its users and by anyone who builds on it.

## 2. How the standard is applied

- **Composition.** A board's `<project>.kicad_dru` is composed by `odapkit dru compose` from its `<project>.dru.toml` manifest, in this order: the fab rule set (for example [`pcbway-hdi`](../../design-rules/pcbway-hdi/)), then [`opendap-craft`](../../design-rules/opendap-craft/), then the product's own rules. The craft rules use only constraints the fab sets do not (assertions, `silk_clearance`, `track_angle`, `track_segment_length`), so they never relax a fab limit; KiCad applies every matching assertion, so product rules cannot relax them either.
- **Exemptions** are built into the rules and are the only ones:
  - impedance-controlled net classes, named `<name>_<ohms>D` (differential, as the T1 board's `USB3_90D`) or `<name>_<ohms>SE` (single-ended), take their widths and geometry from the stackup: exempt from CRAFT-40, CRAFT-42 and CRAFT-43;
  - rule areas named `CRAFT-EXEMPT*` or containing `ESCAPE` (a BGA escape, where the fab floors apply) exempt the copper inside them from CRAFT-40, CRAFT-41, CRAFT-43 and CRAFT-47;
  - a footprint field `Craft_Exempt` = `"CRAFT-30 CRAFT-31: <reason>"` exempts that footprint from the CHK rules it names; the report lists every exemption with its reason. Use it for parts placed from a mechanical datum (connectors, buttons, mounting holes).
- **The check.** `odapkit craft check <board>.kicad_pcb` runs the CHK rules, runs the board's DRC and folds every rule tagged `[Qn]` into the same report, groups results by level, and prints the level the board reaches. A `<project>.craft.toml` next to the board names its target level and its mirrored blocks (CRAFT-34).
- **Ratchet.** A level reached is kept (RFC 0010). A change that makes a passing rule fail is a regression, whatever the rule's level.

## 3. Silkscreen and footprints

The legend is set like a technical drawing: one typeface, four sizes, two reading directions, one stroke weight.

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-01 | Q2 | One typeface: KiCad's stroke font, regular, upright. Logos and the brand wordmark are graphics, never text. | `KiCad Font`, not bold, not italic | A stroke font plots as lines of one width, which the fab reproduces evenly; KLC sizes are given in it; SparkFun requires a vector font for the same reason | [KLC] F5.1; [SFE] | DRC |
| CRAFT-02 | Q2 | Text height and stroke from a closed set; width equals height. | 0.8 × 0.15 mm (dense areas only); **1.0 × 0.15 mm** (reference designators); 1.6 × 0.24 mm (labels); 2.0 × 0.30 mm (board name) | Fewer sizes read as one hierarchy. 1.0 × 0.15 is KLC's reference size; 0.8 mm and 0.15 mm are PCBWay's minimums, and PCBWay gives about 1 : 5 stroke to height as the best ratio; the larger sizes keep 15 % (SparkFun's ratio) | [KLC] F5.1; [PCBWAY]; [JLC]; [SFE] | DRC |
| CRAFT-03 | Q2 | Two reading directions: from the bottom edge (0°) and from the right edge (90°). A flipped footprint keeps its text angle, so the same two values hold on the bottom side. | 0° or 90° | A board read from two sides only, never upside down. No primary source was found for the two-direction convention: OpenDAP's choice | — | DRC |
| CRAFT-04 | Q1 | Text reads from its own side: unmirrored on top, mirrored on the bottom. | — | A reversed legend is not legible; KiCad also flags mirrored text on the front | [KICAD-DRC] | DRC |
| CRAFT-05 | Q2 | One silk stroke for outlines and marks. Filled marks (pin-1 triangles, dots, the brand mark) have no stroke. | 0.15 mm | KLC allows 0.10–0.15 mm (0.12 nominal); PCBWay's minimum line is 0.15 mm, so OpenDAP uses KLC's upper value | [KLC] F5.1; [PCBWAY] | DRC |
| CRAFT-06 | Q1 | No silk inside a solder-mask opening (pads, exposed copper). Set the Board Setup check `silk_over_copper` to error. | — | Silk on a pad prevents soldering; fabs clip it | [KLC] F5.1; [EC-LEG]; [JLC] | DRC (Board Setup) |
| CRAFT-07 | Q2 | Silk clear of pads and via lands. | 0.15 mm from pads; 0.15 mm from via lands (DRC: 0.30 mm from the via hole, see the rule set's README) | JLCPCB's minimum to pads is 0.15 mm; KLC recommends 0.2 mm | [JLC]; [KLC] F5.1 | DRC |
| CRAFT-08 | Q2 | Silk clear of the board edge. | 0.5 mm | KLC's value; Eurocircuits clips legend within 0.25 mm of a routed edge | [KLC] F5.1; [EC-LEG] | CHK (KiCad 10.0.7's DRC does not measure this reliably) |
| CRAFT-09 | Q2 | Text clear of any other silk, so every character stands alone. | 0.15 mm | Legibility; one stroke width of air | — | DRC |
| CRAFT-10 | Q2 | Every part with electrical pads has a visible reference designator on the silk of its side. Where density forbids it, the designator moves to the fabrication layer and the part takes a `Craft_Exempt` with the reason. | — | The open board is a repair document; see [§10](#10-practices-studied-and-the-decisions-taken) for why OpenDAP does not minimise its legend | MNT Reform [MNT]; [SFE] | CHK |
| CRAFT-11 | Q2 | Every part carries `${REFERENCE}` on its fabrication layer. | — | The assembly drawing, which is published, then names every part even where the silk cannot | [KLC] F5.2 | CHK |
| CRAFT-12 | Q3 | Reference designators in one size per side, beside their part (within 2 mm of its courtyard and nearer to it than to any other part), never under an SMD body. | 2 mm | One size reads as one system; a designator nearer another part names the wrong one; KLC forbids silk under SMD bodies | [KLC] F5.1 | CHK |
| CRAFT-13 | Q1 | Every polarised part (ICs, diodes, LEDs, transistors, connectors, batteries, crystals) has a pin-1 or polarity mark next to pin 1, outside the body, visible after assembly and after mating. Forms: a filled triangle for ICs and connectors, a bar at the cathode for diodes, `+` for polarised capacitors. | — | Orientation errors are found at a glance; KLC's mark forms | [KLC] F5.1 | CHK (mark next to pin 1); Review (form) |
| CRAFT-14 | Q1 | Battery and power-input connectors are marked `+` and `−` in silk, within 3 mm. | 3 mm | The battery is user-replaceable (T1-055): its polarity must read without a schematic | T1-055 | CHK |
| CRAFT-15 | Q1 | Footprints follow KLC orientation and anchors: pin 1 top left (IPC-7351 "Level A"), two-terminal parts with pin 1 on the left; SMD anchor at the body centroid, THT anchor at pin 1. The fab package states the convention, as fabs differ (Eurocircuits uses IEC 61188-7, pin 1 bottom left). | — | Pick-and-place rotations come out right without per-part fixes | [KLC] F4.2, F6.2, F7.2; [EC-ROT] | Review (library) |

## 4. Board markings

Every board identifies itself without its documentation. The identity block is one group, on one side, left-aligned, in CRAFT-02 sizes: the board name at 2.0 mm, the rest at 1.0 mm.

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-20 | Q1 | Board name and revision on the silk, from the title block (`${TITLE}`, `${REVISION}`), so the copper and the files cannot disagree. | — | Revision mix-ups are the commonest bring-up error; Raspberry Pi and MNT boards carry both | [RPI4]; [MNT] | CHK |
| CRAFT-21 | Q2 | Issue date (`${ISSUE_DATE}`, ISO 8601), the copyright holder "The OpenDAP Project", and the licence's SPDX identifier on the silk: `CERN-OHL-S-2.0` for product hardware, `CERN-OHL-W-2.0` for HAT reference designs and building blocks. | — | The board carries its own terms; Raspberry Pi prints "© Raspberry Pi 2018", MNT a dated identification line | [RPI4]; [MNT]; workspace licensing rule | CHK |
| CRAFT-22 | Q3 | The source location (`github.com/opendap-project/<repository>`) on the silk, and the OpenDAP mark as a footprint built from the approved files (mark ≥ 5 mm high, wordmark ≥ 4 mm, the print minimums; the mark's gap, 6.9 % of its height, stays above the silk's 0.15 mm line). | 5 mm / 4 mm | CERN-OHL-S §4 requires recipients to be told the source location, and lets a notice require it on the product; OpenDAP puts it on the board. The mark's minimums are the brand's | [CERN-S] §1.9, §4; [BRAND] | CHK (text, `OpenDAP_Mark*` footprint); Review (size) |
| CRAFT-23 | Q1 | The OSHW mark only after OSHWA certifies the board, with its UID next to it. No OpenDAP board is certified today, so no board carries it (**UNVERIFIED** whether certification will be sought). | UID: two letters and up to six digits | OSHWA allows the mark only after certification | [OSHWA] | CHK |
| CRAFT-24 | Q2 | Title block complete: title, revision, ISO 8601 date, company "The OpenDAP Project". | — | Every output (fab drawing, assembly drawing, schematic PDF) inherits it | — | CHK |
| CRAFT-25 | Q1 | Only names the maintainers confirmed: OpenDAP, OpenDAP T1, Blackbird OS, OpenDAP HATs; never an unconfirmed product name. | — | Workspace brand rules | workspace rules | Review |
| CRAFT-26 | Q3 | A silk-free area on each production board for a serial-number or 2D-code label, flat and away from probe points. | Size per board | Traceability in production | — | Review |

## 5. Placement

Placement carries most of a board's visible order: a grid, rows, shared orientations, and mirrored channels laid out as mirrors.

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-30 | Q2 | Footprint anchors on the placement grid, from the board's grid origin. Parts placed from a mechanical datum take a `Craft_Exempt`. | 0.05 mm | A common grid makes rows and alignments exact; 0.05 mm is fine enough for 0.4 mm-pitch HDI placement. OpenDAP's choice (SparkFun uses 0.1 in for the outline) | [SFE] | CHK |
| CRAFT-31 | Q2 | Footprint rotations in multiples of 90°. | — | Pick-and-place and inspection; diagonal parts break rows | — | CHK |
| CRAFT-32 | Q3 | Passives in one placement group share one orientation (0°/180° or 90°/270°). A group is a KiCad group, else a schematic sheet instance. | — | Uniform blocks read as one function and inspect faster | — | CHK |
| CRAFT-33 | Q3 | Passives in a group sit in rows or columns: each shares an x or y centre with another. | 0.01 mm | — | — | CHK |
| CRAFT-34 | Q2 | Mirrored channels are laid out as mirrors: left and right audio channels, and the two halves of a DAC or amplifier, symmetric about an axis (or translated copies), part for part, with the same footprints and mirrored rotations. Declared in `<project>.craft.toml`. | 0.05 mm | Matched channels: TI's OPA1622 EVM keeps the left and right traces "as balanced as possible"; mirrored artwork for matched THD+N is reported in AN-1490 (**UNVERIFIED** verbatim) | [TI-OPA1622] §5.1; [AN-1490] | CHK |
| CRAFT-35 | Q2 | The board outline, mounting holes, connectors and controls come from the enclosure's export (case `export/`, component export contract), never drawn by eye; corners take the case's radii. | — | Hierarchical composition; the board fits its enclosure by construction | Component export contract; [IFX-MB] | Review |
| CRAFT-36 | Q3 | One mounting-hole (screw) size per board, and one screw family across the device, driven by common tools. | — | T1-055: the battery is replaced with common tools | T1-055 | CHK (size); Review (family) |
| CRAFT-37 | Q3 | Shield cans are catalogue parts (T1-038), two-piece (frame and removable lid) where the inside must be probed or reworked, aligned to the placement grid and to the board edges. | — | Off-the-shelf parts; access for repair | T1-038 | Review |
| CRAFT-38 | Q2 | Connectors at the board edge facing their enclosure opening, one family per function, the same mating direction, with a latch or a bracket on every flat-cable and board-to-board connector. | — | Apple's iPhone X holds every logic-board connector under one bracket | [IFX-X] step 5 | Review |
| CRAFT-39 | Q1 | The battery connector is reachable with the back cover removed and nothing else (T1-055), and labelled (CRAFT-14). | — | User-replaceable battery | T1-055 | Review |

## 6. Routing and copper

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-40 | Q2 | Straight segments at multiples of 45°. | 0.001 mm tolerance | One geometry for the whole board | — | DRC |
| CRAFT-41 | Q3 | Corners of 135° or more between connected segments: no right-angle or acute corners; T-junctions are made at a pad or a via, or with 45° entries. | 135° | Even routing; acute corners trap etchant and narrow the copper | — | DRC |
| CRAFT-42 | Q3 | Arcs only where signal integrity justifies them: on impedance-controlled classes. | — | Arcs are a tool for controlled impedance, not a style | — | CHK (KiCad DRC gives arcs no property of their own) |
| CRAFT-43 | Q2 | Track widths from the OpenDAP series; impedance classes take their widths from the stackup. | 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0 mm; wider copper is a pour | A closed series keeps neighbouring tracks visibly related; every value is at or above the fab sets' minimums (3 mil HDI, 4 mil multilayer) | [RES] | DRC |
| CRAFT-44 | Q3 | At most two widths per net class: the class width and one neck-down. | 2 | Width follows function, not the router's mood | — | CHK |
| CRAFT-45 | Q2 | Vias from the OpenDAP set (drill / land). | 0.10 / 0.25 mm laser microvia; 0.20 / 0.46 mm; 0.30 / 0.60 mm | Each meets PCBWay's HDI and multilayer minimums (0.075 mm microvia ring as the research applies it, 5 mil mechanical ring); fewer sizes, fewer tools | [RES] | DRC |
| CRAFT-46 | Q3 | At most eight mechanical drill sizes per board (vias, plated and unplated holes, slots); laser drills not counted. | 8 | Each size is a tool change; consistency | — | CHK |
| CRAFT-47 | Q4 | No jogs: no straight segment shorter than 0.1 mm. | 0.1 mm | Short kinks are router residue | — | DRC |
| CRAFT-48 | Q3 | One teardrop policy for the board: on at every via and pad junction, or off at all of them. Product rules may require them (the T1 board does at Q2). | — | Consistent geometry | — | CHK |
| CRAFT-49 | Q2 | Copper zones remove islands; set the Board Setup check `isolated_copper` to error. | — | No floating copper | — | CHK |
| CRAFT-50 | Q3 | Zone fill minimum width ≥ 0.2 mm and zone outlines at 45° multiples. | 0.2 mm | No slivers; pour edges follow the routing geometry. KiCad's `connection_width` did not report a 1 mm neck against a 2 mm minimum in kicad-cli 10.0.7 tests, so slivers are controlled by the fill's minimum width | — | CHK |
| CRAFT-51 | Q3 | Stitching vias (on no track) in one size, on the placement grid, on a regular pitch; the TI OPA1622 EVM rings its jack ground with stitching vias. | Pitch per board | Even return paths and an even appearance | [TI-OPA1622] §5.1 | CHK (size, grid); Review (pitch) |
| CRAFT-52 | Q4 | Matched visual density: no needless vias, no stray copper, similar fill across a block. | — | — | — | Review |

## 7. Documentation layers

The board file carries its own fabrication drawing, so the published files are complete without a separate PDF.

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-60 | Q2 | Fabrication notes on User.Comments or User.Drawings, titled "Fabrication notes": material, finish, mask and silk colours, impedance and test requirements, the pick-and-place rotation convention (CRAFT-15). | — | The order cannot drift from the design | IPC-2614 covers board fabrication documentation (public summary; the standard itself was not read) | CHK (present); Review (content) |
| CRAFT-61 | Q2 | The stackup table (KiCad: Place > Stackup Table) on a User layer, with the layer legend. | — | One source for the stackup | — | CHK |
| CRAFT-62 | Q2 | Board dimensions on User.Drawings: at least the outline's width and height, and the mounting holes and connector datums. | ≥ 2 | IPC-2615 covers dimensioning (public summary only) | — | CHK (count); Review (datums) |
| CRAFT-63 | Q2 | Layer roles fixed: Edge.Cuts outline only; User.Drawings dimensions; User.Comments notes; F/B.Fab body outlines and `${REFERENCE}` (KLC F5.2); F/B.Courtyard courtyards (KLC F5.3). | — | Every OpenDAP board reads the same | [KLC] F5.2, F5.3 | Review |

## 8. Colour and finish

The design system's palette is graphite, white and one orange accent, with "matte finishes" as an attribute, and orange reserved for the Action button [DS] §2.1, §3, §7. Its default logo colour is white on graphite [DS] §2.3. A board follows that palette; the specific finish is a cost and inspection decision, so it is a proposal.

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-70 | Q3 | **PROPOSAL, for the maintainers:** production boards in matte black solder mask with white silkscreen and ENIG finish; prototypes (Q1) in any PCBWay standard colour, green preferred. | Matte black / white / ENIG | Matte black is the closest offered colour to graphite; white silk is the logo's default colour on graphite. PCBWay offers matte black as a premium colour; its black mask needs a wider web (4 mil for black against 3 mil for green at the advanced minimum; 5 mil for colours other than green on the HDI page), and black hides traces from visual inspection, which is why prototypes stay green. ENIG is the research's proposal for the main board | [PCBWAY]; [RES] | Review |
| CRAFT-71 | Q2 | Mask and silk colours recorded in the KiCad stackup (Board Setup), the same on both sides, so renders and the fab notes match the order. | — | — | — | CHK |
| CRAFT-72 | Q2 | No accent colours on boards: no orange or coloured silk, no coloured mask other than the chosen one. | — | Orange belongs to the Action button | [DS] §3.3, §7 | Review |

## 9. Schematics

Schematics are read as often as boards: by reviewers, by HAT developers and by repairers. Requirements: readable printed at A4 (A3 for a dense top level), one function per sheet, signal flow left to right.

| ID | Level | Rule | Value | Why | Source | Enforcement |
|---|---|---|---|---|---|---|
| CRAFT-80 | Q1 | Title block on every sheet: title, revision, ISO 8601 date, "The OpenDAP Project", the licence's SPDX identifier in a comment field. | — | Same as CRAFT-24 | — | Review |
| CRAFT-81 | Q2 | Sheets A4, or A3 for a dense top level; text at least 1.27 mm (KiCad's default 50 mil). | A4 / A3, ≥ 1.27 mm | Readable when printed | — | Review |
| CRAFT-82 | Q2 | One function per sheet, named after the function; hierarchical sheets for repeated blocks. | — | — | — | Review |
| CRAFT-83 | Q2 | Signal flow left to right (inputs left, outputs right); higher voltages at the top, ground at the bottom. | — | — | — | Review |
| CRAFT-84 | Q2 | Net names in `UPPER_SNAKE_CASE`; differential pairs end `_P` / `_N` (KiCad's pair detection); active-low signals use KiCad's overbar `~{NAME}`; power rails in the R-notation of IEC 60062, `+3V3`, `+1V8`, plus `VBAT`, `VSYS`; one `GND` unless a separate return is designed. | — | Net classes and DRC rules match on names | — | Review |
| CRAFT-85 | Q2 | Power through power symbols only; no power drawn as wires between sheets. | — | — | — | Review |
| CRAFT-86 | Q2 | Symbols at 0° or 90°; pins and wires on KiCad's 1.27 mm grid; ERC check `endpoint_off_grid` at error. | 1.27 mm | — | KiCad defaults | ERC; Review |
| CRAFT-87 | Q3 | Mirrored channels drawn once, as one hierarchical sheet used twice, annotated by sheet (100 per sheet), so that CRAFT-34's pairs are R1xx / R2xx by construction. | offset 100 | Symmetry starts in the schematic | — | Review |

## 10. Practices studied, and the decisions taken

Only what a public source documents or a public photograph shows. "Observed" means seen in the cited photograph; "documented" means stated in the cited text.

| Practice | Evidence | Fits OpenDAP? | Decision |
|---|---|---|---|
| Legend reduced to connector labels and designators of connectors; passives unlabelled | Raspberry Pi 4 (observed) [RPI4] | Partly | **Not adopted.** An open board keeps a full legend (CRAFT-10, CRAFT-11): the published files and the DIY edition make it a repair document. Discipline (CRAFT-01 to -12) keeps it quiet instead |
| Board identification line: name, revision, date, holder, URL; licence on open boards | Raspberry Pi 4 (observed) [RPI4]; MNT Reform motherboard (observed) [MNT] | Yes | CRAFT-20 to CRAFT-22 |
| Open hardware published as KiCad sources under CERN-OHL-S, artwork CC-BY-SA, trademarks reserved | MNT Reform (documented) [MNT] | Yes | Already OpenDAP's licensing; the mark is used per the brand rules (CRAFT-22) |
| Black mask with white silk on an open board | MNT Reform (observed) [MNT] | Yes, as a proposal | CRAFT-70 |
| Silk text ≥ 0.032 in, 15 % ratio, vector font; labels aligned on guide lines; every LED and connector labelled | SparkFun (documented) [SFE] | Yes | CRAFT-01, CRAFT-02, CRAFT-12 |
| Bare PCB as the product's face | Teenage Engineering Pocket Operators (documented by a secondary source only) [TE] | No | The T1 has an enclosure; no rule |
| Mechanical drawings, STEP and pinouts published for third-party boards | Framework Laptop 13 (documented) [FW] | Yes | Already the component export contract |
| Left/right audio traces balanced; solid ground pour; a via at every component ground; stitching around the jack ground; layer plots published | TI OPA1622EVM, SBOU172 §5.1 (documented) [TI-OPA1622] | Yes | CRAFT-34, CRAFT-51; the T1's own audio rules live with the board |
| The inside of the product held to the outside's standard | Macintosh board, 1981 (documented) [FOLK-PCB]; the team's signatures inside every Mac case (documented) [FOLK-SIGN]; the same episode in Isaacson's biography (page **UNVERIFIED**) [ISAACSON] | Yes | The premise of this standard ([§1](#1-why)). Signatures: not adopted; contributors are recorded in the repositories |
| Stacked logic board: two boards soldered together through a perimeter interposer, about 70 % of the previous board's footprint | iPhone X (documented with photos) [IFX-X] steps 8, 9, 14; Apple patent US11006524B2 [PAT]; substrate-like PCB, 10–15 µm lines (search summary of TechInsights, **UNVERIFIED**) | No | **Not adopted.** The interposer is a custom part (T1-038), PCBWay prototyping does not cover the assembly, and rework becomes impractical. The T1 main board stays a single HDI board |
| Board shaped by the enclosure | Retina MacBook 2015: logic board 67 % smaller than the 11-inch MacBook Air's (documented) [IFX-MB] | Yes | CRAFT-35 |
| One bracket over every logic-board connector | iPhone X step 5 (documented) [IFX-X] | Yes | CRAFT-38 |
| Pentalobe and tri-point screws | iPhone X step 5; Retina MacBook 2015 (documented) [IFX-X]; [IFX-MB] | No | **Not adopted.** T1-055 asks for common tools: one standard screw family (CRAFT-36) |
| Glued battery; on iPhone 16, adhesive released electrically (9 V for 90 s) | Retina MacBook 2015 (documented) [IFX-MB]; Apple's iPhone 16 battery manual (documented) [APPLE-BATT] | No | T1-055: replaceable with common tools; the board side keeps the connector reachable and marked (CRAFT-14, CRAFT-39) |
| 100 % recycled gold plating and tin solder on Apple-designed boards | Apple Newsroom, 2026-04-16 (documented) [APPLE-ENV] | Not decided | PCBWay's offer is not known: **UNVERIFIED**; no rule |
| Black or blue mask, minimal silk, underfill, shield-can finish on Apple boards | No teardown step read for these | — | **UNVERIFIED**; no rule rests on them. Underfill is a reliability decision per BGA, to be taken with drop testing (open item) |

## 11. Enforcement summary

| Level | DRC (`opendap-craft.kicad_dru`) | CHK (`odapkit craft check`) | Review |
|---|---|---|---|
| Q1 | CRAFT-04, CRAFT-06 (Board Setup) | CRAFT-13, -14, -20, -23 | CRAFT-15, -25, -39, -80 |
| Q2 | CRAFT-01, -02, -03, -05, -07, -09, -40, -43, -45 | CRAFT-08, -10, -11, -21, -24, -30, -31, -34, -49, -60, -61, -62, -71 | CRAFT-35, -38, -63, -72, -81 to -86 |
| Q3 | CRAFT-41 | CRAFT-12, -22, -32, -33, -36, -42, -44, -46, -48, -50, -51 | CRAFT-26, -37, -70, -87 |
| Q4 | CRAFT-47 | — | CRAFT-52 |

CRAFT-86's grid check runs in ERC. Rules checked partly by a tool and partly by review are listed under the tool.

## 12. Open items

- **CRAFT-70:** the production mask, silk and finish: the maintainers' decision.
- **CRAFT-23:** whether to seek OSHWA certification.
- **The OpenDAP mark as a footprint:** kicad-lib has no `OpenDAP_Mark` footprint yet; it is to be generated from the brand's flat SVGs (blackbird-ui `brand/`), with the print minimum sizes, which the brand marks **UNVERIFIED** until a first print run.
- **Underfill** under the BGAs: a reliability decision after drop testing.
- **Pick-and-place convention per fab** (CRAFT-15): PCBWay's convention is not recorded in the research (**UNVERIFIED**).
- **Schematic checks:** CRAFT-80 to -87 are review items; a schematic counterpart of `odapkit craft check` is not written.

## 13. Sources

Pages fetched on 2026-10-24 unless stated.

| Key | Source |
|---|---|
| KLC | KiCad Library Conventions, footprint rules F4.2, F5.1, F5.2, F5.3, F6.2, F6.3, F7.2: <https://klc.kicad.org> (read from the source repository, <https://gitlab.com/kicad/libraries/klc>, `content/footprint/`) |
| KICAD-DRC | KiCad 10 custom design rules: <https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#custom_design_rules>; behaviour measured with kicad-cli 10.0.7 ([rule set README](../../design-rules/opendap-craft/README.md)) |
| EC-ROT | Eurocircuits, pin 1 and zero-point rotation (IPC-7351 and IEC 61188-7): <https://www.eurocircuits.com/technical-guidelines/pcb-assembly-guidelines/defining-pin-1-zero-point-rotation/> |
| EC-LEG | Eurocircuits, legend print guidelines (0.10 mm line, 1.00 mm height, 0.100 mm to exposed copper, 0.250 mm to a routed edge): <https://www.eurocircuits.com/pcb-design-guidelines-legend-print/> |
| PCBWAY | PCBWay capabilities (silkscreen line ≥ 0.15 mm, height ≥ 0.8 mm, width to height 1 : 5; mask colours: green, red, yellow, blue; premium white, black, matt green, matte black, purple; silk white, black, yellow): <https://www.pcbway.com/capabilities.html> |
| JLC | JLCPCB, character design specifications (≥ 0.15 mm line and ≥ 1.0 mm height standard; ≥ 0.15 mm to pads): <https://jlcpcb.com/blog/character-design-specifications> |
| RES | [PCBWay capabilities research](../research/2026-10-pcbway-capabilities.md) and the fab rule sets in [`design-rules/`](../../design-rules/) |
| SFE | SparkFun, designing for SparkFun manufacture: <https://learn.sparkfun.com/tutorials/how-to-sell-your-widget-on-sparkfun/designing-for-sparkfun-manufacture> |
| RPI4 | Raspberry Pi 4 Model B, top (photograph): <https://commons.wikimedia.org/wiki/File:Raspberry_Pi_4_Model_B_-_Top.jpg> |
| MNT | MNT Reform sources and licences: <https://source.mnt.re/reform/reform>; motherboard photograph: <https://mntre.com/media/reform_v2_images/reform_v2_motherboard.jpg> |
| FW | Framework Laptop 13 published drawings: <https://github.com/FrameworkComputer/Framework-Laptop-13> |
| TE | Pocket Operators (secondary source): <https://en.wikipedia.org/wiki/Pocket_Operators> |
| TI-OPA1622 | TI OPA1622EVM user's guide, SBOU172, §5.1: <https://www.ti.com/lit/pdf/sbou172> |
| AN-1490 | TI (National) AN-1490, LM4702 layout, mirrored channels: the English text was not read, **UNVERIFIED** |
| FOLK-PCB | Andy Hertzfeld, "PC Board Esthetics", July 1981: <https://www.folklore.org/PC_Board_Esthetics.html> |
| FOLK-SIGN | Andy Hertzfeld, "Signing Party", February 1982: <https://www.folklore.org/Signing_Party.html> |
| ISAACSON | Walter Isaacson, *Steve Jobs* (2011): <https://en.wikipedia.org/wiki/Steve_Jobs_(book)>; page **UNVERIFIED** |
| IFX-X | iFixit, iPhone X teardown, steps 5, 8, 9, 14: <https://www.ifixit.com/Teardown/iPhone+X+Teardown/98975> |
| IFX-MB | iFixit, Retina MacBook 2015 teardown: <https://www.ifixit.com/Teardown/Retina+Macbook+2015+Teardown/39841> |
| PAT | Apple Inc., US11006524B2, "Circuit board interposer": <https://patents.google.com/patent/US11006524> |
| APPLE-BATT | Apple, iPhone 16 battery replacement: <https://support.apple.com/en-us/120642> |
| APPLE-ENV | Apple Newsroom, 2026-04-16: <https://www.apple.com/newsroom/2026/04/apple-accelerates-progress-with-highest-ever-recycled-material-in-its-products/> |
| OSHWA | OSHWA certification requirements and mark usage: <https://certification.oshwa.org/requirements.html>, <https://certification.oshwa.org/mark-usage.html> |
| CERN-S | CERN-OHL-S-2.0, §1.9 and §4 (SPDX copy): <https://spdx.org/licenses/CERN-OHL-S-2.0.html> |
| DS | Engineered Matter design system: <https://github.com/opendap-project/blackbird-ui/blob/main/docs/specs/design-system.md> |
| BRAND | OpenDAP mark construction and minimum sizes: <https://github.com/opendap-project/blackbird-ui/blob/main/brand/README.md> |
