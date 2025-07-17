import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   
from sklearn.decomposition import PCA
#*** I need to find a way to just import the ones I want to use***

short_vol_tickers = [
    'FRUSVSUT Index',   # FTSE US Risk Premium Index Series: Low Volatility Short Only Total Return Index — start 2017
    'VIX9D Index',      # Cboe S&P 500 Short Term Volatility Index — start 2011
    'JPRVLAGX Index',   # J.P. Morgan iDex Pure Residual Volatility Short (JPRVLAGX) Index — start 2008
    'ABRXIV Index',     # ABR Enhanced Short Volatility Index — start 2005
    'R1LTELS Index',    # Russell 1000 Pure Low Volatility Target Exposure Factor Long Short Index — start 2012 from 60% to 72.5% if dropped
    'WEIXARB Index',    # Dynamic Short Volatility Futures Index — start 2007
]

file_path = r"C:\repos\factors\short_vol_factors.xlsx"

df = pd.read_excel(
    file_path,
    header=0,
    skiprows=[1, 2 ],
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
    Canada_weights,
    China_weights,
    Australia_weights,
    Asia_Pacific_weights,
    Americas_weights
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
#clean the data for msci
#problem with sci beta it does not have the same last day month returns every 4 months