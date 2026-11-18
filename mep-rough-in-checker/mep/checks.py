"""Code checks. Each check reads the built model and returns (status, [detail lines]).
A rule whose `check` is null or unknown is reported NOT CHECKED: the tool never claims a pass it did not test."""
import math

from .design import FT_PER_M
from .geom import EPS, inside, perim_s, usable_runs


def _devs(m, kind):
    return [d for d in m.devices if d["kind"] == kind]


def receptacle_spacing(m, p):
    lim, fails, n = p["max_distance_m"] * FT_PER_M, [], 0
    for r in m.rooms.values():
        if r["type"] not in p["room_types"]:
            continue
        poly = r["polygon"]
        runs, P = usable_runs(poly, m.walls, m.door_segs)
        rec = [perim_s(poly, (d["x"], d["y"])) for d in _devs(m, "receptacle") if d["room"] == r["id"]]
        rec = [s for s, dist in rec if dist < 0.1]  # only receptacles actually on this room's boundary
        for lo, hi in runs:
            n += 1
            on = [x for s in rec for x in (s, s + P) if lo - EPS <= x <= hi + EPS]
            samples = [lo + k * 0.25 for k in range(int((hi - lo) / 0.25) + 1)] + [hi]
            worst = max(min((abs(t - x) for x in on), default=math.inf) for t in samples)
            if worst > lim + EPS:
                far = "no receptacle" if worst == math.inf else f"a point {worst / FT_PER_M:.2f} m from the nearest receptacle"
                fails.append(f"{r['name']}: {hi - lo:.1f} ft wall run has {far}")
    return ("FAIL", fails) if fails else ("PASS", [f"{n} usable wall runs tested at 3 in steps; all within {p['max_distance_m']} m"])


def gfci(m, p):
    lim = p["max_distance_m"] * FT_PER_M
    wet = [f for f in m.fixtures.values() if f["type"] in p["fixture_types"]]
    near = [(d, f) for d in _devs(m, "receptacle") for f in wet if math.dist((d["x"], d["y"]), f["at"]) <= lim]
    fails = sorted({f"{d['id']} ({d['room']}) is {math.dist((d['x'], d['y']), f['at']) / FT_PER_M:.2f} m from {f['id']} without GFCI"
                    for d, f in near if not d["gfci"]})
    ids = sorted({d["id"] for d, _ in near})
    return ("FAIL", fails) if fails else ("PASS", [f"{len(ids)} receptacles within {p['max_distance_m']} m of a wet fixture, all GFCI: {', '.join(ids)}"])


def afci(m, p):
    dev = {d["id"]: d for d in m.devices}
    need = [c for c in m.circuits if c["volts"] == p["volts"] and any(dev[i]["kind"] == "receptacle" for i in c["devices"])]
    fails = [f"{c['id']} {c['name']} supplies receptacles without AFCI" for c in need if not c["afci"]]
    return ("FAIL", fails) if fails else ("PASS", [f"{len(need)} receptacle circuits, all AFCI"])


def dedicated_circuits(m, p):
    dev, fails, ok = {d["id"]: d for d in m.devices}, [], []
    for f in m.fixtures.values():
        if f["type"] not in p["appliance_types"]:
            continue
        c = next((c for c in m.circuits if any(dev[i].get("fixture") == f["id"] for i in c["devices"])), None)
        if c is None:
            fails.append(f"{f['id']} has no circuit")
        elif len(c["devices"]) != 1:
            fails.append(f"{f['id']} shares {c['id']} with {len(c['devices']) - 1} other device(s)")
        else:
            ok.append(f"{f['id']}={c['id']}")
    for r in m.rooms.values():
        if r["type"] not in p["room_types"]:
            continue
        for c in {dev[d["id"]]["circuit"] for d in _devs(m, "receptacle") if d["room"] == r["id"]}:
            c = next(x for x in m.circuits if x["id"] == c)
            other = [i for i in c["devices"] if dev[i]["room"] != r["id"]]
            if other:
                fails.append(f"{r['name']} circuit {c['id']} also serves {', '.join(other)}")
            else:
                ok.append(f"{r['name']}={c['id']}")
    return ("FAIL", fails) if fails else ("PASS", [f"dedicated: {', '.join(ok)}"])


def _alarm_in(m, kind, room):
    return [d for d in _devs(m, kind) if inside((d["x"], d["y"]), room["polygon"]) and d["room"] == room["id"]]


def smoke_alarms(m, p):
    fails, ok = [], []
    for r in m.rooms.values():
        if r["type"] != "bedroom":
            continue
        (ok if _alarm_in(m, "smoke", r) else fails).append(f"in {r['name']}")
        for d in m.doors:
            for o in d["rooms"]:
                if r["id"] in d["rooms"] and o != r["id"] and o in m.rooms:
                    (ok if _alarm_in(m, "smoke", m.rooms[o]) else fails).append(f"in {m.rooms[o]['name']} outside {r['name']} door")
    return ("FAIL", ["missing alarm " + f for f in fails]) if fails else ("PASS", ["alarm " + ", ".join(dict.fromkeys(ok))])


def co_alarms(m, p):
    fuel = [f["id"] for f in m.fixtures.values() if f.get("fuel", "electric") not in p["fuel_free"]]
    if not fuel:
        return "PASS", ["not required: no fuel-burning appliance in the plan (attached garage not modelled)"]
    lim, fails, ok = p["max_distance_m"] * FT_PER_M, [], []
    for r in m.rooms.values():
        if r["type"] != "bedroom":
            continue
        if _alarm_in(m, "co", r):
            ok.append(f"inside {r['name']}")
            continue
        for d in m.doors:
            if r["id"] in d["rooms"]:
                mid = ((d["a"][0] + d["b"][0]) / 2, (d["a"][1] + d["b"][1]) / 2)
                dist = min((math.dist(mid, (a["x"], a["y"])) for a in _devs(m, "co") if a["room"] != r["id"]), default=math.inf)
                (ok if dist <= lim else fails).append(f"{r['name']} door {d['id']}: nearest CO alarm {dist / FT_PER_M:.1f} m")
    head = f"fuel-burning: {', '.join(fuel)}; distances straight-line"
    return ("FAIL", [head] + fails) if fails else ("PASS", [head] + ok)


def trap_arm(m, p):
    tbl, fails, ok = {float(k): v for k, v in p["max_length_m"].items()}, [], []
    for r in m.runs:
        if r.system != "drain":
            continue
        size, L = r.meta.get("trap_in"), r.legs[0] / FT_PER_M
        lim = tbl.get(float(size)) if size else None
        if lim is None:
            fails.append(f"{r.meta['fixture']}: trap size {size} not in table")
        else:
            (ok if L <= lim + EPS else fails).append(f"{r.meta['fixture']} {size} in trap: {L:.2f} m (max {lim} m)")
    return ("FAIL", fails) if fails else ("PASS", ok)


def vent_present(m, p):
    fails, ok = [], []
    vents = {r.meta.get("fixture") for r in m.runs if r.system == "vent"}
    for f in m.fixtures.values():
        if "drain" not in m.needs(f):
            continue
        d = next((r for r in m.runs if r.system == "drain" and r.meta.get("fixture") == f["id"]), None)
        v = d and d.meta.get("vent")
        if v == "stack":
            ok.append(f"{f['id']} (stack vent)")
        elif v and f["id"] in vents:
            ok.append(f"{f['id']} (individual vent)")
        else:
            fails.append(f"{f['id']} has no vent")
    return ("FAIL", fails) if fails else ("PASS", ok)


CHECKS = {f.__name__: f for f in (receptacle_spacing, gfci, afci, dedicated_circuits, smoke_alarms,
                                   co_alarms, trap_arm, vent_present)}


def run_checks(m, rules):
    out = []
    for r in rules:
        fn = CHECKS.get(r.get("check"))
        status, details = fn(m, r.get("params") or {}) if fn else ("NOT CHECKED", [r.get("reason", "no automated check")])
        out.append(dict(id=r["id"], title=r["title"], status=status, details=details, source=" ".join(r["source"].split())))
    return out
