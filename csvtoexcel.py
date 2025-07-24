import pandas as pd
import numpy as np
import statsmodels.api as sm
from classes1 import FactorPCA
from classes1 import FactorPCA
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load data
funds_df   = pd.read_excel("johnjohn_funds_performance.xlsx", index_col=0, parse_dates=True)
pipelines  = FactorPCA.run_all()
# get the momentum PC1 return series
mom = pipelines["growth"].pc1_returns.dropna()

# pretty print all rows
print("growth PC1 returns (all dates):")
print(mom.to_string())   # prints full series with dates

# OPTIONAL: save to Excel/CSV

# or
# mom.to_frame("momentum_PC1_return").to_csv("momentum_pc1_returns.cs
# Prepare empty results
funds   = funds_df.columns
factors = list(pipelines.keys())

overlap = pd.DataFrame(index=funds, columns=factors, dtype=int)
corrs   = pd.DataFrame(index=funds, columns=factors, dtype=float)
slopes  = pd.DataFrame(index=funds, columns=factors, dtype=float)

for factor in factors:
    fac = pipelines[factor].pc1_returns.dropna()
    for fund in funds:
        f = funds_df[fund].dropna()
        idx = f.index.intersection(fac.index)
        if len(idx) == 0:
            overlap.loc[fund, factor] = 0
            corrs.loc[fund, factor]   = np.nan
            slopes.loc[fund, factor]  = np.nan
        else:
            overlap.loc[fund, factor] = len(idx)
            df = pd.DataFrame({
                'fund': f.loc[idx],
                'fac' : fac.loc[idx]
            })
            corrs.loc[fund, factor] = df['fund'].corr(df['fac'])
            X = sm.add_constant(df['fac']).astype(float)
            model = sm.OLS(df['fund'].astype(float), X).fit()
            slopes.loc[fund, factor] = model.params['fac']

# Show results (you can also inspect particular cells)
print("Overlap counts:\n", overlap)
print("\nCorrelations:\n", corrs)
print("\nUnivariate slopes (raw β):\n", slopes)
from classes1 import FactorPCA
import pandas as pd

for name, pipe in pipelines.items():
    # a) grab the cleaned return DataFrame as the PCA saw it
    df = pipe.df.dropna(how='all').dropna(axis=1)  # drop empty rows & any all-NaN cols

    # b) standardize
    scaler = StandardScaler()
    X = scaler.fit_transform(df)

    # c) run PCA
    pca = PCA(n_components=df.shape[1])
    pca.fit(X)

    # d) unit‐norm PC1 component
    loadings = pd.Series(pca.components_[0], index=df.columns)

    # e) true weights on raw returns
    weights  = loadings.div(scaler.scale_)

    # f) display
    print(f"\n=== {name} PC1 compositions ===")
    print("Loadings (unit length):")
    print(loadings.round(4))
    print("\nWeights on raw returns:")
    print(weights.round(4))
