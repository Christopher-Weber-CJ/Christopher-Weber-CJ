# Trader Mayne Framework (TradingView, Pine v6)

`trader-mayne-framework.pine` implements the trading framework from Trader Mayne's
[Whiteboard Series](https://www.youtube.com/playlist?list=PLKItFyoma4GeQSNjY7LM5qtEgTFUidxYI).

**Status: v1, built from episodes 1-11 of 24. It has not been compiled or tested in TradingView yet.**
Paste it into the Pine Editor, fix any compile message it reports, and check it against charts before relying on it.

## Install

1. TradingView → Pine Editor → paste the file → *Add to chart*.
2. Put it on the entry timeframe (for example 15m or 1h). The bias timeframe defaults to `D`, which must be above the chart timeframe.

## What is implemented, by episode

| Episode | Concept | In the indicator |
|---|---|---|
| 1-2 | Three-candle swings, HH/HL/LH/LL, MSB (continuation), MSS (reversal, break of the last HL/LH) | Structure engine. Breaks need a **close** through the level. `+D` marks a displacement candle. |
| 1-4 | Working / dealing range from major swings, EQ 50%, premium / discount | Dealing range, EQ and shaded premium / discount. Uses the chart range or the HTF range. |
| 3, 11 | Buy-side / sell-side liquidity, equal highs / lows, SFP, break-and-close | Unswept swing levels as lines, EQH / EQL flags, and sweep markers (SFP, BAC). |
| 4 | Internal liquidity is for entries, external range liquidity is for targets | The target is the far end of the HTF dealing range (chart range as fallback). |
| 5 | HTF bias, top-down, 4-point checklist, positive RR | HTF structure bias (non-repainting), checklist dashboard, minimum RR filter. |
| 6 | Fair value gap: 3 candles with a displacement candle in the middle | FVG zones, with entry and stop rules. |
| 7 | Order block = last opposite candle before displacement. Breaker = failed OB (S/R flip). Quality: displacement, MSB, liquidity taken, big candle, FVG overlap. | OB and breaker zones with a 0-7 quality score. The mean threshold is dotted. |
| 8 | Filters: location, context, quality, RR, LTF confirmation. OB + FVG overlap is best. | Location and score gating. `★` marks an OB overlapping an FVG. |
| 9 | OTE 61.8 - 78.6 (ICT 62 / 79), sweet spot 70.5 | OTE band and sweet-spot line. A zone inside the OTE gets a score point. |
| 10 | PO3 / AMD, Judas swing, Asia range, daily / weekly open, Monday range | Asian range box, Judas markers (Asia sweep plus reclaim), daily / weekly open, Monday high / low. |

## Setup logic (the "sync" model from episodes 2, 5, 7, 8)

A long fires when all of these are true:

1. HTF bias is bullish.
2. Chart structure has flipped bullish (MSS / MSB) and left an OB, breaker or FVG.
3. The zone is in discount (below EQ) and scores at least the minimum.
4. Price retests the zone and closes above its 50% mean threshold.
5. An external-range target exists and reward:risk is at least the minimum (default 2R).

Shorts are the mirror image. Optional gates: kill zone, recent liquidity sweep, allow counter-bias.
Stop and entry follow the videos: entry at the zone edge or 50%, stop beyond the zone or beyond the sweep extreme.

## Not yet implemented (episodes 12-25, not read yet)

Episodes 12-25 are: the entry model, top-down analysis, wrong-timeframe fix, when to walk away,
losing trades and win rate, scaling, news trading, advanced dealing ranges, kill zones, SMT divergence,
liquidity trap and learning liquidity, and best-trade breakdown.
YouTube rate-limited transcript downloads after episode 11, so those rules are **not** in the script.
The kill-zone times (Asia 20:00-00:00, London 02:00-05:00, NY 07:00-10:00 New York time) are common ICT defaults,
not confirmed from his kill-zone episode.

## Alerts

Long / short setup, bullish / bearish MSS, sell-side / buy-side sweep, Judas swing.
