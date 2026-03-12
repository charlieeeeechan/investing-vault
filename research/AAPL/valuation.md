# AAPL — Valuation

*Fundamentals: SEC EDGAR 10-K filings. Market data: Yahoo Finance (2026-03-12).*
*Last updated: 2026-03-12*

---

## Current Market Data

| Metric                       | Value               | Source              |
| ---------------------------- | ------------------- | ------------------- |
| Stock Price                  | $260.81             | Yahoo Finance       |
| Shares Outstanding (diluted) | ~15,005M            | SEC EDGAR FY2025    |
| Market Cap                   | $3,833,366M         | Yahoo Finance       |
| Enterprise Value             | $3,852,590M         | Yahoo Finance       |
| Net Debt (LTD - Cash)        | $54,744M            | SEC EDGAR FY2025    |

## Trailing Multiples

*Price and EV from Yahoo Finance (2026-03-12). Fundamentals from SEC EDGAR.*

| Metric            | FY2025 Value   |         Multiple |
| ----------------- | -------------: | ---------------: |
| Revenue           |    $416,161M   | 9.3x EV/Rev     |
| Operating Income  |    $133,050M   | 29.0x EV/EBIT   |
| Net Income (GAAP) |    $112,010M   | 34.2x P/E       |
| EPS Diluted       |         $7.46  | 35.0x P/E        |
| CFO               |    $111,482M   | 34.4x P/CFO     |

---

## DCF Analysis

*Computed using EDGAR fundamentals. All values in $M unless noted.*
*Inputs: base revenue $416,161M (FY2025), net debt $54,744M, 15,005M diluted shares*
*D&A: 2.9% of revenue | CapEx: 2.8% of revenue (3-year average from EDGAR)*

### Scenario Assumptions

| Parameter                  | Base Case | Bull Case | Bear Case |
| -------------------------- | --------: | --------: | --------: |
| Revenue Growth (Yr 1-3)    |  5%/5%/4% |  8%/8%/6% |  2%/2%/1% |
| Revenue Growth (Yr 4-5)    |     4%/3% |     6%/5% |     1%/1% |
| Terminal Growth Rate       |      3.5% |      4.0% |      2.5% |
| EBIT Margin (Yr 1 -> Yr 5) |   32%-33% |   33%-36% |   30%-28% |
| WACC                       |       10% |        8% |       12% |
| Tax Rate                   |       21% |       20% |       22% |
| Exit Multiple (EBITDA)     |       22x |       26x |       16x |

### Projected Free Cash Flow ($M)

| Year  |  Base FCF |  Bull FCF |  Bear FCF |
| ----- | --------: | --------: | --------: |
| Yr 1  |  $106,533 |  $114,611 |   $95,509 |
| Yr 2  |  $111,860 |  $123,780 |   $97,419 |
| Yr 3  |  $118,219 |  $135,323 |   $94,982 |
| Yr 4  |  $124,908 |  $147,805 |   $95,932 |
| Yr 5  |  $128,655 |  $159,777 |   $93,412 |
| **PV of FCFs** | **$381,111** | **$465,402** | **$290,348** |
| Terminal Value (perpetuity) | $1,272,010 | $2,827,279 |  $571,890 |
| Terminal Value (exit mult.) | $2,506,672 | $3,941,977 | $1,251,452 |

### Implied Intrinsic Value

| Method                        |    Base Case |   Bull Case |   Bear Case |
| ----------------------------- | -----------: | ----------: | ----------: |
| EV (perpetuity)               | $1,653,121M  | $3,292,681M |   $862,239M |
| EV (exit mult.)               | $2,887,783M  | $4,407,379M | $1,541,800M |
| **Price/share (perpetuity)**  |  **$106.52** | **$215.79** |  **$53.82** |
| **Price/share (exit mult.)**  |  **$188.81** | **$290.08** |  **$99.10** |

### Sensitivity: Implied Price — WACC vs Terminal Growth Rate (Base Case, Perpetuity Method)

| WACC \ g  |    1.5% |    2.0% |    2.5% |    3.0% |
| --------- | ------: | ------: | ------: | ------: |
| **7%**    | $136.35 | $148.25 | $162.78 | $180.95 |
| **8%**    | $114.04 | $122.12 | $131.67 | $143.13 |
| **9%**    |  $97.74 | $103.53 | $110.20 | $117.99 |
| **10%**   |  $85.32 |  $89.63 |  $94.51 | $100.09 |

### Sensitivity: Implied Price — WACC vs Exit Multiple (Base Case)

| WACC \ Mult |     10x |     12x |     15x |     18x |
| ----------- | ------: | ------: | ------: | ------: |
| **7%**      | $110.73 | $128.17 | $154.33 | $180.48 |
| **8%**      | $106.15 | $122.80 | $147.77 | $172.73 |
| **9%**      | $101.81 | $117.70 | $141.55 | $165.39 |
| **10%**     |  $97.68 | $112.87 | $135.65 | $158.43 |

---

## Valuation Notes

- **The DCF suggests AAPL is overvalued at $260.81 relative to fundamental cash flows.** The bull case perpetuity method ($216) is still well below market, though the exit multiple bull case ($290) now justifies the current price with the lower 8% WACC. Base and bear cases remain far below market, confirming that today's price embeds very optimistic assumptions.

- **The widened WACC spread (8% bull / 12% bear) amplifies the valuation range.** The bull-to-bear spread on the perpetuity method is now $54-$216 (was $61-$171), reflecting greater sensitivity to cost-of-capital assumptions. The terminal value dominates (>70% of EV), so even small WACC changes have outsized effects — the sensitivity table shows a range of $85 to $181 per share just from varying WACC and terminal growth.

- **Apple's valuation premium reflects qualitative factors** that are hard to capture in a DCF: the ecosystem moat, capital return discipline, brand durability, and services growth optionality. The market applies a "quality premium" to Apple that goes beyond near-term cash flow projections.

- **Services segment deserves separate consideration.** Services (~25% of revenue, ~70%+ gross margins) would trade at a much higher multiple standalone. A sum-of-parts approach would value Services at 30-40x earnings and Products at 15-20x, potentially justifying a higher blended value than the unified DCF suggests.

- **Key swing factor: revenue growth trajectory.** If Apple Intelligence triggers a multi-year upgrade supercycle and services monetization accelerates, the bull case becomes more plausible. If smartphone saturation wins out, the bear case is in play.

---

*Fundamentals: SEC EDGAR 10-K filings | Market data: Yahoo Finance (2026-03-12)*
*Not investment advice. Always verify figures before making any investment decision.*
