# MEP Rough-In Checker (prototype)

Routes plumbing and electrical rough-in for one residential unit, detects and reroutes clashes, and checks a
small set of Saskatchewan code rules. Python 3, no paid services, runs locally.

## Run

```bash
pip install -r requirements.txt     # pyyaml, pytest
python3 run.py                      # reads plan.json + rules.yaml, writes output/plan.svg and output/report.md
python3 -m pytest -q                # tests
```

Use another plan or output folder with `python3 run.py path/to/plan.json --rules rules.yaml --out outdir`.

## What it does

1. **Reads `plan.json`**: room polygons, wall segments, door/window openings and fixtures (feet, y to the south).
   Any plan with the same schema works. It must include one `panel`, one `manifold` and one `stack` fixture.
2. **Places devices**: receptacles evenly along usable walls (walls minus doorways and open sides) so no point is
   more than 1.8 m from one, a receptacle near each basin, GFCI where within 1.5 m of a sink/lav/tub/shower,
   a light per room, smoke alarms in bedrooms and outside bedroom doors, and CO alarms there if any fixture has a
   `fuel` other than `electric`.
3. **Makes circuits by room**: a general circuit for each room with receptacles, a bathroom-only circuit, one lighting and alarm
   circuit, and dedicated circuits for each appliance (range, dryer, washer, dishwasher, water heater, furnace).
4. **Routes on a 6-inch grid with A\***. In-wall nodes cost least, then a lane 6 in off the wall, and open floor costs most.
   Exterior walls cost more and doorways are blocked. PEX hot/cold home runs go from the manifold, drains go to the stack
   at a noted 2 % slope, vents rise in the nearest wall (or the stack vent for short bathroom trap arms), and
   circuits run from the panel.
5. **Clashes**: a clash is a grid node shared by electrical and any plumbing run, or by a drain and a supply line
   (end points used by both, such as dishwasher water and power, are exempt). Clashing runs are rerouted with a cost
   penalty and re-checked for up to 8 passes. The best pass is kept and any clashes left are reported.
6. **Checks `rules.yaml`**: each rule names its source in plain words and gets PASS, FAIL or NOT CHECKED.
   Rules with no automated test are always NOT CHECKED.

## Files

| Path | Purpose |
|---|---|
| `plan.json` | Sample ~900 sf two-bedroom unit |
| `rules.yaml` | Rules, limits and plain-word citations (CEC, NBC 2020, NPC 2020 as adopted in Saskatchewan) |
| `mep/geom.py` | Geometry, grid, A* |
| `mep/design.py` | Device placement, circuits, runs, routing, clash resolution |
| `mep/checks.py` | Rule checks |
| `mep/output.py` | SVG plan and Markdown report |
| `run.py` | Command-line entry point |
| `tests/` | pytest: routing, clashes, and a passing and a failing case for each checked rule |

## Not done

No load calculations and no wire, breaker or pipe sizing. Routing is 2D, without elevations or framing. Clause numbers
and limits must be confirmed against the code editions in force. See the *Limitations* section of
`output/report.md`.
