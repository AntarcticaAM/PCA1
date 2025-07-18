import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

class MultiFactorClusterer:
    """
    Automate DBSCAN clustering of hedge funds on multiple PC1 factor series,
    and assign descriptive cluster names based on beta ranges.
    """
    def __init__(
        self,
        pipelines: dict,
        funds_df: pd.DataFrame,
        eps: float = 0.5,
        min_samples: int = 2
    ):
        self.pipelines = pipelines
        self.funds = funds_df.copy()
        self.eps = eps
        self.min_samples = min_samples
        self.results = {}

    def _cluster_factor(self, factor_name: str) -> pd.DataFrame:

        pc1 = self.pipelines[factor_name].pc1_returns.rename('PC1')

        funds = self.funds[~self.funds.index.duplicated(keep='first')]
        series = pc1[~pc1.index.duplicated(keep='first')]

        df_f = funds.reset_index().rename(columns={'index':'Date'})
        df_s = series.reset_index().rename(columns={'index':'Date'})
        df_all = pd.merge(df_f, df_s, on='Date', how='inner').set_index('Date')

        funds_aligned = df_all[funds.columns]
        pc1_aligned = df_all['PC1']


        exposures = {}
        X = sm.add_constant(pc1_aligned).astype(float)
        for fund in funds_aligned.columns:
            y = pd.to_numeric(funds_aligned[fund], errors='coerce')
            y_a, X_a = y.align(X, join='inner')
            if len(y_a) == 0:
                exposures[fund] = 0.0
            else:
                model = sm.OLS(y_a, X_a).fit()
                exposures[fund] = model.params.get('PC1', 0.0)

        df = pd.Series(exposures, name='beta').to_frame()

        scaler = StandardScaler()
        df['beta_z'] = scaler.fit_transform(df[['beta']])
        
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        df['cluster'] = db.fit_predict(df[['beta_z']])

        ranges = df.groupby('cluster')['beta'].agg(min='min', max='max').reset_index()
       
        def make_label(r):
            lo, hi, cl = r['min'], r['max'], r['cluster']
            if cl == -1:
                return f"{factor_name}: Noise ({lo:.2f}–{hi:.2f})"
            return f"{factor_name}: β∈[{lo:.2f},{hi:.2f}]"
        ranges['cluster_name'] = ranges.apply(make_label, axis=1)
        label_map = dict(zip(ranges['cluster'], ranges['cluster_name']))
        df['cluster_name'] = df['cluster'].map(label_map)
        df.drop(columns=['beta_z'], inplace=True)
        return df

    def run_all(self) -> dict:

        for name in self.pipelines:
            self.results[name] = self._cluster_factor(name)
        return self.results

    def plot_factor(self, factor_name: str):
        """
        Plot beta vs. cluster with labels for a given factor.
        """
        df = self.results.get(factor_name)
        if df is None:
            raise ValueError(f"No results for factor '{factor_name}'. Run run_all() first.")
        plt.figure(figsize=(8,5))
        scatter = plt.scatter(df['beta'], df['cluster'], c=df['cluster'], cmap='tab10', s=50)
        for fund, x, y in zip(df.index, df['beta'], df['cluster']):
            plt.text(x, y + 0.02, fund, fontsize=7, ha='center')
        plt.xlabel(f'{factor_name} Exposure (beta)')
        plt.ylabel('Cluster Label')
        plt.title(f'Clusters for {factor_name}')
        plt.yticks(sorted(df['cluster'].unique()))
        plt.colorbar(scatter, label='Cluster')
        plt.grid(True)
        plt.show()

    def plot_all(self):

        for name in self.pipelines:
            self.plot_factor(name)

