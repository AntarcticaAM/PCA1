from xbbg import blp
import blpapi
from blpapi import SessionOptions, Session, Service, Request, Event, Message
import pandas as pd
import numpy as np

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
df_momentum = blp.bdh(
    tickers=momentum_tickers,
    flds='PX_LAST',
    start_date='2014-01-01',
    periodicitySelection='MONTHLY' 
)
df_momentum.to_excel("momentum_factors.xlsx",
            sheet_name="Pure momentum",
            index=True
)

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

df_real_estate = blp.bdh(
    tickers=real_estate_tickers,
    flds='PX_LAST',
    start_date='2018-01-01',
    periodicitySelection='MONTHLY' 

)
inflation_tickers = [
    'CSIIGL Index',     # Citi Inflation Surprise Index – Global — start 1999
    'SBILUU Index',     # FTSE World Inflation-Linked Securities USD — start 2011
    'BTSIIMAI Index',   # Bloomberg IQ Multi-Asset Inflation Index — start 2015
    'MLINFL8 Index',    # BofA Pro Inflation — start year unspecified
    'MLDEFL8 Index',    # BofA Anti-Inflation — start year unspecified
]

df_inflation = blp.bdh(
    tickers=inflation_tickers,
    flds='PX_LAST',
    start_date='2016-01-01',
    periodicitySelection='MONTHLY' 
)
df_inflation.to_excel("inflation_factors.xlsx",
            sheet_name="Pure inflation",
            index=True
)
crowded_tickers = [
    'CGRBEMCR Index',   # Citi most crowded — start 2017
    'CGRBELCR Index',   # Citi least crowded — start 2017
    'BCSUCROW Index',   # 13F HF crowded 13F — start 2004
    'UBPTCRWD Index',   # World Crowded Longs vs. Crowded Shorts — start 2017
]
df_crowded = blp.bdh(
    tickers=crowded_tickers,
    flds='PX_LAST',
    start_date='2018-01-01',
    periodicitySelection='MONTHLY' 
)
df_crowded.to_excel("crowded_factors.xlsx",
            sheet_name="Pure crowded",
            index=True
)
value_tickers = [
    'HSIEQUT Index',   # HSBC Quality Factor Europe Net Total Return Index (USD) — start 2007
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
    'R2FQF Index',      # Russell 2000 Quality Factor Total Return Index — start 2006
    'UBPTQLTY Index',   # UBS L/S Quality Quant Factor — start 2006
    'UBSHTGQG Index',   # UBS HOLT Equity Factor Global Quality USD Gross Total Return Index — start 2006
    'SPXPV INDEX',      # S&P 500 — start 1996
    'SPUSNPV INDEX',    # S&P 900 — start 1996
    'SPUSCPV INDEX',    # S&P 1500 — start 1996
    'PVALUEUS INDEX',   # Bloom US — start 2000
]
df_value = blp.bdh(
    tickers=value_tickers,
    flds='PX_LAST',
    start_date='2008-01-01',
    periodicitySelection='MONTHLY' 
)
df_value.to_excel("value_factors.xlsx",
            sheet_name="Pure value",
            index=True
)
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

    'DBRPAEQU Index',         # DB Asia Equity Quality Factor 2.0 USD Excess Return Index
    'DBRPEEQE Index',         # DB Europe Equity Quality Factor 2.0 EUR Excess Return Index
    'DBRPNEQU Index',         # DB North America Equity Quality Factor 2.0 USD Excess Return Index

    'NQFFQ Index',            # Nasdaq Factor Family US Quality Index

    'R1FQFR Index',           # Russell 1000 Quality Factor Index — start 2017
    'R2FQF Index',            # Russell 2000 Quality Factor Total Return Index — start 2006

    'UBPTQLTY Index',         # UBS L/S Quality Quant Factor — start 2017
    'UBSHTGQG Index',         # UBS HOLT Equity Factor Global Quality USD Gross Total Return Index
]

df_quality = blp.bdh(
    tickers=quality_tickers,
    flds='PX_LAST',
    start_date='2018-01-01',
    periodicitySelection='MONTHLY' 
)
df_quality.to_excel("quality_factors.xlsx",
            sheet_name="Pure quality",
            index=True
)
commodity_tickers = [
    'BCOMTR Index',    # Bloomberg Commodity Index Total Return — start 1960
    'RICIGLTR Index',  # Rogers International Commodity Index Total Return — start 1997
    'BCCFSKAP Index',  # Barclays Commodity BCCFSKAP Index — start 2006
    'BXIIC4RP Index',  # Barclays Diversified Commodity 4% ARP Index — start 2007
    'CCUDLPED Index',  # Citi CCUDLPED Commodity Index — start 1998
    'EWCI Index',      # S&P GSCI Equal Weight Commodity Sector — start 2008
    'PACITR Index',    # Picard Angst Commodity Index – Total Return — start 1997
    'SOLCOSUS Index',  # Solactive Commodities Select Index — start 2007
    'UISECC55 Index',  # UBS Inflation Commodity Portfolio — start 2007
]
df_commodity = blp.bdh(
    tickers=commodity_tickers,
    flds='PX_LAST',
    start_date='2009-01-01',
    periodicitySelection='MONTHLY' 
)
df_commodity.to_excel("commodity_factors.xlsx",
            sheet_name="Pure commodity",
            index=True
)

defensive_tickers = [
    'FIDUSDFP Index',   # Fidelity U.S. Equity Defensive Factor Index PR — start 1994
    'DBGLD2BU Index',   # DB Equity Defensive Factor 2.0 - USD - Bottom Index — start 1999
    'DBGLD2TU Index',   # DB Equity Defensive Factor 2.0 - USD - Top Index — start 1999
    'PU704853 Index',   # MSCI ACWI Defensive Sectors Price USD Index — start 2020
    'RUDDFLCT Index',   # FTSE Developed Defensive Total Return Index — start 1996
    'MXEMDEFC Index',   # EMU Defensive Sectors Capped USD Price Return — start 2014
    'FCFDF Index',      # Abacus FCF Defensive Equity Leaders Index — start 1997
]
df_defensive = blp.bdh(
    tickers=defensive_tickers,
    flds='PX_LAST',
    start_date='2015-01-01',
    periodicitySelection='MONTHLY' 
)
df_defensive.to_excel("defensive_factors.xlsx",
            sheet_name="Pure defensive",
            index=True
)

size_tickers = [
    'CGRQPEUS Index',   # Citi EU Pure Size — start 1994
    'CGRQPAUS Index',   # Citi AU Pure Size — start 1994
    'CGRQPJPS Index',   # Citi JP Pure Size — start year unspecified
    'CGRQPCNS Index',   # Citi China Pure Size — start 1994
    'CGRQPUSS Index',  # Citi US Pure Size — start 1994

    'UBSHTGSN Index',   # UBS HOLT Equity Factor Global Size USD Net Total Return Index — start 2001

    'AWPSTE Index',           # FTSE All-World Pure Size Target Exposure Factor Index — start year unspecified

    'R1FSFR Index',           # Russell 1000 Size Factor Index — start 2017
    'R2FSF Index',            # Russell 2000 Size Factor Total Return Index — start 2006

    'SAW1SZGV Index',         # STOXX Global 1800 Ax Size Gross Return USD — start year unspecified

    'SGEPSBW Index',          # SGI World Size Index — start 2001

    'WUPSL Index',            # FT Wilshire US Large Pure Size Index — start 2017
]

df_size = blp.bdh(
    tickers=size_tickers,
    flds='PX_LAST',
    start_date='2018-01-01',
    periodicitySelection='MONTHLY' 
)
df_size.to_excel("size_factors.xlsx",
            sheet_name="Pure Size",
            index=True
)
short_vol_tickers = [
    'FRUSVSUT Index',   # FTSE US Risk Premium Index Series: Low Volatility Short Only Total Return Index — start 2017
    'VIX9D Index',      # Cboe S&P 500 Short Term Volatility Index — start 2011
    'JPRVLAGX Index',   # J.P. Morgan iDex Pure Residual Volatility Short (JPRVLAGX) Index — start 2008
    'ABRXIV Index',     # ABR Enhanced Short Volatility Index — start 2005
    'R1LTELS Index',    # Russell 1000 Pure Low Volatility Target Exposure Factor Long Short Index — start 2012
    'WEIXARB Index',    # Dynamic Short Volatility Futures Index — start 2007
]
df_short_vol = blp.bdh(
    tickers=short_vol_tickers,
    flds='PX_LAST',
    start_date='2018-01-01',
    periodicitySelection='MONTHLY' 
)
df_short_vol.to_excel("short_vol_factors.xlsx",
            sheet_name="Pure short vol",
            index=True
)