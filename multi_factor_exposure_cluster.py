

import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from classes1 import FactorPCA  
from fund_cluster_summary import FundClusterSummary

class MultiFactorExposureCluster:
    """
    Runs PCA on all configured factor universe (via FactorPCA.run_all())
    Builds an N-factor exposure matrix (fund × factor betas) by regressing
    each fund’s returns on all PC1 factor series simultaneously.
    tandardizes the exposures and clusters the funds in N-dimensional beta space
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

        pc1_dict = {
            name: p.pc1_returns.rename(name)
            for name, p in self.pipelines.items()
        }
        factors_df = pd.concat(pc1_dict.values(), axis=1)
        factors_df = factors_df[~factors_df.index.duplicated(keep='first')]
        funds_clean = self.funds_df[~self.funds_df.index.duplicated(keep='first')]
        
        df_all = pd.concat([factors_df, funds_clean], axis=1).dropna()

        X = sm.add_constant(df_all[factors_df.columns]).astype(float)
        Y = df_all[self.funds_df.columns].astype(float)
        exposures = {}
        for fund in Y:
            model = sm.OLS(Y[fund], X).fit()

            exposures[fund] = model.params.drop("const")


        self.exposure_df = pd.DataFrame(exposures).T
        return self.exposure_df

    def cluster(self) -> pd.DataFrame:
        if self.exposure_df is None:
            raise RuntimeError("Call build_exposures() first.")


        Z = StandardScaler().fit_transform(self.exposure_df)

        labels = DBSCAN(eps=self.eps, min_samples=self.min_samples).fit_predict(Z)

        self.exposure_df['cluster'] = labels
        return self.exposure_df

    def run(self) -> pd.DataFrame:
        self.build_exposures()
        return self.cluster()


if __name__ == "__main__":

    pipelines = FactorPCA.run_all()


    funds_df = pd.read_excel(
        r"C:\repos\factors\real_estate.xlsx",
        index_col=0,
        parse_dates=True
    )


    mfec = MultiFactorExposureCluster(
        pipelines=pipelines,
        funds_df=funds_df,
        eps=0.6,
        min_samples=3
    )
    result = mfec.run()


    print("\nFund exposures and cluster assignments:\n")
    print(result)

