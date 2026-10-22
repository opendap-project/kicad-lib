# KiCad library requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| KLIB-001 | OpenDAP shall maintain its own KiCad parts library, shared by every OpenDAP hardware project. | must | Confirmed |
| KLIB-002 | The library shall include design rules, each with a test board that triggers every rule, for every fab process OpenDAP boards use. | should | Draft |

## Context

- Repository layout, consumption as a pinned submodule and STEP-as-source follow the benchmark in [`toolkit/hardware/docs/research/2026-10-open-hardware-repo-benchmark.md`](https://github.com/opendap-project/toolkit-hardware/blob/main/docs/research/2026-10-open-hardware-repo-benchmark.md).
- The main board is likely to need HDI rules and the flat cables flex (or rigid-flex) rules for PCBWay. No public rule set covers these; they will be written from PCBWay's published capabilities.
