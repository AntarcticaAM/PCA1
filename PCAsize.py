import pandas as pd
from sklearn.preprocessing import StandardScaler   
from sklearn.decomposition import PCA
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use***


size_tickers = [
    'CGRQPEUS Index',   # Citi EU Pure Size — start 1994
    'CGRQPAUS Index',   # Citi AU Pure Size — start 1994
    'CGRQPJPS Index',   # Citi JP Pure Size — start year unspecified
    'CGRQPCNS Index',   # Citi China Pure Size — start 1994
    'CGRQPUSS Index',  # Citi US Pure Size — start 1994
    #if I drop citi it goes to 93.3% from 84.1%
    'UBSHTGSN Index',   # UBS HOLT Equity Factor Global Size USD Net Total Return Index — start 2001

    'AWPSTE Index',           # FTSE All-World Pure Size Target Exposure Factor Index — start year unspecified

    'R1FSFR Index',           # Russell 1000 Size Factor Index — start 2017
    'R2FSF Index',            # Russell 2000 Size Factor Total Return Index — start 2006

    'SAW1SZGV Index',         # STOXX Global 1800 Ax Size Gross Return USD — start year unspecified

    'SGEPSBW Index',          # SGI World Size Index — start 2001

    'WUPSL Index',            # FT Wilshire US Large Pure Size Index — start 2017
    'MS Factor - US Size'
]

file_path = r"C:\repos\theexcels\size_factorsfinal.xlsx"

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
    Asia_Pacific_weights,
    Americas_weights
)

Citi_weights_quality = pd.DataFrame({
    'CGRQPEUS Index': europe_weights,
    'CGRQPAUS Index': Australia_weights,
    'CGRQPJPS Index': Japan_weights,
    'CGRQPCNS Index': China_weights,
    'CGRQPUSS Index': us_weights,
})
sum_of_weights_citi = Citi_weights_quality.sum(axis=1)
Citi_weights_quality = Citi_weights_quality.div(Citi_weights_quality.sum(axis=1), axis=0)
region_citi = df.loc[:,list(Citi_weights_quality)].apply(pd.to_numeric, errors='coerce')
region_citi = region_citi[Citi_weights_quality.columns]
df['citi_World_Quality'] = (region_citi * Citi_weights_quality).sum(axis=1)
df.drop(columns=region_citi.columns, inplace=True) 


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
pc1_returns_size = df_pcs['PC1']
print(pc1_weights)