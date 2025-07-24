import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use***


commodity_tickers = [
    'BCOMTR Index',    # Bloomberg Commodity Index Total Return — start 1960
    'RICIGLTR Index',  # Rogers International Commodity Index Total Return — start 1997
    #'BCCFSKAP Index',  # Barclays Commodity BCCFSKAP Index — start 2006 last one to delete goes from 72.5% to 82.8% the other tow can not be taken into account
    #'BXIIC4RP Index',  # Barclays Diversified Commodity 4% ARP Index — start 2007
    'CCUDLPED Index',  # Citi CCUDLPED Commodity Index — start 1998
    'EWCI Index',      # S&P GSCI Equal Weight Commodity Sector — start 2008
    'PACITR Index',    # Picard Angst Commodity Index – Total Return — start 1997
    'SOLCOSUS Index',  # Solactive Commodities Select Index — start 2007
    #'UISECC55 Index',  # UBS Inflation Commodity Portfolio — start 2007
]
# 1) Load your existing Excel of raw momentum prices
file_path = r"C:\repos\theexcels\commodity_factorsfinal.xlsx"
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

pc1_returns_commodity = df_pcs['PC1']
print(pc1_weights)
