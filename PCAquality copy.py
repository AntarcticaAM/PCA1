import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use***


quality_tickers = [
    'HSIEQETU Index',   # HSBC Quality Factor Europe Net Total Return Index (USD) — start 2006
    'HSIEQUTU Index',   # HSBC Quality Factor US Net Total Return Index (USD)

    'CGRQPEUQ Index',   # Citi EU Pure Quality — start 1994
    'CGRQPUSQ Index',   # Citi US Pure Quality
    'CGRQPCNQ Index',   # Citi China Pure Quality           third to be deleted brings it to 80%
    'CGRQPAUQ Index',   # Citi AU Pure Quality
    'CGRQPJPQ Index',   # Citi JP Pure Quality

    #'GSPEQUAL Index',   # GS EU Quality — start 2001 first to be deleted 62% to 68%

    'SPXQUT Index',     # S&P 500 Quality U.S. Dollar Gross Total Return Index — start 1993

    'AWPQTE Index',     # FTSE All-World Pure Quality Target Exposure Factor Index — start 1999

    'DBRPAEQU Index',         # DB Asia Equity Quality Factor 2.0 USD Excess Return Index
    'DBRPEEQE Index',         # DB Europe Equity Quality Factor 2.0 EUR Excess Return Index
    'DBRPNEQU Index',         # DB North America Equity Quality Factor 2.0 USD Excess Return Index

    'NQFFQ Index',            # Nasdaq Factor Family US Quality Index

    'R1FQFR Index',           # Russell 1000 Quality Factor Index — start 2017
    'R2FQF Index',            # Russell 2000 Quality Factor Total Return Index — start 2006

    'UBPTQLTY Index',         # UBS L/S Quality Quant Factor — start 2017 second 68% to 72%
    'UBSHTGQG Index',         # UBS HOLT Equity Factor Global Quality USD Gross Total Return Index
]

file_path = r"C:\repos\factors\quality_factors.xlsx"

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
    Canada_weights,
    China_weights,
    Australia_weights,
    Asia_Pacific_weights
)

hsbc_weights_quality = pd.DataFrame({
    'HSIEQETU Index': europe_weights,
    'HSIEQUTU Index': us_weights,
})
citi_weights_quality = pd.DataFrame({
    'CGRQPEUQ Index': europe_weights,
    'CGRQPUSQ Index': us_weights,
    'CGRQPCNQ Index': China_weights,
    'CGRQPAUQ Index': Australia_weights,
    'CGRQPJPQ Index': Japan_weights,
})
DB_weights_quality = pd.DataFrame({
    'DBRPAEQU Index': Asia_Pacific_weights,
    'DBRPEEQE Index': europe_weights,
    'DBRPNEQU Index': us_weights,
})
schemes = {
    "hsbc_weights_quality":{
        'HSIEQETU Index': europe_weights,
        'HSIEQUTU Index': us_weights,
    },
    "citi_weights_quality":{
        'CGRQPEUQ Index': europe_weights,
        'CGRQPUSQ Index': us_weights,
        'CGRQPCNQ Index': China_weights,
        'CGRQPAUQ Index': Australia_weights,
        'CGRQPJPQ Index': Japan_weights,
    },
    "DB_weights_quality":{
        'DBRPAEQU Index': Asia_Pacific_weights,
        'DBRPEEQE Index': europe_weights,
        'DBRPNEQU Index': us_weights,
    },
}
for col_name, weight_dict in schemes.items():
    w = pd.DataFrame(weight_dict)
    w = w.div(w.sum(axis=1), axis=0)
    region = df.loc[:,w.columns].apply(pd.to_numeric, errors='coerce')
    df[col_name] = (region * w).sum(axis=1)
    df.drop(columns=list(w.columns), inplace=True)



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

pc1_returns_quality = df_pcs['PC1']

print(pc1_weights)
#clean the data for msci
#problem with sci beta it does not have the same last day month returns every 4 months