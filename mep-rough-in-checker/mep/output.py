"""Writes output/plan.svg and output/report.md."""
import collections
from xml.sax.saxutils import escape

from .design import PLUMBING
from .geom import area, interior_point, pt

COLOUR = {"cold": "#1f6fd6", "hot": "#d62728", "drain": "#8b5a2b", "vent": "#2ca02c", "electrical": "#e8b800"}
OFFSET = {"cold": -0.15, "hot": 0.15, "drain": 0.0, "vent": 0.3, "electrical": -0.3}  # ft, so runs stay visible
S, M = 22, 30  # px per ft, margin px


def _xy(p, o=0.0):
    return f"{M + (p[0] + o) * S:.1f},{M + (p[1] + o) * S:.1f}"


def _corners(path):
    pts = [pt(n) for n in path]
    keep = [pts[0]] + [b for a, b, c in zip(pts, pts[1:], pts[2:])
                       if (b[0] - a[0]) * (c[1] - b[1]) != (b[1] - a[1]) * (c[0] - b[0])] + pts[-1:]
    return keep


def svg(m):
    xs = [p[0] for r in m.rooms.values() for p in r["polygon"]]
    ys = [p[1] for r in m.rooms.values() for p in r["polygon"]]
    w, h = M * 2 + max(xs) * S + 230, max(M * 2 + max(ys) * S, 420)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" font-family="sans-serif" font-size="10">',
         f'<rect width="100%" height="100%" fill="white"/><text x="{M}" y="18" font-size="13" font-weight="bold">'
         f'{escape(m.plan.get("name", "Plan"))} - MEP rough-in</text>']
    for r in m.rooms.values():
        c = interior_point(r["polygon"])
        o.append(f'<polygon points="{" ".join(_xy(p) for p in r["polygon"])}" fill="#f4f4f4" stroke="#bbb"/>'
                 f'<text x="{M + c[0] * S:.0f}" y="{M + (c[1] - 1.2) * S:.0f}" text-anchor="middle" fill="#555">'
                 f'{escape(r["name"])} ({area(r["polygon"]):.0f} sf)</text>')
    for a, b in m.walls:
        o.append(f'<polyline points="{_xy(a)} {_xy(b)}" stroke="#222" stroke-width="5"/>')
    for op in m.plan["openings"]:
        door = op["type"] == "door"
        o.append(f'<polyline points="{_xy(op["a"])} {_xy(op["b"])}" stroke="{"white" if door else "#9fd3f5"}" stroke-width="{7 if door else 4}"/>')
    for sysname in ("drain", "vent", "cold", "hot", "electrical"):
        for r in m.runs:
            if r.system == sysname and r.path:
                dash = ' stroke-dasharray="5 3"' if sysname in ("vent", "electrical") else ""
                o.append(f'<polyline points="{" ".join(_xy(p, OFFSET[sysname]) for p in _corners(r.path))}" fill="none" '
                         f'stroke="{COLOUR[sysname]}" stroke-width="{2.5 if sysname == "drain" else 1.6}"{dash}><title>{r.id}</title></polyline>')
    for f in m.fixtures.values():
        x, y = M + f["at"][0] * S, M + f["at"][1] * S
        fill = {"panel": "#333", "manifold": "#7b4fd6", "stack": "#8b5a2b"}.get(f["type"], "white")
        o.append(f'<rect x="{x - 6:.0f}" y="{y - 6:.0f}" width="12" height="12" fill="{fill}" stroke="#333"><title>{f["id"]}</title></rect>'
                 f'<text x="{x + 8:.0f}" y="{y + 12:.0f}" font-size="8">{escape(f["type"])}</text>')
    for d in m.devices:
        x, y = M + d["x"] * S, M + d["y"] * S
        if d["kind"] == "receptacle":
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="white" stroke="#000"/>'
                     f'<line x1="{x - 2:.0f}" y1="{y - 3:.0f}" x2="{x - 2:.0f}" y2="{y + 3:.0f}" stroke="#000"/>'
                     f'<line x1="{x + 2:.0f}" y1="{y - 3:.0f}" x2="{x + 2:.0f}" y2="{y + 3:.0f}" stroke="#000"/>'
                     + (f'<text x="{x + 6:.0f}" y="{y - 4:.0f}" font-size="8" font-weight="bold">G</text>' if d["gfci"] else ""))
        elif d["kind"] == "light":
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" fill="white" stroke="#000"/><path d="M{x - 4:.0f},{y - 4:.0f}L{x + 4:.0f},{y + 4:.0f}M{x + 4:.0f},{y - 4:.0f}L{x - 4:.0f},{y + 4:.0f}" stroke="#000"/>')
        elif d["kind"] in ("smoke", "co"):
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" fill="{"#ffdddd" if d["kind"] == "smoke" else "#ddeeff"}" stroke="#c00"/>'
                     f'<text x="{x:.0f}" y="{y + 3:.0f}" text-anchor="middle" font-size="7" font-weight="bold">{"S" if d["kind"] == "smoke" else "CO"}</text>')
    for c in m.clashes:
        x, y = M + c["at"][0] * S, M + c["at"][1] * S
        o.append(f'<path d="M{x - 5:.0f},{y - 5:.0f}L{x + 5:.0f},{y + 5:.0f}M{x + 5:.0f},{y - 5:.0f}L{x - 5:.0f},{y + 5:.0f}" stroke="#e0f" stroke-width="2"><title>{c["a"]} x {c["b"]}</title></path>')
    lx, ly = M * 2 + max(xs) * S, M + 10
    o.append(f'<text x="{lx}" y="{ly}" font-weight="bold" font-size="12">Legend</text>')
    items = [(k, f'<line x1="0" y1="0" x2="24" y2="0" stroke="{v}" stroke-width="3"/>') for k, v in COLOUR.items()] + [
        ("receptacle (G = GFCI)", '<circle cx="12" r="5" fill="white" stroke="#000"/>'),
        ("ceiling light", '<circle cx="12" r="6" fill="white" stroke="#000"/>'),
        ("smoke alarm", '<circle cx="12" r="7" fill="#ffdddd" stroke="#c00"/>'),
        ("CO alarm", '<circle cx="12" r="7" fill="#ddeeff" stroke="#c00"/>'),
        ("fixture / equipment", '<rect x="6" y="-6" width="12" height="12" fill="white" stroke="#333"/>'),
        ("panel / manifold / stack", '<rect x="6" y="-6" width="12" height="12" fill="#333"/>'),
        ("remaining clash", '<path d="M7,-5L17,5M17,-5L7,5" stroke="#e0f" stroke-width="2"/>'),
        ("door / window", '<line x1="0" y1="0" x2="24" y2="0" stroke="#9fd3f5" stroke-width="4"/>')]
    for i, (label, sym) in enumerate(items):
        y = ly + 22 + i * 20
        o.append(f'<g transform="translate({lx},{y})">{sym}</g><text x="{lx + 32}" y="{y + 4}">{escape(label)}</text>')
    o.append(f'<text x="{lx}" y="{ly + 22 + len(items) * 20 + 10}" font-size="9" fill="#555">Grid 6 in. Scale {S} px = 1 ft.</text></svg>')
    return "\n".join(o)


def report(m, results, slope):
    dev = collections.Counter(d["kind"] for d in m.devices)
    feet = collections.Counter()
    for r in m.runs:
        feet[r.system] += r.length
    plumb = [f for f in m.fixtures.values() if f["type"] not in ("panel", "manifold", "stack")]
    L = [f"# MEP Rough-In Checker report: {m.plan.get('name', '')}", "",
         "> Prototype output, not a design or a code approval. **No load calculations, wire sizing, breaker sizing or pipe "
         "sizing are done.** Confirm every rule against the code editions in force in Saskatchewan for the permit.", "",
         "## Counts", "", "| Item | Value |", "|---|---|"]
    for s in PLUMBING + ("electrical",):
        longest = max((r.length for r in m.runs if r.system == s), default=0)
        extra = f" (longest run {longest:.1f} ft, drop {longest * slope * 12:.1f} in at {slope * 100:.0f} %)" if s == "drain" else ""
        L.append(f"| {'Cable' if s == 'electrical' else 'Pipe'} length, {s} | {feet[s]:.1f} ft{extra} |")
    L += [f"| Fixtures and equipment | {len(plumb)} ({', '.join(f['type'] for f in plumb)}) |",
          f"| Circuits | {len(m.circuits)} |",
          f"| Receptacles | {dev['receptacle']} ({sum(d['gfci'] for d in m.devices)} GFCI) |",
          f"| Lights / smoke alarms / CO alarms | {dev['light']} / {dev['smoke']} / {dev['co']} |",
          f"| Hard-wired appliance connections | {dev['appliance']} |", "",
          "Lengths are plan lengths along the 6-inch grid; vertical drops, rises and fittings are not included. "
          "PEX lengths are per home run (each fixture has its own hot and/or cold line from the manifold).", "",
          "## Clashes", "",
          f"- First pass: **{len(m.first_clashes)}** clashes "
          f"({sum(c['kind'] == 'shared segment' for c in m.first_clashes)} shared segments, "
          f"{sum(c['kind'] == 'crossing' for c in m.first_clashes)} crossings).",
          f"- After {m.iterations} reroute passes: **{len(m.clashes)}** clashes "
          f"({sum(c['kind'] == 'shared segment' for c in m.clashes)} shared segments, "
          f"{sum(c['kind'] == 'crossing' for c in m.clashes)} crossings) at {len({c['at'] for c in m.clashes})} locations.",
          "- A clash is a grid node used by electrical and any plumbing run, or by a drain and a supply line, other than "
          "a shared end point (e.g. dishwasher water and power)."]
    if m.adjusted:
        L.append(f"- Design adjustment: rerouting lengthened the stack-vented trap arm of "
                 f"{', '.join(r.meta['fixture'] for r in m.adjusted)}, so an individual vent was added and routing re-run.")
    if m.clashes:
        L += ["", "Remaining clashes (shown as magenta X on the plan):", "", "| Location (ft) | Runs | Systems | Type |", "|---|---|---|---|"]
        L += [f"| {c['at'][0]:.1f}, {c['at'][1]:.1f} | {c['a']} / {c['b']} | {c['systems']} | {c['kind']} |" for c in m.clashes]
    L += ["", "## Circuits", "", "| Circuit | Name | Volts | AFCI | Devices | Cable (ft) |", "|---|---|---|---|---|---|"]
    L += [f"| {c['id']} | {c['name']} | {c['volts']} | {'yes' if c['afci'] else 'no'} | {len(c['devices'])} | {m.run(c['id']).length:.1f} |" for c in m.circuits]
    L += ["", "## Rule checklist", "", "| Rule | Check | Status | Result | Source |", "|---|---|---|---|---|"]
    for r in results:
        L.append(f"| {r['id']} | {r['title']} | **{r['status']}** | {'<br>'.join(escape(d) for d in r['details'])} | {r['source']} |")
    n = collections.Counter(r["status"] for r in results)
    L += ["", f"Summary: {n['PASS']} PASS, {n['FAIL']} FAIL, {n['NOT CHECKED']} NOT CHECKED.", "", "## Limitations", ""]
    L += [f"- {x}" for x in (
        "No load calculations, no conductor/breaker sizing and no PEX, drain or vent sizing (rules X1, X2: NOT CHECKED).",
        "Routing is 2D on a 6-inch grid. Elevations are not modelled, so crossings that would really pass over or under "
        "each other are still counted as clashes; framing, joists, beams and fire separations are not modelled. Runs prefer "
        "walls (in-wall, then a 6-inch lane) but may cross open floor/ceiling at a higher cost, which the clash "
        "penalty sometimes forces (e.g. kitchen supply lines).",
        "Drains are assumed at 2 % slope; whether the drop fits in the floor depth is not checked (P3).",
        "Vent rises in the nearest wall; vent pipe routes to the stack are drawn in plan only. Wet-vent and stack-vent "
        "loading (fixture units) is not checked; fixtures in the stack's room with a short trap arm are treated as stack vented.",
        "Distances for GFCI, trap arm and CO alarm rules are measured from fixture connection points, straight line for "
        "GFCI and CO (NBC measures CO distance along corridors and doorways), along the routed drain for trap arms.",
        "Receptacle spacing is checked per room along usable wall (walls minus doorways and open sides); credit from "
        "adjoining spaces, fixed cabinets and counters (E5) is not modelled.",
        "Smoke alarms are checked for presence in each bedroom and in the room outside each bedroom door; "
        "interconnection, ceiling position and clearances are not checked.",
        "Clause numbers in rules.yaml are cited in plain words and should be confirmed against the editions adopted "
        "in Saskatchewan on the permit date.")]
    return "\n".join(L) + "\n"
