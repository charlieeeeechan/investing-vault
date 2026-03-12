#!/usr/bin/env python3
"""
DCF Calculator - Discounted Cash Flow valuation model

Supports:
- Unlevered DCF (Enterprise Value approach)
- Sensitivity analysis (WACC vs Growth, WACC vs Exit Multiple)

Usage:
    from dcf_calculator import UnleveredDCF

    dcf = UnleveredDCF(
        base_revenue=12449,
        net_debt=4200,
        shares_outstanding=592,
        wacc=0.082,
        terminal_growth=0.025,
        exit_multiple=15,
        revenue_growth=[0, 0.05, 0.05, 0.04, 0.035, 0.03],
        ebit_margin=[0.12, 0.12, 0.125, 0.13, 0.13, 0.13],
        tax_rate=0.21,
        da_pct=0.03,
        capex_pct=0.04,
        nwc_pct=0.02
    )
    result = dcf.calculate()
    print(result)
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import json


@dataclass
class DCFResult:
    """Results from DCF calculation"""
    intrinsic_price_perpetuity: float
    intrinsic_price_exit_multiple: float
    fcf_by_year: List[float]
    pv_fcf_by_year: List[float]
    sum_pv_fcf: float
    terminal_value_perpetuity: float
    terminal_value_exit: float
    pv_terminal_perpetuity: float
    pv_terminal_exit: float
    enterprise_value_perpetuity: Optional[float] = None
    enterprise_value_exit: Optional[float] = None
    equity_value_perpetuity: float = 0
    equity_value_exit: float = 0
    sensitivity_perpetuity: Dict[str, Any] = None
    sensitivity_exit: Dict[str, Any] = None

    def to_dict(self) -> dict:
        return {
            'intrinsic_price_perpetuity': round(self.intrinsic_price_perpetuity, 2),
            'intrinsic_price_exit_multiple': round(self.intrinsic_price_exit_multiple, 2),
            'sum_pv_fcf': round(self.sum_pv_fcf, 2),
            'terminal_value_perpetuity': round(self.terminal_value_perpetuity, 2),
            'terminal_value_exit': round(self.terminal_value_exit, 2),
            'equity_value_perpetuity': round(self.equity_value_perpetuity, 2),
            'equity_value_exit': round(self.equity_value_exit, 2),
            'fcf_by_year': [round(x, 2) for x in self.fcf_by_year],
            'sensitivity_perpetuity': self.sensitivity_perpetuity,
            'sensitivity_exit': self.sensitivity_exit,
        }

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class UnleveredDCF:
    """
    Unlevered DCF (Enterprise Value approach)

    Calculates: NOPAT + D&A - Capex - delta_NWC = Unlevered FCF
    Discounts at WACC
    Subtracts Net Debt to get Equity Value
    """

    def __init__(
        self,
        base_revenue: float,
        net_debt: float,
        shares_outstanding: float,
        wacc: float,
        terminal_growth: float,
        exit_multiple: float,
        revenue_growth: List[float],
        ebit_margin: List[float],
        tax_rate: float = 0.21,
        da_pct: float = 0.03,
        capex_pct: float = 0.04,
        nwc_pct: float = 0.02
    ):
        self.base_revenue = base_revenue
        self.net_debt = net_debt
        self.shares = shares_outstanding
        self.wacc = wacc
        self.terminal_growth = terminal_growth
        self.exit_multiple = exit_multiple
        self.revenue_growth = revenue_growth
        self.ebit_margin = ebit_margin
        self.tax_rate = tax_rate
        self.da_pct = da_pct
        self.capex_pct = capex_pct
        self.nwc_pct = nwc_pct

    def calculate(self) -> DCFResult:
        revenue = []
        for i, g in enumerate(self.revenue_growth):
            if i == 0:
                revenue.append(self.base_revenue * (1 + g))
            else:
                revenue.append(revenue[-1] * (1 + g))

        ebit = [revenue[i] * self.ebit_margin[i] for i in range(len(revenue))]
        nopat = [ebit[i] * (1 - self.tax_rate) for i in range(len(revenue))]
        da = [revenue[i] * self.da_pct for i in range(len(revenue))]
        capex = [-revenue[i] * self.capex_pct for i in range(len(revenue))]
        nwc = [-revenue[i] * self.nwc_pct for i in range(len(revenue))]

        ufcf = [nopat[i] + da[i] + capex[i] + nwc[i] for i in range(len(revenue))]

        pv_factors = [1 / (1 + self.wacc) ** i for i in range(len(revenue))]
        pv_ufcf = [ufcf[i] * pv_factors[i] for i in range(len(revenue))]

        sum_pv = sum(pv_ufcf[1:])

        tv_perpetuity = ufcf[-1] * (1 + self.terminal_growth) / (self.wacc - self.terminal_growth)
        pv_tv_perpetuity = tv_perpetuity / (1 + self.wacc) ** 5

        ebitda_terminal = ebit[-1] + da[-1]
        tv_exit = ebitda_terminal * self.exit_multiple
        pv_tv_exit = tv_exit / (1 + self.wacc) ** 5

        ev_perpetuity = sum_pv + pv_tv_perpetuity
        ev_exit = sum_pv + pv_tv_exit

        equity_perpetuity = ev_perpetuity - self.net_debt
        equity_exit = ev_exit - self.net_debt

        price_perpetuity = equity_perpetuity / self.shares
        price_exit = equity_exit / self.shares

        sens_perpetuity = self._sensitivity_perpetuity(ufcf, sum_pv)
        sens_exit = self._sensitivity_exit(ufcf, ebitda_terminal, sum_pv)

        return DCFResult(
            intrinsic_price_perpetuity=price_perpetuity,
            intrinsic_price_exit_multiple=price_exit,
            fcf_by_year=ufcf,
            pv_fcf_by_year=pv_ufcf,
            sum_pv_fcf=sum_pv,
            terminal_value_perpetuity=tv_perpetuity,
            terminal_value_exit=tv_exit,
            pv_terminal_perpetuity=pv_tv_perpetuity,
            pv_terminal_exit=pv_tv_exit,
            enterprise_value_perpetuity=ev_perpetuity,
            enterprise_value_exit=ev_exit,
            equity_value_perpetuity=equity_perpetuity,
            equity_value_exit=equity_exit,
            sensitivity_perpetuity=sens_perpetuity,
            sensitivity_exit=sens_exit
        )

    def _sensitivity_perpetuity(self, ufcf, sum_pv_base):
        wacc_range = [0.07, 0.08, 0.09, 0.10]
        g_range = [0.015, 0.02, 0.025, 0.03]

        table = {}
        for wacc in wacc_range:
            row = {}
            for g in g_range:
                pv_sum = sum(ufcf[i] / (1 + wacc) ** i for i in range(1, len(ufcf)))
                tv = ufcf[-1] * (1 + g) / (wacc - g)
                pv_tv = tv / (1 + wacc) ** 5
                ev = pv_sum + pv_tv
                equity = ev - self.net_debt
                price = equity / self.shares
                row[f"{g:.1%}"] = round(price, 2)
            table[f"{wacc:.0%}"] = row

        return {"wacc_vs_growth": table}

    def _sensitivity_exit(self, ufcf, ebitda, sum_pv_base):
        wacc_range = [0.07, 0.08, 0.09, 0.10]
        mult_range = [10, 12, 15, 18]

        table = {}
        for wacc in wacc_range:
            row = {}
            for mult in mult_range:
                pv_sum = sum(ufcf[i] / (1 + wacc) ** i for i in range(1, len(ufcf)))
                tv = ebitda * mult
                pv_tv = tv / (1 + wacc) ** 5
                ev = pv_sum + pv_tv
                equity = ev - self.net_debt
                price = equity / self.shares
                row[f"{mult}x"] = round(price, 2)
            table[f"{wacc:.0%}"] = row

        return {"wacc_vs_multiple": table}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='DCF Calculator')
    parser.add_argument('--test', action='store_true', help='Run with example defaults')

    args = parser.parse_args()

    if args.test:
        print("=== UNLEVERED DCF (Example) ===\n")
        dcf = UnleveredDCF(
            base_revenue=12449,
            net_debt=4200,
            shares_outstanding=592,
            wacc=0.082,
            terminal_growth=0.025,
            exit_multiple=15,
            revenue_growth=[0, 0.05, 0.05, 0.04, 0.035, 0.03],
            ebit_margin=[0.12, 0.12, 0.125, 0.13, 0.13, 0.13],
            tax_rate=0.21,
            da_pct=0.03,
            capex_pct=0.04,
            nwc_pct=0.02
        )
        result = dcf.calculate()
        print(result)
    else:
        parser.print_help()
