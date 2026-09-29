# Trader Mayne Framework (TradingView, Pine v6)

`trader-mayne-framework.pine` implements the trading framework from Trader Mayne's
[Whiteboard Series](https://www.youtube.com/playlist?list=PLKItFyoma4GeQSNjY7LM5qtEgTFUidxYI).

**Status: v1.13, built from all 25 episodes. It has not been compiled or tested in TradingView yet.**
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
| 18 | News is the driver, liquidity is the destination. Know the calendar, no new entries before news, manage what you have, let the candle close, trade the aftermath. | News window, `NEWS` sweep tags, news-start alert. See below. |
| 19 | Nested ranges, range resets only on displacement, stacking premium / discount across timeframes for A+ setups | Range stack row, A+ / A / B grade, displacement-only resets. See below. |
| 20 | Time and price: kill zones, silver bullet windows, crypto trading day, time as a filter and grade, never an entry on its own | Confirmed session times, afternoon window, crypto window, time-based grade downgrade. See below. |
| 21 | SMT divergence between correlated assets at key levels, as a filter that upgrades conviction, not a signal | Optional SMT check, grade upgrade and filter. See below. |
| 22 | Liquidity-to-liquidity map, daily bias checklist, premium is not a short signal, trigger proves the level | Previous day / week / month liquidity, daily bias row, optional bias filter. See below. |
| 23 | Chart patterns (Wyckoff, head and shoulders, double tops, wedges, flags) are snapshots of liquidity plus market structure; patterns lag, context decides | Range AMD marker, plus the existing sweeps, EQH / EQL and structure breaks. See below. |
| 24 | Full trade review: weekly to hourly to 5m, stop at the sweep high for reversals, partials at internal liquidity, runner for the higher-timeframe idea | Reversal stop now also goes beyond the sweep extreme; partial size up to two-thirds. See below. |
| 25 | Where traders fail: oversizing, lottery brain, no measurement, overtrading, revenge trading, system hopping, quitting, complacency | Guard-rails only. See below. |
| 10 | PO3 / AMD, Judas swing, Asia range, daily / weekly open, Monday range | Asian range box, Judas markers (Asia sweep plus reclaim), daily / weekly open, Monday high / low. |

## Reading the chart (Display settings)

The framework draws a lot, so *Chart view* has three levels and defaults to **Signals**:
- **Signals:** only the trade plans (entry, stop, target, 2R and partial lines, size, grade), the long / short markers, the context-timeframe POI, the chart dealing range with its OTE zone, Judas / SMT / range-AMD markers, and the dashboard. Everything below is hidden.
- **Clean** (the level described next) adds more context.
- **Full** draws everything.

**Clean** adds to Signals:
- **Shown:** the dashboard, the chart dealing range (high, low, EQ and the OTE zone), the context-timeframe POI, the 5-minute-model entry zones (drawn once a qualifying structure break claims them), order blocks / breakers scoring at least 5, equal-high / equal-low liquidity lines, sweeps of those or during news, structure breaks that are reversals or have displacement, Judas / SMT / range-AMD markers, the previous day and week highs and lows, and the last few trade plans.
- **Hidden until you switch to Full:** plain swing-liquidity lines, most sweep and structure labels, premium / discount shading, the sync and direction range lines, the month levels and previous-week midpoint, daily / weekly opens, Monday range, the Asia box, and the afternoon / silver bullet shading.
- *Dashboard text size* makes the checklist larger. To clear the row of input values at the top-left of the pane, open the indicator's Settings, then Status line, and untick Inputs.
- Everything still runs in Clean view. Hidden items are only not drawn, so signals, grades and the dashboard are the same in both views.

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

**News (episode 18).** News is treated as a fast liquidity sweep, not a signal.
- The news window from episode 15 (default 60 minutes before, 120 after, up to three events entered by hand) blocks new signals, which covers "no new entries before news" and "let the candle close". Once it ends, the normal top-down model applies again, which is "trade the aftermath".
- Sweeps that happen inside the window are tagged `NEWS`, so you can see the news spike took a liquidity level while the higher-timeframe bias stayed intact.
- An alert fires when a news window starts, as a prompt to manage open trades (hold, flatten or take a partial; never widen the stop).
- The calendar itself is manual. He uses forexfactory.com (red = high impact), the CME FedWatch probabilities and Yahoo Finance earnings.

**Nested ranges and stacking (episode 19).**
- The dashboard's *Range stack* row shows where price sits in the weekly, daily, H4 and H1 ranges (`D` = discount, `P` = premium). A long wants `D` everywhere, a short wants `P` everywhere.
- Setups are graded **A+** (every range on the right side), **A** (all but one) or **B**. The grade is on each signal label. *Require at least N ranges* can make stacking a filter. *Grade setups... risk more on A+* (off by default) lifts the risk from your normal % to the A+ % (default 2%), as he describes.
- The chart dealing range now resets only on **expansion with displacement**. A sweep, SFP or deviation beyond the range leaves it unchanged. After a displacement reset, the old range high / low stays on the chart as a level of interest (support / resistance flip). The higher-timeframe ranges use the plain swing rule and do not have this displacement check yet.

**Time and price (episode 20).** Time is a filter and a grade. It never creates an entry by itself; the model still has to play out.
- Session times (all New York time, now taken from the video): London kill zone 02:00-05:00, New York kill zone 07:00-10:00, afternoon window 13:30-16:30 (weaker, mostly continuation or a retrace, so it only counts as a kill zone if you switch that on), silver bullet windows 03:00-04:00, 10:00-11:00 and 14:00-15:00. The Asia range (20:00-00:00) is my default for his "overnight session".
- For crypto he suggests treating 08:00-21:00 UTC as the trading day. That window can be made a hard filter.
- **Grading:** a setup outside the kill zones is downgraded one grade (A+ to A, A to B) on the label and in the dashboard. Turn it off with *Downgrade a setup*. Combined with *Grade setups by range stack*, an A+ setup can carry the larger risk %.
- Judas markers now say whether the Asian-range sweep happened in the London or New York window (his pattern: London manipulation, New York distribution). Alerts fire when the London and New York kill zones start.
- He points out that back-testing pattern-only setups overstates results because many losers happen outside these windows.

**SMT divergence (episode 21).** Off by default. He says SMT is a nice-to-have that upgrades a B+ / A setup to A+, never a signal on its own, and that plain SMT indicators are noisy because they mark every disagreement. So this one is deliberately narrow:
- Turn it on and pick a correlated symbol (BTC vs ETH, NQ vs ES, EURUSD vs GBPUSD). It compares the same timeframe on both charts.
- It only counts **at a key level** (price inside a context-timeframe POI, or right after a liquidity sweep), and only when one asset makes a new swing extreme over the window while the other **clearly** does not (default: it must hold 0.1% beyond its prior extreme).
- A bullish or bearish `SMT` marker is drawn, and the signal grade goes up one level while the SMT is recent. Optionally require it (off by default), because a setup without SMT is still a valid setup.
- It says the move on the first chart was likely fake. It does not say which asset to trade or which is stronger. Pick whichever chart shows your model most cleanly.
- Doing the same check by eye at your zone still takes about 10 seconds, and he recommends it.

**Liquidity map and daily bias (episode 22).**
- **Map:** the previous day, week and month highs and lows are plotted (thicker for higher timeframes). They dim once the current period has swept them, which is his "spent / unspent" marking. The previous week's 50% is also plotted, because after a daily sweep of a weekly level he found price pulls back to about that midpoint.
- **Daily bias checklist**, all on the dashboard's *Daily bias* row. A bullish bias needs: the higher-timeframe draw above price (a swept low points up, a swept high points down, otherwise the nearer level); yesterday's daily candle closed in its bottom 10%; the weekly bullish; price in the weekly discount; and yesterday's low either still intact or swept early in the day (within 8 hours of the daily open). Bearish is the mirror image.
- **No-bias day:** if yesterday closed in the middle of its range, the row says so. He says direction is a coin flip and a quarter of the time it is an inside day.
- *Require the full daily bias* and *Skip no-bias days* can turn this into filters. Both are off by default, and the full bias is rare, since every item has to line up. A setup that fails it is not invalid, it is just not A+.
- Premium and discount are still not sell and buy signals by themselves. The indicator only uses them as location filters, together with the trigger.

**Statistics he quotes in that episode (his own tests on BTC, ETH and SOL, not verified here):** the current daily candle takes out the prior day's high or low about 80% of the time (about 84% weekly, 86% monthly); after a close in the top or bottom 10% of the range the next day takes out that extreme about 9 times in 10; after a daily sweep of a weekly level, price returns to the weekly candle's midpoint within five days about half the time and reverses all the way to the other side about one time in six; the same setup worked about 45% of the time in discount versus 37% in premium; a five-year hourly test of the basic level-buying strategy won about 33% (break-even at 2R) and adding the trigger lifted it to about 42%. Use them as context, and back-test on your own data.

**Chart patterns (episode 23).** He argues you never need to memorise a pattern, because each one is a snapshot of liquidity and structure inside an accumulation-manipulation-distribution cycle. Nothing here trades a pattern by itself. What the indicator already draws covers them:
- **Wyckoff accumulation / distribution** is a range where one side is swept and reclaimed, then structure breaks the other way. New *Range AMD* markers (`AMD ↑ spring`, `AMD ↓ UTAD`) fire when a compressed range (default 40 bars, at most 6 ATR tall) has one side swept and reclaimed and a structure break follows within 10 bars.
- **Double tops / bottoms** are equal highs / lows, which the liquidity lines flag (`EQH` / `EQL`) and mark when swept.
- **Head and shoulders** is a sweep of a shoulder, a failed higher high and a structure break. The neckline break is the structure break, and the signal still needs the higher-timeframe context (a neckline break in a bullish discount at an order block can be bait).
- **Wedges, triangles and bull flags** build liquidity on both sides. The trend before them and the higher-timeframe draw decide the direction, which the bias and the range stack already show.
- Patterns are lagging. The framework's signals use the bias, zone, liquidity and model instead.

**Trade review (episode 24).** His walk-through is the framework applied end to end: weekly bearish, a weekly fair value gap in the premium, a daily flip to bearish, a sweep into a bearish order block, then an hourly (or 5m) breaker plus fair value gap. He states that with a reversal the stop goes at the sweep high, not the gap.
- The *Auto* stop for reversals now goes beyond both the context POI and the swept leg extreme.
- His exit was two partials: about two-thirds closed at internal liquidity on the entry timeframe, and the runner held for the weekly idea. Set *Partial size* to about 67 to draw that plan.
- He risks a static $2,000 on a $100,000 account for the journal example (63 trades, about 55% wins, average winner about 2.8R). The size and risk inputs can be set the same way. Those figures are his, not results of this indicator.

**Behaviour (episode 25).** Episode 25 is about the gap between knowing a system and running it. It teaches no chart rules, so the script only adds guard-rails for the failure modes that a chart tool can see:
- **Oversizing:** the dashboard's size row turns red and warns when the risk % is above 2%. He notes that even a 60% edge can be wiped out by a losing streak if you over-bet, and that as the account grows you should keep thinking in % (one R) rather than the dollar amount.
- **Overtrading:** *Overtrading guard* caps signals per day (off by default) and the dashboard shows "Daily signal cap" when it is hit. The many filters in the other episodes are the main defence, since he says a good filter means fewer trades.
- **Revenge trading:** the tilt guard (episode 15) pauses signals after consecutive stopped-out signals.
- **No measurement / complacency:** the dashboard counts wins and losses of the indicator's own signals (with 2R as the default win level), which is a starting point for journaling, not a replacement for it. He says a journal, and following the same checklist every time, is what stops cracks forming.
- **Things a script cannot do:** hard stops, never widening or moving a stop early, not system-hopping, and staying with the process through a losing month. He measures early progress by whether you followed the system, not by P&L, and quotes roughly 1-3 years in the "tuition" phase and 3-5 years to consistent profitability. Those timelines are his opinion.

Set *Entry model* to "OB / breaker / FVG (general)" for the score-filtered order block, breaker and FVG logic from episodes 6-9 instead.
Shorts are the mirror image. Optional gates: kill zone, recent liquidity sweep, allow counter-bias.

The 1-hour step is a "wait" step, so it has no separate setting. The context POI tag is the equivalent.

## Known gaps and cautions

- All 25 episodes of the playlist have been read (episodes 1-11 downloaded, 12-25 supplied as transcripts). The script has **not** been compiled or run in TradingView, so expect a compile error or two on first load, and check every signal against a chart before trusting it.
- Where his rules were discretionary (which swing is "significant", what counts as "clear and obvious", how deep a zone is), the script uses a fixed rule and numeric defaults that I chose. Tune them.
- The higher-timeframe ranges use a plain major-swing rule. The displacement-only range reset (episode 19) applies to the chart range only.
- His combined ladder (half the position at the touch of a daily zone, the rest on lower-timeframe models) is not automated.
- News times and the calendar are entered by hand. Emotion, hard stops and journaling cannot be automated.
- Statistics quoted in the episodes are his own tests and were not re-checked here.

## Alerts

Long / short setup, bullish / bearish MSS, sell-side / buy-side sweep, Judas swing.
