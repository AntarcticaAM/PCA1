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
    'added MS factors but these are not indices'
]

file_path = r"C:\repos\theexcels\quality_factorsfinal.xlsx"

df = pd.read_excel(
    file_path,
    header=0,
    skiprows=[1, 2],
    index_col=0,
    parse_dates=True
)

df = df.ffill()
df = df.apply(lambda c: c.pct_change(fill_method=None) if c.abs().median() > 1 else c)
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
sum_of_weights_hsbc = hsbc_weights_quality.sum(axis=1)
hsbc_weights_quality = hsbc_weights_quality.div(hsbc_weights_quality.sum(axis=1), axis=0)
region_hsbc = df.loc[:,list(hsbc_weights_quality)].apply(pd.to_numeric, errors='coerce')
region_hsbc = region_hsbc[hsbc_weights_quality.columns]
df['hsbc_World_Quality'] = (region_hsbc * hsbc_weights_quality).sum(axis=1)
df.drop(columns=region_hsbc.columns, inplace=True) 

citi_weights_quality = pd.DataFrame({
    'CGRQPEUQ Index': europe_weights,
    'CGRQPUSQ Index': us_weights,
    'CGRQPCNQ Index': China_weights,
    'CGRQPAUQ Index': Australia_weights,
    'CGRQPJPQ Index': Japan_weights,
})
sum_of_weights_citi = citi_weights_quality.sum(axis=1)
citi_weights_quality = citi_weights_quality.div(citi_weights_quality.sum(axis=1), axis=0)
region_citi = df.loc[:,list(citi_weights_quality)].apply(pd.to_numeric, errors='coerce')
region_citi = region_citi[citi_weights_quality.columns]
df['citi_World_Quality'] = (region_citi * citi_weights_quality).sum(axis=1)
df.drop(columns=region_citi.columns, inplace=True) 

MS_weights_quality = pd.DataFrame({
    'MS Factor - US Quality': us_weights,
    'MS Factor - EU Quality': europe_weights,
    'MS Factor - JP Quality': Japan_weights,
    'MS Factor - AxJ Quality': Asia_Pacific_weights - Japan_weights,
})
sum_of_weights_MS = MS_weights_quality.sum(axis=1)
MS_weights_quality = MS_weights_quality.div(MS_weights_quality.sum(axis=1), axis=0)
region_MS = df.loc[:,list(MS_weights_quality)].apply(pd.to_numeric, errors='coerce')
region_MS = region_MS[MS_weights_quality.columns]
df['MS_World_Quality'] = (region_MS * MS_weights_quality).sum(axis=1)
df.drop(columns=region_MS.columns, inplace=True) 

DB_weights_quality = pd.DataFrame({
    'DBRPAEQU Index': Asia_Pacific_weights,        # DB Asia Equity Quality Factor 2.0 USD Excess Return Index
    'DBRPEEQE Index': europe_weights,              # DB Europe Equity Quality Factor 2.0 EUR Excess Return Index
    'DBRPNEQU Index': us_weights + Canada_weights      # DB North America Equity Quality Factor 2.0 USD Excess Return Index
})
sum_of_weights_DB = DB_weights_quality.sum(axis=1)
DB_weights_quality = DB_weights_quality.div(DB_weights_quality.sum(axis=1), axis=0)
region_DB = df.loc[:,list(DB_weights_quality)].apply(pd.to_numeric, errors='coerce')
region_DB = region_DB[DB_weights_quality.columns]
df['DB_World_Quality'] = (region_DB * DB_weights_quality).sum(axis=1)
df.drop(columns=region_DB.columns, inplace=True)

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