
import pandas as pd
import statsmodels.api as sm
from classes1 import FactorPCA  

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

        prices = funds_df.apply(pd.to_numeric, errors='coerce')
        returns_df  = prices.pct_change().dropna(how='all')
        self.funds_df = returns_df

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

        for fund in self.funds_df.columns:

            y = self.funds_df[fund]
            y = y[~y.index.duplicated(keep='first')].rename('fund')

            df = pd.concat([self.factors_df, y], axis=1).dropna()

            X = sm.add_constant(df[self.factors_df.columns]).astype(float)
            y_clean = df['fund'].astype(float)

            model = sm.OLS(y_clean, X).fit()
            betas = model.params.drop('const')
            exposures[fund] = betas

        exposure_df = pd.DataFrame(exposures).T
        return exposure_df


if __name__ == "__main__":

    pipelines = FactorPCA.run_all()

    funds_df = pd.read_excel(
        r"C:\repos\factors\real_estate.xlsx",
        index_col=0,
        parse_dates=True
    )

    analyzer   = FundFactorExposure(pipelines, funds_df)
    all_betas  = analyzer.analyze_all()

    print("\n=== Fund × Factor Beta Matrix ===")
    print(all_betas)
