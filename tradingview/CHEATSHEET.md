# Trader Mayne Framework: abbreviation cheat sheet

## Labels drawn on the chart

| Label | Meaning |
|---|---|
| `MSB` | Market structure break: price closes through the last swing in the trend direction (continuation). |
| `MSS` | Market structure shift: price closes through the last higher low / lower high (possible reversal). |
| `+D` | The break candle was a displacement candle (big body, at least 1.2 ATR by default). |
| `EQH` / `EQL` | Equal highs / equal lows: obvious liquidity that gets swept. |
| `SFP` | Swing failure pattern: wick beyond a level, close back inside. A liquidity sweep. |
| `BAC` | Break and close: closed beyond a level, then closed back inside within 3 bars. A liquidity sweep. |
| `EQ SFP` / `NEWS SFP` | A sweep of equal highs / lows, or a sweep that happened inside a news window. |
| `↑` / `↓` on a sweep | `↑` sell-side liquidity swept (bullish clue). `↓` buy-side liquidity swept (bearish clue). |
| `Bull OB` / `Bear OB` | Order block: last opposite candle before displacement that broke structure. Bull = supports longs. |
| `BRK` | Breaker: a failed order block that flipped (support becomes resistance and the reverse). |
| `FVG` | Fair value gap: three-candle gap left by displacement. |
| Number after the zone name | Quality score, 0 to 7. |
| `★` | An order block that overlaps a fair value gap (best case). |
| `OTE` | Optimal trade entry zone, 62% to 79% retracement, with a dotted sweet spot at 70.5%. |
| `old range high` / `old range low` | The previous dealing range's edge after a displacement reset. Watch for a support / resistance flip. |
| `AMD ↑ spring` / `AMD ↓ UTAD` | A compressed range was swept and reclaimed, then structure broke the other way. Wyckoff spring / upthrust. |
| `Judas ↓` / `Judas ↑` | Asian range swept then reclaimed in London or New York. `↓` is a bullish clue, `↑` a bearish clue. |
| `SMT ↑` / `SMT ↓` | SMT divergence at a key level between your chart and the comparison symbol. |
| `L` / `S` triangle | A long / short setup fired on that bar. |

## Trade plan label

Example: `LONG REV SB A+ RR 2.4 ★5` with a size line under it.

| Part | Meaning |
|---|---|
| `LONG` / `SHORT` | Direction. |
| `CONT` | Continuation: the daily already agrees with the weekly. Default stop is the chart swing. |
| `REV` | Reversal: the daily still disagrees, so it needed H4 or H1 confirmation. Default stop is beyond the higher-timeframe zone and the swept extreme. |
| `SB` | Inside a silver bullet window. |
| `A+` / `A` / `B` | Setup grade from the range stack, then adjusted down outside kill zones and up with SMT. |
| `RR 2.4` | Reward to risk to the target. Minimum is 2 by default. |
| `★5` | Zone quality score. |
| `ADD1`, `ADD2` | Add-on entries when *Add on confirmation* scaling is on. |
| `size ...` | Position size in units from risk % × account ÷ (entry − stop). |
| `E2` / `E3` | Middle and bottom entries when *Scale in zone* is on. |
| `2R` | Dashed line at 2 times your risk. |
| `partial 25%` | Nearest internal liquidity between entry and 2R, where a partial is planned. |

## Dashboard rows

| Row | Meaning |
|---|---|
| `1a Direction (W)` | Weekly structure bias. `Ranging` means too choppy to call. |
| `1b Sync (D)` | Whether the daily agrees with the weekly (`Synced (continuation)`) or not (`Against (reversal)`). |
| `2 Location in range` | `Discount` (below the range midpoint) or `Premium`. Longs want discount, shorts want premium. |
| `2 Context POI (240)` | Whether a live H4 order block or fair value gap exists in the trade direction. |
| `3 Price tagged POI` | Whether price traded into that zone recently. |
| `3 H4 / H1 confirmation` | Which timeframe has flipped in your direction (`Daily agrees`, `H4 flipped`, `H1 flipped`). |
| `4 MSB + disp + FVG` | Whether a qualifying break with displacement left a gap to enter on. |
| `Reward : risk` | RR of the best current zone and the win rate needed to break even. |
| `Session` | Current window: London KZ, New York KZ, NY afternoon, Asia, or silver bullet. |
| `No-trade filter` | The first disqualifier blocking a trade, numbered as in the episode 15 list. `None` means clear. |
| `Signals W / L` | Wins and losses of this indicator's own signals (win at 2R by default). |
| `Size at X% risk` | Position size for the best zone. Turns red above 2% risk. |
| `Range stack W/D/4H/1H` | `D` or `P` for discount or premium in each timeframe's range, plus the grade. |
| `SMT vs ...` | SMT status against the comparison symbol. |
| `Daily bias (ep 22)` | Daily bias from the checklist, the liquidity draw direction, and where yesterday closed in its range. |
| `Take the trade?` | `All boxes ticked` only when every checklist row passes. |
| `✓` / `✗` | Row passes / fails. |

## Market words

| Term | Meaning |
|---|---|
| `HH` `HL` `LH` `LL` | Higher high, higher low, lower high, lower low. |
| `SH` / `SL` | Swing high / swing low (three candles: the middle one is the extreme). |
| `BSL` / `SSL` | Buy-side liquidity (above highs, buy orders) / sell-side liquidity (below lows, sell orders). |
| `IRL` / `ERL` | Internal range liquidity (inside the range, used for entries and partials) / external range liquidity (range extremes, the targets). |
| `DOL` | Draw on liquidity: where price is being pulled next. |
| `POI` / `PD array` | Point of interest: an order block, breaker or fair value gap. |
| `EQ` | Equilibrium: the 50% midpoint of a dealing range. |
| `AMD` / `PO3` | Accumulation, manipulation, distribution (the power of three). |
| `UTAD` | Upthrust after distribution: Wyckoff's bearish sweep. `Spring` is the bullish one. |
| `SMT` | Divergence between correlated assets at a key level. |
| `KZ` | Kill zone: London 02:00-05:00, New York 07:00-10:00, afternoon 13:30-16:30 (weaker), New York time. |
| `SB` | Silver bullet window: 03:00-04:00, 10:00-11:00, 14:00-15:00 New York time. |
| `HTF` / `LTF` | Higher / lower timeframe. |
| `W` `D` `H4` `H1` `M15` `M5` | Weekly, daily, 4-hour, 1-hour, 15-minute, 5-minute. |
| `R` / `RR` | One R is your risk on the trade. Reward to risk. |
| `SL` / `TP` | Stop loss / take profit (in trade context). |
| `ATR` | Average true range, used to size "big" candles and gaps. |
| `ER` | Efficiency ratio: net move divided by distance travelled. Low means ranging. |
| `PDH` `PDL` `PWH` `PWL` | Previous day / week high / low. |

## Signal log

| Column / part | Meaning |
|---|---|
| Header `W x / L y net zR` | Wins, losses and net R of this indicator's own logged signals. |
| `When` | Bar time of the signal, in your session timezone setting. |
| `Setup` | Direction plus `CONT` / `REV`, silver bullet tag and grade, e.g. `LONG REV SB A+`. |
| `Entry` / `Stop` / `Target` | The plan at the time of the signal. `Target` is the external liquidity target. |
| `Result` | `+2.0R` win (at 2R, or the full target if that setting is chosen), `-1R` loss, `open` if neither has been reached. Stop is assumed first if both are hit in one bar. |

## Alerts

Long setup, short setup, bullish / bearish MSS, sell-side / buy-side sweep, news window starting, London / New York kill zone starting, bullish / bearish SMT, range AMD, Judas swing.
