import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
import numpy as np

class MultiFactorClusterer:
    """
    Automate DBSCAN clustering of hedge funds on multiple PC1 factor series,
    and assign descriptive cluster labels based on beta ranges.
    """
    def __init__(self, pipelines: dict, funds_df: pd.DataFrame,
                 eps: float = 0.5, min_samples: int = 2):
        self.pipelines = pipelines
        self.funds = funds_df.copy()
        self.eps = eps
        self.min_samples = min_samples
        self.results = {}

    def _cluster_factor(self, factor_name: str) -> pd.DataFrame:
        """
        For a given factor PCA pipeline, regress each fund on the factor's PC1 series,
        then z-score the betas and apply DBSCAN to assign cluster labels.
        """
        # Build raw exposures: regress each fund on the single factor
        exposures = {}
        series = self.pipelines[factor_name].pc1_returns.rename(factor_name)
        # Ensure unique dates
        series = series[~series.index.duplicated(keep='first')]
        funds_clean = self.funds[~self.funds.index.duplicated(keep='first')]

        for fund in funds_clean.columns:
            df2 = pd.concat([series, funds_clean[fund]], axis=1, join='inner')
            df2.columns = [factor_name, fund]
            df2 = df2.dropna()
            if df2.empty:
                exposures[fund] = np.nan
                continue
            X = sm.add_constant(df2[factor_name]).astype(float)
            y = df2[fund].astype(float)
            model = sm.OLS(y, X).fit()
            exposures[fund] = model.params[factor_name]

        # Convert to DataFrame
        df_beta = pd.Series(exposures, name='beta').to_frame()

        # 1) Drop NaN betas
        df_clean = df_beta[['beta']].dropna()

        # 2) If fewer than 2 points, skip scaling & clustering
        if len(df_clean) < 2:
            df_beta['beta_z'] = np.nan
            df_beta['cluster'] = -1
            return df_beta

        # 3) Standardize betas
        scaler = StandardScaler()
        zvals = scaler.fit_transform(df_clean[['beta']]).flatten()
        df_beta['beta_z'] = np.nan
        df_beta.loc[df_clean.index, 'beta_z'] = zvals

        # 4) Apply DBSCAN on the z-scores
        db = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        # cluster on df_beta's beta_z column, indexed by df_clean
        labels = db.fit_predict(df_beta.loc[df_clean.index, ['beta_z']])

        # 5) Map labels back (others as noise)
        df_beta['cluster'] = -1
        df_beta.loc[df_clean.index, 'cluster'] = labels

        return df_beta

    def run_all(self) -> dict:
        """
        Run clustering for all factors and return a dict of DataFrames.
        """
        for name in self.pipelines:
            self.results[name] = self._cluster_factor(name)
        return self.results

    def plot_factor(self, factor_name: str):
        """
        Plot cluster assignments for a single factor.
        """
        df = self.results.get(factor_name)
        if df is None:
            raise ValueError(f"No results for factor {factor_name}. Run run_all() first.")

        scatter = plt.scatter(df['beta'], df['cluster'], c=df['cluster'], cmap='tab10')
        for fund, beta, cluster in zip(df.index, df['beta'], df['cluster']):
            plt.text(beta, cluster + 0.02, fund, fontsize=7, ha='center')
        plt.xlabel(f'{factor_name} Exposure (beta)')
        plt.ylabel('Cluster Label')
        plt.title(f'Clusters for {factor_name}')
        plt.yticks(sorted(df['cluster'].unique()))
        plt.colorbar(scatter, label='Cluster')
        plt.grid(True)
        plt.show()

    def plot_all(self):
        """
        Plot cluster assignments for all factors.
        """
        for name in self.pipelines:
            self.plot_factor(name)


