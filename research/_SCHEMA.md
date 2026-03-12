# Financial Data Schema

Standard line items for company financials. All data sources get mapped to these.

When you pull numbers from earnings releases, 10-Qs, 10-Ks, or other filings, use the tables below as your canonical format. This keeps everything consistent across companies and makes comparisons straightforward.

---

## Income Statement

The income statement shows how much a company earned (or lost) over a period. It starts with revenue at the top and works down to net income at the bottom.

| Line Item          | Description               | Notes    |
| ------------------ | ------------------------- | -------- |
| Revenue            | Total revenue / Net sales | Top line |
| Cost of Revenue    | COGS / Cost of services   |          |
| Gross Profit       | Revenue - Cost of Revenue |          |
| Operating Expenses | SG&A, R&D, etc.           |          |
| Operating Income   | Earnings from operations  |          |
| Interest Expense   | Net interest cost         |          |
| Other Income       | Non-operating items       |          |
| Pre-tax Income     | EBT                       |          |
| Income Tax         | Tax expense               |          |
| Net Income         | Bottom line               |          |
| EPS (Basic)        | Earnings per share        |          |
| EPS (Diluted)      | Diluted EPS               |          |
| Shares Outstanding | Weighted average          |          |

## Balance Sheet

The balance sheet is a snapshot of what a company owns (assets), owes (liabilities), and the residual value belonging to shareholders (equity) at a single point in time.

| Line Item                 | Description                | Notes |
| ------------------------- | -------------------------- | ----- |
| Cash & Equivalents        | Liquid assets              |       |
| Short-term Investments    | Marketable securities      |       |
| Accounts Receivable       | Net of allowances          |       |
| Inventory                 | If applicable              |       |
| Total Current Assets      |                            |       |
| PP&E (Net)                | Property, plant, equipment |       |
| Goodwill                  | Acquisition premium        |       |
| Intangibles               | Other intangible assets    |       |
| Total Assets              |                            |       |
| Accounts Payable          |                            |       |
| Short-term Debt           | Current portion            |       |
| Total Current Liabilities |                            |       |
| Long-term Debt            |                            |       |
| Total Liabilities         |                            |       |
| Total Equity              | Shareholders' equity       |       |

## Cash Flow Statement

The cash flow statement tracks actual cash moving in and out of the business. It is split into three sections: operations (running the business), investing (buying/selling assets), and financing (debt and equity transactions).

| Line Item               | Description                 | Notes            |
| ----------------------- | --------------------------- | ---------------- |
| Net Income              | Starting point              |                  |
| D&A                     | Depreciation & Amortization |                  |
| Stock-Based Comp        | Non-cash expense            |                  |
| Working Capital Changes | AR, AP, Inventory           |                  |
| CFO                     | Cash from Operations        |                  |
| CapEx                   | Capital expenditures        | Usually negative |
| Acquisitions            | M&A spend                   |                  |
| CFI                     | Cash from Investing         |                  |
| Debt Issued/Repaid      | Net borrowing               |                  |
| Dividends               | Cash dividends paid         |                  |
| Buybacks                | Share repurchases           |                  |
| CFF                     | Cash from Financing         |                  |
| Net Change in Cash      | CFO + CFI + CFF             |                  |

## Key Metrics (Company-Specific)

Track industry-relevant KPIs. Every industry has its own numbers that matter most. Examples:

- **Healthcare:** Medical Care Ratio (MCR), Days Claims Payable
- **Tech:** ARR, DAU/MAU, Churn
- **Retail:** Same-store sales, Inventory turns
- **Finance:** Net Interest Margin, Loan Loss Provisions

---

## Source Tagging

Every data entry should note where it came from and whether it has been double-checked. This prevents confusion when numbers conflict across sources.

_Source: [Earnings Release|10-Q|10-K|Investor Presentation|etc] YYYY-MM-DD_
_Verified: [pending|yes]_

When reconciling from multiple sources, note discrepancies. For example:

> Revenue per 10-Q: $50.1B. Earnings release stated $50.2B (includes one-time adjustment). Using 10-Q figure as authoritative.

---

## Insights Guidelines

Each company's `insights.md` file captures analytical observations that go beyond raw numbers:

- Key takeaways from earnings calls/reports
- Non-obvious patterns or concerns
- Structural vs one-time issues
- Management credibility notes
- What to watch in future quarters
- Trends across quarters (growth rates, margin expansion/compression)
- Comparisons to guidance and consensus estimates
- Red flags or positive surprises worth monitoring

Format each earnings period as a section with dated insights. Build a running record over time. Keep insights concise and linked to specific data points.

---

## File Structure

```
[TICKER]/
├── overview.md
├── financials/
│   ├── income.md
│   ├── balance.md
│   ├── cashflow.md
│   ├── metrics.md
│   └── insights.md
├── earnings/
│   └── YYYY-QX.md
├── valuation.md
└── news.md
```
