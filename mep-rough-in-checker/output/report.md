# MEP Rough-In Checker report: Unit 204 - two-bedroom apartment (sample)

> Prototype output, not a design or a code approval. **No load calculations, wire sizing, breaker sizing or pipe sizing are done.** Confirm every rule against the code editions in force in Saskatchewan for the permit.

## Counts

| Item | Value |
|---|---|
| Pipe length, cold | 81.5 ft |
| Pipe length, hot | 86.0 ft |
| Pipe length, drain | 70.5 ft (longest run 41.5 ft, drop 10.0 in at 2 %) |
| Pipe length, vent | 66.5 ft |
| Cable length, electrical | 466.5 ft |
| Fixtures and equipment | 10 (sink, dishwasher, range, lav, toilet, tub, washer, dryer, water_heater, furnace) |
| Circuits | 12 |
| Receptacles | 23 (4 GFCI) |
| Lights / smoke alarms / CO alarms | 8 / 3 / 1 |
| Hard-wired appliance connections | 6 |

Lengths are plan lengths along the 6-inch grid; vertical drops, rises and fittings are not included. PEX lengths are per home run (each fixture has its own hot and/or cold line from the manifold).

## Clashes

- First pass: **176** clashes (147 shared segments, 29 crossings).
- After 16 reroute passes: **33** clashes (0 shared segments, 33 crossings) at 11 locations.
- A clash is a grid node used by electrical and any plumbing run, or by a drain and a supply line, other than a shared end point (e.g. dishwasher water and power).
- Design adjustment: rerouting lengthened the stack-vented trap arm of lav, so an individual vent was added and routing re-run.

Remaining clashes (shown as magenta X on the plan):

| Location (ft) | Runs | Systems | Type |
|---|---|---|---|
| 26.0, 15.5 | C2 / cold-k-sink | electrical/cold | crossing |
| 26.0, 15.5 | C2 / hot-k-sink | electrical/hot | crossing |
| 24.0, 0.0 | C2 / drain-k-sink | electrical/drain | crossing |
| 24.0, 0.0 | C2 / vent-k-sink | electrical/vent | crossing |
| 26.0, 15.5 | C2 / hot-dw | electrical/hot | crossing |
| 24.0, 17.5 | C5 / drain-k-sink | electrical/drain | crossing |
| 23.0, 17.0 | C5 / vent-k-sink | electrical/vent | crossing |
| 23.0, 17.0 | C5 / cold-lav | electrical/cold | crossing |
| 23.0, 17.0 | C5 / hot-lav | electrical/hot | crossing |
| 23.0, 17.0 | C5 / cold-wc | electrical/cold | crossing |
| 23.0, 17.0 | C5 / cold-tub | electrical/cold | crossing |
| 23.0, 17.0 | C5 / hot-tub | electrical/hot | crossing |
| 23.0, 17.0 | C5 / cold-washer | electrical/cold | crossing |
| 23.0, 17.0 | C5 / hot-washer | electrical/hot | crossing |
| 26.0, 15.5 | C7 / cold-k-sink | electrical/cold | crossing |
| 26.0, 15.5 | C7 / hot-k-sink | electrical/hot | crossing |
| 29.5, 16.5 | C7 / drain-k-sink | electrical/drain | crossing |
| 26.5, 0.5 | C7 / drain-k-sink | electrical/drain | crossing |
| 29.5, 16.5 | C7 / vent-k-sink | electrical/vent | crossing |
| 26.0, 15.5 | C7 / hot-dw | electrical/hot | crossing |
| 25.5, 15.5 | C11 / cold-k-sink | electrical/cold | crossing |
| 25.5, 15.5 | C11 / hot-k-sink | electrical/hot | crossing |
| 25.5, 15.5 | C11 / hot-dw | electrical/hot | crossing |
| 26.5, 0.5 | drain-k-sink / hot-dw | drain/hot | crossing |
| 17.5, 22.0 | drain-k-sink / cold-tub | drain/cold | crossing |
| 17.5, 22.0 | drain-k-sink / hot-tub | drain/hot | crossing |
| 18.5, 20.5 | cold-lav / drain-washer | cold/drain | crossing |
| 18.5, 20.5 | hot-lav / drain-washer | hot/drain | crossing |
| 17.0, 21.5 | drain-lav / cold-wc | drain/cold | crossing |
| 17.0, 21.5 | cold-wc / drain-wc | cold/drain | crossing |
| 17.0, 21.5 | cold-wc / drain-washer | cold/drain | crossing |
| 17.5, 22.5 | cold-tub / drain-tub | cold/drain | crossing |
| 17.5, 22.5 | hot-tub / drain-tub | hot/drain | crossing |

## Circuits

| Circuit | Name | Volts | AFCI | Devices | Cable (ft) |
|---|---|---|---|---|---|
| C1 | Living receptacles + light | 120 | yes | 6 | 73.5 |
| C2 | Kitchen receptacles + light | 120 | yes | 6 | 51.0 |
| C3 | Bathroom receptacle + light | 120 | yes | 2 | 23.5 |
| C4 | Bedroom 1 receptacles + light | 120 | yes | 8 | 99.5 |
| C5 | Bedroom 2 receptacles + light | 120 | yes | 6 | 51.5 |
| C6 | Lighting + smoke/CO alarms | 120 | no | 7 | 49.5 |
| C7 | Dishwasher (dedicated) | 120 | no | 1 | 26.5 |
| C8 | Range (dedicated) | 240 | no | 1 | 65.5 |
| C9 | Washer (dedicated) | 120 | no | 1 | 12.0 |
| C10 | Dryer (dedicated) | 240 | no | 1 | 8.0 |
| C11 | Water Heater (dedicated) | 240 | no | 1 | 2.5 |
| C12 | Furnace (dedicated) | 120 | no | 1 | 3.5 |

## Rule checklist

| Rule | Check | Status | Result | Source |
|---|---|---|---|---|
| E1 | Receptacle spacing along usable walls | **PASS** | 6 usable wall runs tested at 3 in steps; all within 1.8 m | Canadian Electrical Code Part I, Rule 26-712(a): receptacles placed so that no point along the floor line of any usable wall space is more than 1.8 m horizontally from a receptacle. Doorways and open sides of a room (no wall) are not usable wall space. |
| E2 | GFCI protection for receptacles near sinks and tubs | **PASS** | 4 receptacles within 1.5 m of a wet fixture, all GFCI: REC11, REC12, REC13, REC6 | Canadian Electrical Code Part I, Rule 26-700(11): receptacles within 1.5 m of a sink, bathtub or shower stall must be protected by a Class A ground fault circuit interrupter. |
| E3 | AFCI protection of 120 V receptacle circuits | **PASS** | 5 receptacle circuits, all AFCI | Canadian Electrical Code Part I, Rule 26-658: branch circuits supplying 125 V receptacles rated 20 A or less in a dwelling unit must have arc-fault (AFCI) protection. |
| E4 | Dedicated circuits (range, dryer, washer, dishwasher, bathroom) | **PASS** | dedicated: dw=C7, range=C8, washer=C9, dryer=C10, Bathroom=C3 | Canadian Electrical Code Part I, Section 26 dwelling-unit rules (Rules 26-720 to 26-746): the range, clothes dryer, laundry (washer) receptacle and dishwasher each on their own branch circuit. Bathroom receptacles on a circuit serving only the bathroom is a requirement of this project brief; confirm the exact CEC wording that applies. |
| E5 | Kitchen counter receptacles (900 mm rule, split circuits) | **NOT CHECKED** | Counter tops are not part of the plan schema, so counter spacing cannot be tested. | Canadian Electrical Code Part I, Rule 26-712(d): counter receptacles so that no point along the counter wall line is more than 900 mm from a receptacle. |
| F1 | Smoke alarms in each bedroom and in the hallway serving bedrooms | **PASS** | alarm in Bedroom 1, in Hall outside Bedroom 1 door, in Bedroom 2, in Hall outside Bedroom 2 door | National Building Code of Canada 2020 (as adopted in Saskatchewan), Article 9.10.19.3: a smoke alarm in each sleeping room, and between sleeping rooms and the rest of the storey, in the hallway where the sleeping rooms are served by a hallway. |
| F2 | Carbon monoxide alarms where there is a fuel-burning appliance | **PASS** | fuel-burning: ahu; distances straight-line<br>Bedroom 1 door d-bed1: nearest CO alarm 2.0 m<br>Bedroom 2 door d-bed2: nearest CO alarm 1.0 m | National Building Code of Canada 2020 (as adopted in Saskatchewan), Article 9.32.3.9: where a dwelling unit has a fuel-burning appliance, a CO alarm inside each bedroom or outside each bedroom within 5 m of the bedroom door. |
| P1 | Trap arm length per fixture | **PASS** | k-sink 1.5 in trap: 0.15 m (max 1.8 m)<br>lav 1.25 in trap: 0.15 m (max 1.5 m)<br>wc 3.0 in trap: 0.46 m (max 3.6 m)<br>tub 1.5 in trap: 0.30 m (max 1.8 m)<br>washer 2.0 in trap: 0.15 m (max 2.4 m) | National Plumbing Code of Canada 2020 (as adopted in Saskatchewan), Article 2.5.6.3 and its table: maximum length of a trap arm (trap weir to vent) by trap size, e.g. 1-1/2 in trap 1.8 m. |
| P2 | Vent present for every trapped fixture | **PASS** | k-sink (individual vent)<br>lav (individual vent)<br>wc (stack vent)<br>tub (individual vent)<br>washer (individual vent) | National Plumbing Code of Canada 2020 (as adopted in Saskatchewan), Section 2.5: every fixture trap must be protected by a vent (individual, wet, stack or other permitted vent). |
| P3 | Minimum slope of horizontal drains | **NOT CHECKED** | Every drain is drawn at 2 % (1/4 in per ft) and the drop is reported, but floor framing depth is not modelled, so whether that slope fits is not verified. | National Plumbing Code of Canada 2020, Article 2.4.8.1: horizontal drains 3 in and smaller at no less than 1 in 50 (2 %). |
| X1 | Electrical load calculation | **NOT CHECKED** | Out of scope for this prototype. No service or panel load calculation is done. | Canadian Electrical Code Part I, Rule 8-200 (single dwellings) and Rule 8-202 (apartments). |
| X2 | Conductor, breaker and pipe sizing | **NOT CHECKED** | Out of scope. No wire, overcurrent device, PEX, drain or vent sizing is done. | Canadian Electrical Code Part I, Section 4 and Table 2; National Plumbing Code of Canada 2020, Sections 2.4 to 2.6. |

Summary: 8 PASS, 0 FAIL, 4 NOT CHECKED.

## Limitations

- No load calculations, no conductor/breaker sizing and no PEX, drain or vent sizing (rules X1, X2: NOT CHECKED).
- Routing is 2D on a 6-inch grid. Elevations are not modelled, so crossings that would really pass over or under each other are still counted as clashes; framing, joists, beams and fire separations are not modelled. Runs prefer walls (in-wall, then a 6-inch lane) but may cross open floor/ceiling at a higher cost, which the clash penalty sometimes forces (e.g. kitchen supply lines).
- Drains are assumed at 2 % slope; whether the drop fits in the floor depth is not checked (P3).
- Vent rises in the nearest wall; vent pipe routes to the stack are drawn in plan only. Wet-vent and stack-vent loading (fixture units) is not checked; fixtures in the stack's room with a short trap arm are treated as stack vented.
- Distances for GFCI, trap arm and CO alarm rules are measured from fixture connection points, straight line for GFCI and CO (NBC measures CO distance along corridors and doorways), along the routed drain for trap arms.
- Receptacle spacing is checked per room along usable wall (walls minus doorways and open sides); credit from adjoining spaces, fixed cabinets and counters (E5) is not modelled.
- Smoke alarms are checked for presence in each bedroom and in the room outside each bedroom door; interconnection, ceiling position and clearances are not checked.
- Clause numbers in rules.yaml are cited in plain words and should be confirmed against the editions adopted in Saskatchewan on the permit date.
