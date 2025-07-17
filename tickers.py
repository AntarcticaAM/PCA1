value_tickers = [
    'HSIEEQUT Index',   # HSBC Quality Factor Europe Net Total Return Index (USD) — start 2007
    'HSIEQUTU Index',   # HSBC Quality Factor US Net Total Return Index (USD) — start 2007
    'CGRQPUSQ Index',   # Citi pure US — start 1995
    'CGRQPEUQ Index',   # Citi pure EU — start 1995
    'CGRQPAUQ Index',   # Citi pure AU — start 1995
    'CGRQPJPQ Index',   # Citi pure JP — start 1995
    'CGRQPASQ Index',   # Citi pure AsiaexJP — start 1995
    'AWPQTE Index',     # FTSE Pure Target Exposure — start 2000
    'DBRPGEQU Index',   # DB Equity Quality Factor 2.0 USD Excess Return Index — start 2000
    'NQFFLQ Index',     # Nasdaq Factor Laggard US Quality Index — start 2000
    'NQFFQ Index',      # Nasdaq Factor Family US Quality Index — start 2000
    'R1FQFR Index',     # Russell 1000 Quality Factor Index — start 2017
    'R2FQF Index',      # Russell 2000 Quality Factor Total Return Index — start 2006
    'UBPTQLTY Index',   # UBS L/S Quality Quant Factor — start 2006
    'UBSHTGQG Index',   # UBS HOLT Equity Factor Global Quality USD Gross Total Return Index — start 2006
    'SPXPV INDEX',      # S&P 500 — start 1996
    'SPUSNPV INDEX',    # S&P 900 — start 1996
    'SPUSCPV INDEX',    # S&P 1500 — start 1996
    'PVALUEUS INDEX',   # Bloom US — start 2000
]
# Crowded factor tickers
crowded_tickers = [
    'CGRBEMCR Index',   # Citi most crowded — start 2017
    'CGRBELCR Index',   # Citi least crowded — start 2017
    'BCSUCROW Index',   # 13F HF crowded 13F — start 2004
    'UBPTCRWD Index',   # World Crowded Longs vs. Crowded Shorts — start 2017
]

# Short vol factor tickers
short_vol_tickers = [
    'FRUSVSUT Index',   # FTSE US Risk Premium Index Series: Low Volatility Short Only Total Return Index — start 2017
    'VIX9D Index',      # Cboe S&P 500 Short Term Volatility Index — start 2011
    'JPRVLAGX Index',   # J.P. Morgan iDex Pure Residual Volatility Short (JPRVLAGX) Index — start 2008
    'ABRXIV Index',     # ABR Enhanced Short Volatility Index — start 2005
    'R1LTELS Index',    # Russell 1000 Pure Low Volatility Target Exposure Factor Long Short Index — start 2012
    'WEIXARB Index',    # Dynamic Short Volatility Futures Index — start 2007
]

# Inflation factor tickers
inflation_tickers = [
    'CSIIGL Index',     # Citi Inflation Surprise Index – Global — start 1999
    'SBILUU Index',     # FTSE World Inflation-Linked Securities USD — start 2011
    'BTSIIMAI Index',   # Bloomberg IQ Multi-Asset Inflation Index — start 2015
    'MLINFL8 Index',    # BofA Pro Inflation — start year unspecified
    'MLDEFL8 Index',    # BofA Anti-Inflation — start year unspecified
]
real_estate_tickers = [
    'CGRBGREI Index',   # Citi Global Real Estate #2016

    'NDUWREIT Index',   # MSCI World Real Estate Net Total Return USD Index 2005

    'APREITUT',         # iEdge APAC REIT Index (Total Return) USD — start 2009
    'WGREIT',           # Wilshire Global REIT Index — start 2003

    'SOLWR30',          # Solactive World REIT 30 Index — start 2014

    'BXIIGRU0',         # Shiller Barclays Global REITs Value Gross TR USD Index — start 2004

    'SXGREL',           # STOXX Global 1800 Real Estate Index USD — starts end-2008

    'SPDL60UP',         # S&P World Real Estate (Sector) Index (USD) — start 2016

    'RGUSF06',          # Russell 3000 Index Real Estate — start 2013
    'R250035T',         # Russell 2500 Real Estate Total Return Index — start 2009

    'IXRE',             # Real Estate Select Sector Index — start 2011

    'NTDREP',           # NORTHERN TRUST DEVELOPED REAL ESTATE PRICE INDEX (USD) — start 2016

    'MREIGRUP',         # Morningstar Global Markets REIT PR USD — start 2004

    'MQ5CREAP',         # MerQube US Large Cap Real Estate Index — start 2002


    'IIDKRYT',          # Invesco Developed Markets ex-Japan All Cap REIT Total Return Index (JPY) — start 2006
    'IIJRYT',           # Invesco Japan All Cap REIT Total Return Index (JPY) — start 2006

    'REITGLEU',         # GPR 250 REIT WORLD INDEX/ EUR — start 1998

    'DWLDREP',          # Euronext Developed World Real Estate Total Market — start 2009

    'DWRTF',            # Dow Jones Wilsire REIT Index Full Cap — start 1998

    'BXIICCRT',         # DigitalBridge Fundamental US Real Estate Index Total Return — start 2003

    'DWMFRT',           # DJMEAslct REIT — start 2005
    'DWEURT',           # DJEurpslct REIT — start 2004
    'DWAPRT',           # DJAsiaPslct REIT — start 2004
    'DWAMRT',           # DJAmrslct REIT — start 2004

    'CRSPRE1',          # CRSP US Real Estate & REITs Index — start 2010

    'SZ399367',         # CNI Real Estate 50 Index — start 2009

    'MLEUREAL',         # BofA EU Real Estate — start 1999

    'WLSTR Index',      # Bloomberg World Real Estate Large, Mid & Small Cap Total Return Index — start 2002
    'SREITWHT',         # BMI Developed REIT JPY-Hedged TR — start 1988
    'IMOBBV',           # BM&FBOVESPA Real Estate Index — start 2007

    'SAP10XP',          # 10X SA Property Index — start 2015
]
momentum_tickers = [
    'SP500MUP Index',    # S&P 500 Momentum U.S. Dollar Index — start 1971

    'AWPMTE Index',      # FTSE All-World Pure Momentum Target Exposure Factor Index — start 1999

    'CIISPMUT Index',    # Citi Pure Price Momentum US Long-Short TR Index — start 2003
    'CIISPMJT Index',    # Citi Pure Price Momentum Japan Long-Short Net TR Index — start 2005
    'CIISPMET Index',    # Citi Price Momentum Pure Europe TR Index — start 1998

    'SBEXMHMN Index',    # SciBeta Eurozone High-Momentum Multi-Strat Net Return — start 2001
    'SBJXMHMN Index',    # SciBeta Japan High-Momentum Multi-Strat Net Return — start year unspecified
    'SBUXMLMN Index',    # SciBeta USA High-Momentum Multi-Strat Net Return — start year unspecified

    'GSISEMJG Index',    # GS TFS Momentum Japan Top GTR JPY — start 2015
    'GSPEMOMO Index',    # GS EU High Beta Momentum — start 2006
    'GSCNDMOS Index',    # GS CND US Momentum Short — start 2010
    'GSCNDMOL Index',    # GS CND US Momentum Long — start year unspecified

    'BXIIMMUE Index',    # Barclays US Momentum Equity Market Hedged Index ER — start 2004
    'BXIIMMJD Index',    # Barclays Japan Momentum Equity Market Hedged Index USD ER — start 2004
    'BXIIMMED Index',    # Barclays Eurozone Momentum Equity Market Hedged Index USD ER — start 2003

    'HSIEMUPU Index',    # HSBC Momentum Factor US Price Return Index (USD) — start 2006
    'HSIEMEPU Index',    # HSBC Momentum Factor Europe Price Return Index (USD) — start 2006

    'UBPTMOMO Index',    # UBS L/S Momentum Quant Factor — start 2016

    'AQRMOMLC',          # AQR Momentum Index — start 2002

    'BNPIF3AM',          # BNP Paribas Alpha Momentum Index — start 2001

    'BSMOU',             # BSE Momentum Index (USD) — start 2004

    'DJTMNMO',           # Dow Jones U.S. Thematic Market Neutral Momentum Index — start 2000

    'R2FPMF',            # Russell 2000 Momentum Factor Total Return Index — start 2006
    'R1FPMFR',           # Russell 1000 Momentum Factor Index — start 2016


    'M1WOMOM',           # MSCI World Momentum Net Total Return USD Index — start 1973
    'IIGMT',             # Invesco Global Price Momentum Total Return Index — start 2001

    'MMO50P',            # Morningstar US Momentum Target 50 USD PR — start 2002
    'MSDMUP',            # Morningstar Developed Markets ex-North America Target Momentum PR USD — start 2013
    'MCMOP',             # Morningstar Canada Momentum Index PR CAD — start 1999

    'NQFFM',             # Nasdaq Factor Family US Momentum Index — start 2006
    'ISMGMU',            # iSTOXX MUTB Global Momentum 600 Gross Return USD — start 2002
    'SAW1MOGV',          # STOXX Global 1800 Ax Momentum Gross Return USD — start 2001
    'SPIMPC',            # SPI Momentum Premium® CHF (Total Return) — start 2003

    'RBCUMTML',          # RBC US Momentum Long Index USD GROSS — start 2006
    'RBCUMTMS',          # RBC US Momentum Short Index USD GROSS — start 2006

    'SGEPMBW',           # SGI World Momentum Index — start 2001
]
growth_tickers = [
    'SGX Index',         # S&P 500 Growth Index — start 1991
    'CGRQPEUG Index',    # Citi EU Pure Growth — start 1994
    'CGRQPAUG Index',    # Citi AU Pure Growth — start year unspecified
    'CGRQPJPG Index',    # Citi JP Pure Growth — start year unspecified
    'CGRQPCNG Index',    # Citi China Pure Growth — start year unspecified
    'CGRQPUSG Index',    # Citi US Pure Growth — start year unspecified

    'CGUSECOG',          # Economic Growth Equity Implied Macro Factor — start 1999

    'SPSG Index',        # S&P Small Cap 600/Citigroup Growth Provisional Index — start 2010
    'SPMG Index',        # S&P MidCap 400/Citigroup Growth Provisional Index — start 2010

    'MXWO000G Index',    # MSCI World Growth Index — start 1974

    'BXIIGG10 Index',    # Barclays Golden Growth RC10 Index — start 2005
    'BXIITG10 Index',    # Barclays Tactical Growth 10% Index — start 2002

    'UBPTGWTH Index',    # UBS L/S Growth Quant Factor — start 2016

    'GSXUSGRO Index',    # GS Secular Growth — start 2005
    'GSPEMFGR Index',    # GS EU Growth — start 2006
    'GSINGFUS',          # GS Growth Factor United States Macro Basket — start 2006

    'AWORLDSG Index',    # FTSE All-World Growth Index — start 2017

    'WORLDGN Index',     # Bloomberg World Large & Mid Cap Growth Net Return Index — start 2015
    'RUTP50TR',          # Russell Top 50 Index Total Return — start 2004

    'INDX6146',          # iNDEX World Growth — start 2016

    'RU10USPG',          # Russell 1000 USD Price Return Growth Index — start 2005
    'RU20GRTR',          # Russell 2000 Total Return Growth Index — start year unspecified
    'RU30GRTR',          # Russell 3000 Total Return Growth Index — start year unspecified
    'RU25USPG',          # Russell 2500 USD Price Return Growth Index — start year unspecified

    'SBVGIGEN',          # Solactive BBVA ixS Global Inclusive Growth EUR Index NTR — start 2009
    'NFGGI',             # New Frontier Global Growth Index — start 2003
    'BSDFU',             # BSE Diversified Financials Revenue Growth Index (USD) — start 2005

    'BBEQUGUN',          # BBVA US Sector Neutral Growth Index NTR — start 2005

    'BNPIFEGU',          # BNP Paribas Growth US Index — start 2005

    'CAFGTR',            # Pacer US Small Cap Cash Cows Growth Leaders Index — start year unspecified
    'COWGTR1',           # Pacer US Large Cap Cash Cows Growth Leaders Total Return Index — start year unspecified

    'CAPSGEU',           # The EU Growth Strength Index — start 2011
    'CCUSTGH',           # CITIC CLSA US Stable Growth Basket — start 2011

    'DWLG',              # Dow Jones US Large-Cap Growth Total Stock Market Index — start year unspecified
    'DWSMDG',            # Dow Jones US Low-Cap Growth Total Stock Market Index USD — start year unspecified
    'DWMG',              # Dow Jones US Mid-Cap Growth Total Stock Market Index — start year unspecified

    'FCIWAGN',           # FCI WORLD AC GROWTH 600 (NET) Index — start 2011

    'GRINNT',            # Victory International Free Cash Flow Growth Net Total Return Index — start year unspecified

    'HZIGB',             # Horizon Growth Buffer Index us — start year unspecified

    'IIDGROW',           # Invesco Dynamic Growth Index — start 2006

    'MSGGTMGU',          # Morningstar Global Growth Target Market Exposure GR USD — start 2007
]
quality_tickers = [
    'HSIEQETU Index',   # HSBC Quality Factor Europe Net Total Return Index (USD) — start 2006
    'HSIEQUTU Index',   # HSBC Quality Factor US Net Total Return Index (USD)

    'CGRQPEUQ Index',   # Citi EU Pure Quality — start 1994
    'CGRQPUSQ Index',   # Citi US Pure Quality
    'CGRQPCNQ Index',   # Citi China Pure Quality
    'CGRQPAUQ Index',   # Citi AU Pure Quality
    'CGRQPJPQ Index',   # Citi JP Pure Quality

    'GSPEQUAL Index',   # GS EU Quality — start 2001

    'SPXQUT Index',     # S&P 500 Quality U.S. Dollar Gross Total Return Index — start 1993

    'AWPQTE Index',     # FTSE All-World Pure Quality Target Exposure Factor Index — start 1999

    'DBRPAEQU',         # DB Asia Equity Quality Factor 2.0 USD Excess Return Index
    'DBRPEEQE',         # DB Europe Equity Quality Factor 2.0 EUR Excess Return Index
    'DBRPNEQU',         # DB North America Equity Quality Factor 2.0 USD Excess Return Index

    'NQFFQ',            # Nasdaq Factor Family US Quality Index

    'R1FQFR',           # Russell 1000 Quality Factor Index — start 2017
    'R2FQF',            # Russell 2000 Quality Factor Total Return Index — start 2006

    'UBPTQLTY',         # UBS L/S Quality Quant Factor — start 2017
    'UBSHTGQG',         # UBS HOLT Equity Factor Global Quality USD Gross Total Return Index
]
credit_tickers = [
    'CFIIXPVU',   # FTSE Nomura CaRD World Government Bond XOPV Index — start 2006
]
commodity_tickers = [
    'BCOMTR',    # Bloomberg Commodity Index Total Return — start 1960
    'RICIGLTR',  # Rogers International Commodity Index Total Return — start 1997
    'BCCFSKAP',  # Barclays Commodity BCCFSKAP Index — start 2006
    'BXIIC4RP',  # Barclays Diversified Commodity 4% ARP Index — start 2007
    'CCUDLPED',  # Citi CCUDLPED Commodity Index — start 1998
    'EWCI',      # S&P GSCI Equal Weight Commodity Sector — start 2008
    'PACITR',    # Picard Angst Commodity Index – Total Return — start 1997
    'SOLCOSUS',  # Solactive Commodities Select Index — start 2007
    'UISECC55',  # UBS Inflation Commodity Portfolio — start 2007
]
defensive_tickers = [
    'FIDUSDFP',   # Fidelity U.S. Equity Defensive Factor Index PR — start 1994
    'DBGLD2BU',   # DB Equity Defensive Factor 2.0 - USD - Bottom Index — start 1999
    'DBGLD2TU',   # DB Equity Defensive Factor 2.0 - USD - Top Index — start 1999
    'PU704853',   # MSCI ACWI Defensive Sectors Price USD Index — start 2020
    'RUDDFLCT',   # FTSE Developed Defensive Total Return Index — start 1996
    'MXEMDEFC',   # EMU Defensive Sectors Capped USD Price Return — start 2014
    'FCFDF',      # Abacus FCF Defensive Equity Leaders Index — start 1997
]
size_tickers = [
    'CGRQPEUS Index',   # Citi EU Pure Size — start 1994
    'CGRQPAUS Index',   # Citi AU Pure Size — start 1994
    'CGRQPJPS Index',   # Citi JP Pure Size — start year unspecified
    'CGRQPCNS Index',   # Citi China Pure Size — start 1994
    'CGRQPUSS Index',  # Citi US Pure Size — start 1994

    'UBSHTGSN Index',   # UBS HOLT Equity Factor Global Size USD Net Total Return Index — start 2001

    'FDFSF Index',      # FTSE Developed Size Factor Index TR — start 2000
    'FEFSF Index',      # FTSE Emerging Size Factor Index TR — start 2000

    'AWPSTE',           # FTSE All-World Pure Size Target Exposure Factor Index — start year unspecified

    'R1FSFR',           # Russell 1000 Size Factor Index — start 2017
    'R2FSF',            # Russell 2000 Size Factor Total Return Index — start 2006

    'SAW1SZGV',         # STOXX Global 1800 Ax Size Gross Return USD — start year unspecified

    'SGEPSBW',          # SGI World Size Index — start 2001

    'WUPSL',            # FT Wilshire US Large Pure Size Index — start 2017
]
citi_weights_value = {
    'CGRQPUSQ Index': 0.63,
    'CGRQPEUQ Index': 0.16,
    'CGRQPAUQ Index': 0.02,
    'CGRQPJPQ Index': 0.05,
    'CGRQPASQ Index': 0.14,
}
hsbc_weights_value = {
    'HSIEEQUT Index':0.63,   # HSBC Quality Factor Europe Net Total Return Index (USD) — start 2007
    'HSIEQUTU Index':0.16,   # HSBC Quality Factor US Net Total Return Index (USD) — start 2007
}

Nasdaq_weights_value = {
    'NQFFLQ Index':0.63/2,  # Nasdaq Factor Laggard US Quality Index — start 2000
    'NQFFQ Index':0.63/2,  # Nasdaq Factor Family US Quality Index — start 2000
}
Bloomberg_weights_value = {
    'PVALUEUS INDEX':0.63,  # Bloom US — start 2000
}
rusell1000_weights_value = {
    'R1FQFR Index':0.63,  # Russell 1000 Quality Factor Index — start 2017
}
ruswll2000_weights_value = {
    'R2FQF Index':0.63,  # Russell 2000 Quality Factor Total Return Index — start 2006
}
sansp500_weights_value = {
        'SPXPV INDEX':0.63,  # S&P 500 — start 1996
    }
sandp900_weights_value = {
    'SPUSNPV INDEX':0.63,  # S&P 900 — start 1996
}
citi_weights_crowded ={
    'CGRBEMCR Index':0.5,  # Citi most crowded — start 2017
    'CGRBELCR Index':0.5,  # Citi least crowded — start 2017
}
FTSEUS_weights_value = {
    'SPUSNPV INDEX':0.63,  # S&P 900 — start 1996
}
SANDP5900_weights_shortvol = {
    'SPUSNPV INDEX':0.63,  # S&P 900 — start 1996
}
SandP500_weights_shortvol = {
    'VIX9D Index':0.63,  # Cboe S&P 500 Short Term Volatility Index — start 2011
}
BofA_weights_inflation = {
    'MLINFL8 Index':0.5,  # BofA Pro Inflation — start year unspecified
    'MLDEFL8 Index':0.5,  # BofA Anti-Inflation — start year unspecified
}
# MerQube (US vs. Funds)
merqube_weights_realestate = {
    'MQ5CREAP':0.63,   # MerQube US Large Cap Real Estate
}

# Invesco (Dev Mkts ex-Japan vs. Japan)
invesco_weights_realestate = {
    'IIDKRYT':0.95,   # Invesco Dev Mkts ex-Japan All Cap REIT (JPY)
    'IIJRYT':0.05,   # Invesco Japan All Cap REIT (JPY)
}

# Morningstar (7 regional REIT series)

# Dow Jones Multi‐Region Select
DJ_weights_realestate = {
    'DWEURT': 0.16,   # DJ Eurpslct REIT
    'DWAPRT': 0.19,   # DJ AsiaPslct REIT
    'DWAMRT': 0.65,   # DJ Amrslct REIT
}

# Solactive (Global vs. 30)
# STOXX (Europe vs. Global)

# Russell US (3000 vs. 2500)
Russell2500_weights_realestate = {

    'R250035T':0.63,   # Russell 2500 Real Estate Total Return
}
Russell3000_weights_realestate = {
    'RGUSF06':0.63,   # Russell 3000 Real Estate
}
CRSP_SP_IXRE_weights_realestate = {
    'CRSPRE1':0.63  ,   # CRSP US Real Estate & REITs Index
}

# Other multi-region (Bloomberg vs. BMI vs. Brazil vs. 10X)
Other_weights_realestate = {
    'SREITWHT': 0.95 , # BMI Developed REIT JPY-Hedged TR
}
other1_weights_realestate = {
    'USREITS':0.63,          # US REITs iNDEX — start 2016
}
digitale_weights_realestate = {
    'BXIICCRT':0.63,  # DigitalBridge Fundamental US Real Estate Index Total Return — start 2003
}
bofa_weights_realestate = {
    'MLEUREAL':0.16,  # BofA EU Real Estate — start 1999
}

# 1) Citi regionals
Citi_weights_momentum = {
    'CIISPMUT Index': 0.63,  # US
    'CIISPMJT Index': 0.05,  # Japan
    'CIISPMET Index': 0.16,  # Europe
    'CITSPMAT INDEX':0.14,
}

# 2) SciBeta multi-region
SciBeta_weights_momentum = {
    'SBEXMHMN Index': 0.16,  # Eurozone High-Momentum
    'SBJXMHMN Index': 0.05,  # Japan High-Momentum
    'SBUXMLMN Index': 0.63,  # USA High-Momentum
}

# 3) GS multi-region
GS_weights_momentum = {
    'GSISEMJG Index': 0.05,  # Japan Top GTR JPY
    'GSPEMOMO Index': 0.16,  # EU High Beta Momentum
    'GSCNDMOS Index': 0.315,  # CND US Short
    'GSCNDMOL Index': 0.315,  # CND US Long
}

# 4) Barclays multi-region
Barclays_weights_momentum = {
    'BXIIMMUE Index': 0.63,  # US Market Hedged ER
    'BXIIMMJD Index': 0.05,  # Japan Market Hedged ER
    'BXIIMMED Index': 0.16,  # Eurozone Market Hedged ER
}

# 5) HSBC multi-region
HSBC_weights_momentum = {
    'HSIEMUPU Index': 0.63,  # US Price Return
    'HSIEMEPU Index': 0.16,  # Europe Price Return
}
Dow_weights_momentum = {
    'DJTMNMO':0.63,  # Dow Jones U.S. Thematic Market Neutral Momentum Index — start 2000
}

# 6) Russell US (3000 vs. 2000)
Russell1000_weights_momentum = {
    'R1FPMFR Index': 0.63,   # Russell 1000 Momentum
}
Russell2000_weights_momentum = {
    'R2FPMF Index': 0.63,    # Russell 2000 Momentum
}
# 7) Morningstar multi-region
Morningstar_weights_momentum = {
    'MMO50P': 0.63,          # US Momentum Target 50
    'MSDMUP': 0.35,          # Dev Mkts ex-NA Momentum
    'MCMOP': 0.02,           # Canada Momentum
}

# 8) RBC US (Long vs. Short)
RBC_weights_momentum = {
    'RBCUMTML': 0.315,        # US Momentum Long
    'RBCUMTMS': 0.315,        # US Momentum Short
}
NASDAQ_weights_momentum = {
    'NQFFM':0.63,  # Nasdaq Factor Family US Momentum Index — start 2006
}
# 1) Citi (5 regionals)
Citi_weights_growth = {
    'CGRQPEUG Index': 0.16,  # Citi EU Pure Growth
    'CGRQPAUG Index': 0.02,  # Citi AU Pure Growth
    'CGRQPJPG Index': 0.05,  # Citi JP Pure Growth
    'CGRQPASG Index': 0.14,  # asia without japan
    'CGRQPUSG Index': 0.63,  # Citi US Pure Growth
}

# 2) Barclays (2 series)
Barclays_weights_growth = {
    'BXIIGG10 Index': 0.5,  # Barclays Golden Growth RC10
    'BXIITG10 Index': 0.5,  # Barclays Tactical Growth 10%
}

# 3) GS (3 series)
GS_weights_growth = {
    'GSPEMFGR Index': 0.14,  # GS EU Growth

}

# 4) Russell US (4 regionals)
Russell1000_weights_growth = {
    'RU10USPG': 0.63,  # Russell 1000 USD Price Return Growth
}
Russell2000_weights_growth ={
    'RU20GRTR': 0.63,  # Russell 2000 Total Return Growth
}
Russell3000_weights_growth ={
    'RU30GRTR': 0.63,  # Russell 3000 Total Return Growth
}
Russell_weights_growth ={
    'RU25USPG': 0.63,  # Russell 2500 USD Price Return Growth
}

# 5) Pacer (2 series)
Pacer_weights_growth = {
    'CAFGTR':  0.315,   # Pacer US Small Cap Cash Cows Growth Leaders
    'COWGTR1': 0.315,   # Pacer US Large Cap Cash Cows Growth Leaders
}

# 6) Dow Jones Thematic (3 series)
DJ_growth_weights = {
    'DWLG':   0.63/3,    # Dow Jones US Large-Cap Growth
    'DWSMDG': 0.63/3,    # Dow Jones US Low-Cap Growth
    'DWMG':   0.63/3,    # Dow Jones US Mid-Cap Growth
}
# 1) HSBC (Europe vs. US variants)
HSBC_weights_quality = {
    'HSIEQETU Index': 0.16,   # Europe Net Total Return
    'HSIEQUTU Index': 0.63,   # US Net Total Return
    # (you could also include HSIEQUGU, HSIEQUPU, HSIEQU1U, HSIEQU2U here if you wish)
}

# 2) Citi (5 regionals)
Citi_weights_quality = {
    'CGRQPEUQ Index': 0.16,   # Citi EU Pure Quality
    'CGRQPUSQ Index': 0.63,   # Citi US Pure Quality
    'CGRQPASQ Index': 0.14,   # asia ex jp Pure Quality
    'CGRQPAUQ Index': 0.02,   # Citi AU Pure Quality
    'CGRQPJPQ Index': 0.05,   # Citi JP Pure Quality
}

# 3) Deutsche Bank (Asia vs. Europe vs. North America)
DB_weights_quality = {
    'DBRPAEQU':   0.19,       # DB Asia Equity Quality Factor
    'DBRPEEQE':   0.16,       # DB Europe Equity Quality Factor
    'DBRPNEQU':   0.63,       # DB North America Equity Quality Factor
}
russel1000_weights_quality = {
'R1FQFR':0.63,
}
russel2000_weights_quality = {
    'R2FQF':0.63,  # Russell 2000 Quality Factor Total Return Index — start 2006
}
GS_weights_quality ={
    'GSPEQUAL Index':0.16,  # GS EU Quality — start 2001
}
SANDP_weights_quality ={
    'SPXQUT Index',  # S&P 500 Quality U.S. Dollar Gross Total Return Index — start 1993
}
fidelity_defensive_weights = {
    'FIDUSDFP':0.63,   # Fidelity U.S. Equity Defensive Factor Index PR — start 1994
}
# 1) Citi (5 regionals)
Citi_weights_size = {
    'CGRQPEUS Index': 0.16,  # Citi EU Pure Size
    'CGRQPAUS Index': 0.02,  # Citi AU Pure Size
    'CGRQPJPS Index': 0.05,  # Citi JP Pure Size
    'CGRQPASS Index': 0.14,  # Citi asia ex jp Pure Size
    'CGRQPUSS Index': 0.63,  # Citi US Pure Size
}

# 2) UBS HOLT (global only – already worldwide, no dict needed)
#    'UBSHTGSN Index' stays as-is

# 3) FTSE (2 regionals)
FTSE_weights_size = {
    'FDFSF Index': 0.98,     # FTSE Developed Size Factor
    'FEFSF Index': 0.02,     # FTSE Emerging Size Factor
}

# 4) FTSE All-World Pure Size (already worldwide – no dict needed)
#    'AWPSTE' stays as-is

# 5) Russell US (2 regionals)
Russell1000_weights_size = {
    'R1FSFR': 0.63,          # Russell 1000 Size Factor
}
Russell1000_weights_size = {
    'R2FSF': 0.63,           # Russell 2000 Size Factor
}
