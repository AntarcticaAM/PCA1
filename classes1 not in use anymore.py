import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from schems import (
    schemes_growth,
    schemes_quality,
    schemes_inflation,
    schemes_realestate,
    schemes_size,
    schemes_value,
)

class FactorPCA:

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
    }

    def __init__(self, name, file_path, schemes=None, skiprows=[1,2], index_col=0):
        self.name      = name
        self.path      = file_path
        self.schemes   = schemes or {}
        self.skiprows  = skiprows
        self.index_col = index_col

    def load_returns(self):
        df = pd.read_excel(
            self.path,
            header=0,
            skiprows=self.skiprows,
            index_col=self.index_col,
            parse_dates=True
        )
        df = df.ffill().pct_change()
        self.df = df[(df != 0).all(axis=1)]

    def apply_schemes(self):
        if not self.schemes:
            return
        df = self.df.copy()
        for out_col, weight_dict in self.schemes.items():
            w = pd.DataFrame(weight_dict)
            w = w.div(w.sum(axis=1), axis=0)
            region = df.loc[:, w.columns].apply(pd.to_numeric, errors='coerce')
            df[out_col] = (region * w).sum(axis=1)
            df.drop(columns=list(w.columns), inplace=True)

        self.df = df

    def run_pca(self):
        df = self.df.dropna()
        scaler = StandardScaler()
        X_std  = scaler.fit_transform(df)

        pca = PCA()
        pcs = pca.fit_transform(X_std)
        pc_cols = [f"PC{i+1}" for i in range(pcs.shape[1])]
        self.scores = pd.DataFrame(pcs, index=df.index, columns=pd.Index(pc_cols))

        self.loadings = pca.components_
        self.pc1_weights = pd.Series(
            self.loadings[0],
            index=df.columns,
            name=f"{self.name}_PC1_weight"
        )
        self.pc1_returns = self.scores["PC1"].copy()
        self.pc1_returns.name = f"{self.name}_PC1_return"
        self.explained_variance_ratio = pd.Series(
            pca.explained_variance_ratio_,
            index=pc_cols,
            name=f"{self.name}_explained_variance_ratio"
        )

    def run(self):
        self.load_returns()
        self.apply_schemes()
        self.run_pca()
        return self

    @classmethod
    def run_all(cls):

        pipelines = {}
        for name, cfg in cls.CONFIG.items():
            schemes = cfg.get('schemes', {})
            pipelines[name] = cls(
                name=name,
                file_path=cfg['file_path'],
                schemes=schemes
            ).run()
        return pipelines

if __name__ == "__main__":
    pipelines = FactorPCA.run_all()
    for name, pipe in pipelines.items():
        print(f"{name} explained variance ratios:\n{pipe.explained_variance_ratio}\n")
