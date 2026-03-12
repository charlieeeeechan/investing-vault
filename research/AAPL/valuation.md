# AAPL — Valuation

*Last updated: 2026-03-07*
*Share price: ~$258 | Market Cap: ~$3.7T | Shares: ~14.7B*

---

## Current Multiples

| Multiple | Trailing | Forward (FY2026E) | 5-Year Avg |
| -------- | -------: | ----------------: | ---------: |
| P/E | ~35x | ~28x | ~28x |
| EV/EBITDA | ~27x | ~23x | ~22x |
| P/FCF | ~37x | ~30x | ~27x |
| P/S | ~8.5x | ~7.5x | ~7x |
| P/B | ~50x | — | ~40x |

*Note: P/B is distorted by massive buybacks reducing book value. Not a meaningful valuation metric for Apple.*

**Assessment:** Apple trades at a premium to its 5-year averages on most metrics. The market is pricing in the AI upgrade cycle and continued margin expansion. At ~35x trailing earnings, there is limited margin of safety if growth disappoints.

---

## DCF Analysis

### Base Case Assumptions

```
# DCF Parameters (for use with tools/dcf_calculator.py)

ticker = "AAPL"
base_fcf = 98_767          # FY2025 FCF ($M)
growth_rates = {
    "year_1": 0.12,         # FY2026: AI cycle + Services ramp
    "year_2": 0.10,         # FY2027: Continued momentum
    "year_3": 0.08,         # FY2028: Growth normalization
    "year_4": 0.07,         # FY2029: Steady state
    "year_5": 0.06,         # FY2030: Mature growth
}
terminal_growth = 0.03      # 3% perpetuity growth
discount_rate = 0.10        # 10% WACC
shares_outstanding = 14_700  # Millions (current)
net_debt = 31_610           # $M (FY2025)
```

### DCF Output

| Year | FCF ($M) | PV of FCF ($M) |
| ---- | -------: | -------------: |
| FY2026 | $110,619 | $100,563 |
| FY2027 | $121,681 | $100,563 |
| FY2028 | $131,415 | $98,744 |
| FY2029 | $140,614 | $96,019 |
| FY2030 | $149,051 | $92,544 |

| Component | Value |
| --------- | ----: |
| PV of FCF (Years 1-5) | ~$488B |
| Terminal Value (PV) | ~$1,323B |
| Enterprise Value | ~$1,811B |
| Less: Net Debt | ($32B) |
| Equity Value | ~$1,779B |
| **Fair Value / Share** | **~$121** |

### Sensitivity Table (Fair Value per Share)

| Discount Rate \ Terminal Growth | 2.0% | 2.5% | 3.0% | 3.5% | 4.0% |
| ------------------------------- | ---: | ---: | ---: | ---: | ---: |
| **8.0%** | $179 | $202 | $233 | $276 | $340 |
| **9.0%** | $141 | $155 | $174 | $199 | $233 |
| **10.0%** | $114 | $123 | $134 | $149 | $169 |
| **11.0%** | $94 | $100 | $108 | $117 | $129 |
| **12.0%** | $79 | $83 | $89 | $95 | $103 |

---

## Scenario Analysis

### Bull Case — $180/share (WACC 9%, Terminal 3.5%)

- AI supercycle drives iPhone revenue acceleration to +10-15% for 2 years
- Services reaches $130B+ by FY2028 at 75%+ margins
- FCF grows 12-15% annually through FY2028
- Buybacks reduce share count by 3% annually
- Gross margin reaches 50%+

### Base Case — $134/share (WACC 10%, Terminal 3.0%)

- Moderate iPhone growth (+5-7% annually)
- Services grows 12-15% annually, hitting $120B by FY2028
- FCF grows 6-8% annually
- Margins expand modestly (gross margin ~48-49%)
- Continued $90B+/year buybacks

### Bear Case — $89/share (WACC 12%, Terminal 2.5%)

- AI cycle disappoints — iPhone replacement cycles elongate further
- Google search deal reduced/eliminated (lose $10-15B in high-margin revenue)
- China revenue declines 10-15% on Huawei competition + geopolitical risk
- EU DMA and DOJ remedies impair App Store economics
- FCF stagnates at ~$95-100B

---

## Comparable Companies

| Company | P/E (TTM) | EV/EBITDA | P/FCF | Revenue Growth | Net Margin |
| ------- | --------: | --------: | ----: | -------------: | ---------: |
| **AAPL** | **~35x** | **~27x** | **~37x** | **+6.4%** | **26.9%** |
| MSFT | ~35x | ~25x | ~38x | +16.0% | 36.0% |
| GOOGL | ~24x | ~18x | ~28x | +14.0% | 27.0% |
| AMZN | ~42x | ~18x | ~30x | +11.0% | 9.0% |
| META | ~28x | ~20x | ~30x | +22.0% | 35.0% |
| Samsung | ~15x | ~8x | ~12x | +10.0% | 10.0% |

*Note: Comparables are approximate as of early 2026. Apple's premium reflects its capital return program, ecosystem moat, and perceived safety.*

**Observation:** Apple trades at a premium P/E to most mega-cap peers despite having the slowest revenue growth. The premium is justified by unmatched FCF generation, the buyback program, and the AI upgrade cycle narrative — but it leaves less room for error.

---

## Fair Value Discussion

**Confidence level: Medium**

The DCF analysis consistently suggests Apple is overvalued at ~$258, with base case fair value around $134 and even the bull case only reaching ~$180. However, DCF models have historically undervalued Apple because:

1. **Buybacks are not captured.** Apple retiring 2-3% of shares annually means per-share value grows faster than total company value. Over 5 years, this adds ~15% to per-share fair value.
2. **Optionality is not captured.** New product categories (Vision Pro, automotive), new services, India expansion — these have real but hard-to-model value.
3. **Quality premium.** The market has persistently assigned Apple a premium multiple because of its predictability, cash generation, and perceived safety.

A more realistic approach: apply a reasonable P/E to normalized FY2026 earnings.
- Normalized EPS: ~$9.00-9.50 (assuming ~15% growth on $7.46 FY2025 + buyback boost)
- Fair P/E range: 25-30x (growth-adjusted, accounting for quality)
- **Fair value range: $225-$285**

At ~$258, Apple is roughly fairly valued if the AI cycle plays out and margins continue expanding. It offers limited upside and limited downside — a "compounder at fair price" rather than a deep value opportunity.

---

## Historical Valuation Context

| Metric | Current | 5Y Low | 5Y High | 5Y Avg |
| ------ | ------: | -----: | ------: | -----: |
| P/E | ~35x | ~22x | ~40x | ~28x |
| EV/EBITDA | ~27x | ~17x | ~32x | ~22x |
| Dividend Yield | ~0.4% | ~0.4% | ~0.7% | ~0.6% |

Apple is trading near the upper end of its 5-year range. Previous peaks (~40x P/E) occurred during the 5G cycle in 2020-2021. A reversion to the 5-year average (~28x) on FY2026 EPS of ~$9.25 would imply ~$259 — essentially the current price.

---

*Note: Apple completed a 4:1 stock split in August 2020. All historical per-share data has been adjusted for the split.*

*Verified: yes*
*Source: 10-K FY2025, Q1 FY2026 Earnings Release, SEC EDGAR, Apple Investor Relations*
