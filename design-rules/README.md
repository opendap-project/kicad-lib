# Design rules

KiCad custom design rules (`.kicad_dru`) for the fabs OpenDAP uses.

## OpenDAP rule sets

Written from PCBWay's published capabilities as recorded in [`docs/research/2026-10-pcbway-capabilities.md`](../docs/research/2026-10-pcbway-capabilities.md) (pages fetched 2026-10-22). Each folder holds the rules, a README with the process, the stackup assumed, a rule-to-source table, what DRC cannot check and the values still UNVERIFIED, and a generated test board that triggers every rule.

| Set | Process | Rules | For |
|---|---|---|---|
| [`pcbway-hdi/`](pcbway-hdi/) | Advanced HDI: laser microvias, blind and buried vias, 18 µm base copper | 16 | Main board |
| [`pcbway-multilayer/`](pcbway-multilayer/) | Advanced multilayer, through vias only; 18 µm and 35 µm base copper variants | 13 each | HAT device-side piece, rigid faceplate boards |
| [`pcbway-flex/`](pcbway-flex/) | Flexible PCB (FPC) | 6 | HAT flat cable, faceplate cable |

The values are PCBWay's normal values. Tighter published limits are listed in each README as floors, for a product to apply in its own product rules, in a named area or net class. KiCad checks the solder mask in Board Setup, not in custom rules: each README gives the Board Setup values to set.

## Vendored rule sets

`vendor/kicad-druid/`: rules for PCBWay, JLCPCB and a generic set (2, 4 and 6 layers), each with a pass/fail test board, vendored unmodified from [Cimos/kicad-druid](https://github.com/Cimos/kicad-druid) at the commit in `UPSTREAM_COMMIT` (MIT). Checked with KiCad 10.0.7: the PCBWay test board loads the rules and they fire. Use them for simple 2- to 6-layer boards without impedance control.

## Use

Copy the `.kicad_dru` file next to the KiCad project and name it `<project>.kicad_dru`. Then set the Board Setup values listed in the set's README.

## Test boards

Each OpenDAP set has `test/make_test_board.py`, which builds the test board from the rules file with KiCad's Python (`pcbnew`), and the shared [`tools/check_drc.py`](tools/check_drc.py), which runs `kicad-cli pcb drc` on it and fails unless every rule fires exactly as expected and nothing else does. A rules file that KiCad cannot compile makes `kicad-cli` report a clean board, so the check also proves the file compiled.

```sh
KICAD_PY=/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3
for set in pcbway-hdi pcbway-multilayer pcbway-flex; do
  $KICAD_PY design-rules/$set/test/make_test_board.py
done
python3 design-rules/tools/check_drc.py design-rules/*/test/*.kicad_pcb
```

`check_drc.py` finds `kicad-cli` in `/Applications/KiCad/KiCad.app` (override with `KICAD_APP`) or on `PATH`. Run both after changing a rules file, and commit the regenerated boards; generation is reproducible, so an unchanged rule set gives unchanged files.

New sets go next to these as `<fab>-<process>/` with the same layout.
