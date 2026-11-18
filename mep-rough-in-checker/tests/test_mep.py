import copy
import json
import pathlib
import sys

import pytest
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mep import checks  # noqa: E402
from mep.design import Run, build, find_clashes, resolve  # noqa: E402
from mep.geom import Grid, astar, node, pt, usable_runs  # noqa: E402

RULES = yaml.safe_load((ROOT / "rules.yaml").read_text())["rules"]
PARAMS = {r["check"]: r.get("params") or {} for r in RULES if r.get("check")}
SQUARE = [(0, 0), (4, 0), (4, 4), (0, 4)]
SQUARE_WALLS = [((0, 0), (4, 0)), ((4, 0), (4, 4)), ((4, 4), (0, 4)), ((0, 4), (0, 0))]


@pytest.fixture(scope="module")
def model():
    return build(json.loads((ROOT / "plan.json").read_text()), RULES)


def status(m, check):
    return checks.CHECKS[check](m, PARAMS[check])[0]


# ---- routing -------------------------------------------------------------------------------------
def test_astar_hugs_walls():
    g = Grid([SQUARE], SQUARE_WALLS, [])
    path = astar(g, node((0, 2)), node((4, 2)))
    assert path[0] == node((0, 2)) and path[-1] == node((4, 2))
    assert all(g.cost[n] == 1.0 for n in path)  # went round the walls, not across the open floor
    assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for a, b in zip(path, path[1:]))


def test_astar_does_not_pass_through_doorway():
    g = Grid([SQUARE], SQUARE_WALLS, [((1.2, 0), (2.8, 0))])
    path = astar(g, node((0, 0)), node((4, 0)))
    assert not {node((1.5, 0)), node((2, 0)), node((2.5, 0))} & set(path)


def test_astar_penalty_forces_detour():
    g = Grid([SQUARE], SQUARE_WALLS, [])
    base = astar(g, node((0, 0)), node((4, 0)))
    detour = astar(g, node((0, 0)), node((4, 0)), {n: 100 for n in base[1:-1]})
    assert not set(base[1:-1]) & set(detour)


def test_every_fixture_service_is_routed(model):
    ids = {r.id for r in model.runs}
    for f in model.fixtures.values():
        for s in ("cold", "hot", "drain"):
            if s in model.needs(f):
                assert f"{s}-{f['id']}" in ids
    assert all(r.path and r.path[0] == r.waypoints[0] and r.path[-1] == r.waypoints[-1] for r in model.runs)


# ---- clashes -------------------------------------------------------------------------------------
def test_clash_kinds_and_exemptions():
    e = Run("e", "electrical", [(0, 0), (3, 0)], path=[(0, 0), (1, 0), (2, 0), (3, 0)])
    cross = Run("c", "cold", [(1, -1), (1, 1)], path=[(1, -1), (1, 0), (1, 1)])
    share = Run("h", "hot", [(0, 1), (2, 1)], path=[(0, 1), (1, 0), (2, 0), (2, 1)])
    same = Run("e2", "electrical", [(0, 0), (3, 0)], path=[(0, 0), (1, 0), (2, 0), (3, 0)])
    end = Run("dw", "hot", [(5, 5), (3, 0)], path=[(3, 1), (3, 0)])  # shares only an end point with e
    kinds = sorted((c["b"], c["kind"]) for c in find_clashes([e, cross, share, same, end]) if c["a"] == "e")
    assert kinds == [("c", "crossing"), ("h", "shared segment")]
    assert not find_clashes([cross, share])  # hot and cold may run together


def test_reroute_removes_clashes():
    walls = SQUARE_WALLS + [((0, 2), (4, 2))]
    g = Grid([SQUARE], walls, [])
    runs = [Run("e", "electrical", [node((0, 2)), node((4, 2))]), Run("w", "cold", [node((0, 1.5)), node((4, 1.5))])]
    first, final, _ = resolve(runs, g)
    assert first and not final


def test_sample_reroute_reduces_clashes(model):
    assert len(model.first_clashes) > 0
    assert len(model.clashes) < len(model.first_clashes)
    assert not [c for c in model.clashes if c["kind"] == "shared segment"]


# ---- rules: one pass and one fail each -----------------------------------------------------------
def test_usable_runs_skip_doors_and_open_sides():
    runs, P = usable_runs(SQUARE, SQUARE_WALLS[:3], [((1, 0), (2, 0))])  # west side open, door on north
    assert P == 16 and sorted(round(hi - lo, 6) for lo, hi in runs) == [1, 10]


def test_receptacle_spacing(model):
    assert status(model, "receptacle_spacing") == "PASS"
    m = copy.deepcopy(model)
    m.devices = [d for d in m.devices if not (d["kind"] == "receptacle" and d["room"] == "living")]
    m.devices.append(dict(id="X", kind="receptacle", room="living", x=0.0, y=6.5, gfci=False, circuit="C1"))
    st, det = checks.receptacle_spacing(m, PARAMS["receptacle_spacing"])
    assert st == "FAIL" and any("Living" in d for d in det)


def test_gfci(model):
    assert status(model, "gfci") == "PASS"
    m = copy.deepcopy(model)
    next(d for d in m.devices if d["gfci"])["gfci"] = False
    assert status(m, "gfci") == "FAIL"


def test_afci(model):
    assert status(model, "afci") == "PASS"
    m = copy.deepcopy(model)
    m.circuits[0]["afci"] = False
    assert status(m, "afci") == "FAIL"


def test_dedicated_circuits(model):
    assert status(model, "dedicated_circuits") == "PASS"
    m = copy.deepcopy(model)
    rng = next(c for c in m.circuits if c["appliance"] == "range")
    rng["devices"].append(next(d["id"] for d in m.devices if d["kind"] == "light"))
    assert status(m, "dedicated_circuits") == "FAIL"
    m = copy.deepcopy(model)
    bath = next(c for c in m.circuits if c["kind"] == "bathroom")
    bath["devices"].append(next(d["id"] for d in m.devices if d["room"] == "bed1"))
    assert status(m, "dedicated_circuits") == "FAIL"


def test_smoke_alarms(model):
    assert status(model, "smoke_alarms") == "PASS"
    m = copy.deepcopy(model)
    m.devices = [d for d in m.devices if not (d["kind"] == "smoke" and d["room"] == "bed2")]
    assert status(m, "smoke_alarms") == "FAIL"


def test_co_alarms(model):
    assert status(model, "co_alarms") == "PASS"
    m = copy.deepcopy(model)
    m.devices = [d for d in m.devices if d["kind"] != "co"]
    assert status(m, "co_alarms") == "FAIL"
    for f in m.fixtures.values():
        f["fuel"] = "electric"
    st, det = checks.co_alarms(m, PARAMS["co_alarms"])
    assert st == "PASS" and "not required" in det[0]


def test_trap_arm(model):
    assert status(model, "trap_arm") == "PASS"
    m = copy.deepcopy(model)
    m.run("drain-k-sink").legs[0] = 10.0  # 3.05 m on a 1-1/2 in trap (max 1.8 m)
    assert status(m, "trap_arm") == "FAIL"


def test_vent_present(model):
    assert status(model, "vent_present") == "PASS"
    m = copy.deepcopy(model)
    m.run("drain-tub").meta["vent"] = None
    assert status(m, "vent_present") == "FAIL"


def test_untested_rules_are_not_checked(model):
    res = {r["id"]: r for r in checks.run_checks(model, RULES)}
    for rid in ("E5", "P3", "X1", "X2"):
        assert res[rid]["status"] == "NOT CHECKED"
    assert all(r["source"] for r in res.values())


# ---- end to end ----------------------------------------------------------------------------------
def test_outputs_written(tmp_path):
    import run
    run.main([str(ROOT / "plan.json"), "--out", str(tmp_path)])
    svg, md = (tmp_path / "plan.svg").read_text(), (tmp_path / "report.md").read_text()
    assert svg.startswith("<svg") and "#1f6fd6" in svg and "Legend" in svg
    for text in ("## Counts", "## Clashes", "## Rule checklist", "## Limitations", "No load calculations", "NOT CHECKED"):
        assert text in md
    assert pt(node((1.2, 3.3))) == (1.0, 3.5)
