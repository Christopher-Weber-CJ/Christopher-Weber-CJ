"""Builds the rough-in design: devices, circuits, plumbing/electrical runs, routing and clash resolution."""
import math
from dataclasses import dataclass, field

from .geom import STEP, Grid, astar, interior_point, node, perim_point, perim_s, pt, usable_runs

FT_PER_M = 1 / 0.3048
# fixture type -> (services needed, trap size in inches, electrical supply volts)
FIXTURES = {
    "sink": (["cold", "hot", "drain"], 1.5, None),
    "lav": (["cold", "hot", "drain"], 1.25, None),
    "tub": (["cold", "hot", "drain"], 1.5, None),
    "shower": (["cold", "hot", "drain"], 2.0, None),
    "toilet": (["cold", "drain"], 3.0, None),
    "washer": (["cold", "hot", "drain", "electrical"], 2.0, 120),
    "dishwasher": (["hot", "electrical"], None, 120),  # drains through the sink tailpiece
    "range": (["electrical"], None, 240),
    "dryer": (["electrical"], None, 240),
    "water_heater": (["cold", "electrical"], None, 240),
    "furnace": (["electrical"], None, 120),
    "panel": ([], None, None), "manifold": ([], None, None), "stack": ([], None, None),
}
PLUMBING = ("cold", "hot", "drain", "vent")
# pairs of systems that may not share a grid node (crossing or common segment)
CONFLICTS = {frozenset(("electrical", s)) for s in PLUMBING} | {frozenset(("drain", "cold")), frozenset(("drain", "hot"))}
PENALTY = 60.0


def conflicts(a, b):
    return frozenset((a, b)) in CONFLICTS


def param(rules, check, key, default=None):
    for r in rules:
        if r.get("check") == check:
            return (r.get("params") or {}).get(key, default)
    return default


@dataclass
class Run:
    id: str
    system: str
    waypoints: list
    meta: dict = field(default_factory=dict)
    path: list = field(default_factory=list)
    legs: list = field(default_factory=list)

    @property
    def length(self):
        return sum(self.legs)


class Model:
    def __init__(self, plan):
        self.plan = plan
        self.rooms = {r["id"]: dict(r, polygon=[tuple(p) for p in r["polygon"]]) for r in plan["rooms"]}
        self.walls = [(tuple(w["a"]), tuple(w["b"])) for w in plan["walls"]]
        self.doors = [o for o in plan["openings"] if o["type"] == "door"]
        self.door_segs = [(tuple(o["a"]), tuple(o["b"])) for o in self.doors]
        ext = [(tuple(w["a"]), tuple(w["b"])) for w in plan["walls"] if w.get("exterior")]
        self.grid = Grid([r["polygon"] for r in self.rooms.values()], self.walls, self.door_segs, ext)
        self.fixtures = {f["id"]: dict(f, at=tuple(f["at"])) for f in plan["fixtures"]}
        self.devices, self.circuits, self.runs = [], [], []
        self.first_clashes, self.clashes, self.iterations = [], [], 0

    def one(self, ftype):
        for f in self.fixtures.values():
            if f["type"] == ftype:
                return f
        raise ValueError(f"plan has no fixture of type '{ftype}'")

    def needs(self, f):
        return f.get("needs", FIXTURES.get(f["type"], ([], None, None))[0])

    def run(self, rid):
        return next(r for r in self.runs if r.id == rid)


def build(plan, rules):
    m = Model(plan)
    place_devices(m, rules)
    make_circuits(m)
    make_runs(m, rules)
    m.first_clashes, m.clashes, m.iterations = resolve(m.runs, m.grid)
    m.adjusted = [r for r in m.runs if r.meta.get("vent") == "stack" and r.legs[0] > r.meta["max_ft"]]
    for r in m.adjusted:  # rerouting stretched a stack-vented trap arm: give it its own vent, re-resolve
        add_vent(m, r, r.waypoints[0], m.stack_node)
    if m.adjusted:
        _, m.clashes, it = resolve(m.runs, m.grid)
        m.iterations += it
    return m


def add_device(m, kind, room, p, **kw):
    q = pt(node(p))
    d = dict(id=f"{kind[:3].upper()}{sum(x['kind'] == kind for x in m.devices) + 1}", kind=kind,
             room=room, x=q[0], y=q[1], gfci=False, circuit=None, **kw)
    m.devices.append(d)
    return d


def place_devices(m, rules):
    D = param(rules, "receptacle_spacing", "max_distance_m", 1.8) * FT_PER_M - 0.3  # margin for 6-in snap
    types = param(rules, "receptacle_spacing", "room_types", [])
    for r in m.rooms.values():
        poly = r["polygon"]
        runs, P = usable_runs(poly, m.walls, m.door_segs)
        if r["type"] in types:  # evenly spaced so every wall point is within D of a receptacle
            for lo, hi in runs:
                n = max(1, math.ceil((hi - lo) / (2 * D)))
                for k in range(n):
                    add_device(m, "receptacle", r["id"], perim_point(poly, lo + (k + 0.5) * (hi - lo) / n))
        if r["type"] == "bathroom":  # one receptacle on the wall about 0.6-0.9 m from each basin
            for f in m.fixtures.values():
                if f["room"] == r["id"] and f["type"] in ("lav", "sink"):
                    s, _ = perim_s(poly, f["at"])
                    for off in (2, -2, 3, -3):
                        t = (s + off) % P
                        if any(lo <= t <= hi or lo <= t + P <= hi for lo, hi in runs):
                            add_device(m, "receptacle", r["id"], perim_point(poly, t))
                            break
        add_device(m, "light", r["id"], interior_point(poly))
    fuel = [f for f in m.fixtures.values() if f.get("fuel", "electric") not in param(rules, "co_alarms", "fuel_free", ["electric"])]
    outside = []
    for r in m.rooms.values():
        if r["type"] == "bedroom":
            c = interior_point(r["polygon"])
            add_device(m, "smoke", r["id"], (c[0] + 1, c[1]))
            outside += [x for d in m.doors if r["id"] in d["rooms"] for x in d["rooms"] if x != r["id"] and x in m.rooms]
    for rid in dict.fromkeys(outside):  # hallway / space outside the bedroom doors
        c = interior_point(m.rooms[rid]["polygon"])
        add_device(m, "smoke", rid, (c[0] + 1, c[1]))
        if fuel:
            add_device(m, "co", rid, (c[0] + 2, c[1]))
    lim = param(rules, "gfci", "max_distance_m", 1.5) * FT_PER_M
    wet = [f["at"] for f in m.fixtures.values() if f["type"] in param(rules, "gfci", "fixture_types", [])]
    for d in m.devices:
        if d["kind"] == "receptacle":
            d["gfci"] = any(math.dist((d["x"], d["y"]), w) <= lim for w in wet)
    for f in m.fixtures.values():
        if "electrical" in m.needs(f):
            add_device(m, "appliance", f["room"], f["at"], fixture=f["id"], type=f["type"],
                       volts=f.get("volts", FIXTURES.get(f["type"], (0, 0, 120))[2] or 120))


def make_circuits(m):
    def add(name, kind, volts, devs, appliance=None):
        cid = f"C{len(m.circuits) + 1}"
        m.circuits.append(dict(id=cid, name=name, kind=kind, volts=volts, appliance=appliance,
                               afci=volts == 120 and any(d["kind"] == "receptacle" for d in devs),
                               devices=[d["id"] for d in devs]))
        for d in devs:
            d["circuit"] = cid

    pool = [d for d in m.devices if d["kind"] in ("smoke", "co")]
    for r in m.rooms.values():
        devs = [d for d in m.devices if d["room"] == r["id"] and d["kind"] in ("receptacle", "light")]
        if r["type"] == "bathroom":
            add(f"{r['name']} receptacle + light", "bathroom", 120, devs)
        elif any(d["kind"] == "receptacle" for d in devs):
            add(f"{r['name']} receptacles + light", "general", 120, devs)
        else:
            pool += devs
    if pool:
        add("Lighting + smoke/CO alarms", "lighting", 120, pool)
    for d in m.devices:
        if d["kind"] == "appliance":
            add(f"{d['type'].replace('_', ' ').title()} (dedicated)", "dedicated", d["volts"], [d], d["type"])


def nn_order(start, pts):
    out, cur, rest = [], start, list(dict.fromkeys(pts))
    while rest:
        cur = min(rest, key=lambda q: abs(q[0] - cur[0]) + abs(q[1] - cur[1]))
        rest.remove(cur)
        out.append(cur)
    return out


def make_runs(m, rules):
    g, dev = m.grid, {d["id"]: d for d in m.devices}
    panel, man = node(m.one("panel")["at"]), node(m.one("manifold")["at"])
    stack_f = m.one("stack")
    stack = node(stack_f["at"])
    tbl = {float(k): v * FT_PER_M for k, v in (param(rules, "trap_arm", "max_length_m", {}) or {}).items()}
    for c in m.circuits:
        pts = [node((dev[i]["x"], dev[i]["y"])) for i in c["devices"]]
        m.runs.append(Run(c["id"], "electrical", [panel] + nn_order(panel, pts), {"circuit": c["id"]}))
    for f in m.fixtures.values():
        n, needs, fid = node(f["at"]), m.needs(f), f["id"]
        if f["type"] == "water_heater":
            m.runs.append(Run("hot-supply", "hot", [n, man], {"fixture": fid}))
        for s in ("cold", "hot"):
            if s in needs:
                m.runs.append(Run(f"{s}-{fid}", s, [man, n], {"fixture": fid}))
        if "drain" not in needs:
            continue
        trap = f.get("trap_in", FIXTURES.get(f["type"], (0, None))[1])
        run = Run(f"drain-{fid}", "drain", [n, stack], {"fixture": fid, "trap_in": trap, "max_ft": tbl.get(trap, 0), "vent": "stack"})
        m.runs.append(run)
        direct = astar(g, n, stack)
        if f["room"] != stack_f["room"] or not direct or (len(direct) - 1) * STEP > run.meta["max_ft"]:
            add_vent(m, run, n, stack)
    m.stack_node = stack


def add_vent(m, run, n, stack):
    """Individual vent rising in the wall nearest the fixture; the trap arm ends there."""
    v = min(m.grid.wall, key=lambda k: (abs(k[0] - n[0]) + abs(k[1] - n[1]), k))
    run.waypoints, run.meta["vent"] = [n, v, stack], v
    m.runs.append(Run(f"vent-{run.meta['fixture']}", "vent", [v, stack], {"fixture": run.meta["fixture"]}))


def route(run, grid, penalty=None):
    run.path, run.legs = [], []
    for a, b in zip(run.waypoints, run.waypoints[1:]):
        seg = astar(grid, a, b, penalty)
        if seg is None:
            raise RuntimeError(f"no route for {run.id} from {pt(a)} to {pt(b)}")
        run.legs.append((len(seg) - 1) * STEP)
        run.path += seg if not run.path else seg[1:]


def find_clashes(runs):
    """A clash is a grid node used by two runs of conflicting systems, unless it is an end point of both
    (e.g. dishwasher water + power). Consecutive shared nodes form a 'shared segment', a lone one a 'crossing'."""
    out = []
    for i, a in enumerate(runs):
        for b in runs[i + 1:]:
            if not conflicts(a.system, b.system):
                continue
            common = set(a.path) & set(b.path) - (set(a.waypoints) & set(b.waypoints))
            group, seen = [], set()
            for n in a.path + [None]:
                if n in common and n not in seen:
                    seen.add(n)
                    group.append(n)
                elif group:
                    out.append(dict(a=a.id, b=b.id, systems=f"{a.system}/{b.system}", at=pt(group[0]),
                                    nodes=group, kind="shared segment" if len(group) > 1 else "crossing"))
                    group = []
    return out


def resolve(runs, grid, max_iter=8):
    """Route everything, then reroute runs involved in clashes with a cost penalty on nodes used by
    conflicting systems, re-checking after every pass and keeping the best pass.
    Returns (first-pass clashes, final clashes, passes run)."""
    for r in runs:
        route(r, grid)
    first = clashes = find_clashes(runs)
    best, it = (len(first), [(r.path, r.legs) for r in runs]), 0
    order = ["electrical", "cold", "hot", "vent", "drain"]
    while clashes and it < max_iter:
        it += 1
        involved = {c["a"] for c in clashes} | {c["b"] for c in clashes}
        for r in sorted((r for r in runs if r.id in involved), key=lambda r: order.index(r.system)):
            pen = {n: PENALTY for o in runs if o is not r and conflicts(r.system, o.system)
                   for n in o.path if n not in r.waypoints}
            route(r, grid, pen)
        clashes = find_clashes(runs)
        if len(clashes) < best[0]:
            best = (len(clashes), [(r.path, r.legs) for r in runs])
    for r, (p, l) in zip(runs, best[1]):
        r.path, r.legs = p, l
    return first, find_clashes(runs), it
