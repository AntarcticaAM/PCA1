import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use***


momentum_tickers = [
    'SP500MUP Index',    # S&P 500 Momentum U.S. Dollar Index — start 1971

    'AWPMTE Index',      # FTSE All-World Pure Momentum Target Exposure Factor Index — start 1999

    'SBEXMHMN Index',    # SciBeta Eurozone High-Momentum Multi-Strat Net Return — start 2001
    'SBJXMHMN Index',    # SciBeta Japan High-Momentum Multi-Strat Net Return — start year unspecified
    'SBUXMLMN Index',    # SciBeta USA High-Momentum Multi-Strat Net Return — start year unspecified

    'GSPEMOMO Index',    # GS EU High Beta Momentum — start 2006
    'GSCNDMOS Index',    # GS CND US Momentum Short — start 2010
    'GSCNDMOL Index',    # GS CND US Momentum Long — start year unspecified

    'BXIIMETE Index',    # Barclays Eurozone Momentum Equity TR EUR Index start 2001
    'BXIIMJTJ Index',    # Barclays Japan Momentum Equity TR JPY Index
    'BXIIMUTU Index',    # Barclays US Momentum Equity TR USD Index



    'AQRMOMLC Index',          # AQR Momentum Index — start 2002


    'R2FPMF Index',            # Russell 2000 Momentum Factor Total Return Index — start 2006


    'M1WOMOM Index',           # MSCI World Momentum Net Total Return USD Index — start 1973
    'IIGMT Index',             # Invesco Global Price Momentum Total Return Index — start 2001

    'MMO50P Index',            # Morningstar US Momentum Target 50 USD PR — start 2002
    'MSDMUP Index',            # Morningstar Developed Markets ex-North America Target Momentum PR USD — start 2013
    'MCMOP Index',             # Morningstar Canada Momentum Index PR CAD — start 1999

    'NQFFM Index',             # Nasdaq Factor Family US Momentum Index — start 2006
    'ISMGMU Index',            # iSTOXX MUTB Global Momentum 600 Gross Return USD — start 2002
    'SAW1MOGV Index',          # STOXX Global 1800 Ax Momentum Gross Return USD — start 2001

    'RBCUMTML Index',          # RBC US Momentum Long Index USD GROSS — start 2006
    'RBCUMTMS Index',          # RBC US Momentum Short Index USD GROSS — start 2006

    'SGEPMBW Index',           # SGI World Momentum Index — start 2001
]

file_path = r"C:\repos\theexcels\momentum_factors144.xlsx"

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

Sci_weights_momentum = pd.DataFrame({
    'SBEXMHMN Index': europe_weights,
    'SBJXMHMN Index': Japan_weights,
    'SBUXMLMN Index': us_weights
})
sum_of_weights_Sci = Sci_weights_momentum.sum(axis=1)
Sci_weights_momentum = Sci_weights_momentum.div(Sci_weights_momentum.sum(axis=1), axis=0)
region_Sci = df.loc[:,list(Sci_weights_momentum)].apply(pd.to_numeric, errors='coerce')
region_hsbc = region_Sci[Sci_weights_momentum.columns]
df['Sci_World_Momentum'] = (region_hsbc * Sci_weights_momentum).sum(axis=1)
df.drop(columns=region_Sci.columns, inplace=True)

GS_weights_momentum = pd.DataFrame({
    'GSPEMOMO Index': europe_weights,
    'GSCNDMOS Index': us_weights/2,
    'GSCNDMOL Index': us_weights/2,
})
sum_of_weights_GS = GS_weights_momentum.sum(axis=1)
GS_weights_momentum = GS_weights_momentum.div(GS_weights_momentum.sum(axis=1), axis=0)
region_GS = df.loc[:,list(GS_weights_momentum)].apply(pd.to_numeric, errors='coerce')
region_GS = region_GS[GS_weights_momentum.columns]
df['GS_World_Momentum'] = (region_GS * GS_weights_momentum).sum(axis=1)
df.drop(columns=region_GS.columns, inplace=True)

Barclays_weights_momentum = pd.DataFrame({
    'BXIIMETE Index': europe_weights,
    'BXIIMJTJ Index': Japan_weights,
    'BXIIMUTU Index': us_weights,
})
sum_of_weights_Barclays = Barclays_weights_momentum.sum(axis=1)
Barclays_weights_momentum = Barclays_weights_momentum.div(Barclays_weights_momentum.sum(axis=1), axis=0)
region_Barclays = df.loc[:,list(Barclays_weights_momentum)].apply(pd.to_numeric, errors='coerce')
region_Barclays = region_Barclays[Barclays_weights_momentum.columns]
df['Barclays_World_Momentum'] = (region_Barclays * Barclays_weights_momentum).sum(axis=1)
df.drop(columns=region_Barclays.columns, inplace=True)

Morningstar_weights_momentum = pd.DataFrame({
    'MMO50P Index': us_weights,
    'MSDMUP Index': developped_exNorthAmerica_weights,
    'MCMOP Index': Canada_weights,
})
sum_of_weights_Morningstar = Morningstar_weights_momentum.sum(axis=1)
Morningstar_weights_momentum = Morningstar_weights_momentum.div(Morningstar_weights_momentum.sum(axis=1), axis=0)
region_Morningstar = df.loc[:,list(Morningstar_weights_momentum)].apply(pd.to_numeric, errors='coerce')
region_Morningstar = region_Morningstar[Morningstar_weights_momentum.columns]
df['Morningstar_World_Momentum'] = (region_Morningstar * Morningstar_weights_momentum).sum(axis=1)
df.drop(columns=region_Morningstar.columns, inplace=True)

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

pc1_returns_momentum = df_pcs['PC1']

print(pc1_weights)