"""Geometry helpers, the 6-inch routing grid and A* pathfinding. Units are feet."""
import heapq
import itertools
import math

STEP = 0.5  # grid pitch, ft (6 in)
EPS = 1e-6
INF = float("inf")
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def edges(poly):
    return list(zip(poly, poly[1:] + poly[:1]))


def seg_dist(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    l2 = dx * dx + dy * dy
    t = 0.0 if l2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def boundary_dist(p, poly):
    return min(seg_dist(p, a, b) for a, b in edges(poly))


def inside(p, poly):
    """Point in polygon; the boundary counts as inside."""
    if boundary_dist(p, poly) < EPS:
        return True
    res = False
    for (x1, y1), (x2, y2) in edges(poly):
        if (y1 > p[1]) != (y2 > p[1]) and p[0] < x1 + (p[1] - y1) * (x2 - x1) / (y2 - y1):
            res = not res
    return res


def area(poly):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in edges(poly))) / 2


def interior_point(poly, clearance=1.0):
    """Centroid, or the nearest grid point at least `clearance` ft inside the polygon."""
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in edges(poly):
        c = x1 * y2 - x2 * y1
        a, cx, cy = a + c, cx + (x1 + x2) * c, cy + (y1 + y2) * c
    c = (cx / (3 * a), cy / (3 * a))
    if inside(c, poly) and boundary_dist(c, poly) >= clearance:
        return c
    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
    cands = [(i * STEP, j * STEP) for i in range(int(min(xs) / STEP), int(max(xs) / STEP) + 1)
             for j in range(int(min(ys) / STEP), int(max(ys) / STEP) + 1)]
    cands = [q for q in cands if inside(q, poly) and boundary_dist(q, poly) >= clearance] or [poly[0]]
    return min(cands, key=lambda q: math.dist(q, c))


def perimeter(poly):
    return sum(math.dist(a, b) for a, b in edges(poly))


def perim_point(poly, s):
    """Point at distance s along the polygon boundary (wraps)."""
    s %= perimeter(poly)
    for a, b in edges(poly):
        L = math.dist(a, b)
        if s <= L + EPS:
            t = s / L if L else 0.0
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
        s -= L
    return poly[0]


def perim_s(poly, p):
    """(s, distance) of the boundary point nearest to p."""
    best, acc = (INF, 0.0), 0.0
    for a, b in edges(poly):
        L = math.dist(a, b)
        t = max(0.0, min(L, ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / L))
        d = math.dist(p, (a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L))
        if d < best[0] - EPS:
            best = (d, acc + t)
        acc += L
    return best[1], best[0]


def overlap(a, b, c, d):
    """Interval (ft from a) where segment c-d lies along segment a-b, or None."""
    L = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    if any(abs((q[0] - a[0]) * uy - (q[1] - a[1]) * ux) > EPS for q in (c, d)):
        return None
    t1, t2 = [(q[0] - a[0]) * ux + (q[1] - a[1]) * uy for q in (c, d)]
    lo, hi = max(0.0, min(t1, t2)), min(L, max(t1, t2))
    return (lo, hi) if hi - lo > EPS else None


def usable_runs(poly, walls, doors):
    """Continuous stretches of room perimeter that are wall and not doorway, as (s0, s1) along the
    perimeter. Runs continue round corners; one run may wrap past the perimeter length P."""
    out, acc = [], 0.0
    for a, b in edges(poly):
        holes = sorted(filter(None, (overlap(a, b, *d) for d in doors)))
        for lo, hi in sorted(filter(None, (overlap(a, b, *w) for w in walls))):
            for h0, h1 in holes:
                if h1 <= lo or h0 >= hi:
                    continue
                if h0 > lo:
                    out.append((acc + lo, acc + h0))
                lo = max(lo, h1)
            if hi - lo > EPS:
                out.append((acc + lo, acc + hi))
        acc += math.dist(a, b)
    merged = []
    for lo, hi in out:
        if merged and lo - merged[-1][1] < EPS:
            merged[-1] = (merged[-1][0], max(hi, merged[-1][1]))
        else:
            merged.append((lo, hi))
    if len(merged) > 1 and merged[0][0] < EPS and acc - merged[-1][1] < EPS:
        merged = [(merged[-1][0], acc + merged[0][1])] + merged[1:-1]
    return merged, acc


def node(p):
    return (round(p[0] / STEP), round(p[1] / STEP))


def pt(n):
    return (n[0] * STEP, n[1] * STEP)


class Grid:
    """6-inch routing grid over the unit. In-wall nodes are cheapest (exterior walls dearer, to keep
    water out of cold walls), the lane 6 in off a wall is next, open floor/ceiling is expensive so
    runs hug walls. Nodes inside a doorway are blocked."""

    def __init__(self, rooms, walls, doors, exterior=(), lane_cost=1.5, open_cost=8.0, ext_cost=3.0):
        xs = [p[0] for r in rooms for p in r]
        ys = [p[1] for r in rooms for p in r]
        self.cost, self.wall = {}, set()
        for i in range(node((min(xs), 0))[0], node((max(xs), 0))[0] + 1):
            for j in range(node((0, min(ys)))[1], node((0, max(ys)))[1] + 1):
                p = pt((i, j))
                if not any(inside(p, r) for r in rooms):
                    continue
                if any(seg_dist(p, a, b) < EPS and min(math.dist(p, a), math.dist(p, b)) > EPS for a, b in doors):
                    continue
                d = min((seg_dist(p, a, b) for a, b in walls), default=INF)
                if d < EPS:
                    self.wall.add((i, j))
                    ext = any(seg_dist(p, a, b) < EPS for a, b in exterior)
                    self.cost[(i, j)] = ext_cost if ext else 1.0
                else:
                    self.cost[(i, j)] = lane_cost if d <= STEP + EPS else open_cost


def astar(grid, start, goal, penalty=None, turn_cost=0.25):
    """Orthogonal A* from start to goal node. `penalty` adds cost per node. Returns node list or None."""
    pen, cost = penalty or {}, grid.cost
    if start not in cost or goal not in cost:
        return None
    h = lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1])  # noqa: E731 (admissible: min step cost 1)
    tie = itertools.count()
    heap = [(h(start), 0.0, next(tie), start, None)]
    best, prev = {(start, None): 0.0}, {}
    while heap:
        _, g, _, n, d = heapq.heappop(heap)
        if n == goal:
            path, s = [n], (n, d)
            while s in prev:
                s = prev[s]
                path.append(s[0])
            return path[::-1]
        if g > best.get((n, d), INF):
            continue
        for nd in DIRS:
            nb = (n[0] + nd[0], n[1] + nd[1])
            c = cost.get(nb)
            if c is None:
                continue
            ng = g + c + pen.get(nb, 0.0) + (turn_cost if d is not None and nd != d else 0.0)
            if ng < best.get((nb, nd), INF):
                best[(nb, nd)], prev[(nb, nd)] = ng, (n, d)
                heapq.heappush(heap, (ng + h(nb), ng, next(tie), nb, nd))
    return None
