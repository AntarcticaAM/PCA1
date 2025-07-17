import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   
from sklearn.decomposition import PCA
#*** I need to find a way to just import the ones I want to use***

crowded_tickers = [
    'CGRBEMCR Index',   # Citi most crowded — start 2017
    'CGRBELCR Index',   # Citi least crowded — start 2017
    'BCSUCROW Index',   # 13F HF crowded 13F — start 2004
    'UBPTCRWD Index',   # World Crowded Longs vs. Crowded Shorts — start 2017  by dropping goes from 75% to 89%
]

file_path = r"C:\repos\factors\crowded_factors.xlsx"

df = pd.read_excel(
    file_path,
    header=0,
    skiprows=[1, 2],
    index_col=0,
    parse_dates=True
)

df = df.ffill()
df = df.pct_change()
print(df)

df = df[(df != 0).all(axis=1)]



from weights import (
    europe_weights,
    us_weights,
    Japan_weights,
    developped_exNorthAmerica_weights,
    Canada_weights
)

print(df)
df = df.dropna()
scaler = StandardScaler()
X_std = scaler.fit_transform(df)


pca = PCA()
pcs = pca.fit_transform(X_std)

pc_cols = [f"PC{i+1}" for i in range(pcs.shape[1])]
df_pcs = pd.DataFrame(pcs, index=df.index, columns=pc_cols)

print(df_pcs.head())
print("Explained variance:", pca.explained_variance_ratio_)

loadings = pca.components_

pc1_weights = pd.Series(
    loadings[0],              
    index=df.columns, 
    name="PC1_weight"
)

print(pc1_weights)