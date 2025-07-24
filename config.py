import pandas as pd
from schems import ( schemes_growth, schemes_quality, schemes_inflation, schemes_realestate, schemes_size, schemes_value, schemes_momentum )

CONFIG = {
        'growth': {
            'file_path': r"C:\repos\factors\growth_factors1.xlsx",
            'schemes': schemes_growth
        },
        'quality': {
            'file_path': r"C:\repos\factors\quality_factors.xlsx",
            'schemes': schemes_quality
        },
        'inflation': {
            'file_path': r"C:\repos\factors\inflation_factors.xlsx",
            'schemes': schemes_inflation
        },
        'realestate': {
            'file_path': r"C:\repos\factors\real_estate.xlsx",
            'schemes': schemes_realestate
        },
        'size': {
            'file_path': r"C:\repos\factors\size_factors.xlsx",
            'schemes': schemes_size
        },
        'value': {
            'file_path': r"C:\repos\factors\value_factors2.xlsx",
            'schemes': schemes_value
        },
        'commodity': {
            'file_path': r"C:\repos\factors\commodity_factors.xlsx",
        },
        'defensive': {
            'file_path': r"C:\repos\factors\defensive_factors.xlsx",
        },
        'crowded': {
            'file_path': r"C:\repos\factors\crowded_factors.xlsx",
        },
        'shortvol': {
            'file_path': r"C:\repos\factors\short_vol_factors.xlsx",
        },
        'momentum': {
            'file_path': r"C:\repos\factors\momentum_factors144.xlsx",
            'schemes': schemes_momentum
        },
}