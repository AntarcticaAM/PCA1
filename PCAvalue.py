import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA

from tickers2 import hsbc_weights_value
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use**
value_tickers = [
    'HSIEQEUT Index',   # HSBC Quality Factor Europe Net Total Return Index (USD) — start 2007
    'HSIEQUTU Index',   # HSBC Quality Factor US Net Total Return Index (USD) — start 2007
    'CGRQPUSQ Index',   # Citi pure US — start 1995
    'CGRQPEUQ Index',   # Citi pure EU — start 1995
    'CGRQPAUQ Index',   # Citi pure AU — start 1995
    'CGRQPJPQ Index',   # Citi pure JP — start 1995
    'CGRQPASQ Index',   # Citi pure AsiaexJP — start 1995
    'AWPQTE Index',     # FTSE Pure Target Exposure — start 2000
    'DBRPGEQU Index',   # DB Equity Quality Factor 2.0 USD Excess Return Index — start 2000 if removed 65% to 70% first one to be
    'NQFFLQ Index',     # Nasdaq Factor Laggard US Quality Index — start 2000
    'NQFFQ Index',      # Nasdaq Factor Family US Quality Index — start 2000
    'R2FQF Index',      # Russell 2000 Quality Factor Total Return Index — start 2006
    'UBPTQLTY Index',   # UBS L/S Quality Quant Factor — start 2017
    'UBSHTGQG Index',   # UBS HOLT Equity Factor Global Quality USD Gross Total Return Index — start 2006
    'SPXPV INDEX',      # S&P 500 — start 1996
    'SPUSNPV INDEX',    # S&P 900 — start 1996
    'SPUSCPV INDEX',    # S&P 1500 — start 1996
    'PVALUEUS INDEX',   # Bloom US — start 2000 ~ second to be 70 to 75%
]
# 1) Load your existing Excel of raw momentum prices
file_path = r"C:\repos\factors\value_factors2.xlsx"
# Assume dates are in the first column and tickers as headers
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

hsbc_weights_value = pd.DataFrame({
    'HSIEQETU Index': europe_weights,
    'HSIEQUTU Index': us_weights,
})
sum_of_weights_hsbc = hsbc_weights_value.sum(axis=1)
hsbc_weights_value = hsbc_weights_value.div(hsbc_weights_value.sum(axis=1), axis=0)
region_hsbc = df[list(hsbc_weights_value)].apply(pd.to_numeric, errors='coerce')
region_hsbc = region_hsbc[hsbc_weights_value.columns]

# Element-wise multiply and sum across regions for each date
df['hsbc_World_Growth'] = (region_hsbc * hsbc_weights_value).sum(axis=1)
df.drop(columns=region_hsbc.columns, inplace=True) 


citi_weights_value = pd.DataFrame({
    'CGRQPUSQ Index': us_weights,   # Citi pure US — start 1995
    'CGRQPEUQ Index': europe_weights,   # Citi pure EU — start 1995
    'CGRQPAUQ Index': Australia_weights,   # Citi pure AU — start 1995
    'CGRQPJPQ Index': Japan_weights,   # Citi pure JP — start 1995
    'CGRQPASQ Index': Asia_Pacific_weights - Japan_weights,   # Citi pure AsiaexJP — start 1995
})
sum_of_weights_citi = citi_weights_value.sum(axis=1)
citi_weights_value = citi_weights_value.div(citi_weights_value.sum(axis=1), axis=0)
region_citi = df[list(citi_weights_value)].apply(pd.to_numeric, errors='coerce')
region_citi = region_citi[citi_weights_value.columns]

# Element-wise multiply and sum across regions for each date
df['citi_World_value'] = (region_citi * citi_weights_value).sum(axis=1)
df.drop(columns=region_citi.columns, inplace=True) 


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