---
description: "Full company research — business, moat, financials, valuation"
argument: "[TICKER] — Stock ticker symbol (e.g., MSFT, GOOG)"
---

# Research Skill

Run a full 6-stage research pipeline for the given ticker and produce a complete research folder.

## Setup

1. Normalize the ticker to uppercase.
2. Set the research directory: `research/{TICKER}/`
3. Read `research/_SCHEMA.md` for financial data formatting conventions.
4. Read `research/_TEMPLATE.md` for the expected folder structure and file templates.

## Stage 1: Company Identification

Look up the company's CIK number from SEC EDGAR.

Use Python `requests` to fetch the ticker-to-CIK mapping:

```python
import requests, json

headers = {"User-Agent": "InvestingVault research@example.com"}
resp = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
tickers = resp.json()

# Find the CIK for our ticker
cik = None
company_name = None
for entry in tickers.values():
    if entry["ticker"].upper() == ticker.upper():
        cik = entry["cik_str"]
        company_name = entry["title"]
        break

# Pad CIK to 10 digits
cik_padded = str(cik).zfill(10)
```

If the ticker is not found, stop and tell the user.

## Stage 2: Fetch Financial Data from SEC EDGAR

Fetch the XBRL company facts:

```python
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
resp = requests.get(url, headers=headers)
facts = resp.json()
```

Extract data from `facts["facts"]["us-gaap"]`. Key fields to look for (try each, some companies use different names):

**Income Statement:**
- Revenue: `Revenues` or `RevenueFromContractWithCustomerExcludingAssessedTax` or `SalesRevenueNet`
- Net Income: `NetIncomeLoss`
- EPS: `EarningsPerShareDiluted`
- Operating Income: `OperatingIncomeLoss`
- Gross Profit: `GrossProfit`
- R&D: `ResearchAndDevelopmentExpense`

**Balance Sheet:**
- Total Assets: `Assets`
- Total Liabilities: `Liabilities`
- Stockholders Equity: `StockholdersEquity`
- Cash: `CashAndCashEquivalentsAtCarryingValue`
- Long-term Debt: `LongTermDebt` or `LongTermDebtNoncurrent`

**Cash Flow:**
- Operating Cash Flow: `NetCashProvidedByOperatingActivities`
- Capex: `PaymentsToAcquirePropertyPlantAndEquipment`
- Free Cash Flow: compute as Operating CF - Capex

For each field, extract annual data (filter for `form: "10-K"`) and get the most recent 5 years. Each data point has `val`, `end` (date), `fy` (fiscal year), `fp` (fiscal period).

```python
def get_annual_data(facts_gaap, field_name, n_years=5):
    """Extract the most recent n_years of annual (10-K) data for a field."""
    if field_name not in facts_gaap:
        return []
    units = facts_gaap[field_name]["units"]
    # Usually "USD" for dollar amounts, "USD/shares" for per-share
    unit_key = list(units.keys())[0]
    entries = units[unit_key]
    annual = [e for e in entries if e.get("form") == "10-K" and e.get("fp") == "FY"]
    # Deduplicate by fiscal year, keep latest filing
    by_fy = {}
    for e in annual:
        fy = e["fy"]
        if fy not in by_fy or e["end"] > by_fy[fy]["end"]:
            by_fy[fy] = e
    sorted_years = sorted(by_fy.keys(), reverse=True)[:n_years]
    return [by_fy[y] for y in sorted(sorted_years)]
```

## Stage 3: Create Folder Structure

Create the following files (matching `_TEMPLATE.md` structure):

```
research/{TICKER}/
  overview.md
  financials/
    income.md
    balance.md
    cashflow.md
    metrics.md
    insights.md
  earnings/
    (empty directory — earnings skill populates this)
  valuation.md
  news.md
```

## Stage 4: Write Files

### `overview.md`
Fill in using data gathered and your knowledge of the company:
- **Company:** Name, ticker, sector, industry, HQ
- **Business Overview:** What they do, segments, revenue breakdown
- **Moat Analysis:** Sources of competitive advantage (network effects, switching costs, brand, scale, IP)
- **Bull Case:** 3-5 reasons to be optimistic
- **Bear Case:** 3-5 reasons to be cautious
- **Thesis:** One-paragraph investment thesis
- **Key Metrics to Watch:** What would change the thesis

### `financials/income.md`
Format the income statement data from EDGAR as a markdown table. Include columns for each fiscal year. Follow `_SCHEMA.md` formatting (dollar amounts in millions, growth rates as percentages).

### `financials/balance.md`
Format balance sheet data similarly. Include total assets, liabilities, equity, cash, debt.

### `financials/cashflow.md`
Format cash flow data. Include operating CF, capex, free cash flow, FCF margin.

### `financials/metrics.md`
Key financial ratios and KPIs: margins, growth rates, returns on capital, per-share data.

### `financials/insights.md`
Analytical observations: key takeaways, strengths, concerns, questions to watch.

### `valuation.md`
Include:
- Current market data note (tell user to fill in current price/market cap since we cannot fetch live prices)
- DCF assumptions table (revenue growth, margins, WACC, terminal growth)
- Reference to `tools/dcf_calculator.py` for running the model
- Relative valuation notes (P/E, EV/EBITDA ranges)
- Fair value estimate range

### `news.md`
Create as an empty log with header and template entry:
```markdown
# {TICKER} News & Updates

<!-- Add entries in reverse chronological order -->

## YYYY-MM-DD — [Headline]
- **Source:** [link]
- **Impact:** [thesis impact assessment]
- **Action:** None / Monitor / Review thesis
```

## Stage 5: Validation

After writing all files:
1. Verify each file was created and is non-empty.
2. Check that financial tables have actual numbers (not placeholders).
3. If any EDGAR fields were missing, note them clearly in the relevant file with `⚠️ Data not available from EDGAR`.

## Stage 6: Summary

Print a summary:
```
Research complete for {TICKER} ({company_name})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Created:
  ✓ research/{TICKER}/overview.md
  ✓ research/{TICKER}/financials/income.md
  ✓ research/{TICKER}/financials/balance.md
  ✓ research/{TICKER}/financials/cashflow.md
  ✓ research/{TICKER}/financials/metrics.md
  ✓ research/{TICKER}/financials/insights.md
  ✓ research/{TICKER}/valuation.md
  ✓ research/{TICKER}/news.md

Data coverage: {X} years of annual financials from SEC EDGAR
Missing fields: {list any fields not found}

Next steps:
  - Review overview.md and refine the thesis
  - Fill in current market price in valuation.md
  - Run /earnings {TICKER} for latest quarterly data
  - Run /bear-case {TICKER} for contrarian analysis
```
