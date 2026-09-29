# Trader Mayne Framework (TradingView, Pine v6)

`trader-mayne-framework.pine` implements the trading framework from Trader Mayne's
[Whiteboard Series](https://www.youtube.com/playlist?list=PLKItFyoma4GeQSNjY7LM5qtEgTFUidxYI).

**Status: v1.6, built from episodes 1-17 of 24. It has not been compiled or tested in TradingView yet.**
Paste it into the Pine Editor, fix any compile message it reports, and check it against charts before relying on it.

## Install

1. TradingView → Pine Editor → paste the file → *Add to chart*.
2. Put it on your execution timeframe (for example 5m). The direction, sync and context timeframes default to `W`, `D` and `240` (H4), and must be above the chart timeframe.

## What is implemented, by episode

| Episode | Concept | In the indicator |
|---|---|---|
| 1-2 | Three-candle swings, HH/HL/LH/LL, MSB (continuation), MSS (reversal, break of the last HL/LH) | Structure engine. Breaks need a **close** through the level. `+D` marks a displacement candle. |
| 1-4 | Working / dealing range from major swings, EQ 50%, premium / discount | Dealing range, EQ and shaded premium / discount. Uses the daily range, weekly range or chart range. |
| 3, 11 | Buy-side / sell-side liquidity, equal highs / lows, SFP, break-and-close | Unswept swing levels as lines, EQH / EQL flags, and sweep markers (SFP, BAC). |
| 4 | Internal liquidity is for entries, external range liquidity is for targets | Targets are equal highs / lows and higher-timeframe range extremes. |
| 5 | HTF bias, top-down, 4-point checklist, positive RR | HTF structure bias (non-repainting), checklist dashboard, minimum RR filter. |
| 6 | Fair value gap: 3 candles with a displacement candle in the middle | FVG zones, with entry and stop rules. |
| 7 | Order block = last opposite candle before displacement. Breaker = failed OB (S/R flip). Quality: displacement, MSB, liquidity taken, big candle, FVG overlap. | OB and breaker zones with a 0-7 quality score. The mean threshold is dotted. |
| 8 | Filters: location, context, quality, RR, LTF confirmation. OB + FVG overlap is best. | Location and score gating. `★` marks an OB overlapping an FVG. |
| 9 | OTE 61.8 - 78.6 (ICT 62 / 79), sweet spot 70.5 | OTE band and sweet-spot line. A zone inside the OTE gets a score point. |
| 12 | Four-step top-down process: weekly + daily direction, H4 context, H1 setup, M5 entry. Stop beyond the H4 POI, targets from the higher timeframes. | Direction (W) and sync (D) timeframes, context (H4) POIs plotted, zone must sit inside a context POI, stop beyond that POI, target = nearest equal high/low or higher-timeframe range extreme paying at least minRR. |
| 13 | Five-minute model: zone tag, 5m structure break, displacement, FVG pullback entry, stop beyond the 5m swing (or the HTF zone), HTF targets, minimum 2R | Default entry model. See below. |
| 14 | Reversal vs continuation setups, H4 / H1 confirmation before the model, 15-minute model = same model on a higher chart, silver bullet windows | Reversal / continuation labels and stop rule, confirmation gate, silver bullet windows. See below. |
| 15 | Seven disqualifiers: no HTF bias, wrong zone, no target or under 2R, incomplete model, chasing, news, emotion | No-trade filters and a dashboard row naming the first disqualifier. See below. |
| 16 | Stop = invalidation, hard stop that never widens, position size from the stop, TP from internal / external liquidity, partials in 25% or 1/3, 2:1 minimum, break-even win-rate math | Risk and exits inputs, position size on every signal, 2R and partial levels. See below. |
| 17 | Scaling in: split the same risk, never add risk. Scale within a zone, or add only on new confirmed models. No averaging down. | *Entry scaling* setting. See below. |
| 10 | PO3 / AMD, Judas swing, Asia range, daily / weekly open, Monday range | Asian range box, Judas markers (Asia sweep plus reclaim), daily / weekly open, Monday high / low. |

## Setup logic

Put the indicator on your **execution** timeframe (for example 5m). The defaults follow his examples:
weekly + daily → H4 → (H1: wait) → 5m.

**Top-down (episode 12).**
1. Weekly structure sets bias. The daily must agree with it. If the daily is still pulling back against the weekly, the dashboard says *Wait* and there are no signals.
2. Premium / discount is measured in the daily range. The live H4 order block or fair value gap is drawn as a shaded context POI.
3. Wait for price to tag that context POI.

**Five-minute model (episode 13, the default entry model).** All five steps must happen in order:
1. Price **trades into** the context POI (overlapping it, not just near it).
2. The chart timeframe breaks structure in the trade direction after the tag (a bullish break of the last lower high for longs).
3. The break comes with a **displacement** candle (body of at least 1.2 ATR by default).
4. The displacement leaves a **fair value gap** (created during the leg or within 3 bars after the break). Enter on the pullback: the signal fires when price retests it and closes past its 50%. Each new qualifying break can give a new entry.
5. The stop goes beyond the chart swing before the break (default). The alternative, beyond the context POI, is his safer choice for reversals. The target is the nearest equal high / low or daily / weekly range extreme that pays at least the minimum reward:risk (default 2R).

No zone tag, no displacement, or under 2R means no signal. The dashboard shows which step is missing.
**Reversal vs continuation and confirmation (episode 14).**
- If the daily already agrees with the weekly, the setup is a **continuation** (`CONT`). The stop defaults to the chart swing before the break (tight).
- If the daily still disagrees, it is a **reversal** (`REV`). It only fires after the H4 or H1 has flipped in the trade direction (structure break), and the stop defaults to beyond the context POI (wider, smaller size). Turn *Allow reversal setups* off to wait for the daily instead.
- Stop = *Auto* applies those two rules. It can be forced to the chart swing, the context POI or the zone edge.
- The **15-minute model** is the same model: run the indicator on a 15m chart. The same works on 1h.
- **Silver bullet:** the three windows (03:00-04:00, 10:00-11:00, 14:00-15:00 New York time) are shaded, and signals inside them are tagged `SB`. *Only trade inside a silver bullet window* makes them a filter. Turn on *Require a recent liquidity sweep* to match his "sweep, break, FVG" description.

**No-trade filters (episode 15).** If any of his seven disqualifiers is active there is no signal, and the dashboard's *No-trade filter* row names the first one:

| # | Disqualifier | How the indicator checks it |
|---|---|---|
| 1 | No clear HTF bias | Direction timeframe must have structure bias and an efficiency ratio above the minimum (ranging = no trade). Default 0.10 is my own guess, so tune it. |
| 2 | Price in the wrong zone | Longs only below the range midpoint, shorts only above it. Applies to the 5m model too. |
| 3 | No target, or under 2R | A target must exist and pay at least the minimum reward:risk. |
| 4 | Model did not fully trigger | The five steps must complete in order. |
| 5 | Chasing | A 5m-model FVG is cancelled if price runs 5 ATR away without a retest. Signals only fire on the retest bar. |
| 6 | News | Pine cannot see an economic calendar. Enter up to three event times by hand; the window (60 min before, 120 after) is shaded red and blocks signals. |
| 7 | Emotion | It cannot measure emotion. Instead, *Tilt guard* can pause signals after N consecutive stopped-out signals. The dashboard also counts the indicator's own signal wins and losses (stop assumed first if both are hit in one bar). |

**Risk and exits (episode 16).** Enter your account size and risk % (his range is 0.5-2%).
- **Stop:** the stop stays at the invalidation point (the chart swing for continuations, the context POI for reversals), plus a small ATR buffer so it is not on the exact tick.
- **Position size** = risk % × account ÷ |entry − stop|. It is written on each signal label and on the dashboard. Leverage and margin are not part of it. Units are coins or contracts, so check the contract size for futures / forex.
- **Exits:** each signal draws the stop, the external target, a dashed **2R** line, and, if one exists between entry and 2R, a **partial** level at the nearest internal liquidity (default 25%). His mechanical default is to close everything at 2R and leave partials and trailing for later.
- **Break-even win rate** for the current reward:risk is on the dashboard (2R needs 33%, 3R needs 25%).
- Nothing drags the target or the stop to force 2R. If the chart's own levels do not pay 2R, there is no signal.
- Not enforceable by an indicator, so follow them yourself: place the stop as a hard order at entry, never widen it, do not move it to break even too early, and do not take profit just because the trade is green.
- The dashboard's signal win / loss count now counts a win at 2R by default (*Count a signal as a win at*).

**Scaling in (episode 17).** Scaling splits your predefined risk into pieces. It never adds risk. The default is *Single entry*, which is his advice until you are comfortable with the basic model.
- **Scale in zone:** entries at the top, middle and bottom of the entry zone (default weights 30 / 30 / 40). The stop stays at the single planned stop. Sizes are solved so that, if all three fill and the stop is hit, you lose exactly your risk %. A shallow pullback fills less and risks less. Each signal label shows the three sizes and the reward:risk at your average entry. The signal itself is still gated on the top-of-zone reward:risk.
- **Add on confirmation:** the first entry is a fraction of full size (default 50%). Each later add (default two, 25% each) fires only when a **new, separate model** forms (structure break, displacement, new FVG, retest) in the same direction. The stop can move up to each new model's swing low (never down), and the labels are tagged `ADD1`, `ADD2`. No adds fire after the campaign stop has been hit, which is how the indicator keeps you out of averaging down.
- His combined ladder (half at the top of a daily zone, the rest on lower-timeframe models) can be approximated by using *Add on confirmation* on a lower-timeframe chart. The half-at-the-zone-touch entry is not automated.

Set *Entry model* to "OB / breaker / FVG (general)" for the score-filtered order block, breaker and FVG logic from episodes 6-9 instead.
Shorts are the mirror image. Optional gates: kill zone, recent liquidity sweep, allow counter-bias.

The 1-hour step is a "wait" step, so it has no separate setting. The context POI tag is the equivalent.

## Not yet implemented (episodes 18-25, not read yet)

Episodes 18-25 are:
news trading, advanced dealing ranges, kill zones, SMT divergence,
liquidity trap and learning liquidity, best-trade breakdown, and trading psychology.
YouTube rate-limited transcript downloads after episode 11. Episodes 12-17 were supplied by hand. Episodes 18-25 are **not** in the script yet.
The kill-zone times (Asia 20:00-00:00, London 02:00-05:00, NY 07:00-10:00 New York time) are common ICT defaults,
not confirmed from his kill-zone episode.

## Alerts

Long / short setup, bullish / bearish MSS, sell-side / buy-side sweep, Judas swing.
