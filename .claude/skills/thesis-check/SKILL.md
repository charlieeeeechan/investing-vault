---
description: "Check if an investment thesis still holds against latest data"
argument: "[TICKER] — Stock ticker symbol"
---

# Thesis Check Skill

Validate a stored investment thesis against the latest available financial data. Surfaces thesis drift, tripwire triggers, and key metric changes so the user can decide whether to hold, monitor, or review a position.

## Prerequisites

1. Normalize the ticker to uppercase.
2. Check if `research/{TICKER}/overview.md` exists.
   - If it does NOT exist, tell the user: "No existing research found for {TICKER}. Run `/research {TICKER}` first to build a thesis before checking it."
   - Stop execution.
3. Read `research/{TICKER}/overview.md` — extract:
   - **Investment Thesis** section
   - **Bull Case** points
   - **Bear Case** points
   - **Key Metrics to Watch** section
4. If a `## Bear Case Deep Dive` section exists in `overview.md`, also extract:
   - **What Would Prove The Bears Right** (tripwires)
   - **Financial Red Flags**
5. Read the most recent earnings file in `research/{TICKER}/earnings/` if any exist (for last-known quarterly data).
6. Read `research/{TICKER}/financials/metrics.md` and `research/{TICKER}/financials/income.md` for historical context.
7. Read `research/{TICKER}/valuation.md` if it exists, for valuation context.

**EDGAR Data Fetching:** See `research/_EDGAR-HELPERS.md` for the standard CIK lookup and XBRL fetch pattern used in Step 1.

## Step 1: Fetch Latest Financial Data

Fetch the most recent quarterly and annual data from SEC EDGAR:

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
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
resp = requests.get(url, headers=headers)
facts = resp.json()
facts_gaap = facts["facts"]["us-gaap"]
```

Extract the most recent quarterly AND annual data for key thesis-relevant metrics:

**Revenue & Growth:**
- Revenue (latest quarter + YoY change)
- Revenue (latest annual + 3-year CAGR)

**Profitability:**
- Gross margin (latest quarter + trend)
- Operating margin (latest quarter + trend)
- Net income (latest quarter + YoY change)

**Cash Flow Quality:**
- Operating cash flow (latest annual)
- Free cash flow (latest annual)
- FCF-to-net-income ratio

**Balance Sheet:**
- Cash and equivalents
- Long-term debt
- Net debt position

**Per-share:**
- EPS diluted (latest quarter + YoY)
- Shares outstanding (for buyback pace)

Use the same `get_annual_data` and `get_quarterly_data` helper functions as in the `/research` and `/earnings` skills.

## Step 2: Build Thesis Scorecard

For each item in the stored thesis, map it to observable data and assess:

### 2a. Key Metrics Check

Take each item from `## Key Metrics to Watch` in `overview.md` and check it against the latest data:

| Metric | Thesis Expectation | Latest Data | Status |
|--------|-------------------|-------------|--------|
| [metric name] | [what the thesis assumed] | [actual current value + trend] | On Track / Monitor / Drifting |

### 2b. Bull Case Validation

For each bull case point, assess whether recent data supports or undermines it:

| Bull Case Point | Evidence For | Evidence Against | Status |
|-----------------|-------------|-----------------|--------|
| [point] | [supporting data] | [contradicting data] | Supported / Weakening / Invalidated |

### 2c. Bear Case / Tripwire Check

If bear case tripwires exist (from `## Bear Case Deep Dive > What Would Prove The Bears Right`), check each one:

| Tripwire | Threshold | Current Value | Triggered? |
|----------|-----------|---------------|-----------|
| [tripwire description] | [threshold from bear case] | [actual current data] | No / Watch / YES |

If no tripwires exist, check the general bear case points against recent data and note any that have materialized or are materializing.

### 2d. Financial Health Quick Check

Compare current vs historical:
- Revenue growth trajectory (accelerating / stable / decelerating)
- Margin trend (expanding / stable / compressing)
- FCF quality (improving / stable / deteriorating)
- Balance sheet trajectory (strengthening / stable / weakening)

## Step 3: Determine Thesis Status

Based on the scorecard, assign an overall thesis status:

- **On Track** — Core thesis intact. Key metrics tracking as expected. No tripwires triggered. Bull case points still supported.
- **Monitor** — Thesis holds but warning signs exist. One or more key metrics showing early drift. One or more bear case risks starting to materialize. Recommend checking again next quarter.
- **Drifting** — Thesis is weakening. Multiple key metrics diverging from expectations. One or more tripwires at risk of triggering. Bull case points losing support. Consider whether the original thesis needs revision.
- **Broken** — Original thesis no longer valid. Multiple tripwires triggered. Fundamental change in business trajectory. Thesis rewrite or position exit warranted.

Be honest and calibrated. Don't default to "On Track" — if the data is genuinely mixed, say "Monitor." The goal is to protect against thesis drift, not confirm priors.

## Step 4: Write Thesis Check File

Create `research/{TICKER}/thesis-checks/{YYYY-MM-DD}.md`:

```markdown
# {TICKER} — Thesis Check

*Date: {YYYY-MM-DD}*
*Data source: SEC EDGAR (latest available quarterly + annual)*
*Last research update: [date from overview.md]*

---

## Thesis Status: [emoji] [STATUS]

**One-line summary:** [One sentence — is the thesis holding, weakening, or broken?]

---

## Key Metrics Scorecard

| Metric | Thesis Expectation | Latest Data | Trend | Status |
|--------|-------------------|-------------|-------|--------|
| [metric] | [expected] | [actual] | [direction] | [emoji + status] |

## Bull Case Check

| Point | Status | Evidence |
|-------|--------|----------|
| [bull point] | Supported / Weakening / Invalidated | [brief data point] |

## Bear Case / Tripwire Check

| Risk / Tripwire | Threshold | Current | Triggered? |
|-----------------|-----------|---------|-----------|
| [risk] | [threshold] | [actual] | [No / Watch / YES] |

## Financial Health

| Dimension | Direction | Detail |
|-----------|-----------|--------|
| Revenue growth | Accelerating / Stable / Decelerating | [data] |
| Margins | Expanding / Stable / Compressing | [data] |
| FCF quality | Improving / Stable / Deteriorating | [data] |
| Balance sheet | Strengthening / Stable / Weakening | [data] |

## Changes Since Last Review

[Note any material changes since the last thesis check or earnings analysis. If this is the first check, compare against the original research date.]

## Recommended Action

- **None** — thesis on track, no changes needed
- **Update thesis** — thesis holds but key assumptions need refreshing
- **Deepen research** — run `/earnings` or `/stress-test` for updated analysis
- **Review position** — thesis weakening, consider trimming or setting a stop
- **Exit review** — thesis broken, evaluate whether to exit

---

*Next check recommended: [date — typically next quarter or next earnings]*
```

## Step 5: Update Overview (If Drift Detected)

If the thesis status is **Monitor**, **Drifting**, or **Broken**, append a note to the `### Thesis Update Log` section in `overview.md`:

```markdown
- **{YYYY-MM-DD} (thesis-check):** Status: [status]. [One sentence explaining the key finding.]
```

If the `### Thesis Update Log` section doesn't exist yet, create it at the bottom of `overview.md` (before any Bear Case Deep Dive section).

## Step 6: Summary

Print a summary:
```
Thesis check complete for {TICKER}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Thesis Status: [emoji] [STATUS]

Key Metrics:  {N} on track / {N} monitor / {N} drifting
Bull Case:    {N} supported / {N} weakening / {N} invalidated
Tripwires:    {N} clear / {N} watch / {N} triggered

One-line: [summary sentence]

Created: research/{TICKER}/thesis-checks/{YYYY-MM-DD}.md
[Updated: research/{TICKER}/overview.md (thesis update log) — if drift detected]

Next steps:
  - [Context-specific recommendation]
  - Next check recommended: [date]
```
