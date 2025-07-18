import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA

real_estate_tickers = [
    'CGRBGREI Index',   # Citi Global Real Estate #2016

    'NDUWREIT Index',   # MSCI World Real Estate Net Total Return USD Index 2005

    'APREITUT Index',         # iEdge APAC REIT Index (Total Return) USD — start 2009
    'WGREIT Index',           # Wilshire Global REIT Index — start 2003

    'SOLWR30 Index',          # Solactive World REIT 30 Index — start 2014

    'BXIIGRU0 Index',         # Shiller Barclays Global REITs Value Gross TR USD Index — start 2004

    'SXGREL Index',           # STOXX Global 1800 Real Estate Index USD — starts end-2008

    'SPDL60UP Index',         # S&P World Real Estate (Sector) Index (USD) — start 2016

    'RGUSF06 Index',          # Russell 3000 Index Real Estate — start 2013
    'R250035T Index',         # Russell 2500 Real Estate Total Return Index — start 2009

    'IXRE Index',             # Real Estate Select Sector Index — start 2011

    'NTDREP Index',           # NORTHERN TRUST DEVELOPED REAL ESTATE PRICE INDEX (USD) — start 2016

    'MREIGRUP Index',         # Morningstar Global Markets REIT PR USD — start 2004

    'MQ5CREAP Index',         # MerQube US Large Cap Real Estate Index — start 2002


    'IIDKRYT Index',          # Invesco Developed Markets ex-Japan All Cap REIT Total Return Index (JPY) — start 2006
    'IIJRYT Index',           # Invesco Japan All Cap REIT Total Return Index (JPY) — start 2006

    'REITGLEU Index',         # GPR 250 REIT WORLD INDEX/ EUR — start 1998

    'DWLDREP Index',          # Euronext Developed World Real Estate Total Market — start 2009

    'DWRTF Index',            # Dow Jones Wilsire REIT Index Full Cap — start 1998

    'BXIICCRT Index',         # DigitalBridge Fundamental US Real Estate Index Total Return — start 2003

    'DWEURT Index',           # DJEurpslct REIT — start 2004
    'DWAPRT Index',           # DJAsiaPslct REIT — start 2004
    'DWAMRT Index',           # DJAmrslct REIT — start 2004

    'CRSPRE1 Index',          # CRSP US Real Estate & REITs Index — start 2010

    'SZ399367 Index',         # CNI Real Estate 50 Index — start 2009

    'MLEUREAL Index',         # BofA EU Real Estate — start 1999

    'WLSTR Index',      # Bloomberg World Real Estate Large, Mid & Small Cap Total Return Index — start 2002
    'SREITWHT Index',         # BMI Developed REIT JPY-Hedged TR — start 1988
    'IMOBBV Index',           # BM&FBOVESPA Real Estate Index — start 2007

    'SAP10XP Index',          # 10X SA Property Index — start 2015
]

file_path = r"C:\repos\factors\real_estate.xlsx"

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