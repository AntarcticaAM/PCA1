import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from fund_cluster_summary import FundClusterSummary

class FactorClusterer:
    """
    Cluster hedge funds based on their exposure to a single PC1 factor series using DBSCAN,
    and plot the results.
    """

    def __init__(
        self,
        factor_series: pd.Series,
        fund_returns: pd.DataFrame,
        eps: float,
        min_samples: int 
    ):
        self.factor = factor_series.rename('PC1')
        self.funds = fund_returns.copy()
        self.eps = eps
        self.min_samples = min_samples

    def align_data(self):

        self.funds = self.funds[~self.funds.index.duplicated(keep='first')]
        self.factor = self.factor[~self.factor.index.duplicated(keep='first')]

        df_funds = self.funds.reset_index().rename(columns={'index':'Date'})
        df_factor = self.factor.reset_index().rename(columns={'index':'Date'})
        df_all = pd.merge(df_funds, df_factor, on='Date', how='inner')
        df_all = df_all.set_index('Date')

        self.aligned_funds = df_all[self.funds.columns]
        self.aligned_factor = df_all['PC1']


    def compute_exposures(self):
        exposures = {}
        X = sm.add_constant(self.aligned_factor)
        X = X.astype(float)
        for fund in self.aligned_funds.columns:
            y = self.aligned_funds[fund]
            y = pd.to_numeric(y, errors='coerce')
            y_aligned, X_aligned = y.align(X, join='inner')
            model = sm.OLS(y_aligned, X_aligned).fit()
            exposures[fund] = model.params.get('PC1', 0.0)
        self.exposure_df = pd.Series(exposures, name='beta').to_frame()

    def standardize(self):
        scaler = StandardScaler()
        Z = scaler.fit_transform(self.exposure_df[['beta']])
        self.features = pd.DataFrame(Z, index=self.exposure_df.index, columns=['beta_z'])

    def cluster(self):
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        labels = db.fit_predict(self.features)
        self.exposure_df['cluster'] = labels

    def run(self) -> pd.DataFrame:

        self.align_data()
        self.compute_exposures()
        self.standardize()
        self.cluster()
        return self.exposure_df

    def plot_clusters(self, result: pd.DataFrame):


        x = result['beta']
        y = result['cluster']
        plt.figure(figsize=(8, 5))
        catter = plt.scatter(x, y, c=y, cmap='tab10', s=50)
        plt.xlabel('Exposure (beta)')
        plt.ylabel('Cluster Label')
        plt.title('Fund Clusters by Factor Exposure')
        plt.yticks(sorted(result['cluster'].unique()))
        plt.show()

if __name__ == '__main__':
    from classes1 import FactorPCA 
    pipelines = FactorPCA.run_all()

    pc1_growth = pipelines['value'].pc1_returns

    import pandas as pd
    funds_df = pd.read_excel(
        r"C:\repos\factors\quality_factors.xlsx",
        index_col=0,
        parse_dates=True
    )

    clusterer = FactorClusterer(
        factor_series=pc1_growth,
        fund_returns=funds_df,
        eps=0.5 ,
        min_samples=2
    )
    result = clusterer.run()
    clusterer.plot_clusters(result)

    print(result.sort_values('beta'))


if __name__ == "__main__":

    pipelines = FactorPCA.run_all()

    funds_df = pd.read_excel(
        r"C:\repos\factors\real_estate.xlsx",
        index_col=0, parse_dates=True
    )


    summary_builder = FundClusterSummary(
        pipelines=pipelines,
        funds_df=funds_df,
        eps=0.5,
        min_samples=2
    )
    fund_table = summary_builder.build()
    print(fund_table)
    fund_table.to_excel(r"C:\repos\factors\fund_table.xlsx")
