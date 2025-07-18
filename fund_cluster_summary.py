import pandas as pd
from multi_factor_clusterer import MultiFactorClusterer

class FundClusterSummary:
    """
    Summarizes, for each fund, its cluster assignments across multiple factors
    and the beta ranges defining each cluster.

    Usage:
        from classes1 import FactorPCA
        from fund_cluster_summary import FundClusterSummary

        # 1) Run PCA pipelines to get PC1s
        pipelines = FactorPCA.run_all()
        # 2) Load hedge fund returns DataFrame
        funds_df = pd.read_excel(
            r"C:\repos\factors\hedge_fund_returns.xlsx",
            index_col=0, parse_dates=True
        )
        # 3) Instantiate summary builder
        summary = FundClusterSummary(
            pipelines=pipelines,
            funds_df=funds_df,
            eps=0.5,
            min_samples=2
        )
        # 4) Build summary table
        fund_table = summary.build()
        print(fund_table)
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
        """
        Runs clustering and constructs a summary DataFrame:
        index = fund names
        columns per factor:
            - '<factor>_cluster': numeric cluster label
            - '<factor>_label': descriptive cluster name (beta range)
        """
        # Run clustering for all factors
        self.results = self.clusterer.run_all()

        # Initialize summary with fund list
        funds = list(self.funds_df.columns)
        summary = pd.DataFrame(index=funds)

        # For each factor, merge cluster and label into summary
        for factor, df in self.results.items():
            # df has index=fund, columns=['beta', 'cluster', 'cluster_name']
            summary[f'{factor}_cluster'] = df['cluster']
            summary[f'{factor}_label'] = df['cluster_name']

        return summary
