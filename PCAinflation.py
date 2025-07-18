import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   
from sklearn.decomposition import PCA
#*** I need to find a way to just import the ones I want to use***

from weights import (
    europe_weights,
    us_weights,
    Japan_weights,
    developped_exNorthAmerica_weights,
    Canada_weights
)

inflation_tickers = [
    'CSIIGL Index',     # Citi Inflation Surprise Index – Global — start 1999 from 65% to 78% if dropped
    'SBILUU Index',     # FTSE World Inflation-Linked Securities USD — start 2011
    'BTSIIMAI Index',   # Bloomberg IQ Multi-Asset Inflation Index — start 2015
    'MLINFL8 Index',    # BofA Pro Inflation — start year unspecified
    'MLDEFL8 Index',    # BofA Anti-Inflation — start year unspecified
]

file_path = r"C:\repos\factors\inflation_factors.xlsx"

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





BofA_weights_momentum = pd.DataFrame({
    'MLINFL8 Index': us_weights/2, # PRO INFLATION
    'MLDEFL8 Index': us_weights/2, # ANTI INFLATION
})
sum_of_weights_BofA = BofA_weights_momentum.sum(axis=1)
BofA_weights_momentum = BofA_weights_momentum.div(BofA_weights_momentum.sum(axis=1), axis=0)
region_BofA = df.loc[:,list(BofA_weights_momentum)].apply(pd.to_numeric, errors='coerce')
region_BofA = region_BofA[BofA_weights_momentum.columns]


df['BofA_World_Growth'] = (region_BofA * BofA_weights_momentum).sum(axis=1)
df.drop(columns=list(region_BofA), inplace=True) 


print(df)
df = df.dropna()
scaler = StandardScaler()
X_std = scaler.fit_transform(df)


pca = PCA()
pcs = pca.fit_transform(X_std)

pc_cols = [f"PC{i+1}" for i in range(pcs.shape[1])]
df_pcs = pd.DataFrame(pcs, index=df.index, columns=pd.Index(pc_cols))

print(df_pcs.head())
print("Explained variance:", pca.explained_variance_ratio_)

loadings = pca.components_

pc1_weights = pd.Series(
    loadings[0],              
    index=df.columns, 
    name="PC1_weight"
)

pc1_returns_inflation = df_pcs['PC1']

print(pc1_weights)
#clean the data for msci
#problem with sci beta it does not have the same last day month returns every 4 months