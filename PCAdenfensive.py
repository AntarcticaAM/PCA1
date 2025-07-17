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
# 1) Load your existing Excel of raw momentum prices
file_path = r"C:\repos\factors\defensive_factors copy.xlsx"
# Assume dates are in the first column and tickers as headers
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



# 1) Load the CSV
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

# 3) PCA
pca = PCA()
pcs = pca.fit_transform(X_std)

# 4) Build a DataFrame of PC scores
pc_cols = [f"PC{i+1}" for i in range(pcs.shape[1])]
df_pcs = pd.DataFrame(pcs, index=df.index, columns=pc_cols)

# 5) (Optional) Inspect
print(df_pcs.head())
print("Explained variance:", pca.explained_variance_ratio_)

loadings = pca.components_

# 2) make a Series for PC1’s weights
pc1_weights = pd.Series(
    loadings[0],              # the first row of components_
    index=df.columns, # your 8 index names
    name="PC1_weight"
)

print(pc1_weights)
#clean the data for msci
#problem with sci beta it does not have the same last day month returns every 4 months