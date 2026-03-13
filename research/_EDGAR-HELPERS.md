# EDGAR Helpers — Shared Fetch Patterns

Shared reference for SEC EDGAR data fetching used across investing-vault skills. All code uses the SEC XBRL API with structured JSON responses — no HTML scraping.

---

## CIK Lookup

Map a stock ticker to its SEC Central Index Key (CIK).

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

If the ticker is not found, stop and notify the user.

---

## XBRL Company Facts Fetch

Retrieve all reported financial data for a company.

```python
url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
resp = requests.get(url, headers=headers)
facts = resp.json()
facts_gaap = facts["facts"]["us-gaap"]
```

Data lives under `facts["facts"]["us-gaap"]`. Each field contains `units` (keyed by `"USD"`, `"USD/shares"`, `"shares"`, etc.), and each unit contains an array of filing entries with `val`, `end`, `fy`, `fp`, and `form`.

---

## Helper Functions

### `get_annual_data()`

Extract the most recent N years of annual (10-K) data for a given XBRL field.

```python
def get_annual_data(facts_gaap, field_name, n_years=5):
    """Extract the most recent n_years of annual (10-K) data for a field."""
    if field_name not in facts_gaap:
        return []
    units = facts_gaap[field_name]["units"]
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

### `get_quarterly_data()`

Extract quarterly filing entries, sorted by end date descending.

```python
def get_quarterly_data(facts_gaap, field_name):
    """Extract quarterly (10-Q and 10-K) data for a field, most recent first."""
    if field_name not in facts_gaap:
        return []
    units = facts_gaap[field_name]["units"]
    unit_key = list(units.keys())[0]
    entries = units[unit_key]
    quarterly = [e for e in entries if e.get("form") in ("10-Q", "10-K")]
    quarterly.sort(key=lambda x: x["end"], reverse=True)
    return quarterly
```

### Entry structure

Each entry returned by these functions is a dict:

| Key    | Description                          | Example          |
|--------|--------------------------------------|------------------|
| `val`  | Reported value (raw units)           | `323900000000`   |
| `end`  | Period end date                      | `"2024-06-30"`   |
| `fy`   | Fiscal year                          | `2024`           |
| `fp`   | Fiscal period (`FY`, `Q1`, `Q2`...)  | `"FY"`           |
| `form` | Filing type                          | `"10-K"`         |

---

## Common GAAP Fields Reference

Field names vary by company. Try each variant in order; use the first that returns data.

### Income Statement

| Metric           | XBRL Field(s)                                                                         |
|------------------|---------------------------------------------------------------------------------------|
| Revenue          | `Revenues`, `RevenueFromContractWithCustomerExcludingAssessedTax`, `SalesRevenueNet`  |
| Net Income       | `NetIncomeLoss`                                                                       |
| EPS (Diluted)    | `EarningsPerShareDiluted`                                                             |
| Operating Income | `OperatingIncomeLoss`                                                                 |
| Gross Profit     | `GrossProfit`                                                                         |
| R&D Expense      | `ResearchAndDevelopmentExpense`                                                       |
| D&A              | `DepreciationDepletionAndAmortization`, `DepreciationAndAmortization`                 |

### Balance Sheet

| Metric               | XBRL Field(s)                                                                         |
|----------------------|---------------------------------------------------------------------------------------|
| Total Assets         | `Assets`                                                                              |
| Total Liabilities    | `Liabilities`                                                                         |
| Stockholders' Equity | `StockholdersEquity`                                                                  |
| Cash & Equivalents   | `CashAndCashEquivalentsAtCarryingValue`                                               |
| Long-term Debt       | `LongTermDebt`, `LongTermDebtNoncurrent`                                              |
| Shares Outstanding   | `CommonStockSharesOutstanding`, `WeightedAverageNumberOfDilutedSharesOutstanding`     |

### Cash Flow Statement

| Metric              | XBRL Field(s)                                        |
|---------------------|------------------------------------------------------|
| Operating Cash Flow | `NetCashProvidedByOperatingActivities`                |
| Capital Expenditure | `PaymentsToAcquirePropertyPlantAndEquipment`          |
| Free Cash Flow      | *Computed:* Operating CF minus CapEx                  |

---

## Usage

This pattern is used by `/research`, `/earnings`, and `/thesis-check` skills. See those skills for context-specific extraction logic.
