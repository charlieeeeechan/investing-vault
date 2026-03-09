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
- D&A: `DepreciationDepletionAndAmortization` or `DepreciationAndAmortization`

**Balance Sheet:**
- Total Assets: `Assets`
- Total Liabilities: `Liabilities`
- Stockholders Equity: `StockholdersEquity`
- Cash: `CashAndCashEquivalentsAtCarryingValue`
- Long-term Debt: `LongTermDebt` or `LongTermDebtNoncurrent`
- Diluted Shares: `CommonStockSharesOutstanding` or `WeightedAverageNumberOfDilutedSharesOutstanding`

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

After extracting EDGAR data, compute these derived values for use in the DCF later:

```python
# Latest fiscal year values (in $M — divide raw values by 1,000,000)
revenue_data = get_annual_data(facts_gaap, "Revenues") or get_annual_data(facts_gaap, "RevenueFromContractWithCustomerExcludingAssessedTax") or get_annual_data(facts_gaap, "SalesRevenueNet")
opincome_data = get_annual_data(facts_gaap, "OperatingIncomeLoss")
cash_data = get_annual_data(facts_gaap, "CashAndCashEquivalentsAtCarryingValue")
ltd_data = get_annual_data(facts_gaap, "LongTermDebt") or get_annual_data(facts_gaap, "LongTermDebtNoncurrent")
capex_data = get_annual_data(facts_gaap, "PaymentsToAcquirePropertyPlantAndEquipment")
da_data = get_annual_data(facts_gaap, "DepreciationDepletionAndAmortization") or get_annual_data(facts_gaap, "DepreciationAndAmortization")
shares_data = get_annual_data(facts_gaap, "WeightedAverageNumberOfDilutedSharesOutstanding") or get_annual_data(facts_gaap, "CommonStockSharesOutstanding")
eps_data = get_annual_data(facts_gaap, "EarningsPerShareDiluted")

# Base revenue (most recent FY, in $M)
base_revenue_m = revenue_data[-1]["val"] / 1e6 if revenue_data else None

# Net debt (in $M): positive = net debt, negative = net cash
latest_cash = cash_data[-1]["val"] / 1e6 if cash_data else 0
latest_ltd = ltd_data[-1]["val"] / 1e6 if ltd_data else 0
net_debt_m = latest_ltd - latest_cash

# Shares outstanding (in millions)
shares_m = shares_data[-1]["val"] / 1e6 if shares_data else None
# Note: if shares are already in units (not thousands), skip /1e6 and use /1e6 only if val > 1e8

# Average D&A % of revenue (last 3 years, fallback to 4% if not available)
if da_data and revenue_data and len(da_data) >= 1:
    da_pcts = [da_data[i]["val"] / revenue_data[i]["val"] for i in range(min(3, len(da_data), len(revenue_data)))]
    da_pct = sum(da_pcts) / len(da_pcts)
else:
    da_pct = 0.04  # fallback

# Average Capex % of revenue (last 3 years, fallback to 5% if not available)
if capex_data and revenue_data and len(capex_data) >= 1:
    capex_pcts = [capex_data[i]["val"] / revenue_data[i]["val"] for i in range(min(3, len(capex_data), len(revenue_data)))]
    capex_pct = sum(capex_pcts) / len(capex_pcts)
else:
    capex_pct = 0.05  # fallback

# Latest EBIT margin
latest_ebit_margin = opincome_data[-1]["val"] / revenue_data[-1]["val"] if opincome_data and revenue_data else None

# EPS diluted (latest)
latest_eps = eps_data[-1]["val"] if eps_data else None
```

## Stage 2b: Fetch Market Data from Yahoo Finance

After fetching EDGAR data, attempt to pull live market data from Yahoo Finance. This gives current price, market cap, and EV — which EDGAR does not provide.

```python
import datetime

yf_fetch_date = datetime.date.today().isoformat()
market = {
    "price": None,
    "market_cap_m": None,
    "ev_m": None,
    "yf_available": False,
}

try:
    import yfinance as yf
    yf_obj = yf.Ticker(ticker)

    # Try fast_info first (lighter endpoint, less rate-limited)
    try:
        fi = yf_obj.fast_info
        price = fi.last_price
        mkt_cap_raw = fi.market_cap
        # fast_info doesn't include EV — fall through to info for that
        ev_raw = None
        try:
            info = yf_obj.info
            ev_raw = info.get("enterpriseValue")
            # If fast_info price failed, try info as backup
            if not price:
                price = info.get("currentPrice") or info.get("regularMarketPrice")
            if not mkt_cap_raw:
                mkt_cap_raw = info.get("marketCap")
        except Exception:
            pass  # EV unavailable — ok, proceed without it
    except Exception:
        # fast_info failed — fall back to info only
        info = yf_obj.info
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        mkt_cap_raw = info.get("marketCap")
        ev_raw = info.get("enterpriseValue")

    market["price"] = price
    market["market_cap_m"] = round(mkt_cap_raw / 1e6) if mkt_cap_raw else None
    market["ev_m"] = round(ev_raw / 1e6) if ev_raw else None
    market["yf_available"] = True
except Exception:
    market["yf_available"] = False
```

If `yfinance` is not installed, note it and continue — all market data fields will display "N/A (install yfinance)".

Compute trailing multiples from market data + EDGAR fundamentals:
```python
def fmt_multiple(numerator, denominator, suffix="x"):
    if numerator and denominator and denominator != 0:
        return f"{numerator / denominator:.1f}{suffix}"
    return "—"

# Price-based
trailing_pe = fmt_multiple(market["price"], latest_eps) if latest_eps and latest_eps > 0 else "—"

# EV-based (use $M values throughout)
latest_revenue_m = revenue_data[-1]["val"] / 1e6 if revenue_data else None
latest_opincome_m = opincome_data[-1]["val"] / 1e6 if opincome_data else None
cfo_data = get_annual_data(facts_gaap, "NetCashProvidedByOperatingActivities")
latest_cfo_m = cfo_data[-1]["val"] / 1e6 if cfo_data else None

ev_revenue = fmt_multiple(market["ev_m"], latest_revenue_m)
ev_ebit = fmt_multiple(market["ev_m"], latest_opincome_m)
price_cfo = fmt_multiple(market["price"] * shares_m if market["price"] and shares_m else None, latest_cfo_m)
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

**This file must contain actual computed numbers, not instructions to fill in later.**

#### Part 1: Market Data

Write the market data table using values fetched from Yahoo Finance. Format:

```markdown
# {TICKER} — Valuation

*Fundamentals: SEC EDGAR 10-K filings. Market data: Yahoo Finance ({yf_fetch_date}).*
*Last updated: {today}*

---

## Current Market Data

| Metric                       | Value               | Source              |
| ---------------------------- | ------------------- | ------------------- |
| Stock Price                  | ${price}            | Yahoo Finance       |
| Shares Outstanding (diluted) | ~{shares_m:.0f}M    | SEC EDGAR FY{year}  |
| Market Cap                   | ${market_cap_m:,}M  | Yahoo Finance       |
| Enterprise Value             | ${ev_m:,}M          | Yahoo Finance       |
| Net Debt (LTD − Cash)        | ${net_debt_m:,}M    | SEC EDGAR FY{year}  |
```

If Yahoo Finance was unavailable, show "N/A — install yfinance or fill in manually" and note the installation command: `pip install yfinance`.

#### Part 2: Trailing Multiples

Populate using EDGAR fundamentals + Yahoo Finance EV/price. If any value is unavailable, show "—".

```markdown
## Trailing Multiples

*Price and EV from Yahoo Finance ({yf_fetch_date}). Fundamentals from SEC EDGAR.*

| Metric            | FY{year} Value | Multiple         |
| ----------------- | -------------: | ---------------: |
| Revenue           | ${revenue_m:,}M | {ev_revenue} EV/Rev |
| Operating Income  | ${opincome_m:,}M | {ev_ebit} EV/EBIT |
| Net Income (GAAP) | ${net_income_m:,}M | {trailing_pe} P/E |
| EPS Diluted       | ${latest_eps:.2f} | {trailing_pe} P/E |
| CFO               | ${cfo_m:,}M    | {price_cfo} P/CFO |
```

#### Part 3: DCF Analysis — Run and Embed Results

**Execute the DCF calculator with EDGAR-derived inputs for all three scenarios. Do not leave this as "run the script yourself" — compute the numbers and write them into the file.**

```python
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "tools"))
from dcf_calculator import UnleveredDCF

# Determine scenario growth rates based on company's historical CAGR and sector
# Use the last 3-year revenue CAGR as the anchor for base case
# Bull case = base + ~4pp in early years; Bear case = base - ~4pp
# Steady-state margins should reflect the company's trajectory and sector norms
# WACC: use 10% base, 9% bull, 11% bear as defaults — adjust for company risk profile
# Terminal growth: 3.5% base (reasonable long-run GDP+inflation assumption)
# Exit multiple: use a multiple appropriate for the sector (tech: 20-25x EBITDA; retail: 10-15x)

# Example for a high-growth tech company — adjust parameters to match the specific company:
scenarios = {
    "base": dict(
        revenue_growth=[g_base_yr1, g_base_yr1, g_base_yr2, g_base_yr2, g_base_yr3],
        ebit_margin=[m_base_yr1, m_base_yr2, m_base_yr3, m_base_yr4, m_base_yr5],
        wacc=0.10,
        terminal_growth=0.035,
        exit_multiple=20,
        tax_rate=0.21,
    ),
    "bull": dict(
        revenue_growth=[g_bull_yr1, g_bull_yr1, g_bull_yr2, g_bull_yr2, g_bull_yr3],
        ebit_margin=[m_bull_yr1, m_bull_yr2, m_bull_yr3, m_bull_yr4, m_bull_yr5],
        wacc=0.09,
        terminal_growth=0.040,
        exit_multiple=25,
        tax_rate=0.20,
    ),
    "bear": dict(
        revenue_growth=[g_bear_yr1, g_bear_yr1, g_bear_yr2, g_bear_yr2, g_bear_yr3],
        ebit_margin=[m_bear_yr1, m_bear_yr2, m_bear_yr3, m_bear_yr4, m_bear_yr5],
        wacc=0.11,
        terminal_growth=0.025,
        exit_multiple=15,
        tax_rate=0.22,
    ),
}

results = {}
for name, params in scenarios.items():
    dcf = UnleveredDCF(
        base_revenue=base_revenue_m,
        net_debt=net_debt_m,
        shares_outstanding=shares_m,
        da_pct=da_pct,
        capex_pct=capex_pct,
        nwc_pct=0.01,
        **params,
    )
    results[name] = dcf.calculate()
```

Set the growth rates and margins using **real judgment based on the company's historical data and sector**:
- Derive base growth rate from the 3-year revenue CAGR computed from EDGAR data
- Set EBIT margins as a progression from current observed margin toward a reasonable steady-state
- Do not use placeholder variable names like `g_base_yr1` — replace them with actual numbers

Write the results into the file in this format:

```markdown
## DCF Analysis

*Computed using EDGAR fundamentals. All values in $M unless noted.*
*Inputs: base revenue ${base_revenue_m:,.0f}M (FY{year}), net debt ${net_debt_m:,.0f}M, {shares_m:.0f}M diluted shares*
*D&A: {da_pct:.1%} of revenue | CapEx: {capex_pct:.1%} of revenue (3-year average from EDGAR)*

### Scenario Assumptions

| Parameter                   | Base Case | Bull Case | Bear Case |
| --------------------------- | --------: | --------: | --------: |
| Revenue Growth (Yr 1–3)     |      {x}% |      {x}% |      {x}% |
| Revenue Growth (Yr 4–5)     |      {x}% |      {x}% |      {x}% |
| Terminal Growth Rate        |     {x}%  |     {x}%  |     {x}%  |
| EBIT Margin (steady-state)  |      {x}% |      {x}% |      {x}% |
| WACC                        |      {x}% |      {x}% |      {x}% |
| Tax Rate                    |      {x}% |      {x}% |      {x}% |
| Exit Multiple (EBITDA)      |       {x}x |       {x}x |       {x}x |

### Projected Free Cash Flow ($M)

| Year  | Base FCF | Bull FCF | Bear FCF |
| ----- | -------: | -------: | -------: |
| Yr 1  | {base_result.fcf_by_year[0]:,.0f} | {bull} | {bear} |
| Yr 2  | {base_result.fcf_by_year[1]:,.0f} | ... | ... |
| Yr 3  | ...      | ...      | ...      |
| Yr 4  | ...      | ...      | ...      |
| Yr 5  | ...      | ...      | ...      |
| PV of FCFs | {base_result.sum_pv_fcf:,.0f} | ... | ... |
| Terminal Value (perpetuity) | {base_result.pv_terminal_perpetuity:,.0f} | ... | ... |
| Terminal Value (exit mult.) | {base_result.pv_terminal_exit:,.0f} | ... | ... |

### Implied Intrinsic Value

| Method            |   Base Case |  Bull Case |  Bear Case |
| ----------------- | ----------: | ---------: | ---------: |
| EV (perpetuity)   | ${base_result.enterprise_value_perpetuity:,.0f}M | ... | ... |
| EV (exit mult.)   | ${base_result.enterprise_value_exit:,.0f}M | ... | ... |
| **Price/share (perpetuity)** | **${base_result.intrinsic_price_perpetuity:.2f}** | **$...** | **$...**  |
| **Price/share (exit mult.)** | **${base_result.intrinsic_price_exit_multiple:.2f}** | **$...** | **$...**  |
```

Also embed the base case sensitivity table (WACC vs terminal growth):

```markdown
### Sensitivity: Implied Price — WACC vs Terminal Growth Rate (Base Case, Perpetuity Method)

| WACC \ g  |  1.5% |  2.0% |  2.5% |  3.0% |
| --------- | ----: | ----: | ----: | ----: |
| **7%**    | $...  | $...  | $...  | $...  |
| **8%**    | $...  | $...  | $...  | $...  |
| **9%**    | $...  | $...  | $...  | $...  |
| **10%**   | $...  | $...  | $...  | $...  |
```

Populate every cell from `results["base"].sensitivity_perpetuity["wacc_vs_growth"]`.

#### Part 4: Valuation Notes

Include a brief qualitative section: what makes this company hard or easy to value, key swing factors, and the most important assumption to get right. Keep it to 3–5 bullet points.

Also include a sum-of-parts table if the company has meaningfully distinct segments with different margin profiles (e.g., AWS vs Amazon retail, Azure vs Office vs Gaming). Base the SOTP on actual EDGAR segment data if available.

Close with the standard disclaimer:
```markdown
---
*Fundamentals: SEC EDGAR 10-K filings | Market data: Yahoo Finance ({yf_fetch_date})*
*Not investment advice. Always verify figures before making any investment decision.*
```

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
3. Check that `valuation.md` contains actual DCF output numbers — not "run the script" instructions.
4. If any EDGAR fields were missing, note them clearly in the relevant file with `⚠️ Data not available from EDGAR`.
5. If Yahoo Finance was unavailable, note it in `valuation.md` with the install instruction.

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
Market data: Yahoo Finance as of {yf_fetch_date}
Missing fields: {list any fields not found}

Next steps:
  - Review overview.md and refine the thesis
  - Run /earnings {TICKER} for latest quarterly data
  - Run /bear-case {TICKER} for contrarian analysis
```
