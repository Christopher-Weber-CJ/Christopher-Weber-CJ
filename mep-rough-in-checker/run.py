"""MEP Rough-In Checker. Usage: python3 run.py [plan.json] [--rules rules.yaml] [--out output]"""
import argparse
import json
import pathlib

import yaml

from mep.checks import run_checks
from mep.design import build
from mep.output import report, svg


def main(argv=None):
    here = pathlib.Path(__file__).parent
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plan", nargs="?", default=here / "plan.json")
    ap.add_argument("--rules", default=here / "rules.yaml")
    ap.add_argument("--out", default=here / "output")
    a = ap.parse_args(argv)
    plan = json.loads(pathlib.Path(a.plan).read_text())
    rules = yaml.safe_load(pathlib.Path(a.rules).read_text())["rules"]
    m = build(plan, rules)
    results = run_checks(m, rules)
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "plan.svg").write_text(svg(m))
    slope = next((r["params"]["design_slope"] for r in rules if "design_slope" in (r.get("params") or {})), 0.02)
    (out / "report.md").write_text(report(m, results, slope))
    print(f"clashes: {len(m.first_clashes)} first pass -> {len(m.clashes)} after rerouting")
    for r in results:
        print(f"{r['id']:3} {r['status']:12} {r['title']}")
    print(f"wrote {out / 'plan.svg'} and {out / 'report.md'}")
    return m, results


if __name__ == "__main__":
    main()
