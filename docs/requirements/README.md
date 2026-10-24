# KiCad library requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| KLIB-001 | OpenDAP shall maintain its own KiCad parts library, shared by every OpenDAP hardware project. | must | Confirmed |
| KLIB-002 | The library shall include design rules, each with a test board that triggers every rule, for every fab process OpenDAP boards use. | should | Confirmed |
| KLIB-003 | Every OpenDAP board shall follow the OpenDAP PCB craft standard ([`docs/specs/pcb-craft-standard.md`](../specs/pcb-craft-standard.md)), checked by its DRC rule set, `odapkit craft check` and review, each rule at its quality level. | must | Confirmed |

## Context

- KLIB-002 confirmed by the maintainers on 2026-10-24: OpenDAP keeps its own design rules, complementing PCBWay's, that fit the project's quality requirements. Rule sets: `pcbway-hdi`, `pcbway-flex`, `pcbway-multilayer` in [`design-rules/`](../../design-rules/). Product rules live with each board and are composed on top of a fab set.
- KLIB-003 confirmed by the maintainers on 2026-10-24: OpenDAP's boards should be elegant and visibly made with care for engineering, quality and appearance, beyond function, shared by every board (T1 main board, faceplates, HATs). The standard's rules and values were written by Claude under their delegation; the production mask colour and finish (CRAFT-70) stay a proposal for them. Each rule carries its RFC 0010 quality level, so a prototype is held to the Q1 rules and the rest is recorded as debt.
- Repository layout, consumption as a pinned submodule and STEP-as-source follow the benchmark in [`toolkit/hardware/docs/research/2026-10-open-hardware-repo-benchmark.md`](https://github.com/opendap-project/toolkit-hardware/blob/main/docs/research/2026-10-open-hardware-repo-benchmark.md).
- The main board is likely to need HDI rules and the flat cables flex (or rigid-flex) rules for PCBWay. No public rule set covers these; they will be written from PCBWay's published capabilities.
