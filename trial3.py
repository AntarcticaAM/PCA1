# fund_factor_exposure_combined.py

import pandas as pd
import statsmodels.api as sm

class FundFactorExposureCombined:
    """
    Same idea as FundFactorExposure, but we pass a dict of ready-made
    PC1 series instead of FactorPCA pipelines.
    """

    def __init__(self, factors: dict[str, pd.Series], funds_prices: pd.DataFrame):
        """
        factors: {factor_name: pd.Series of PC1 returns (index = dates)}
        funds_prices: DataFrame of fund PRICES; we convert to pct returns here.
        """
        # ---- factors ----
        self.factors_df = (
            pd.concat([s.rename(name) for name, s in factors.items()], axis=1)
              .pipe(lambda df: df[~df.index.duplicated(keep='first')])
        )

        # ---- funds → numeric % returns ----
        prices = funds_prices.apply(pd.to_numeric, errors='coerce')
        returns = prices.pct_change(fill_method=None).dropna(how='all')
        returns = returns[~returns.index.duplicated(keep='first')]
        self.funds_df = returns

    def analyze_all(self) -> pd.DataFrame:
        """
        Return (n_funds × n_factors) betas by OLS of fund returns on PC1 factors.
        """
        exposures = {}
        for fund in self.funds_df.columns:
            y = self.funds_df[fund].astype(float).rename('fund')

            df = pd.concat([self.factors_df, y], axis=1).dropna()
            X  = sm.add_constant(df[self.factors_df.columns]).astype(float)
            model = sm.OLS(df['fund'].astype(float), X).fit()
            exposures[fund] = model.params.drop('const')

        return pd.DataFrame(exposures).T
