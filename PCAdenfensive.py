import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use***


defensive_tickers = [
    'FIDUSDFP Index',   # Fidelity U.S. Equity Defensive Factor Index PR — start 1994
    'DBGLD2BU Index',   # DB Equity Defensive Factor 2.0 - USD - Bottom Index — start 1999
    'DBGLD2TU Index',   # DB Equity Defensive Factor 2.0 - USD - Top Index — start 1999
    'PU704853 Index',   # MSCI ACWI Defensive Sectors Price USD Index — start 2020
    'RUDDFLCT Index',   # FTSE Developed Defensive Total Return Index — start 1996
    'MXEMDEFC Index',   # EMU Defensive Sectors Capped USD Price Return — start 2014
    #'FCFDF Index',      # Abacus FCF Defensive Equity Leaders Index — start 1997 brings from 74.5% to 86.45%
]

file_path = r"C:\repos\theexcels\defensive_factorsfinal - Copy.xlsx"

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
df_pcs = pd.DataFrame(pcs, index=df.index, columns=pd.Index(pc_cols))

loadings = pca.components_
pc1_weights = pd.Series(
    loadings[0],              
    index=df.columns, 
    name="PC1_weight"
)
print("Explained variance:", pca.explained_variance_ratio_)
pc1_returns_defensive = df_pcs['PC1']
print(pc1_weights)