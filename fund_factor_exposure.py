# fund_factor_exposure.py

# fund_factor_exposure.py

import pandas as pd
import statsmodels.api as sm
from classes1 import FactorPCA  # your PCA engine :contentReference[oaicite:2]{index=2}

class FundFactorExposure:
    """
    Compute multi-factor exposures (betas) for each fund by regressing
    fund returns on the PC1 time series of each factor universe.
    """

    def __init__(self, pipelines: dict, funds_df: pd.DataFrame):
        """
        pipelines: dict of { factor_name: FactorPCA instance }
        funds_df:  DataFrame of fund returns (index=date, cols=real tickers)
        funds are here in price and not percentage returns this is a test
        """
        self.pipelines = pipelines
        # convert price levels → simple pct-change returns
        prices = funds_df.apply(pd.to_numeric, errors='coerce')
        returns_df  = prices.pct_change().dropna(how='all')
        self.funds_df = returns_df

        # Build DataFrame of all PC1 factor series
        self.factors_df = pd.concat(
            [pipe.pc1_returns.rename(name)
             for name, pipe in pipelines.items()],
            axis=1
        )

    def analyze_all(self) -> pd.DataFrame:
        """
        Returns a DataFrame of shape (n_funds × n_factors),
        where each row is one fund’s beta vector.
        """
        exposures = {}
        # loop over each real ticker column
        for fund in self.funds_df.columns:
            # 1) Align fund and factor series on dates
            # 1) extract the fund’s series, drop duplicate dates
            y = self.funds_df[fund]
            y = y[~y.index.duplicated(keep='first')].rename('fund')

            # 2) align dates with factors and drop any missing
            df = pd.concat([self.factors_df, y], axis=1).dropna()

            # 3) build regression matrix: intercept + all PC1s
            X = sm.add_constant(df[self.factors_df.columns]).astype(float)
            y_clean = df['fund'].astype(float)

            # 4) fit OLS and grab betas (drop intercept)
            model = sm.OLS(y_clean, X).fit()
            betas = model.params.drop('const')
            exposures[fund] = betas

        # assemble into DataFrame: rows = funds, cols = factor betas
        exposure_df = pd.DataFrame(exposures).T
        return exposure_df


if __name__ == "__main__":
    # 1) Compute all your PC1 series
    pipelines = FactorPCA.run_all()

    # 2) Load your hedge-fund returns (first column = date)
    funds_df = pd.read_excel(
        r"C:\repos\factors\real_estate.xlsx",
        index_col=0,
        parse_dates=True
    )

    # 3) Compute the full fund×factor beta matrix
    analyzer   = FundFactorExposure(pipelines, funds_df)
    all_betas  = analyzer.analyze_all()

    # 4) Print: index = real tickers, columns = factor names
    print("\n=== Fund × Factor Beta Matrix ===")
    print(all_betas)
