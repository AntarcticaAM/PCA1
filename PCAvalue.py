import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   
from sklearn.decomposition import PCA

from tickers2 import hsbc_weights_value
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use**
value_tickers = [
    "AWPVTE Index",  # FTSE All-World Pure Value Target Exposure Factor Index — start 1999
    "FIDINVLT Index",  # Fidelity International Value Factor Index TR — start 1994
    "GSIPVALL Index",  # GS International Value long — start 2006
    "GSRPEVWG Index",  # GS Tactical Factor Value World Top GTR USD — start 2006
    "GSRPEVWH Index",  # GS Tactical Factor Value World Bottom GTR USD — start 2006
    "NQFFV Index",  # Nasdaq Factor Family US Value Index — start 2002
    "RADMFUVT Index",  # Radcliffe US Value Factor Index TR — start 1990
    "UBSHTGVG Index",  # UBS HOLT Equity Factor Global Value USD Gross Total Return Index — start 2002
    "VFVANV Index",  # Vanguard U.S. Value Factor NAV Index - start 2018
    "CGRQPEUV Index",  # Citi EU Pure Value — start 1994
    "CGRQPUSV Index",  # Citi US Pure Value — start 1994
    "CGRQPJPV Index",  # Citi JP Pure Value — start 1996
    "CGRQPASV Index",  # Citi AsiaexJP Pure Value — start 1996
    "CGRQPAUV Index",  # Citi AU Pure Value — start 1996
    "SPUSCPV Index",  # S&P 1500 Value U.S. Dollar Index — start 1996
    "SPMPV Index",  # S&P MidCap 400 Value U.S. Dollar Index — start 1996
    "R2KPVALP Index",  # Russell 2000 Value Index — start 1997
    "UBXXPVAL Index",  # UBS Factor Value Index — start 2017
    "AWPVTE Index",  # FTSE All-World Pure Value Target Exposure Factor Index — start 2001
    "PVALUEUS Index",  # Bloomberg US Value Factor Index — start 2000jp
    "JVALTR Index",  # JPMorgan US Value Factor Index TR — start 2000
    "MXWO000V Index",  # MSCI World Value Index — start 1974
]
# 1) Load your existing Excel of raw momentum prices
file_path = r"C:\repos\theexcels\value_factorsfinal - Copy.xlsx"
# Assume dates are in the first column and tickers as headers
df = pd.read_excel(
    file_path,
    header=0,
    skiprows=[1, 2 ],
    index_col=0,
    parse_dates=True
)

df = df.ffill()
df = df.apply(lambda c: c.pct_change(fill_method=None) if c.abs().median() > 1 else c)
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

GS_weights_Value = pd.DataFrame({
    'GSRPEVWG Index': us_weights,  # DJEurpslct REIT — start 2004
    'GSRPEVWH Index': us_weights,  # DJAsiaPslct REIT — start 2004
})

sum_of_weights_GS = GS_weights_Value.sum(axis=1)
GS_weights_Value = GS_weights_Value.div(GS_weights_Value.sum(axis=1), axis=0)
region_GS = df.loc[:,list(GS_weights_Value)].apply(pd.to_numeric, errors='coerce')
region_GS = region_GS[GS_weights_Value.columns]
df['GS_World_Value'] = (region_GS * GS_weights_Value).sum(axis=1)
print(df['GS_World_Value'])
df.drop(columns=region_GS.columns, inplace=True)

citi_weights_Value = pd.DataFrame({
    'CGRQPEUV Index': europe_weights,  # DJEurpslct REIT — start 2004
    "CGRQPUSV Index": us_weights,  # Citi US Pure Value — start 1994
    "CGRQPJPV Index": Japan_weights,  # Citi JP Pure Value — start 1996
    "CGRQPASV Index": Asia_Pacific_weights - Japan_weights,  # Citi AsiaexJP Pure Value — start 1996
    "CGRQPAUV Index": Australia_weights,  # Citi AU Pure Value — start 1996
})

sum_of_weights_citi = citi_weights_Value.sum(axis=1)
citi_weights_Value = citi_weights_Value.div(citi_weights_Value.sum(axis=1), axis=0)
region_citi = df.loc[:,list(citi_weights_Value)].apply(pd.to_numeric, errors='coerce')
region_citi = region_citi[citi_weights_Value.columns]
df['Citi_World_Value'] = (region_citi * citi_weights_Value).sum(axis=1)
print(df['Citi_World_Value'])
df.drop(columns=region_citi.columns, inplace=True)

SP_weights_Value = pd.DataFrame({
    "SPUSCPV Index": us_weights,  # S&P 1500 Value U.S. Dollar Index — start 1996
    "SPMPV Index": us_weights,  # S&P MidCap 400 Value U.S. Dollar Index — start 1996
})

sum_of_weights_SP = SP_weights_Value.sum(axis=1)
SP_weights_Value = SP_weights_Value.div(SP_weights_Value.sum(axis=1), axis=0)
region_SP = df.loc[:,list(SP_weights_Value)].apply(pd.to_numeric, errors='coerce')
region_SP = region_SP[SP_weights_Value.columns]
df['SP_World_Value'] = (region_SP * SP_weights_Value).sum(axis=1)
print(df['SP_World_Value'])
df.drop(columns=region_SP.columns, inplace=True)


print(df)
df = df.dropna()
scaler = StandardScaler()
X_std = scaler.fit_transform(df)

# 3) PCA
pca = PCA()
pcs = pca.fit_transform(X_std)

# 4) Build a DataFrame of PC scores
pc_cols = [f"PC{i+1}" for i in range(pcs.shape[1])]
df_pcs = pd.DataFrame(pcs, index=df.index, columns=pd.Index(pc_cols))

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
pc1_returns_value = df_pcs['PC1']
print(pc1_weights)
#clean the data for msci
#problem with sci beta it does not have the same last day month returns every 4 months