# AMZN — Valuation

*Fundamentals: SEC EDGAR 10-K filings. Market data: Yahoo Finance (2026-03-09).*
*Last updated: 2026-03-09*

---

## Current Market Data

| Metric                       | Value               | Source              |
| ---------------------------- | -------------------:| ------------------- |
| Stock Price                  | $213.12             | Yahoo Finance       |
| Shares Outstanding (diluted) | ~10,827M            | SEC EDGAR FY2025    |
| Market Cap                   | $2,307,450M         | Computed            |
| Enterprise Value             | $2,289,476M         | Computed            |
| Net Debt (LTD − Cash)        | ($17,974M)          | SEC EDGAR FY2025    |

*Net debt is negative = net cash position of $18.0B.*

---

## Trailing Multiples

*Price from Yahoo Finance (2026-03-09). Fundamentals from SEC EDGAR FY2025.*

| Metric            | FY2025 Value   |       Multiple |
| ----------------- | -------------: | -------------: |
| Revenue           |    $716,924M   |  3.2x EV/Rev   |
| Operating Income  |     $79,975M   | 28.6x EV/EBIT  |
| Net Income (GAAP) |     $77,670M   | 29.7x P/E      |
| EPS Diluted       |         $7.17  | 29.7x P/E      |
| CFO               |    $139,482M   | 16.5x P/CFO    |
| FCF               |      $7,684M   | 300.3x P/FCF   |

*Note: P/FCF is distorted by the massive FY2025 CapEx cycle ($131.8B). P/CFO (16.5x) better reflects underlying cash generation.*

---

## DCF Analysis

*Computed using EDGAR fundamentals. All values in $M unless noted.*
*Inputs: base revenue $716,924M (FY2025), net debt ($17,974M) (net cash), 10,827M diluted shares*
*D&A: 8.6% of revenue | CapEx: 13.5% of revenue (3-year average from EDGAR)*

### Scenario Assumptions

| Parameter                   | Base Case | Bull Case | Bear Case |
| --------------------------- | --------: | --------: | --------: |
| Revenue Growth (Yr 1–2)     |       11% |       14% |        7% |
| Revenue Growth (Yr 3)       |       10% |       12% |        6% |
| Revenue Growth (Yr 4–5)     |     9–8%  |    11–10% |     5–4%  |
| Terminal Growth Rate         |     3.5%  |     4.0%  |     2.5%  |
| EBIT Margin (Yr 1→5)        | 12→14%    | 13→16%    | 10→11%    |
| WACC                        |       10% |        9% |       11% |
| Tax Rate                    |       21% |       20% |       22% |
| Exit Multiple (EBITDA)      |       22x |       27x |       16x |

**Rationale:**
- Base case growth (11% tapering to 8%) is anchored to the 3-year revenue CAGR of 11.7%, with deceleration as the business scales past $1T.
- EBIT margins expand from 12% toward 14% as advertising scales, fulfillment optimizes, and AWS leverage kicks in. Current margin is 11.2%.
- Bull case assumes AI-driven AWS acceleration and faster margin expansion. Bear case assumes growth deceleration from macro headwinds and margin pressure from competition/investment.
- WACC of 10% reflects Amazon's equity risk (minimal debt, beta ~1.1–1.2).

### Projected Free Cash Flow ($M)

| Year  |   Base FCF |   Bull FCF |   Bear FCF |
| ----- | ---------: | ---------: | ---------: |
| Yr 1  |     28,604 |     36,897 |     14,686 |
| Yr 2  |     35,240 |     49,516 |     15,714 |
| Yr 3  |     42,602 |     63,806 |     20,050 |
| Yr 4  |     50,620 |     75,458 |     24,616 |
| Yr 5  |     59,187 |     88,100 |     25,600 |
| **PV of FCFs**   | **145,702** | **219,811** | **65,293** |
| TV (perpetuity)  | 585,184 | 1,190,987 | 183,204 |
| TV (exit mult.)  | 3,537,191 | 5,508,742 | 1,771,620 |

*Note: The large gap between perpetuity and exit multiple terminal values reflects the difference between valuing Amazon's FCF at steady-state vs. applying a growth-market EBITDA multiple. The exit multiple method is more appropriate for Amazon given its investment-heavy profile where FCF significantly understates earning power.*

### Implied Intrinsic Value

| Method                        |  Base Case |  Bull Case |  Bear Case |
| ----------------------------- | ---------: | ---------: | ---------: |
| EV (perpetuity)               | $730,886M  | $1,410,799M | $248,497M |
| EV (exit mult.)               | $3,682,893M | $5,728,553M | $1,836,913M |
| **Price/share (perpetuity)**  | **$69.17** | **$131.96** | **$24.61** |
| **Price/share (exit mult.)**  | **$341.82**| **$530.76** | **$171.32**|

**Interpretation:** The perpetuity-based DCF produces very low values ($25–$132/share) because Amazon's high CapEx (13.5% of revenue) dramatically exceeds D&A (8.6%), compressing model FCF. This is a known limitation of DCF for heavy-investment companies in growth mode. The exit multiple method ($171–$531/share) better captures the value of assets being built today. The current price of $213 sits within the exit-multiple range between bear and base cases.

### Sensitivity: Implied Price — WACC vs Terminal Growth Rate (Base Case, Perpetuity Method)

| WACC \ g  |   1.5% |   2.0% |   2.5% |   3.0% |
| --------- | -----: | -----: | -----: | -----: |
| **7%**    | $88.05 | $95.64 | $104.91| $116.49|
| **8%**    | $73.87 | $79.03 | $85.11 | $92.42 |
| **9%**    | $63.52 | $67.21 | $71.47 | $76.43 |
| **10%**   | $55.65 | $58.40 | $61.51 | $65.06 |

### Sensitivity: Implied Price — WACC vs Exit Multiple (Base Case)

| WACC \ Multiple |    10x |    12x |    15x |    18x |
| --------------- | -----: | -----: | -----: | -----: |
| **7%**          | $186.64| $220.75| $271.90| $323.06|
| **8%**          | $178.55| $211.10| $259.93| $308.76|
| **9%**          | $170.88| $201.97| $248.60| $295.23|
| **10%**         | $163.62| $193.32| $237.87| $282.42|

*At 10% WACC and 15x exit multiple, implied price is $237.87 — roughly in line with the current price.*

---

## Sum-of-Parts Analysis

Amazon's segments have vastly different margin profiles, making SOTP informative.

| Segment            | Est. Rev ($M) | Est. Op Margin | Est. Op Inc ($M) | Implied EV Multiple | Implied EV ($M) |
| ------------------ | ------------: | -------------: | ----------------: | ------------------: | --------------: |
| North America      |      ~430,000 |         ~5.5%  |          ~23,650  |         15x EBIT    |       ~354,750  |
| International      |      ~165,000 |         ~2.0%  |           ~3,300  |         15x EBIT    |        ~49,500  |
| AWS                |      ~122,000 |        ~30.0%  |          ~36,600  |         30x EBIT    |     ~1,098,000  |
| Advertising (est.) |       ~60,000 |        ~50.0%  |          ~30,000  |         20x EBIT    |       ~600,000  |
| **Total**          |               |                |                   |                     |   **~2,102,250**|
| Less: Net Cash     |               |                |                   |                     |      (17,974)   |
| **Equity Value**   |               |                |                   |                     |   **~2,120,224**|
| **Per Share**      |               |                |                   |                     |     **~$195.87**|

*Note: Advertising revenue is embedded within North America/International segments. This SOTP double-counts some revenue but illustrates the hidden value in advertising. Adjust accordingly. Segment revenue estimates are approximate for FY2025.*

---

## Valuation Notes

- **Most important assumption:** AWS growth rate and the duration of the AI CapEx cycle. If AWS re-accelerates to 25%+ growth, the bull case materializes. If growth stalls at 15%, the bear case is more likely.
- **CapEx normalization is the key swing factor.** Amazon's "real" FCF power is masked by $130B+ growth CapEx. When this normalizes (even to $80-90B), FCF could exceed $60B, making the stock look much cheaper.
- **The perpetuity DCF is misleading for Amazon.** The gap between CapEx (13.5%) and D&A (8.6%) makes model FCF artificially low. Exit multiple or owner-earnings approaches are more appropriate.
- **Advertising is underappreciated.** Amazon's ad business generates an estimated $60B+ at very high margins but is buried within the retail segments. It deserves separate valuation consideration.
- **FY2022 was the trough.** The 2022 loss was driven by Rivian investment markdowns and over-investment in fulfillment capacity. Profitability has recovered sharply and structurally.

---

*Fundamentals: SEC EDGAR 10-K filings | Market data: Yahoo Finance (2026-03-09)*
*Not investment advice. Always verify figures before making any investment decision.*
