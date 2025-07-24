# PCAonFunds_from_combined.py

import pandas as pd
from PCAs_combined import (
    pc1_returns_growth, pc1_returns_value, pc1_returns_quality,
    pc1_returns_inflation, pc1_returns_realestate, pc1_returns_size,
    pc1_returns_commodity, pc1_returns_defensive, pc1_returns_crowded,
    pc1_returns_shortvol,
)
from trial3 import FundFactorExposureCombined

def main():
    # pack factors into a dict
    factors = {
        "growth":     pc1_returns_growth,
        "value":      pc1_returns_value,
        "quality":    pc1_returns_quality,
        "inflation":  pc1_returns_inflation,
        "realestate": pc1_returns_realestate,
        "size":       pc1_returns_size,
        "commodity":  pc1_returns_commodity,
        "defensive":  pc1_returns_defensive,
        "crowded":    pc1_returns_crowded,
        "shortvol":   pc1_returns_shortvol,
    }

    # load funds (prices)
    prices = pd.read_excel(
        r"C:\repos\factors\johnjohn_funds_performance.xlsx",
        index_col=0, parse_dates=True
    )

    analyzer = FundFactorExposureCombined(factors, prices)
    betas = analyzer.analyze_all()

    print("\n=== Fund × Factor Beta Matrix ===")
    print(betas.round(6))
    betas.to_excel(r"C:\repos\factors\fund_factor_betas_from_combined.xlsx")

if __name__ == "__main__":
    main()
