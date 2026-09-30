# Mayne Day Planner: cheat sheet

The planner does not give entries. It tells you what kind of day it is, where the liquidity is, how long you have, and how much you can risk. Take entries from the main framework.

## The plan card (top to bottom)

| Row | What it shows | How to read it |
|---|---|---|
| Title | `Mayne Day Planner <symbol>` | Intraday charts only. |
| **Clock** | `Flat in 3h 10m`, or `Flat period, trading resumes in 0h 40m` | Time to the forced flat (14:45 default). Turns red with `no new entries` inside the last 45 minutes, and during the flat period. After the 16:00 reopen it counts to the next day's 14:45. |
| **Window** | `Silver bullet / London kill zone`, `New York kill zone`, `Asia (accumulation)`, `Outside the kill zones` | Orange means a kill zone or silver bullet is live. Grey means it is not a prime window. |
| **Daily bias** | `Bullish`, `Bearish`, `Unclear`, `No-bias day (mid close)` | Episode 22 checklist. `No-bias day`: yesterday closed in the middle of its range, so he skips bias. `Unclear`: the checklist didn't fully line up. |
| **Bias detail** | `draw up \| close 68% \| weekly premium` | `draw` is the liquidity being pulled toward (a swept high points down, a swept low points up, otherwise the nearer level). `close` is where yesterday closed in its range (0% = low, 100% = high). Last part is price against the previous week's midpoint. |
| **Daily AMD** | Current stage of today's cycle | See the AMD table below. |
| **Daily open** | `Above open, dipped below earlier (bullish AMD)` | A bullish day dips under the daily open early, then reclaims it. The bearish mirror is `Below open, poked above earlier (bearish AMD)`. |
| **Liquidity above** | `PDH 30725.25  +32.8 pts (8% ADR)` | Nearest unswept level above price, its distance, and that distance as a share of the 5-day average daily range. |
| **Liquidity below** | `PDL 30371.75  -320.8 pts (75% ADR)` | Same, below price. |
| **Risk budget** | `daily room $500 \| risk this trade $250` | What you can risk on one trade after the daily-loss and drawdown limits. Reads `DAILY LIMIT REACHED: stop trading` in red when the limit is gone. |
| **Calculator** | `20 pts stop: 5 contracts ($200 risk)` | Fill in an entry and stop price in the settings. Rounds down. `stop too wide for 1` means one contract already risks more than your budget. |
| **Main signal** | `LONG entry stop target \| N contracts` | Last framework signal today, sized to your budget. `not linked` means the link is off. `no signal this trading day` means none has fired since the day rolled. |

## Daily AMD stages

| Card text | Meaning | What to do |
|---|---|---|
| `Waiting for the Asia session` | Asia range not started. | Nothing yet. |
| `Accumulation: Asia range forming (X pts)` | Inside the Asia window. | Wait. Do not trade the range. |
| `Range set, waiting for a sweep: hi / lo` | Asia is done, price still inside. | Watch both edges. |
| `Asia high swept, waiting for a reclaim` | Manipulation: a high was taken (bearish clue). | Watch for a close back under the Asia high within 6 bars. |
| `Asia low swept, waiting for a reclaim` | Manipulation: a low was taken (bullish clue). | Watch for a close back above the Asia low. |
| `Range break, not a sweep: expect continuation` | Price stayed outside the range for more than 6 bars. | It is a real break, not a Judas swing. Do not fade it. |
| `Reclaimed, waiting for displacement down/up` | Back inside the range. | The move needs a big body (1.2 ATR) within 12 bars in the opposite direction. |
| `Reclaimed, no displacement (weak)` | The window closed with no big candle. | Lower quality. Treat with suspicion. |
| `Distribution UP/DOWN under way` | The real move of the day has started. `(agrees with bias)` means it matches the daily bias. | Look for a main-indicator entry in that direction. |

## Chart items

| Item | Meaning |
|---|---|
| Purple box `Asia` | Asian range (18:00-22:00 Mountain), extends until the day resets. |
| Blue box `London` | London kill zone range (00:00-03:00). |
| Blue / amber background | London / New York kill zone. |
| Grey background | Forced-flat period (14:45-16:00). |
| Label `Asia high swept` / `Asia low swept` | The sweep bar. |
| Label `Reclaimed` | The close back inside. |
| Label `Distribution up` / `Distribution down` | The displacement bar. Large label. |
| Lines PDH / PDL | Previous day high (red) / low (green). Dim grey once swept. |
| Thick lines PWH / PWL | Previous week high / low. Dim grey once swept. |
| Amber line | Daily open. |

## Settings you must fill in

| Setting | Why |
|---|---|
| **Point value** | MES 5, MNQ 2, ES 50, NQ 20. Wrong value means wrong contract counts. Also set it in the framework's Day trading group. |
| Account size, risk % | Sets the base risk per trade. |
| Daily loss limit | Enables the daily room and the stop-trading warning. Assumed to run from the start-of-day balance. Check your firm's rule. |
| Today's realized P&L | **Manual.** Update it as you trade or the daily room is stale. |
| Room left to max drawdown | **Manual.** |
| Fraction of remaining room | Default 0.5: never risk more than half of what is left on one trade. |
| Link to main | Turn on *Read signals from the main framework indicator*, then set the four sources to the framework's `Export:` plots (signal, entry, stop, target). |
| Card position / size | Move it if it covers price. |

## Alerts

15 minutes to flat, London kill zone starting, New York kill zone starting, silver bullet starting, Asia range swept, sweep reclaimed, distribution started.

## Mountain-time defaults

| Window | Mountain |
|---|---|
| Asia | 18:00-22:00 |
| London kill zone | 00:00-03:00 |
| New York kill zone | 05:00-08:00 |
| Silver bullets | 01:00-02:00, 08:00-09:00, 12:00-13:00 |
| Forced flat / resume | 14:45 / 16:00 |

## Quick routine

1. Open the chart at the reopen and read **Daily bias** and **Bias detail**. `No-bias day` means trade smaller or sit out.
2. Note **Liquidity above** and **below**: the nearer one that is also in the bias direction is the target. If it is under about 15% ADR away, there is little room.
3. Follow **Daily AMD** through the stages. No sweep and reclaim means no textbook day.
4. Take entries only from the main indicator, inside a kill zone or silver bullet.
5. Read **Risk budget** and **Main signal** for contracts. Stop trading at `DAILY LIMIT REACHED`.
6. Stop entering when the Clock turns red. Be flat before 14:45.
