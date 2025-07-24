# cluster_betas.py

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from classes1 import FactorPCA
from fund_factor_exposure import FundFactorExposure

def main():
    # 1) Build all PC1 factor pipelines
    pipelines = FactorPCA.run_all()

    # 2) Load price data & convert to returns
    prices = pd.read_excel(
        r"C:\repos\factors\johnjohn_funds_performance.xlsx",
        index_col=0,
        parse_dates=True
    )
    # ensure all columns are floats (coerce any unparseable to NaN)
    prices = prices.apply(pd.to_numeric, errors='coerce')
    # form simple pct-change returns (no forward‐fill), drop all‐NaN rows
    returns_df = prices.pct_change(fill_method=None).dropna(how='all')
    returns_df = prices.pct_change().dropna(how='all')

    # 3) Compute the fund × factor beta matrix
    analyzer    = FundFactorExposure(pipelines, returns_df)
    exposures_df = analyzer.analyze_all()  # shape = (n_funds × n_factors)

    # 4) Cluster in N-dimensional β-space
    kmeans = KMeans(n_clusters=4, random_state=42)
    labels = kmeans.fit_predict(exposures_df)

    # 5) Reduce to 2D for visualization
    pca    = PCA(n_components=2, random_state=42)
    coords = pca.fit_transform(exposures_df)

    # 6) Plot
    plt.figure(figsize=(10,6))
    scatter = plt.scatter(
        coords[:,0], coords[:,1],
        c=labels, cmap='tab10', s=60, alpha=0.8
    )
    plt.title("Funds clustered by multi-factor betas (PCA projection)")
    plt.xlabel("Exposure PCA 1")
    plt.ylabel("Exposure PCA 2")
    plt.colorbar(scatter, label="Cluster label")

    # annotate each point with its ticker
    for i, ticker in enumerate(exposures_df.index):
        plt.text(
            coords[i,0], coords[i,1], ticker,
            fontsize=7, alpha=0.7
        )

    plt.tight_layout()
    plt.show()

    # 7) Print cluster membership
    exposures_df['cluster'] = labels
    for cl in sorted(exposures_df['cluster'].unique()):
        members = exposures_df.index[exposures_df['cluster']==cl].tolist()
        print(f"\nCluster {cl} ({len(members)} funds):")
        print(", ".join(members))

if __name__ == "__main__":
    main()
