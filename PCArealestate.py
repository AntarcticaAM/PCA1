import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA


file_path = r"C:\repos\factors\real_estate.xlsx"
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
    Canada_weights,
    China_weights,
    Australia_weights,
    Asia_Pacific_weights,
    Americas_weights
)

DJ_weights_realestate = pd.DataFrame({
    'DWEURT Index': europe_weights,  # DJEurpslct REIT — start 2004
    'DWAPRT Index': Asia_Pacific_weights,  # DJAsiaPslct REIT — start 2004
    'DWAMRT Index': Americas_weights,  # DJAmrslct REIT — start 2004
})

sum_of_weights_DJ = DJ_weights_realestate.sum(axis=1)
DJ_weights_realestate = DJ_weights_realestate.div(DJ_weights_realestate.sum(axis=1), axis=0)
region_DJ = df.loc[:,list(DJ_weights_realestate)].apply(pd.to_numeric, errors='coerce')
region_DJ = region_DJ[DJ_weights_realestate.columns]
df['DJ_World_Realestate'] = (region_DJ * DJ_weights_realestate).sum(axis=1)
print(df['DJ_World_Realestate'])
df.drop(columns=region_DJ.columns, inplace=True) 


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
pc1_returns_realestate = df_pcs['PC1']

print(pc1_weights)