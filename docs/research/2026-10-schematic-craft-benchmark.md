# Research: KiCad schematic and symbol craft in open hardware projects

- **Date:** 2026-10-24
- **Status:** Research note, written by Claude for the schematic part of the [PCB craft standard](../specs/pcb-craft-standard.md) (§9). It records what published projects do; the decisions taken from it are in the standard's §9.9 and in §5 below.
- **Scope:** generic: what any OpenDAP board's schematics and symbols should follow. The T1 is mentioned only as an example.

## 1. Method

On 2026-10-24 each candidate repository was cloned shallowly (`git clone --depth 1 --filter=blob:limit=5m`) into a scratch directory, and the commit was recorded with `git rev-parse HEAD`. The Raspberry Pi CM4 IO board was downloaded as the official zip (`https://datasheets.raspberrypi.com/cm4io/CM4IO-KiCAD.zip`, SHA-256 `5ea867e17968cb9c117fbce7a982ea395d66a6ee605253a9a0879483bbfcb0aa`). No files were copied anywhere else.

Measurements come from a small Python S-expression parser run over every `.kicad_sch`, `.kicad_sym` and `.kicad_pro` in each project, plus regular expressions for KiCad 5 `.sch` files. It reads:

- file format `version` and `generator`, `paper`, `title_block`;
- `sheet` instances, sheet names and sheet pins, and what is placed on the root sheet;
- placed `symbol`s. Power symbols (`power:` lib ids or `#` references) are counted separately. For each field the parser records whether it is present, filled and visible;
- `label` / `global_label` / `hierarchical_label` counts and net-name style. Style covers case, active-low notation and bus syntax; differential `_N` names whose `_P` partner exists are excluded from the active-low counts;
- `junction`, `no_connect`, `wire`, `bus`, `text`, `image`, `table`, `polyline`;
- `(dnp yes)`, `(in_bom no)`, font faces;
- pins in the embedded `lib_symbols`. Only symbols with five or more pins (ICs, connectors) are measured, by length, grid alignment and electrical type, weighted by pin count;
- in `.kicad_pro`: `text_variables`, drawing sheet path, ERC severities changed from default, net classes and bus aliases.

Caveats: symbol counts are per placement in a file and are not multiplied by repeated sheet instances. A field "present" on 100 % of symbols can still be empty; both numbers are given. Mapping file-format versions to KiCad releases where no `generator_version` is written (20211123 → KiCad 6, 20230121 → KiCad 7) is from general knowledge: **UNVERIFIED** against KiCad release notes in this run. CI was checked by reading repository CI files only. External CI templates that are not public could not be read.

## 2. Sources

| Project | Source | Commit / checksum | KiCad files inspected |
|---|---|---|---|
| MNT Reform 2 motherboard 3.0 | <https://source.mnt.re/reform/reform> | `9dcb9a8df504f7c448625f463d4340d86197ee82` | `reform2-motherboard30-pcb/` (13 sheets, eeschema 8.0); also `reform2-imx8mplus/` |
| MNT Pocket Reform motherboard | <https://source.mnt.re/reform/pocket-reform> | `dac3836e92c4b80b59c8f006516e6e4b80262176` | `pocket-reform-motherboard/` (1 sheet, eeschema 10.0) |
| Great Scott Gadgets Cynthion | <https://github.com/greatscottgadgets/cynthion-hardware> | `13aa71c2fb0be3837cd2ec580ee5d2c25fc1c678` | root (17 files, format 20230121) |
| Great Scott Gadgets HackRF One | <https://github.com/greatscottgadgets/hackrf> | `468c5d93b66032c892c95bbf9ff15ff1b803e84f` | `hardware/hackrf-one/` (4 files, format 20211123) |
| Great Scott Gadgets GreatFET (brief) | <https://github.com/greatscottgadgets/greatfet-hardware> | `ecd3ca18efa2ec5a096f27ce671451b87aceff6e` | `azalea/azalea.sch` (KiCad 5 legacy) |
| Glasgow Interface Explorer revD1 | <https://github.com/GlasgowEmbedded/glasgow> | `bd383cafc9978f835bcd6a50f0a722803b426187` | `hardware/boards/glasgow/revD1/` (8 files, eeschema 10.0) |
| Antmicro Jetson Orin baseboard | <https://github.com/antmicro/jetson-orin-baseboard> | `34f0e7f5fbca441191e20ed55d93cf8614e12bed` | root (10 files, eeschema 8.0) |
| Antmicro Kria K26 devboard | <https://github.com/antmicro/kria-k26-devboard> | `9ead4dfc5b29fa9308206ccdfe013dd8f6d93b67` | root (19 files, format 20230121) |
| Antmicro SDI-MIPI bridge | <https://github.com/antmicro/sdi-mipi-bridge> (umbrella `0ee4fb382c105459187c432268055f4e17f37759`) → <https://github.com/antmicro/sdi-mipi-bridge-hw> | `0d08a865eba70ac02bfe16601bbf6d719d5c9d41` | 1 file, format 20230121 |
| Raspberry Pi CM4 IO board | <https://datasheets.raspberrypi.com/cm4io/CM4IO-KiCAD.zip> | SHA-256 above | `CM4IOv5.kicad_*` (7 files, format 20211123) |
| Olimex OLinuXino (A64 rev H, STMP157-LIME2 rev B1) | <https://github.com/OLIMEX/OLINUXINO> | `b48543c9674439c97a5bfa2024830f22a94d7a35` | `HARDWARE/A64-OLinuXino/1. Latest hardware revision/…rev H/`, `HARDWARE/STMP157-OLinuXino-LIME2/1. Latest…/` (KiCad 5 legacy) |
| Framework expansion cards | <https://github.com/FrameworkComputer/ExpansionCards> | `2904a95d60d4ba771c5c3c56d6fdba7078243fe8` | `Electrical/KiCad_templates/Expansion_Card/`, `Electrical/Microcontroller/` (KiCad 5 legacy) |
| KiCad official symbols | <https://gitlab.com/kicad/libraries/kicad-symbols> | `9280a937942c74c7d6fd5148a2d49ee7d87773d1` (2026-10-15) | all 22,908 `.kicad_sym` (format 20251024, generator 10.0) |
| KiCad Library Conventions (KLC) | <https://gitlab.com/kicad/libraries/klc> | `6e8cbad9556359879d2b91f904d6df82517d97d1` | `content/symbol/S3`, `S4`, `S6`, `S7` |
| KiCad library tools (KLC CI) | <https://gitlab.com/kicad/libraries/kicad-library-tools> | `36d1ed208379d7c4127661ac384118cc6837392b` | `.gitlab-ci-symbols.yml` |
| SparkFun KiCad libraries | <https://github.com/sparkfun/SparkFun-KiCad-Libraries> | `bb5d58fc355c36ba934326785eea3517d13284ab` | `symbols/` (30 files, 780 symbols) |

Candidates skipped or not found:

- **Precursor** (<https://github.com/betrusted-io/betrusted-hardware>, `fecea1061a07330163fad5ab834a63d52f23e575`): the sources are Altium (`*.SchDoc`, `*.PrjPcb`), not KiCad.
- **OpenMV** (<https://github.com/openmv/openmv-boards>, `44d4267aebae054ca22951e27e945163afbb30ce`): contains only `boards.json`, pinout JSON and a `.glb` model, with no schematic sources.
- **Adafruit KiCad library**: `github.com/adafruit/Adafruit-KiCad-Library` and `Adafruit_KiCad_Library` returned "Repository not found". Not inspected.
- **Pine64**: `github.com/pine64/pinecil` returned "Repository not found". Pine64 KiCad sources were not located. **UNVERIFIED** whether any exist.
- **Raspberry Pi CM5 IO**: three guessed URLs under `datasheets.raspberrypi.com/cm5/` returned 404. **UNVERIFIED** whether KiCad files are published.
- **Antmicro templates**: `antmicro/antmicro-kicad-templates`, `kicad-templates` and `antmicro-pcb-release-ci-template` are not public on GitHub. Antmicro's `.ci.yml` includes `antmicro-pcb-release-ci-template@main`, so its contents are **UNVERIFIED**.
- **Not inspected for time**: Sipeed, Radxa, Arduino UNO Q / Portenta carriers, Framework mainboard docs, the GreatScott library.

## 3. Per-project findings

### 3.1 MNT Reform 2 motherboard 3.0 (reform)

- **Drawing sheet and title block.** Default drawing sheet (no `page_layout_descr_file`). On 12 of 13 sheets the title block holds a per-sheet title, `date 2023-02-13`, `rev 2.5D-2`, `company MNT Research GmbH`, `comment1 <https://mntre.com>`, `comment2 Engineer: Lukas F. Hartmann` and `comment3 License: CERN-OHL-S 2.0`. Paper: A4 (12 files), A4 portrait (1).
- **Hierarchy.** 12 sheet instances: 8 on the root, the rest nested. Every sheet is named "Reform 2 <function>" (Audio, Display, Ethernet, HDMI, LPC, PCIe, Power, Regulators, SD Card, USB, USB Power, USB-C). The sheet symbols carry **0 sheet pins**: connectivity is flat, through global labels. The root also holds 32 components (mounting holes, BOOTCFG DIP switch, I²C) and 18 notes.
- **Symbols.** Placed symbols come mostly from the KiCad stock libraries (`Device` 406 of 529), plus project libraries. IC/connector pins: 60 % at 2.54 mm, 27 % at 5.08 mm, 12 % at 3.81 mm; 83 % on the 100 mil grid, 16 % on 50 mil only.
- **Fields.** 529 placed symbols. `Manufacturer` and `Manufacturer_No` are present and filled on 100 %. `Distributor` is on 80 % (400 "Mouser"). `Checked` is on 80 %, with 417 "y" and 10 empty: a per-part review tick. `LCSC` is on 15 %. Every field beyond Reference and Value is hidden.
- **Nets.** 143 local labels, 396 global, 0 hierarchical. 503 of 546 names are UPPER case. Active low uses `~{…}` on 5 unique names. 55 differential negatives use `_N`/`N` with a `_P` partner.
- **Power.** GND 178, +3V3 23, PWR_FLAG 22, +5V 9, +1V8 5. 610 junctions, 203 no-connects, 130 text notes.
- **Variants.** 24 symbols carry `(dnp yes)`; 3 % also carry a `DNP` field.
- **Checks.** `.gitlab-ci.yml` builds firmware only (`build-all.sh`); there is no ERC/DRC in CI. The `.kicad_pro` overrides ERC only for `simulation_model_issue`. Net classes: Default and BIGPWR.
- **Contrast.** `reform2-imx8mplus` is a single A2 sheet with 247 global labels, 0 local labels and an empty title block (date only).

### 3.2 MNT Pocket Reform motherboard

- **Single sheet.** One A0 sheet, eeschema 10.0, with 443 symbols, 2,115 wires, 206 text notes and 2 images. An A3 "poster" PDF is committed (`pocket-reform-motherboard/pocket-reform-schematics-poster-a3.pdf`).
- **Title block.** `MNT Pocket Reform`, `2026-06-01`, `rev 2.0 R-1`, company, engineer and licence in comment1–2.
- **Drawing sheet.** `.kicad_pro` points at `${KICAD_USER_TEMPLATE_DIR}/blank.kicad_wks`, which is not in the repository, so the drawing sheet is not reproducible from the repo.
- **Fields.** `Manufacturer_No` on 98 %, `LCSC` on 95 %. 23 other field names appear on fewer than 1 % of symbols, as SnapEDA leftovers such as `SNAPEDA_PN`, `Check_prices`, `Purchase-URL`.
- **Nets.** 94 local labels, 477 global. 65 differential negatives; `~{…}` on 10 names.
- **Other.** 537 junctions, 208 no-connects, `(dnp yes)` on 34 symbols. Net classes: Default, "90ohm diff inner layer", Power. No schematic CI.

### 3.3 Great Scott Gadgets Cynthion

- **Title block through text variables.** `.kicad_pro` defines `TITLE=Cynthion`, `DATE=2024-08-27`, `VERSION=1.4.0`, `COPYRIGHT=Copyright 2019-2024 Great Scott Gadgets` and `LICENSE=Licensed under the CERN-OHL-P v2`. All 17 title blocks use `${TITLE}`, `${DATE}`, `${VERSION}`, `${COPYRIGHT}`, `${LICENSE}`, so one edit updates every sheet. Paper is A4 throughout.
- **Root is a functional block diagram.** It holds 14 sheet symbols with 68 sheet pins, wired with 32 bus segments and 3 `bus_alias` definitions. Its only symbol is an OSHW logo, and its one note reads "ECP5 FPGA". Sheet names describe function: "FPGA Banks 2 and 3", "Power Distribution and Monitoring", "TARGET Type C Controller"… One schematic, `usb_phy`, is reused for the AUX, CONTROL and TARGET PHYs (19 instances from 17 files).
- **Buses.** Group buses such as `AUX_PHY{ULPI}`, `FPGA_JTAG{JTAG}` and `RAM{HyperRAM}` use member names like `AUX_PHY.~{RESET}`. Vector buses `LED[0..5]` and `PMOD_A[1..10]` appear on 11 labels, group buses on 44. There are 278 bus segments and 226 bus entries.
- **Labels.** 283 local, 88 hierarchical, 33 global. The global labels are kept to power-sense nets (`*_VBUS`, `*_SENSE±`).
- **Naming.** Upper case on 401 of 412 names; active low always `~{…}` (24 unique).
- **Symbols.** IC/connector pins are 85 % 5.08 mm (200 mil). 83 % of pin endpoints sit on the 50 mil grid only, which deviates from KLC S4.1's 100 mil rule.
- **Fields.** `Manufacturer`, `Part Number` and `Description` on 85 %. `Substitution` on 64 %: 145 "any equivalent", plus lists of approved alternates such as `LFE5U-12F-*BG256*, LFE5U-25F-*BG256*`.
- **DNP.** A visible `DNP` field ("DNP" on 11 symbols) plus `(in_bom no)` on 48. The `(dnp yes)` attribute is not used.
- **Checks.** No ERC/DRC CI in the repository. ERC override: `simulation_model_issue` only.

### 3.4 Great Scott Gadgets HackRF One

- **Title block.** The same text-variable title block as Cynthion (`VERSION=10`, `DATE=2023-12-09`). Paper is a user size of 431.8 × 279.4 mm (11 × 17 in), and the default text size is raised to 60 mil.
- **Root.** 3 sheets (`baseband`, `frontend`, `mcu/usb/power`), with 0 sheet pins and nothing else. Connectivity is flat through 161 global and 326 local labels.
- **Symbols.** IC pins are 78 % 7.62 mm (300 mil, the KLC maximum).
- **Fields.** `Manufacturer`, `Part Number` and `Description` on 77 %; `Substitution` on 60 %.
- **DNP.** A `DNP` field ("DNP" on 34 symbols) and `(in_bom no)` on 78.
- **Active low.** Leading `!` (5 names), not `~{}`. All 228 unique names are UPPER.
- **Checks.** ERC override `multiple_net_names: ignore`. The GitHub workflows (`build.yml`, `clang-format-check.yml`, `includes-check.yml`) cover firmware and host software, not hardware.

### 3.5 GreatFET Azalea (brief, KiCad 5)

US Ledger paper. `Manufacturer`/`Part Number`/`Description` on 74 %, `Note` on 30 % (87 % of them visible). The title block puts the licence in comment1 (`License: BSD-3-Clause`) and the URL in comment2. 252 local labels, 0 global.

### 3.6 Glasgow revD1

- **Title block.** KiCad 10 files (`generator_version 10.0`). Per-sheet titles ("FPGA - IF, Flash and Sync"), `date 2026-09-23`, `rev D1`, `company ln / Fully Automated`, `comment1 Glasgow Debug Tool`. A4 throughout.
- **Root.** 5 sheet symbols with 49 sheet pins wired by buses (73 bus segments on the root), plus 90 symbols (FX2 MCU support, LEDs, test points) and 13 engineering notes. Examples: "Imax(USB) @ 3V3 = 80 mA", "Release reset while shorting these pads if it ever stops enumerating", and a link to a KiCad library merge request. 10 sheet instances in total; the IO bank sheet is reused for Banks A–D.
- **Table.** A **KiCad `table`** (3 columns, 60 cells) on the root gives the I²C address map: Address / Device / Note.
- **Buses.** 4 project bus aliases (`ADC`, `FX2`, `LVDS`, `NAFE`) in `.kicad_pro`. 500 bus segments, 404 bus entries.
- **Labels.** 623 local, 97 hierarchical, 17 global (4 unique). Active low is `~{…}`; it is even nested inside alias members (`NAFE_{~{CS}}`).
- **Fields.** `MPN` and `LCSC` on 92 %, filled on 99 %. `Description` on 100 %. `MPN_Alt` and `Note` are rare. `KLC_S4.1` (empty) is inherited from stock symbols on 86 %. Values are short ("1uF", "4.7k", "0").
- **Variants.** `(dnp yes)` on 43, `(in_bom no)` on 11, `(exclude_from_sim yes)` on 4.
- **Symbols.** IC/connector pins are 62 % 5.08 mm and 30 % 2.54 mm; 88 % on the 100 mil grid.
- **Project settings.** `label_size_ratio 0.375`, `pin_symbol_size 25`. ERC ignores `four_way_junction`, `single_global_label`, `footprint_filter`.
- **Outputs.** Fabrication outputs and `output/schematics.pdf` are committed. GitHub CI (`main.yml`) covers software and firmware; there is no ERC/DRC job. `hardware/scripts/` holds BOM XSLT (`bom2grouped_csv.xsl`, `bom2mouser.xslt`).

### 3.7 Antmicro Jetson Orin baseboard

- **Title block.** A3 throughout. Title `Jetson Orin Baseboard`, `date 2025-03-12`, `rev 1.3.4` (semantic version), `company Antmicro Ltd`, `comment1 www.antmicro.com`.
- **Root.** 9 sheets with **0 sheet pins**, plus a 3D render of the board, logos, and the repository URL as text. Connectivity is flat: 517 local and 441 global labels, 0 hierarchical. `.kicad_pro` sets `intersheets_ref_show: true`, so global labels print the sheets they appear on.
- **Atomic parts library.** Lib ids encode value and package: Values are `R_0R_0402` (120), `C_100n_0402` (96), `TP_0.75mm_SMD`. The Value field is hidden on 100 %. A separate `Val` field (`0R`, `100n`, `10k`) is visible on 67 % of symbols, the passives. `MPN` and `Manufacturer` are on 100 % (filled 92 %). `Datasheet` is filled 92 %. `License: Apache-2.0` and `Author: Antmicro` sit on every symbol (1,600 property occurrences). `Tolerance`, `Voltage` and `Dielectric` appear on 23–39 %.
- **Net classes and nets.** 8 net classes named by impedance and interface: `85Ohm-diff_USB_SS`, `100Ohm-diff_HDMI`, `PoE`… plus 5 `netclass_flag` directives in the schematic. 957 of 967 names are UPPER, with 104 differential negatives as `_N`. Active low: `~{…}` on 29 names.
- **Variants.** `(dnp yes)` on 77, `(in_bom no)` on 125.
- **Checks.** ERC ignores `pin_to_pin`. `.ci.yml` includes `antmicro-pcb-release-ci-template@main:.pcb-repo-ci.yml`; its contents are **UNVERIFIED** (not public). A schematic PDF is committed under `doc/`.

### 3.8 Antmicro Kria K26 devboard and SDI-MIPI bridge

- **Kria root.** A3 throughout, 19 files, 18 sheet instances. The root wires **13 sheets with 176 sheet pins** (fully hierarchical, unlike the Orin board) and carries logos.
- **Kria labels and library.** 668 local, 232 hierarchical, 143 global (12 unique) labels. Vector buses on 29 hierarchical labels. All 664 symbols come from one project library (`kria-k26-devboard:`), the same atomic-part scheme (`R_330R_0402`).
- **Kria title block.** The company goes in comment2 (`Antmicro Ltd.`), and the company field is filled on only 1 of 19 sheets.
- **Kria checks.** ERC ignores `pin_to_pin` and `no_connect_connected`.
- **SDI-MIPI bridge.** A single A2 sheet with 188 symbols, 220 local and 20 global labels, `MPN` on 100 % (filled 89 %) and a `DNP` field on 12 %.

### 3.9 Raspberry Pi CM4 IO board

- **Title block.** A4. Per-sheet titles ("Compute Module 4 IO Board - PSUs"), `company © 2020-2022 Raspberry Pi Ltd …`, `comment1 www.raspberrypi.com`. Rev is filled on 6 of 7 sheets; there is no date.
- **Root.** 6 sheets wired with 54 sheet pins. Beside each sheet a text note lists the connectors it contains ("Connectors / ------- / HDMI 0 / HDMI 1 / CSI 0…"). Sheet names: `PSUs`, `PCIe-connector`, `USB2-HUB`, `CM4_HighSpeed`…
- **Fields.** Unnamed custom fields `Field4`–`Field8` hold distributor, distributor PN, MPN, manufacturer and an internal number (`Digikey`, `490-14381-1-ND`, `GRM21BR71A106KA73L`, `Murata`, `111893011`) on about 98 %. `Part Description` is on 95 %. The meaning of the fields is not self-describing.
- **Nets.** 362 local and 55 hierarchical labels, 0 global. Case is mixed: 61 lower-case uses. Active low uses an `n` prefix (`nRESET` style, 5 names). 7 net classes by impedance (`100R`, `90R`, `50R`, `75R`, `HDMI`, `POE TAPS`).
- **Checks.** No ERC overrides.

### 3.10 Olimex OLinuXino (KiCad 5)

- **A64 rev H.** Root A2 plus 3 A3 sheets named by content ("USB&HDMI,WiFi&BT,Ethernet,LCD"). Title block: `Title`, `Date 2025-05-21`, `Rev H`, `Comp OLIMEX LTD, Bulgaria`, `Comment1 <c> 2025`.
- **Values.** Values encode the specification: `100nF\10V/10%`, `10uF\6.3V/20%`. There are no MPN fields: custom fields are template placeholders (`"Fieldname 1"`, value `"Value 1"`) on 11 %.
- **Variants.** Handled by one BOM file per variant (6 BOMs for A64 rev H: `_1G_BOM`, `_2Ge16G-IND_BOM`…), and "NA" as a Value for unpopulated parts (12).
- **Nets.** Active low as `#` suffix (`AP-RESET#`) and `-N`. Hyphen-separated names (`BT-UART-TX`).
- **STMP157-LIME2 rev B1.** Same style: 635 local and 121 global labels.

### 3.11 Framework expansion cards (KiCad 5, brief)

The templates are shipped as KiCad project templates (`meta/info.html`, `meta/icon.png`). Title block: `Title`, `Rev X1`, `Comp Framework`, licence text in comment1 (CC-BY-4.0), URL in comment4. The Microcontroller card adds a visible `Population` field on 9 % of symbols. The cards are small (11 to 32 symbols), local labels only. These show template distribution rather than schematic craft.

### 3.12 KiCad official library and KLC as practised

The KLC text (repo `klc`, `content/symbol/`) sets these rules:

- **S4.1** Pin origin on the 100 mil grid. Pin length at least 100 mil, in 50 mil steps, at most 300 mil, and all pins on a symbol the same length.
- **S3.1** Origin centred.
- **S3.2** Text 50 mil.
- **S3.3** Body line 10 mil; background fill for black-box ICs, no fill for simple parts.
- **S4.2** Positive supplies at the top, ground at the bottom, inputs left, outputs right, pins grouped by function.
- **S4.3** Since KiCad 10, native pin stacks; the overlapping-pin workaround "must not be used anymore".
- **S4.6** No hidden pins except NC.
- **S6.2** Reference and Value visible. Footprint and Datasheet hidden. Description and keywords filled. "No other custom fields" (exceptions as `KLC_…`).
- **S7.1** Power symbols: `#PWR`, one visible `power_in` pin since KiCad 8.

Measured over all 22,908 symbol files (12,324 derived via `extends`):

- **Pins** (8,985 symbols with five or more pins, 537,706 pins). Lengths: 6.35 mm 32 %, 5.08 mm 29 %, 2.54 mm 20 %, 3.81 mm 11 %. **98 % on the 100 mil grid.** The long pins follow the S4.1 rule tying length to pin-number width (BGA pins such as "AB12" need longer pins).
- **Fields.** Reference visible on 99 %. Footprint hidden on 100 % (filled 79 %: generic symbols leave it empty by rule). Datasheet hidden, filled 87 %. Description filled 98 %. `ki_keywords` on 98 %, `ki_fp_filters` on 94 %.
- **Bodies.** Body rectangles are 0.254 mm on 12,207 rectangles, with background fill on 11,645. A further 50,013 rectangles at 0.1524 mm with no fill are mostly connector pin stubs; that attribution is inferred from counts and is **UNVERIFIED** symbol by symbol.
- **Audio library subset** (118 symbols: DACs, ADCs, codecs). IC pins are 98 % 2.54 mm and 100 % on the 100 mil grid; Description, keywords and footprint filters are on 100 %.
- **CI** (`kicad-library-tools/.gitlab-ci-symbols.yml`): every merge request touching `*.kicad_sym` runs `klc-check` (`check_symbols.sh`, JUnit report; exit code 2 means warnings only). A `visual_diff` job then renders HTML diffs with `kicad-cli` in `kicad/kicad:nightly`.

### 3.13 SparkFun KiCad libraries (brief)

780 symbols in 30 files, no `extends`. IC pins: 72 % 2.54 mm, 25 % 3.81 mm. Only **47 % on the 100 mil grid**, 52 % on 50 mil.

An internal `PROD_ID` field is on 82 %. The README says it holds SparkFun's internal part numbers for its SMD line, and that the library follows KLC "where it makes sense" and prefers stock KiCad symbols. `Tolerance`, `Voltage`, `IMax` and `VMax` are visible fields on passives.

GitHub workflows (`build_asset.yml`, `build_asset_release.yml`) package the library; no symbol checks were found in them.

## 4. Cross-project synthesis

### 4.1 Measured overview

| Project | Sheets (root wiring) | Paper | Local / hier / global labels | Sourcing fields (present / filled) | DNP mechanism | Active low | IC pin length mode | 100 mil grid |
|---|---|---|---|---|---|---|---|---|
| Reform MB 3.0 | 12 (0 pins, flat) | A4 | 143 / 0 / 396 | Manufacturer + MPN 100 % / 100 % | `(dnp yes)` 24 | `~{}` | 2.54 (60 %) | 83 % |
| Pocket Reform MB | 1 | A0 | 94 / 0 / 477 | MPN 98 %, LCSC 95 % | `(dnp yes)` 34 | `~{}` | 2.54 (61 %) | 91 % |
| Cynthion | 19 (68 pins, buses) | A4 | 283 / 88 / 33 | MPN 85 %, Substitution 64 % | DNP field + `in_bom no` | `~{}` | 5.08 (85 %) | 16 % |
| HackRF One | 3 (0 pins, flat) | 11×17 in | 326 / 0 / 161 | MPN 77 %, Substitution 60 % | DNP field + `in_bom no` | `!` | 7.62 (78 %) | 42 % |
| Glasgow revD1 | 10 (49 pins, buses) | A4 | 623 / 97 / 17 | MPN 92 %, LCSC 92 % | `(dnp yes)` 43 | `~{}` | 5.08 (62 %) | 88 % |
| Antmicro Orin | 9 (0 pins, flat + intersheet refs) | A3 | 517 / 0 / 441 | MPN 100 % / 92 % | `(dnp yes)` 77 | `~{}` | 2.54 (48 %) | 81 % |
| Antmicro Kria | 18 (176 pins) | A3 | 668 / 232 / 143 | MPN 100 % / 89 % | `(dnp yes)` 28 | `~{}` | 2.54 (61 %) | 74 % |
| RPi CM4 IO | 6 (54 pins) | A4 | 362 / 55 / 0 | unnamed Field4–8 ~98 % | none found | `n` prefix | 2.54 (46 %) | 90 % |
| Olimex A64 H | 3 + root | A2/A3 | 559 / 0 / 76 | none (spec in Value) | per-variant BOM files, "NA" | `#` suffix | n/m | n/m |
| KiCad library | — | — | — | (KLC forbids custom fields) | — | (`~{}` in pin names) | 6.35 (32 %) | 98 % |

(n/m: not measured. The legacy `.lib` pin parser was not built.)

### 4.2 Common practice (≥ 6 of 9 KiCad 6+ projects)

- **Upper-case net names**, above 90 % of names in every project except CM4 IO. Differential pairs as `_P`/`_N`.
- **Active low with KiCad overbar `~{…}`**: 7 of 9 (Reform, Pocket, Cynthion, Glasgow, Orin, Kria, SDI).
- **Stock KiCad stroke font.** No `(font (face …))` appears in any inspected schematic.
- **No custom drawing sheet.** 0 `.kicad_wks` files in any repository; the title block is filled through the stock layout.
- **Title block fields.** Title, date, revision, company and a URL or licence in the comment lines in 8 of 9. Licence text appears in the title block at MNT, GSG, Framework and GreatFET.
- **Hidden sourcing fields.** A manufacturer part number on at least 77 % of placed symbols (7 of 9), always hidden. Reference and Value are the only routinely visible fields, except Antmicro (visible `Val`) and GSG (visible `DNP`).
- **`(dnp yes)` attribute** in the KiCad 8+ projects (Reform, Pocket, Glasgow, Orin, Kria). The KiCad 7 GSG projects use a DNP field instead.
- **No ERC/DRC in repository CI** in any board project. ERC is changed per project by ignoring rules, most often `simulation_model_issue`. Antmicro ignores `pin_to_pin`.
- **Impedance-named net classes** at Orin, CM4 IO, Pocket and Kria.

### 4.3 Rare but strong practice

- **Title block from project text variables** (GSG: `${TITLE}`, `${VERSION}`, `${DATE}`, `${COPYRIGHT}`, `${LICENSE}`). One source of truth for revision and licence on every sheet.
- **Root sheet as a wired functional block diagram** (Cynthion: 14 sheet symbols, buses, bus aliases; Kria: 176 sheet pins). By contrast, Reform, HackRF and Orin roots show unconnected boxes and rely on globals.
- **Bus aliases and group buses** for interfaces (Glasgow `FX2`/`LVDS`/`NAFE`; Cynthion `ULPI`, `JTAG`, `HyperRAM`).
- **Reused sheets for repeated channels** (Cynthion `usb_phy` ×3, Glasgow IO banks ×4).
- **A KiCad table for a design register** (Glasgow I²C address map on the root).
- **Engineering notes with numbers** beside the circuit: Glasgow current budgets, Reform BOOTCFG notes, CM4 IO connector index per sheet.
- **An approved-alternates field** (GSG `Substitution`, Glasgow `MPN_Alt`).
- **A per-part review tick** (`Checked: y` on 417 Reform parts).
- **Intersheet references on global labels** (Orin `intersheets_ref_show: true`).
- **Committed schematic PDF** next to sources (Glasgow `output/schematics.pdf`, Orin `doc/…pdf`, Pocket A3 poster).
- **Library-level CI** (KiCad: `klc-check` and a `kicad-cli` visual diff on every merge request). It is not seen at board level in any project.

### 4.4 Observed weaknesses (to avoid)

- Drawing sheet referenced from a user directory outside the repo (Pocket: `${KICAD_USER_TEMPLATE_DIR}/blank.kicad_wks`).
- Unnamed custom fields (`Field4`–`Field8` at CM4 IO) and placeholder fields (`Fieldname 1` at Olimex).
- SnapEDA leftover fields on imported symbols (Pocket, Reform `Mouser Price/Stock`).
- Specification packed into Value (Olimex `100nF\10V/10%`), and variants as separate hand-made BOM files.
- Pins off the 100 mil grid (Cynthion 83 % on the 50 mil grid only, SparkFun 52 %).
- Several active-low conventions in one ecosystem (`~{}`, `!`, `#`, `n`).
- Silencing whole ERC classes (`pin_to_pin` at Antmicro).
- No automated ERC anywhere at board level.

## 5. What OpenDAP adopts, adapts or rejects

Decided by Claude under the maintainers' delegation (2026-10-24) in the craft standard §9; the rows marked **for the maintainers** are listed in the standard's open items.

| Practice | Decision | Rule | Reason |
|---|---|---|---|
| KLC S3, S4, S6, S7 for symbols (100 mil grid, pin length by pin-number width, 50 mil text, 10 mil body, background fill, supplies top, ground bottom, inputs left, outputs right, native pin stacks) | Adopt | CRAFT-120 to -131 | The stock library meets it (98 % on grid), so OpenDAP symbols mix with it |
| No hidden pins, NC pins included | Adapt (stricter than KLC S4.6) | CRAFT-125 | A hidden pin cannot take a visible no-connect flag; every pin is accounted for on the sheet |
| Upper-case net names, differential pairs `_P` / `_N` | Adopt | CRAFT-84 | Majority practice |
| Active low as `~{NAME}` on nets | **Adapt, for the maintainers:** `~{}` on symbol pin names (KLC S4.7), suffix `_N` on net names | CRAFT-84, CRAFT-124 | The T1's pin plan and net classes already name nets with `_N` (pinout v1); a plain suffix survives netlists, CSV pin plans, devicetree and net-class patterns without markup. The clash with differential `_N` is resolved by the partner: a net ending `_N` is a pair member only if its `_P` exists |
| Title block from project text variables | Adopt | CRAFT-80, -101 | One source for project, board, licence and source location (Cynthion, HackRF) |
| Custom drawing sheet | Adapt: one, in kicad-lib, referenced through the pinned submodule | CRAFT-100 | No benchmark project ships one; Pocket Reform's points outside its repository |
| Root sheet as a wired block diagram, function-named sheets, reused sheets for repeated channels | Adopt | CRAFT-82, -87, -110 to -113 | Cynthion, Glasgow, Kria; the root shows the architecture and the connectivity |
| Flat designs through global labels | Reject | CRAFT-150 | Reform, HackRF, Orin roots show no data flow; globals only for rails |
| Hidden named sourcing fields, an alternates field | Adopt | CRAFT-140, -144 | MPN on 77–100 % in 7 of 9 projects; GSG `Substitution`, Glasgow `MPN_Alt` |
| `(dnp yes)` and KiCad 10 design variants | Adopt | CRAFT-147 | Native; variants as data (RFC 0011) |
| Impedance-named net classes from the schematic | Adopt | CRAFT-155 | Orin, CM4 IO; the T1 board already names classes `<name>_<ohms>D` |
| Engineering notes with numbers, KiCad tables for registers | Adopt | CRAFT-115, -172, -176 | Glasgow I²C table and current notes |
| Visible value of passives | Adapt: short SI Value plus a visible `Spec` field | CRAFT-141, -143 | Keeps Value machine-readable; rejects Olimex's packed values and Antmicro's hidden Value |
| Atomic value-specific symbols | Reject | — | Multiplies symbols, departs from the stock library |
| Unnamed, placeholder or vendor-leftover fields | Reject | CRAFT-140, -143 | CM4 IO, Olimex, Pocket |
| Single poster-size sheet | Reject | CRAFT-81 | Pocket, i.MX8M Plus board: readable only as a poster |
| Disabling ERC rule classes | Reject | CRAFT-158 | Hides real errors |
| ERC and library checks only in a CI elsewhere | Adapt: local, through `odapkit craft check` and pre-commit | CRAFT-158, §9.8 | No board project runs ERC in CI; OpenDAP runs checks locally |
| Schematic PDF next to the sources | Adapt: generated at release by the fab package, never committed | — | Local-only pipeline; no generated outputs in repositories |
| Per-part review tick (Reform `Checked`) | Not adopted now; **open** | — | Useful at bring-up; needs a decision on who clears it |
