import pandas as pd
from xbbg import blp
from sklearn.preprocessing import StandardScaler   # to standardize your returns
from sklearn.decomposition import PCA
      # the PCA implementation
#*** I need to find a way to just import the ones I want to use***

growth_tickers = [
    'SGX Index',         # S&P 500 Growth Index — start 1991
    'CGRQPEUG Index',    # Citi EU Pure Growth — start 1994
    'CGRQPAUG Index',    # Citi AU Pure Growth — start year unspecified
    'CGRQPJPG Index',    # Citi JP Pure Growth — start year unspecified
    'CGRQPCNG Index',    # Citi China Pure Growth — start year unspecified
    'CGRQPUSG Index',    # Citi US Pure Growth — start year unspecified

    #'CGUSECOG Index',          # Economic Growth Equity Implied Macro Factor — start 1999

    'SPSG Index',        # S&P Small Cap 600/Citigroup Growth Provisional Index — start 2010
    'SPMG Index',        # S&P MidCap 400/Citigroup Growth Provisional Index — start 2010

    'MXWO000G Index',    # MSCI World Growth Index — start 1974

    'BXIIGG10 Index',    # Barclays Golden Growth RC10 Index — start 2005
    'BXIITG10 Index',    # Barclays Tactical Growth 10% Index — start 2002

    #'UBPTGWTH Index',    # UBS L/S Growth Quant Factor — start 2016

    'GSXUSGRO Index',    # GS Secular Growth — start 2005
    'GSPEMFGR Index',    # GS EU Growth — start 2006
    'GSINGFUS Index',          # GS Growth Factor United States Macro Basket — start 2006

    'AWORLDSG Index',    # FTSE All-World Growth Index — start 2017

    'WORLDGN Index',     # Bloomberg World Large & Mid Cap Growth Net Return Index — start 2015
    'RUTP50TR Index',          # Russell Top 50 Index Total Return — start 2004

    'INDX6146 Index',          # iNDEX World Growth — start 2016

    'RU10USPG Index',          # Russell 1000 USD Price Return Growth Index — start 2005
    'RU20GRTR Index',          # Russell 2000 Total Return Growth Index — start year unspecified
    'RU30GRTR Index',          # Russell 3000 Total Return Growth Index — start year unspecified
    'RU25USPG Index',          # Russell 2500 USD Price Return Growth Index — start year unspecified

    'SBVGIGEN Index',          # Solactive BBVA ixS Global Inclusive Growth EUR Index NTR — start 2009
    'NFGGI Index',             # New Frontier Global Growth Index — start 2003
    'BSDFU Index',             # BSE Diversified Financials Revenue Growth Index (USD) — start 2005

    'BBEQUGUN Index',          # BBVA US Sector Neutral Growth Index NTR — start 2005

    'BNPIFEGU Index',          # BNP Paribas Growth US Index — start 2005

    'CAFGTR Index',            # Pacer US Small Cap Cash Cows Growth Leaders Index — start year unspecified
    'COWGTR1 Index',           # Pacer US Large Cap Cash Cows Growth Leaders Total Return Index — start year unspecified

    'CAPSGEU Index',           # The EU Growth Strength Index — start 2011
    'CCUSTGH Index',           # CITIC CLSA US Stable Growth Basket — start 2011

    'DWLG Index',              # Dow Jones US Large-Cap Growth Total Stock Market Index — start year unspecified
    'DWSMDG Index',            # Dow Jones US Low-Cap Growth Total Stock Market Index USD — start year unspecified
    'DWMG Index',              # Dow Jones US Mid-Cap Growth Total Stock Market Index — start year unspecified

    'FCIWAGN Index',           # FCI WORLD AC GROWTH 600 (NET) Index — start 2011

    'GRINNT Index',            # Victory International Free Cash Flow Growth Net Total Return Index — start year unspecified

    'HZIGB Index',             # Horizon Growth Buffer Index us — start year unspecified

    'IIDGROW Index',           # Invesco Dynamic Growth Index — start 2006

    'MSGGTMGU Index',          # Morningstar Global Growth Target Market Exposure GR USD — start 2007
    'now also features ms factors but these are not indices'
]

file_path = r"C:\repos\theexcels\growth_factorsfinal.xlsx"

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
    Asia_Pacific_weights
)

Citi_weights_growth = pd.DataFrame({
    'CGRQPEUG Index': europe_weights,  # Citi EU Pure Growth — start 1994
    'CGRQPAUG Index': Australia_weights,  # Citi AU Pure Growth — start year unspecified
    'CGRQPJPG Index': Japan_weights,  # Citi JP Pure Growth — start year unspecified
    'CGRQPCNG Index': China_weights,  # Citi China Pure Growth — start year unspecified
    'CGRQPUSG Index': us_weights,  # Citi US Pure Growth — start year unspecified
})
sum_of_weights_Citi = Citi_weights_growth.sum(axis=1)

Citi_weights_growth = Citi_weights_growth.div(Citi_weights_growth.sum(axis=1), axis=0)


region_Citi = df.loc[:,list(Citi_weights_growth)].apply(pd.to_numeric, errors='coerce')
region_Citi = region_Citi[Citi_weights_growth.columns]


df['Citi_World_Growth'] = (region_Citi * Citi_weights_growth).sum(axis=1)
df.drop(columns=list(region_Citi), inplace=True) 

SPSG_weights_growth = pd.DataFrame({
    'SPSG Index': us_weights,  # S&P Small Cap 600/Citigroup Growth Provisional Index — start 2010
    'SPMG Index': us_weights,  # S&P MidCap 400/Citigroup Growth Provisional Index — start 2010
})
sum_of_weights_SPSG = SPSG_weights_growth.sum(axis=1)
SPSG_weights_growth = SPSG_weights_growth.div(SPSG_weights_growth.sum(axis=1), axis=0)


region_SPSG = df.loc[:,list(SPSG_weights_growth)].apply(pd.to_numeric, errors='coerce')
region_SPSG = region_SPSG[SPSG_weights_growth.columns]

# Element-wise multiply and sum across regions for each date
df['SPSG_World_Growth'] = (region_SPSG * SPSG_weights_growth).sum(axis=1)

df.drop(columns=region_SPSG.columns, inplace=True) 

Barclays_weights_growth = pd.DataFrame({
    'BXIIGG10 Index': us_weights/2,  # Barclays Golden Growth RC10 Index — start 2005
    'BXIITG10 Index': us_weights/2,  # Barclays Tactical Growth 10% Index — start 2002
})
sum_of_weights_Barclays = Barclays_weights_growth.sum(axis=1)
Barclays_weights_growth = Barclays_weights_growth.div(Barclays_weights_growth.sum(axis=1), axis=0)
region_Barclays = df.loc[:,list(Barclays_weights_growth)].apply(pd.to_numeric, errors='coerce')
region_Barclays = region_Barclays[Barclays_weights_growth.columns]
df['Barclays_World_Growth'] = (region_Barclays * Barclays_weights_growth).sum(axis=1)

df.drop(columns=region_Barclays.columns, inplace=True) 


GS_weights_growth = pd.DataFrame({
    'GSPEMFGR Index': europe_weights,  # GS EU Growth — start 2006
    'GSINGFUS Index': us_weights,  # GS Growth Factor United States Macro Basket — start 2006
})
sum_of_weights_GS = GS_weights_growth.sum(axis=1)
GS_weights_growth = GS_weights_growth.div(GS_weights_growth.sum(axis=1), axis=0)
region_GS = df.loc[:,list(GS_weights_growth)].apply(pd.to_numeric, errors='coerce')
region_GS = region_GS[GS_weights_growth.columns]
df['GS_World_Growth'] = (region_GS * GS_weights_growth).sum(axis=1)
df.drop(columns=region_GS.columns, inplace=True) 


CITIC_weights_growth = pd.DataFrame({
    'CCUSTGH Index': us_weights,  # CITIC CLSA US Stable Growth Basket — start 2011
    'CAPSGEU Index': europe_weights,  # The EU Growth Strength Index — start 2011
})
sum_of_weights_CITIC = CITIC_weights_growth.sum(axis=1)
CITIC_weights_growth = CITIC_weights_growth.div(CITIC_weights_growth.sum(axis=1), axis=0)
region_CITIC = df.loc[:,list(CITIC_weights_growth)].apply(pd.to_numeric, errors='coerce')
region_CITIC = region_CITIC[CITIC_weights_growth.columns]
df['CITIC_World_Growth'] = (region_CITIC * CITIC_weights_growth).sum(axis=1)
df.drop(columns=region_CITIC.columns, inplace=True) 

MS_weights_growth = pd.DataFrame({
    'MS Factor - US GROWTH': us_weights,  # CITIC CLSA US Stable Growth Basket — start 2011
    'MS Factor - EU Growth': europe_weights,
    'MS Factor - JP Growth': Japan_weights,
    'MS Factor - AxJ Growth': Asia_Pacific_weights - Japan_weights,
})
sum_of_weights_MS = MS_weights_growth.sum(axis=1)
MS_weights_growth = MS_weights_growth.div(MS_weights_growth.sum(axis=1), axis=0)
region_MS = df.loc[:,list(MS_weights_growth)].apply(pd.to_numeric, errors='coerce')
region_MS = region_MS[MS_weights_growth.columns]
df['MS_World_Growth'] = (region_MS * MS_weights_growth).sum(axis=1)
df.drop(columns=region_MS.columns, inplace=True)

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
pc1_returns_growth = df_pcs['PC1']
print(pc1_weights)
print(pc1_returns_growth)
#clean the data for msci
#problem with sci beta it does not have the same last day month returns every 4 months