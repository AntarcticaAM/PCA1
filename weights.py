import pandas as pd

file_path2 = r"C:\Users\johnjohn\Downloads\msci_acwi_weights_202507111011 (1).csv"
df_w = pd.read_csv(file_path2, header=0, dtype=str)


df_w['value_date'] = pd.to_datetime(
    df_w['value_date'],
    format='%d/%m/%Y',
    errors='raise'
)
df_w['year_month'] = df_w['value_date'].dt.to_period('M')


df_w['weight'] = pd.to_numeric(df_w['weight'], errors='raise')

df_monthly = (
    df_w
      .groupby(['geo_name', 'year_month'])['weight']
      .mean()
      .reset_index()
      .rename(columns={'weight': 'monthly_avg_weight'})
)


start_period = pd.Period('2014-01', freq='M')
end_period   = df_monthly['year_month'].max()
full_range   = pd.period_range(start=start_period, end=end_period, freq='M')

regions = df_monthly['geo_name'].unique()
idx = pd.MultiIndex.from_product(
    [regions, full_range],
    names=['geo_name', 'year_month']
)


df_monthly = (
    df_monthly
      .set_index(['geo_name', 'year_month'])
      .reindex(idx)  
)
df_monthly['monthly_avg_weight'] = (
    df_monthly['monthly_avg_weight']
      .groupby(level=0)  
      .bfill()           
)


df_monthly = df_monthly.reset_index()


monthly_pivot = df_monthly.pivot(
    index='year_month',
    columns='geo_name',
    values='monthly_avg_weight'
)

print(monthly_pivot)


df_w = df_w[(df_w['weight'] >= 0) & (df_w['weight'] <= 100)]
df_w = df_w.dropna(subset=['weight'])
last_dates = df_w.groupby('geo_name')['value_date'] \
                 .transform('max')


df_latest = df_w.loc[df_w['value_date'] == last_dates]



europe_weights = df_monthly.loc[df_monthly['geo_name'] == 'Western Europe', ['year_month', 'monthly_avg_weight']]
europe_weights = europe_weights.set_index('year_month')['monthly_avg_weight']
europe_weights.index = europe_weights.index.to_timestamp('M')

us_weights = df_monthly.loc[df_monthly['geo_name'] == 'U.S.', ['year_month', 'monthly_avg_weight']]
us_weights = us_weights.set_index('year_month')['monthly_avg_weight']
us_weights.index = us_weights.index.to_timestamp('M')

Japan_weights = df_monthly.loc[df_monthly['geo_name'] == 'Japan', ['year_month', 'monthly_avg_weight']]
Japan_weights = Japan_weights.set_index('year_month')['monthly_avg_weight']
Japan_weights.index = Japan_weights.index.to_timestamp('M')

developped_exNorthAmerica_members = ['Western Europe', 'Japan', 'Taiwan', 'Australia', 'New Zealand']
developped_exNorthAmerica_weights = df_monthly.loc[df_monthly['geo_name'].isin(developped_exNorthAmerica_members), ['year_month', 'monthly_avg_weight']]
developped_exNorthAmerica_weights = developped_exNorthAmerica_weights.groupby('year_month')['monthly_avg_weight'].sum()
developped_exNorthAmerica_weights.index = developped_exNorthAmerica_weights.index.to_timestamp('M')

Canada_weights = df_monthly.loc[df_monthly['geo_name'] == 'Canada', ['year_month', 'monthly_avg_weight']]
Canada_weights = Canada_weights.set_index('year_month')['monthly_avg_weight']
Canada_weights.index = Canada_weights.index.to_timestamp('M')

China_weights = df_monthly.loc[df_monthly['geo_name'] == 'China', ['year_month', 'monthly_avg_weight']]
China_weights = China_weights.set_index('year_month')['monthly_avg_weight']
China_weights.index = China_weights.index.to_timestamp('M')

Australia_weights = df_monthly.loc[df_monthly['geo_name'] == 'Australia', ['year_month', 'monthly_avg_weight']]
Australia_weights = Australia_weights.set_index('year_month')['monthly_avg_weight']
Australia_weights.index = Australia_weights.index.to_timestamp('M')

Asia_Pacific_weights = df_monthly.loc[df_monthly['geo_name'].isin(developped_exNorthAmerica_members), ['year_month', 'monthly_avg_weight']]
Asia_Pacific_weights = Asia_Pacific_weights.groupby('year_month')['monthly_avg_weight'].sum()
Asia_Pacific_weights.index = Asia_Pacific_weights.index.to_timestamp('M')

Americas_members = ['North America', 'South & Central America']
Americas_weights = df_monthly.loc[df_monthly['geo_name'].isin(Americas_members), ['year_month', 'monthly_avg_weight']]
Americas_weights = Americas_weights.groupby('year_month')['monthly_avg_weight'].sum()
Americas_weights.index = Americas_weights.index.to_timestamp('M')