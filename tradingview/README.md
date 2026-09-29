# Trader Mayne Framework (TradingView, Pine v6)

`trader-mayne-framework.pine` implements the trading framework from Trader Mayne's
[Whiteboard Series](https://www.youtube.com/playlist?list=PLKItFyoma4GeQSNjY7LM5qtEgTFUidxYI).

**Status: v1.1, built from episodes 1-12 of 24. It has not been compiled or tested in TradingView yet.**
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
| 12 | Four-step top-down process: weekly + daily direction, H4 context, H1 setup, M5 entry. Stop beyond the H4 POI, targets from the higher timeframes. | Direction (W) and sync (D) timeframes, context (H4) POIs plotted, zone must sit inside a context POI, stop beyond that POI, target = nearest equal high/low or higher-timeframe range extreme paying at least minRR. |
| 10 | PO3 / AMD, Judas swing, Asia range, daily / weekly open, Monday range | Asian range box, Judas markers (Asia sweep plus reclaim), daily / weekly open, Monday high / low. |

## Setup logic (the four-step process, episode 12)

Put the indicator on the **execution** timeframe (for example 5m). The defaults follow his example:
weekly + daily → H4 → (H1: wait) → 5m.

1. **Direction / sync.** Weekly structure sets bias. The daily must agree with it. If the daily is still pulling back against the weekly, the dashboard says *Wait* and there are no signals.
2. **Context.** Premium / discount is measured in the daily range. The H4 order block or fair value gap that is still live is drawn as a shaded context POI.
3. **Setup.** Wait for price to tag that context POI (the dashboard shows *Waiting* until it has).
4. **Entry.** On the chart timeframe, a structure break in the bias direction leaves an OB, breaker or FVG inside the context POI. A retest that closes above (longs) or below (shorts) the zone's 50% fires the signal.

The stop goes beyond the context POI, because the idea is wrong there. Targets come from the higher timeframes:
the nearest equal high / low, then the daily and weekly range extremes, taking the nearest one that pays at least the minimum reward:risk (default 2R).
Shorts are the mirror image. Optional gates: kill zone, recent liquidity sweep, allow counter-bias, and switching off the context-POI requirement.

The 1-hour step is a "wait" step, so it has no separate setting. The context POI tag is the equivalent.

## Not yet implemented (episodes 12-25, not read yet)

Episodes 13-25 are: the entry model, wrong-timeframe fix, when to walk away,
losing trades and win rate, scaling, news trading, advanced dealing ranges, kill zones, SMT divergence,
liquidity trap and learning liquidity, and best-trade breakdown.
YouTube rate-limited transcript downloads after episode 11. Episode 12 was supplied by hand. Episodes 13-25 are **not** in the script yet.
The kill-zone times (Asia 20:00-00:00, London 02:00-05:00, NY 07:00-10:00 New York time) are common ICT defaults,
not confirmed from his kill-zone episode.

## Alerts

Long / short setup, bullish / bearish MSS, sell-side / buy-side sweep, Judas swing.
