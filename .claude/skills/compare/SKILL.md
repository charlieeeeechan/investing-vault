---
description: "Side-by-side comparison of two companies"
argument: "[T1] [T2] — Two stock ticker symbols to compare"
---

# Compare Skill

Perform a 15-dimension side-by-side comparison of two companies and produce a structured comparison report.

## Prerequisites

1. Parse the argument to extract two ticker symbols. Normalize both to uppercase.
2. Check if `research/{T1}/overview.md` and `research/{T2}/overview.md` exist.
   - If EITHER is missing, tell the user which one(s) are missing and suggest: "Run `/research {TICKER}` first to build the research base."
   - If BOTH are missing, suggest running `/research` for each.
   - Stop execution if either is missing (do not attempt a partial comparison).
3. Read the full research folder for both tickers:
   - `research/{T1}/overview.md` and `research/{T2}/overview.md`
   - `research/{T1}/financials/income-statement.md` and `research/{T2}/financials/income-statement.md`
   - `research/{T1}/financials/balance-sheet.md` and `research/{T2}/financials/balance-sheet.md`
   - `research/{T1}/financials/cash-flow.md` and `research/{T2}/financials/cash-flow.md`
   - `research/{T1}/valuation.md` and `research/{T2}/valuation.md`
   - Any earnings files in `research/{T1}/earnings/` and `research/{T2}/earnings/`

## Step 1: Extract Key Data

From the financial files, extract the most recent annual data for both companies:
- Revenue, revenue growth rate
- Gross margin, operating margin, net margin
- Operating cash flow, free cash flow, FCF margin
- Total assets, total liabilities, net debt, debt-to-equity
- EPS, P/E (if available in valuation.md)
- R&D spend, R&D as % of revenue

From overview.md, extract:
- Business description, key segments
- Moat analysis and competitive advantages
- Bull and bear case points

## Step 2: Run 15-Dimension Comparison

Evaluate both companies across all 15 dimensions. For each dimension, provide:
- Data/evidence for each company
- A clear winner or "Tie" verdict
- Brief rationale (1-2 sentences)

The 15 dimensions:

1. **Revenue Scale & Growth** — Total revenue and trailing growth rate. Bigger and faster-growing wins.
2. **Profitability** — Gross, operating, and net margins. Higher and more consistent wins.
3. **Cash Flow Generation** — FCF, FCF margin, FCF conversion. Stronger and more reliable wins.
4. **Balance Sheet Strength** — Net debt, debt-to-equity, current ratio, interest coverage. Cleaner balance sheet wins.
5. **Valuation** — P/E, EV/EBITDA, PEG ratio (if available). Cheaper relative to quality wins.
6. **Moat / Competitive Advantage** — Switching costs, network effects, brand, scale, IP. Wider and more durable wins.
7. **Revenue Quality** — Recurring vs one-time, subscription vs transactional, contract length. More predictable wins.
8. **Management Quality** — Track record, capital allocation history, insider ownership, alignment. Better stewards win.
9. **Capital Allocation** — Buybacks, dividends, M&A track record, reinvestment returns. Higher ROIC wins.
10. **Innovation / R&D** — R&D spend, R&D efficiency, product pipeline, patent portfolio. More innovative wins.
11. **Geographic Diversification** — Revenue by region, international exposure. More diversified wins (unless concentration is a strength).
12. **Customer Concentration** — Top customer %, revenue diversification. Less concentrated wins.
13. **Regulatory Risk** — Antitrust exposure, data privacy, sector regulation. Lower risk profile wins.
14. **ESG / Governance** — Board independence, executive comp alignment, environmental track record. Better governance wins.
15. **Risk-Adjusted Return Potential** — Upside vs downside, margin of safety, asymmetry. Better risk/reward wins.

## Step 3: Create Comparison File

Create the `research/comparisons/` directory if it doesn't exist.

Write `research/comparisons/{T1}-vs-{T2}.md`:

```markdown
# {T1} vs {T2} — Comparative Analysis

*Generated: {YYYY-MM-DD}*

## Company Profiles

| | {T1} | {T2} |
|---|---|---|
| **Company** | {Full name} | {Full name} |
| **Sector** | {Sector} | {Sector} |
| **Revenue** | ${X}B | ${X}B |
| **Market Cap** | {if available} | {if available} |
| **Thesis** | {1-line from overview} | {1-line from overview} |

## Dimension Scorecard

| # | Dimension | {T1} | {T2} | Winner |
|---|-----------|------|------|--------|
| 1 | Revenue Scale & Growth | [brief] | [brief] | {T1}/{T2}/Tie |
| 2 | Profitability | [brief] | [brief] | {T1}/{T2}/Tie |
| ... | ... | ... | ... | ... |
| 15 | Risk-Adjusted Return | [brief] | [brief] | {T1}/{T2}/Tie |

**Score: {T1} {X} — {T2} {Y} (Ties: {Z})**

## Detailed Analysis

### 1. Revenue Scale & Growth
[2-3 paragraphs with data]

### 2. Profitability
[2-3 paragraphs with data]

[... continue for all 15 dimensions ...]

## Key Financial Comparison

| Metric | {T1} | {T2} |
|--------|------|------|
| Revenue | $X.XB | $X.XB |
| Revenue Growth | X.X% | X.X% |
| Gross Margin | X.X% | X.X% |
| Operating Margin | X.X% | X.X% |
| Net Margin | X.X% | X.X% |
| FCF Margin | X.X% | X.X% |
| Debt/Equity | X.Xx | X.Xx |
| ROE | X.X% | X.X% |
| P/E | X.Xx | X.Xx |

## Bottom Line

### If You Can Only Own One
[Clear recommendation with rationale — which company is the better investment and why]

### When {T1} Wins
[Scenarios or investor profiles where {T1} is the better pick]

### When {T2} Wins
[Scenarios or investor profiles where {T2} is the better pick]

### Portfolio Consideration
[Could you own both? Are they correlated? Do they serve different portfolio roles?]
```

## Step 4: Summary

Print a summary:
```
Comparison complete: {T1} vs {T2}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Scorecard: {T1} {X} — {T2} {Y} (Ties: {Z})
Winner: {T1/T2} by {margin}

Created: research/comparisons/{T1}-vs-{T2}.md

Key differentiator: [One sentence on the biggest gap between the two]
```
