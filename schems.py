import pandas as pd
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

schemes_growth = {
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
schemes_quality = {
    "hsbc_weights_quality":{
        'HSIEQETU Index': europe_weights,
        'HSIEQUTU Index': us_weights,
    },
    "citi_weights_quality":{
        'CGRQPEUQ Index': europe_weights,
        'CGRQPUSQ Index': us_weights,
        'CGRQPCNQ Index': China_weights,
        'CGRQPAUQ Index': Australia_weights,
        'CGRQPJPQ Index': Japan_weights,
    },
    "DB_weights_quality":{
        'DBRPAEQU Index': Asia_Pacific_weights,
        'DBRPEEQE Index': europe_weights,
        'DBRPNEQU Index': us_weights,
    },
}
schemes_inflation = {
    "BofA_weights_inflation":{
        'MLINFL8 Index': us_weights/2, # PRO INFLATION
        'MLDEFL8 Index': us_weights/2, # ANTI INFLATION
    },
}
schemes_realestate = {
    "DJ_weights_realestate":{
        'DWEURT Index': europe_weights,  # DJEurpslct REIT — start 2004
        'DWAPRT Index': Asia_Pacific_weights,  # DJAsiaPslct REIT — start 2004
        'DWAMRT Index': Americas_weights,  # DJAmrslct REIT — start 2004
    },
}
schemes_size = {
    "Citi_weights_size":{
        'CGRQPEUS Index': europe_weights,
        'CGRQPAUS Index': Australia_weights,
        'CGRQPJPS Index': Japan_weights,
        'CGRQPCNS Index': China_weights,
        'CGRQPUSS Index': us_weights,
    },
}
schemes_value = {
    "hsbc_weights_value":{
        'HSIEQETU Index': europe_weights,
        'HSIEQUTU Index': us_weights,
    },
    "citi_weights_value":{
        'CGRQPUSQ Index': us_weights,
        'CGRQPEUQ Index': europe_weights,
        'CGRQPAUQ Index': Australia_weights,
        'CGRQPJPQ Index': Japan_weights,
    },
}


