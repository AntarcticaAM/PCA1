# PCAonFunds_from_combined.py

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

# ---- 1) Import the ready-made PC1 series -----------------------------------
# PCAs_combined just exposes variables like pc1_returns_growth, pc1_returns_value, ...
from PCAs_combined import (
    pc1_returns_growth,
    pc1_returns_value,
    pc1_returns_quality,
    pc1_returns_inflation,
    pc1_returns_realestate,
    pc1_returns_size,
    pc1_returns_commodity,
    pc1_returns_defensive,
    pc1_returns_crowded,
    pc1_returns_shortvol,
)

# Put them in a dict for convenience
factor_dict = {
    "growth":     pc1_returns_growth,
    "value":      pc1_returns_value,
    "quality":    pc1_returns_quality,
    "inflation":  pc1_returns_inflation,
    "realestate": pc1_returns_realestate,
    "size":       pc1_returns_size,
    "commodity":  pc1_returns_commodity,
    "defensive":  pc1_returns_defensive,
    "crowded":    pc1_returns_crowded,
    "shortvol":   pc1_returns_shortvol,
}

# ---- 2) Load fund prices, convert to returns --------------------------------
prices = pd.read_excel(
    r"C:\repos\factors\johnjohn_funds_performance.xlsx",
    index_col=0, parse_dates=True
)
prices = prices.apply(pd.to_numeric, errors='coerce')
fund_returns = prices.pct_change(fill_method=None).dropna(how='all')

# ---- 3) Build a fund × factor beta matrix -----------------------------------
# Align all factors first:
factors_df = pd.concat(
    [s.rename(name) for name, s in factor_dict.items()],
    axis=1
)
# Ensure unique dates then inner-join with funds
factors_df = factors_df[~factors_df.index.duplicated(keep='first')]
fund_returns = fund_returns[~fund_returns.index.duplicated(keep='first')]

df_all = pd.concat([factors_df, fund_returns], axis=1, join='inner').dropna()

X = sm.add_constant(df_all[factors_df.columns]).astype(float)
betas = {}
for fund in fund_returns.columns:
    y = df_all[fund].astype(float)
    model = sm.OLS(y, X, missing='drop').fit()
    betas[fund] = model.params.drop('const')  # keep only factor slopes

beta_matrix = pd.DataFrame(betas).T  # rows=funds, cols=factors

print("=== Fund × Factor Beta Matrix ===")
print(beta_matrix.round(6))

# ---- 4) Cluster funds on full beta vectors (optional DBSCAN) ----------------
# Standardize betas first
Z = StandardScaler().fit_transform(beta_matrix)
labels = DBSCAN(eps=0.5, min_samples=3).fit_predict(Z)
beta_matrix['cluster'] = labels

print("\n=== Cluster memberships ===")
for cl in sorted(beta_matrix['cluster'].unique()):
    members = beta_matrix.index[beta_matrix['cluster'] == cl]
    print(f"Cluster {cl}: {len(members)} funds")
    print(", ".join(members))

# ---- 5) 2D PCA projection just for plotting ---------------------------------
from sklearn.decomposition import PCA
coords = PCA(n_components=2, random_state=42).fit_transform(Z)

plt.figure(figsize=(9,6))
scatter = plt.scatter(coords[:,0], coords[:,1], c=labels, cmap='tab10', s=55, alpha=0.85)
for i, name in enumerate(beta_matrix.index):
    plt.text(coords[i,0], coords[i,1], name, fontsize=7, alpha=0.7)
plt.xlabel("Exposure PCA 1")
plt.ylabel("Exposure PCA 2")
plt.title("Funds clustered by multi-factor betas (using PCAs_combined)")
plt.colorbar(scatter, label="Cluster")
plt.tight_layout()
plt.show()
