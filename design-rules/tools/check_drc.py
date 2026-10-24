#!/usr/bin/env python3
"""Check a rule set's test board: every rule fires, and nothing else does.

Usage: check_drc.py <test>.kicad_pcb [...]

For each board it runs `kicad-cli pcb drc --format json --severity-all` and
compares the report with `<test>.expected.json` (written by the test-board
script) and with the rule names in `<test>.kicad_dru`:

- every rule in the rules file fires, exactly as often as expected;
- every Board Setup check listed as expected fires, exactly as often;
- no other violation and no unconnected item is reported;
- no violation touches the PASS column.

A rules file KiCad cannot compile makes kicad-cli report a clean board, so
"every rule fires" also proves the file compiled.

Exit code 0 when every board passes.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter

KICAD_APP = os.environ.get("KICAD_APP", "/Applications/KiCad/KiCad.app")


def kicad_cli() -> str:
    bundled = os.path.join(KICAD_APP, "Contents", "MacOS", "kicad-cli")
    if os.path.exists(bundled):
        return bundled
    found = shutil.which("kicad-cli")
    if not found:
        sys.exit("kicad-cli not found (set KICAD_APP or put kicad-cli on PATH)")
    return found


def rule_names(dru: str) -> list:
    names = []
    with open(dru, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r'\s*\(rule\s+"([^"]+)"', line)
            if m:
                names.append(m.group(1))
    return names


def run_drc(pcb: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "drc.json")
        subprocess.run(
            [kicad_cli(), "pcb", "drc", "--format", "json", "--severity-all",
             "--units", "mm", "--output", out, pcb],
            check=True, stdout=subprocess.DEVNULL)
        with open(out, encoding="utf-8") as fh:
            return json.load(fh)


def check(pcb: str) -> bool:
    stem = pcb[: -len(".kicad_pcb")]
    dru, expected_path = stem + ".kicad_dru", stem + ".expected.json"
    for path in (dru, expected_path):
        if not os.path.exists(path):
            print(f"FAIL {pcb}: missing {os.path.basename(path)}")
            return False
    with open(expected_path, encoding="utf-8") as fh:
        expected = json.load(fh)
    names = rule_names(dru)
    report = run_drc(pcb)

    fired, checks, problems = Counter(), Counter(), []
    pass_edge = expected["pass_column_starts_at_mm"]
    for v in report["violations"]:
        m = re.search(r"\(rule '([^']+)'", v["description"])
        if m and m.group(1) in names:
            fired[m.group(1)] += 1
        else:
            checks[v["type"]] += 1
        for item in v["items"]:
            if item["pos"]["x"] >= pass_edge:
                problems.append(f"violation in the PASS column: {v['description']} "
                                f"({item['description']})")
    if report["unconnected_items"]:
        problems.append(f"{len(report['unconnected_items'])} unconnected items")

    print(f"{os.path.basename(pcb)} (KiCad {report['kicad_version']})")
    print(f"  {'rule':58} expected  fired")
    for name in names:
        want = expected["rules"].get(name, 0)
        mark = "ok" if fired[name] == want and want > 0 else "MISMATCH"
        print(f"  {name:58} {want:8} {fired[name]:6}  {mark}")
        if want == 0:
            problems.append(f"rule '{name}' has no test object")
        elif fired[name] != want:
            problems.append(f"rule '{name}' fired {fired[name]}x, expected {want}x")
    for name in fired:
        if name not in names:
            problems.append(f"unknown rule '{name}' fired")
    for check_type in sorted(set(checks) | set(expected["board_setup_checks"])):
        want = expected["board_setup_checks"].get(check_type, 0)
        mark = "ok" if checks[check_type] == want else "MISMATCH"
        print(f"  {'Board Setup check: ' + check_type:58} {want:8} "
              f"{checks[check_type]:6}  {mark}")
        if checks[check_type] != want:
            problems.append(f"check '{check_type}' fired {checks[check_type]}x, "
                            f"expected {want}x")

    total = sum(fired.values())
    print(f"  rules fired: {sum(1 for n in names if fired[n])}/{len(names)}; "
          f"violations: {total} from rules, {sum(checks.values())} from Board Setup checks")
    for p in problems:
        print(f"  FAIL: {p}")
    print("  PASS" if not problems else "  FAILED")
    return not problems


def main(argv: list) -> int:
    if not argv:
        print(__doc__)
        return 2
    results = [check(os.path.abspath(p)) for p in argv]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
