# trialA1.py  (multi-factor betas for every fund)

import numpy as np
import pandas as pd
import statsmodels.api as sm

from classes1 import FactorPCA   # <-- or classes1 import, whatever holds FactorPCA


# ---------- helpers ----------
def load_fund_returns(path: str) -> pd.DataFrame:
    """Read fund prices and convert to decimal returns."""
    prices = pd.read_excel(path, index_col=0, parse_dates=True)
    prices = prices.apply(pd.to_numeric, errors='coerce')
    rets   = prices.pct_change(fill_method=None).dropna(how='all')
    rets   = rets[~rets.index.duplicated(keep='first')]
    return rets


def rescale_factors(f_df: pd.DataFrame) -> pd.DataFrame:
    """
    If factors look like % points (>1 median abs), divide by 100. Otherwise leave as is.
    """
    scales = {}
    for c in f_df.columns:
        med = f_df[c].abs().median()
        scales[c] = 100.0 if med > 1 else 1.0
    return f_df.div(pd.Series(scales)), scales


# ---------- main ----------
def main():
    # 1) Build factor PC1 series
    pipelines = FactorPCA.run_all()

    factors_df = pd.concat(
        [p.pc1_returns.rename(name) for name, p in pipelines.items()],
        axis=1
    ).dropna(how="all")
    factors_df = factors_df[~factors_df.index.duplicated(keep='first')]

    # 2) Scale to match fund units (funds are decimals)
    factors_df, used_scales = rescale_factors(factors_df)
    print("Factor rescale used:", used_scales)

    # 3) Load funds (prices -> returns)
    funds_path = r"C:\repos\factors\johnjohn_funds_performance.xlsx"
    fund_rets  = load_fund_returns(funds_path)

    # 4) Clean infinities / ensure numeric BEFORE merging
    for df_ in (factors_df, fund_rets):
        df_.replace([np.inf, -np.inf], np.nan, inplace=True)
        df_.dropna(how="all", inplace=True)

    # drop near-constant cols (avoid singular matrices)
    tiny_fact = factors_df.std() < 1e-10
    if tiny_fact.any():
        print("Dropping near-constant factors:", list(tiny_fact[tiny_fact].index))
        factors_df = factors_df.loc[:, ~tiny_fact]

    tiny_fund = fund_rets.std() < 1e-10
    if tiny_fund.any():
        print("Dropping near-constant funds:", list(tiny_fund[tiny_fund].index))
        fund_rets = fund_rets.loc[:, ~tiny_fund]

    # 5) Align on dates (inner join to keep common history)
    all_df = pd.concat([factors_df, fund_rets], axis=1, join='inner').dropna(how='any')

    factor_cols = factors_df.columns.tolist()
    X = sm.add_constant(all_df[factor_cols]).astype(float)

    betas = {}   # <-- DEFINE IT
    for fund in fund_rets.columns:
        y = all_df[fund].astype(float)

        if y.std() < 1e-10:          # skip flat series
            continue

        model = sm.OLS(y, X, missing='drop').fit()
        coefs = model.params.drop('const').replace([np.inf, -np.inf], np.nan)
        betas[fund] = coefs

    beta_matrix = pd.DataFrame.from_dict(betas, orient='index')

    print("\n=== Fund × Factor Beta Matrix ===")
    print(beta_matrix.round(6))

    out_path = r"C:\repos\factors\fund_multi_factor_betas6.xlsx"
    beta_matrix.to_excel(out_path)
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
