---
description: "Review portfolio for thesis drift and concentration risk"
---

# Portfolio Review Skill

Review the current portfolio for thesis drift, concentration risk, and correlated bets. Generate a structured quarterly review.

## Prerequisites

1. Read `portfolio/positions.md` to get the current holdings list.
   - If `portfolio/positions.md` does not exist, tell the user: "No positions file found at `portfolio/positions.md`. Create this file with your current holdings before running a portfolio review."
   - Stop execution.
2. Parse the positions file to extract each held ticker, position size, cost basis, and any other available data.
3. Determine the current quarter (e.g., 2026-Q1) from today's date for the review filename.

## Step 1: Load Research for Each Holding

For each ticker found in `positions.md`:
- Check if `research/{TICKER}/overview.md` exists
- If it exists, read it (thesis, bull case, bear case, key metrics)
- If it does NOT exist, note it as "No research on file" — flag this in the output
- Also read `research/{TICKER}/financials/income-statement.md` if available
- Also read the most recent earnings file in `research/{TICKER}/earnings/` if any exist

Build a summary data structure of all holdings with their thesis status.

## Step 2: Thesis Drift Check

*Note: This is a lightweight check using existing research data. For holdings flagged as "Drifting" or "Broken," run `/thesis-check {TICKER}` for a deep validation with fresh SEC EDGAR data.*

For each holding with existing research, assess:

1. **Original Thesis:** What was the investment thesis from `overview.md`?
2. **Current Evidence:** Based on the most recent earnings data and any thesis update log entries, is the thesis still intact?
3. **Drift Status:** Assign one of:
   - **On Track** — thesis playing out as expected
   - **Monitor** — some signals warrant attention but thesis holds
   - **Drifting** — thesis is weakening, position should be reviewed
   - **Broken** — original thesis is no longer valid

Look for specific signals:
- Revenue growth decelerating below thesis assumptions
- Margin compression vs thesis expectations
- Competitive position changes noted in bear case
- Management changes or strategy shifts
- Any "tripwires" from bear case analysis that have triggered

## Step 3: Concentration Audit

Analyze portfolio concentration across multiple dimensions:

1. **Position Sizing** — Flag any single position > 15% of portfolio
2. **Sector Concentration** — Flag if any sector > 35% of portfolio
3. **Geographic Concentration** — Assess revenue geographic exposure (from overview.md data)
4. **Market Cap Concentration** — Distribution across large/mid/small cap
5. **Factor Concentration** — Are positions clustered on growth, value, momentum, etc.?

## Step 4: Correlation Analysis

Identify correlated bets — holdings that would move together:

1. **Direct Competitors** — Holdings in the same industry competing for the same customers
2. **Supply Chain Links** — Holdings where one is a supplier/customer of another
3. **Macro Sensitivity** — Holdings that share the same macro risk factors (interest rates, consumer spending, ad market, etc.)
4. **Thematic Overlap** — Holdings riding the same secular trend (e.g., multiple AI plays, multiple cloud plays)

Flag any cluster of 3+ correlated holdings as a "concentration risk."

## Step 5: Performance Attribution (Qualitative)

Since we do not have live price data, perform a qualitative assessment:
- Which holdings are executing best against their thesis?
- Which holdings have delivered negative thesis surprises?
- Which holdings have the strongest/weakest risk-reward going forward?
- Rank holdings by conviction level (High / Medium / Low)

## Step 6: Generate Review File

Create the `portfolio/quarterly-reviews/` directory if it doesn't exist.

Write `portfolio/quarterly-reviews/{YYYY}-Q{X}.md`:

```markdown
# Portfolio Review — {YYYY} Q{X}

*Generated: {YYYY-MM-DD}*
*Holdings reviewed: {N}*

## Portfolio Summary

| Ticker | Position % | Thesis Status | Conviction | Notes |
|--------|-----------|---------------|------------|-------|
| {TICK} | XX% | On Track / Monitor / Drifting / Broken | High/Med/Low | [brief] |
| ... | ... | ... | ... | ... |

## Thesis Drift Check

### On Track
| Ticker | Thesis | Supporting Evidence |
|--------|--------|-------------------|
| {TICK} | [1-line thesis] | [recent data point] |

### Monitor
| Ticker | Thesis | Concern |
|--------|--------|---------|
| {TICK} | [1-line thesis] | [what to watch] |

### Drifting / Broken
| Ticker | Thesis | Issue | Recommended Action |
|--------|--------|-------|-------------------|
| {TICK} | [1-line thesis] | [what changed] | Trim / Exit / Hold & Review |

### No Research on File
- {TICK} — Run `/research {TICK}` to build a thesis

## Concentration Audit

### Position Sizing
[Flag any position > 15% — include exact %]

### Sector Exposure
| Sector | % of Portfolio | Holdings |
|--------|---------------|----------|
| Technology | XX% | TICK1, TICK2 |
| ... | ... | ... |

[Flag if any sector > 35%]

### Correlated Bets
[List clusters of correlated holdings]

| Cluster | Holdings | Shared Risk | Combined Weight |
|---------|----------|-------------|----------------|
| [Theme] | TICK1, TICK2 | [risk factor] | XX% |

## Conviction Ranking

1. **{TICK}** — [1-line rationale] (High)
2. **{TICK}** — [1-line rationale] (High)
3. ...

## Action Items

- [ ] [Specific action — e.g., "Trim TICK — position > 15%, thesis monitor"]
- [ ] [Specific action — e.g., "Run /research TICK — no thesis on file"]
- [ ] [Specific action — e.g., "Review TICK — thesis drifting, Q2 earnings will be decisive"]
- [ ] [Specific action — e.g., "Evaluate correlation: TICK1 + TICK2 + TICK3 all exposed to ad market"]
- [ ] Run /thesis-check {TICK} — thesis drifting, needs deep validation against latest data

## Appendix: Data Gaps

List any data limitations encountered:
- No live price data (positions based on portfolio/positions.md allocations)
- Missing research for: {list tickers}
- Stale earnings data for: {list tickers with old or no earnings files}
```

## Step 7: Summary

Print a summary:
```
Portfolio review complete — {YYYY} Q{X}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Holdings reviewed: {N}
  On Track: {N}
  Monitor:  {N}
  Drifting: {N}
  Broken:   {N}
  No Research: {N}

Concentration alerts: {N}
Correlated clusters: {N}
Action items: {N}

Deep checks needed: {N} (run /thesis-check for each)
  - /thesis-check {TICK1}
  - /thesis-check {TICK2}

Created: portfolio/quarterly-reviews/{YYYY}-Q{X}.md
```

The "Deep checks needed" block should only be printed if there are holdings with Drifting or Broken status. Omit it entirely if all holdings are On Track or Monitor.
