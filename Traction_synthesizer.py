#!/usr/bin/env python3
"""
Scientia Traction Economics Synthesizer (v1.4.0)
Automated Startup Unit Economics, Cohort LTV/CAC & Runway Stress-Testing Engine.
Repurposed from open-source financial data libraries (Pandas / FastEmbed).

Scientia Partners · Independent Advisory & Engineering Hub · UAE
hello@scientiapartners.com
"""

import argparse
import json
import sys
from typing import Dict, Any


class TractionEconomicsSynthesizer:
    def __init__(self, company_name: str, currency: str = "USD"):
        self.company_name = company_name
        self.currency = currency

    def analyze_economics(
        self,
        mrr: float,
        monthly_churn_pct: float,
        arpu_monthly: float,
        cac: float,
        gross_margin_pct: float,
        monthly_operating_expenses: float,
        cash_balance: float,
        revenue_growth_rate_pct: float = 10.0
    ) -> Dict[str, Any]:
        """
        Calculates key venture metrics and runway viability.
        """
        churn_rate = max(0.001, monthly_churn_pct / 100.0)
        gross_margin = gross_margin_pct / 100.0

        # Customer Lifetime (in months)
        customer_lifetime_months = 1.0 / churn_rate

        # Customer Lifetime Value (LTV)
        ltv = arpu_monthly * gross_margin * customer_lifetime_months

        # LTV / CAC Ratio
        ltv_cac_ratio = ltv / cac if cac > 0 else 0.0

        # CAC Payback Period (in months)
        monthly_gross_profit_per_user = arpu_monthly * gross_margin
        cac_payback_months = cac / monthly_gross_profit_per_user if monthly_gross_profit_per_user > 0 else 999.0

        # Monthly Revenue & Gross Profit
        gross_profit_monthly = mrr * gross_margin
        net_burn_monthly = max(0.0, monthly_operating_expenses - gross_profit_monthly)

        # Runway in Months
        runway_months = (cash_balance / net_burn_monthly) if net_burn_monthly > 0 else 999.0

        # Rule of 40 (Growth Rate % + Free Cash Flow Margin %)
        fcf_margin_pct = ((gross_profit_monthly - monthly_operating_expenses) / mrr * 100.0) if mrr > 0 else 0.0
        rule_of_40_score = revenue_growth_rate_pct + fcf_margin_pct

        # Institutional Venture Benchmark Assessment
        ltv_cac_status = "TOP DECILE (>= 4x)" if ltv_cac_ratio >= 4.0 else "HEALTHY (3x - 4x)" if ltv_cac_ratio >= 3.0 else "UNSUSTAINABLE (< 3x)"
        payback_status = "EXCELLENT (< 12mo)" if cac_payback_months <= 12 else "ACCEPTABLE (12-18mo)" if cac_payback_months <= 18 else "PROLONGED (> 18mo)"
        runway_status = "EXPANSION (>= 18mo)" if runway_months >= 18 else "CAUTION (12-18mo)" if runway_months >= 12 else "CRITICAL FUNDRAISE REQUIRED (< 12mo)"

        return {
            "company": self.company_name,
            "currency": self.currency,
            "core_metrics": {
                "arr": round(mrr * 12, 2),
                "mrr": round(mrr, 2),
                "gross_margin_percent": gross_margin_pct,
                "monthly_churn_percent": monthly_churn_pct,
                "customer_lifetime_months": round(customer_lifetime_months, 1),
                "ltv": round(ltv, 2),
                "cac": round(cac, 2),
                "ltv_to_cac_ratio": round(ltv_cac_ratio, 2),
                "cac_payback_months": round(cac_payback_months, 1),
            },
            "burn_and_runway": {
                "cash_balance": round(cash_balance, 2),
                "monthly_operating_expenses": round(monthly_operating_expenses, 2),
                "net_monthly_burn": round(net_burn_monthly, 2),
                "estimated_runway_months": round(runway_months, 1) if runway_months < 900 else "CASH FLOW POSITIVE",
                "rule_of_40_score": round(rule_of_40_score, 1),
            },
            "venture_benchmark_audit": {
                "ltv_cac_health": ltv_cac_status,
                "cac_payback_health": payback_status,
                "runway_urgency": runway_status,
            }
        }


def main():
    parser = argparse.ArgumentParser(description="Scientia Traction Economics Synthesizer CLI")
    parser.add_argument("--company", default="Aura Health Systems", help="Startup legal name")
    parser.add_argument("--currency", default="USD", help="Reporting currency")
    parser.add_argument("--mrr", type=float, default=65000.0, help="Monthly Recurring Revenue")
    parser.add_argument("--churn", type=float, default=2.2, help="Monthly Churn Rate %")
    parser.add_argument("--arpu", type=float, default=450.0, help="Average Revenue Per User / mo")
    parser.add_argument("--cac", type=float, default=1800.0, help="Customer Acquisition Cost")
    parser.add_argument("--margin", type=float, default=82.0, help="Gross Margin %")
    parser.add_argument("--expenses", type=float, default=95000.0, help="Monthly Opex")
    parser.add_argument("--cash", type=float, default=1250000.0, help="Current Cash in Bank")
    parser.add_argument("--growth", type=float, default=15.0, help="Monthly revenue growth rate %")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()
    engine = TractionEconomicsSynthesizer(company_name=args.company, currency=args.currency)
    result = engine.analyze_economics(
        mrr=args.mrr,
        monthly_churn_pct=args.churn,
        arpu_monthly=args.arpu,
        cac=args.cac,
        gross_margin_pct=args.margin,
        monthly_operating_expenses=args.expenses,
        cash_balance=args.cash,
        revenue_growth_rate_pct=args.growth
    )

    if args.json:
        print(json.dumps(result, indent=2))
        return

    c = result['currency']
    print("=" * 72)
    print("  SCIENTIA PARTNERS · TRACTION ECONOMICS SYNTHESIZER")
    print("=" * 72)
    print(f"Company:           {result['company']}")
    print(f"ARR / MRR:         {c} {result['core_metrics']['arr']:,.2f} / {c} {result['core_metrics']['mrr']:,.2f}")
    print(f"LTV / CAC Ratio:   {result['core_metrics']['ltv_to_cac_ratio']}x ({result['venture_benchmark_audit']['ltv_cac_health']})")
    print(f"CAC Payback:       {result['core_metrics']['cac_payback_months']} months ({result['venture_benchmark_audit']['cac_payback_health']})")
    print(f"Net Monthly Burn:  {c} {result['burn_and_runway']['net_monthly_burn']:,.2f}")
    print(f"Current Runway:    {result['burn_and_runway']['estimated_runway_months']} months ({result['venture_benchmark_audit']['runway_urgency']})")
    print(f"Rule of 40 Score:  {result['burn_and_runway']['rule_of_40_score']}%")
    print("=" * 72)


if __name__ == "__main__":
    main()