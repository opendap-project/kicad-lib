# Design rules

KiCad custom design rules (`.kicad_dru`) for the fabs OpenDAP uses.

- `vendor/kicad-druid/`: rules for PCBWay, JLCPCB and a generic set (2, 4 and 6 layers), each with a pass/fail test board, vendored unmodified from [Cimos/kicad-druid](https://github.com/Cimos/kicad-druid) at the commit in `UPSTREAM_COMMIT` (MIT). Checked with KiCad 10.0.7: the PCBWay test board loads the rules and they fire.
- OpenDAP's own rule sets (for example HDI with microvias, or flex for the flat cables) go next to `vendor/` as `<fab>-<process>/`, each with the capability source it follows and a test board that triggers every rule. None yet.

To use a rule set in a KiCad project, copy the `.kicad_dru` file next to the project and name it `<project>.kicad_dru`.
