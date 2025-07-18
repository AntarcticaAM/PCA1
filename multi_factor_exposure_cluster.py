# multi_factor_exposure_cluster.py

import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from classes1 import FactorPCA  # assumes classes1.py is in the same folder
from fund_cluster_summary import FundClusterSummary

class MultiFactorExposureCluster:
    """
    1) Runs PCA on all configured factor universes (via FactorPCA.run_all())
    2) Builds an N-factor exposure matrix (fund × factor betas) by regressing
       each fund’s returns on all PC1 factor series simultaneously.
    3) Standardizes the exposures and clusters the funds in N-dimensional beta space
       via DBSCAN, adding a 'cluster' column.
    """
    def __init__(self, pipelines: dict, funds_df: pd.DataFrame,
                 eps: float = 0.5, min_samples: int = 2):
        self.pipelines   = pipelines
        self.funds_df    = funds_df.copy()
        self.eps         = eps
        self.min_samples = min_samples
        self.exposure_df = None

    def build_exposures(self) -> pd.DataFrame:
        # 1) Assemble PC1 series for every factor into one DataFrame
        pc1_dict = {
            name: p.pc1_returns.rename(name)
            for name, p in self.pipelines.items()
        }
        factors_df = pd.concat(pc1_dict.values(), axis=1)

        # 2) Align on dates and drop any rows with missing data
        df_all = pd.concat([factors_df, self.funds_df], axis=1).dropna()
        X = sm.add_constant(df_all[factors_df.columns]).astype(float)
        Y = df_all[self.funds_df.columns].astype(float)

        # 3) Regress each fund on all factors at once
        exposures = {}
        for fund in Y:
            model = sm.OLS(Y[fund], X).fit()
            # drop intercept, keep one beta per factor
            exposures[fund] = model.params.drop("const")

        # 4) build DataFrame: rows = funds, cols = factor betas
        self.exposure_df = pd.DataFrame(exposures).T
        return self.exposure_df

    def cluster(self) -> pd.DataFrame:
        if self.exposure_df is None:
            raise RuntimeError("Call build_exposures() first.")

        # Standardize the N-dimensional beta vectors
        Z = StandardScaler().fit_transform(self.exposure_df)
        # Cluster in N-dimensional space
        labels = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(Z)
        # Append cluster labels
        self.exposure_df['cluster'] = labels
        return self.exposure_df

    def run(self) -> pd.DataFrame:
        self.build_exposures()
        return self.cluster()


if __name__ == "__main__":
    # 1) Run PCA on all your factor universes
    pipelines = FactorPCA.run_all()

    # 2) Load hedge-fund returns (Excel with date as first column)
    funds_df = pd.read_excel(
        r"C:\repos\factors\real_estate.xlsx",
        index_col=0,
        parse_dates=True
    )

    # 3) Build exposures and cluster
    mfec = MultiFactorExposureCluster(
        pipelines=pipelines,
        funds_df=funds_df,
        eps=0.6,
        min_samples=3
    )
    result = mfec.run()

    # 4) Inspect
    print("\nFund exposures and cluster assignments:\n")
    print(result)

    # (Optional) Save to CSV
    # result.to_csv("funds_multi_factor_clusters.csv")
