import pandas as pd
from multi_factor_clusterer import MultiFactorClusterer

class FundClusterSummary:
    """
    Summarizes, for each fund, its cluster assignments across multiple factors
    and the beta ranges defining each cluster.

    """

    def __init__(
        self,
        pipelines: dict,
        funds_df: pd.DataFrame,
        eps: float = 0.5,
        min_samples: int = 2
    ):
        self.pipelines = pipelines
        self.funds_df = funds_df.copy()
        self.eps = eps
        self.min_samples = min_samples
        self.clusterer = MultiFactorClusterer(
            pipelines=self.pipelines,
            funds_df=self.funds_df,
            eps=self.eps,
            min_samples=self.min_samples
        )
        self.results = None

    def build(self) -> pd.DataFrame:


        self.results = self.clusterer.run_all()


        funds = list(self.funds_df.columns)
        summary = pd.DataFrame(index=funds)


        for factor, df in self.results.items():

            summary[f'{factor}_cluster'] = df['cluster']
            summary[f'{factor}_label'] = df['cluster_name']

        return summary
