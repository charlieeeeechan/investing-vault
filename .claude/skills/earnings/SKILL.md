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

## Step 4: Update Financials

Append the new quarter's data to the relevant financials files:
- Add a note at the top of `financials/income-statement.md` referencing the latest quarter
- If the quarter is Q4 (full year), update the annual data row

## Step 5: Thesis Drift Check

Compare the earnings against the thesis in `overview.md`:
- Read the "Bull Case" and "Bear Case" sections
- Check if any bull case items were validated or invalidated
- Check if any bear case risks materialized
- If there is meaningful drift, add a note to the bottom of `overview.md`:

```markdown
---
### Thesis Update Log
- **{YYYY}-Q{X}:** [Brief note on thesis impact]
```

## Step 6: Summary

Print a summary:
```
Earnings analysis complete for {TICKER} — {YYYY} Q{X}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Revenue: $X.XB (YoY: +X.X%)
EPS:     $X.XX (YoY: +X.X%)
Thesis:  ✅ On Track / ⚠️ Monitor / 🔴 Review

Created: research/{TICKER}/earnings/{YYYY}-Q{X}.md
Updated: research/{TICKER}/financials/ (quarterly note)

Next steps:
  - Review the earnings analysis
  - Check thesis drift assessment
  - Run /bear-case {TICKER} if concerns emerged
```
