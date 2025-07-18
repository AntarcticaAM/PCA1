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
]

file_path = r"C:\repos\factors\growth_factors1.xlsx"

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
    Australia_weights
)
schemes = {
    "Citi_weights_growth":{
        'CGRQPEUG Index': europe_weights,  # Citi EU Pure Growth — start 1994
        'CGRQPAUG Index': Australia_weights,  # Citi AU Pure Growth — start year unspecified
        'CGRQPJPG Index': Japan_weights,  # Citi JP Pure Growth — start year unspecified
        'CGRQPCNG Index': China_weights,  # Citi China Pure Growth — start year unspecified
        'CGRQPUSG Index': us_weights,  # Citi US Pure Growth — start year unspecified
},

    "SPSG_weights_growth":{
        'SPSG Index': us_weights,  # S&P Small Cap 600/Citigroup Growth Provisional Index — start 2010
        'SPMG Index': us_weights,  # S&P MidCap 400/Citigroup Growth Provisional Index — start 2010
},

    "Barclays_weights_growth":{
        'BXIIGG10 Index': us_weights/2,  # Barclays Golden Growth RC10 Index — start 2005
        'BXIITG10 Index': us_weights/2,  # Barclays Tactical Growth 10% Index — start 2002
},


    "GS_weights_growth":{
        'GSPEMFGR Index': europe_weights,  # GS EU Growth — start 2006
        'GSINGFUS Index': us_weights,  # GS Growth Factor United States Macro Basket — start 2006
},


    "CITIC_weights_growth" :{
        'CCUSTGH Index': us_weights,  # CITIC CLSA US Stable Growth Basket — start 2011
        'CAPSGEU Index': europe_weights,  # The EU Growth Strength Index — start 2011
}
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
pc1_returns_growth = df_pcs['PC1']
print(pc1_weights)
