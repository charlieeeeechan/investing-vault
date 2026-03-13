---
description: "Analyze latest quarterly earnings"
argument: "[TICKER] — Stock ticker symbol"
---

# Earnings Skill

Fetch and analyze the latest quarterly earnings for the given ticker, update the research folder.

## Prerequisites

1. Normalize the ticker to uppercase.
2. Check if `research/{TICKER}/overview.md` exists.
   - If it does NOT exist, tell the user: "No existing research found for {TICKER}. Run `/research {TICKER}` first to create the base research folder."
   - Stop execution.
3. Read `research/{TICKER}/overview.md` to understand the current thesis.
4. Read `research/_SCHEMA.md` for formatting conventions.

**EDGAR Data Fetching:** See `research/_EDGAR-HELPERS.md` for the standard CIK lookup and XBRL fetch pattern used in Steps 1-2.

## Step 1: Fetch Company CIK

```python
import requests

headers = {"User-Agent": "InvestingVault research@example.com"}
resp = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
tickers = resp.json()

cik = None
company_name = None
for entry in tickers.values():
    if entry["ticker"].upper() == ticker.upper():
        cik = entry["cik_str"]
        company_name = entry["title"]
        break

cik_padded = str(cik).zfill(10)
```

## Step 2: Fetch Latest Quarterly Data

Fetch XBRL company facts:

```python
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
resp = requests.get(url, headers=headers)
facts = resp.json()
```

Extract the most recent quarterly data points. Filter for `form: "10-Q"` entries (or `form: "10-K"` for Q4 which is often reported in the 10-K).

Key fields to extract for quarterly analysis:
- Revenue (look for `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, or `SalesRevenueNet`)
- Net Income (`NetIncomeLoss`)
- EPS (`EarningsPerShareDiluted`)
- Operating Income (`OperatingIncomeLoss`)
- Gross Profit (`GrossProfit`)
- Operating Cash Flow (`NetCashProvidedByOperatingActivities`)

For each field, get the most recent quarterly entry and the year-ago quarter for comparison:

```python
def get_quarterly_data(facts_gaap, field_name):
    if field_name not in facts_gaap:
        return []
    units = facts_gaap[field_name]["units"]
    unit_key = list(units.keys())[0]
    entries = units[unit_key]
    quarterly = [e for e in entries if e.get("form") in ("10-Q", "10-K")]
    # Sort by end date descending
    quarterly.sort(key=lambda x: x["end"], reverse=True)
    return quarterly
```

Determine the fiscal quarter (Q1, Q2, Q3, Q4) and fiscal year from the most recent entry's `fp` and `fy` fields.

## Step 3: Create Earnings File

Create `research/{TICKER}/earnings/{YYYY}-Q{X}.md` with this structure:

```markdown
# {TICKER} — {YYYY} Q{X} Earnings Analysis

**Report Date:** {date of filing}
**Period Ending:** {end date}
**Source:** SEC EDGAR (10-Q / 10-K)

## Key Metrics

| Metric | Q{X} {YYYY} | Q{X} {YYYY-1} | YoY Change |
|--------|-------------|----------------|------------|
| Revenue | $X.XB | $X.XB | +X.X% |
| Net Income | $X.XB | $X.XB | +X.X% |
| EPS (Diluted) | $X.XX | $X.XX | +X.X% |
| Operating Income | $X.XB | $X.XB | +X.X% |
| Gross Margin | XX.X% | XX.X% | +X.Xpp |
| Operating Margin | XX.X% | XX.X% | +X.Xpp |

## Segment Breakdown

(Fill in if segment data is available from EDGAR, otherwise note "Segment data not available from XBRL — check earnings press release")

## Analysis

### vs Expectations
- Revenue: [above/below/in-line] — commentary
- EPS: [above/below/in-line] — commentary
- Margins: [expanding/contracting/stable] — commentary

### Notable Items
- List any unusual or one-time items
- Guidance changes if mentioned in filing
- Key operational metrics

## Thesis Check

Read the current thesis from `overview.md` and assess:
- **Thesis Status:** ✅ On Track / ⚠️ Monitor / 🔴 Review
- **Key Observation:** One sentence on whether this quarter supports or challenges the thesis
- **Action:** None / Update thesis / Reassess position
```

## Step 4: Update Financials (Incremental)

This step ADDS the new quarter's data to existing financials tables. **Do not overwrite existing data — append new columns/rows.**

### 4a. Income Statement (`financials/income.md`)

1. Read the existing `research/{TICKER}/financials/income.md`.
2. Add a new quarterly column to the table with the following fields from EDGAR XBRL data:
   - Revenue
   - Cost of Revenue / COGS
   - Gross Profit
   - Operating Income
   - Net Income
   - EPS (Diluted)
3. Insert the new column in chronological order (most recent quarter on the right).
4. If the quarter is Q4 (10-K filing), also add or update the full-year annual row/column with the 10-K annual totals.

### 4b. Balance Sheet (`financials/balance.md`)

1. Read the existing `research/{TICKER}/financials/balance.md`.
2. Add a new quarterly column with the latest balance sheet snapshot:
   - Total Assets
   - Total Liabilities
   - Total Stockholders' Equity
   - Cash & Cash Equivalents (+ Short-Term Investments if available)
   - Total Debt (Short-Term + Long-Term)
3. Preserve all prior quarter columns — this is a point-in-time snapshot, so each quarter's data stands on its own.

### 4c. Cash Flow Statement (`financials/cashflow.md`)

1. Read the existing `research/{TICKER}/financials/cashflow.md`.
2. Add a new quarterly column with:
   - Operating Cash Flow (`NetCashProvidedByOperatingActivities`)
   - Capital Expenditures (`PaymentsToAcquirePropertyPlantAndEquipment` or similar)
   - Free Cash Flow (Operating CF minus CapEx)
3. If Q4 (10-K), also add the full-year annual totals.

### 4d. Key Metrics (`financials/metrics.md`)

1. Read the existing `research/{TICKER}/financials/metrics.md`.
2. Update or append a new row/column with the latest quarter's derived metrics:
   - Gross Margin (%)
   - Operating Margin (%)
   - Net Margin (%)
   - Revenue Growth (YoY %)
   - EPS Growth (YoY %)
   - FCF per Share
   - Return on Equity (if calculable from balance sheet data)
3. Keep all historical metric values intact.

### Important Notes
- If any financials file does not yet exist, create it with the current quarter as the first column, following the format in `research/_SCHEMA.md`.
- Always cite the source filing (10-Q or 10-K) and period end date in the table header.
- Numbers should use consistent formatting: `$X.XB` for billions, `$X.XM` for millions, percentages to one decimal.

## Step 5: Summary

Print a summary:
```
Earnings analysis complete for {TICKER} — {YYYY} Q{X}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Revenue: $X.XB (YoY: +X.X%)
EPS:     $X.XX (YoY: +X.X%)

Created: research/{TICKER}/earnings/{YYYY}-Q{X}.md
Updated: research/{TICKER}/financials/ (income, balance, cashflow, metrics)

Next steps:
  - Review the earnings analysis
  - Run /thesis-check {TICKER} to validate your thesis against this new data
  - Run /stress-test {TICKER} if concerns emerged
```
