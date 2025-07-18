# classes1.py

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from config import CONFIG

class FactorPCA:
    def __init__(self, name, file_path, schemes=None, skiprows=None, index_col=0):
        self.name      = name
        self.path      = file_path
        self.schemes   = schemes or {}
        self.skiprows  = skiprows or [1, 2]
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

        # 1) Fit PCA on the standardized data
        scaler = StandardScaler()
        X_std  = scaler.fit_transform(df)
        pca    = PCA().fit(X_std)

        # 2) (Optional) keep z-scored scores & explained variance
        pc_cols = [f"PC{i+1}" for i in range(pca.n_components_)]
        self.scores = pd.DataFrame(
            pca.transform(X_std),
            index=df.index,
            columns=pc_cols
        )
        self.explained_variance_ratio = pd.Series(
            pca.explained_variance_ratio_,
            index=pc_cols,
            name=f"{self.name}_explained_variance_ratio"
        )

        # 3) Reconstruct PC1 in raw %-return units:
        #    loadings on standardized data ÷ original σ’s
        loadings    = pca.components_[0]        # eigenvector for PC1
        raw_weights = loadings / scaler.scale_  # scaler.scale_ = σ’s of each column

        #    dot into the raw df to get PC1 in %-return units
        pc1_raw = df.dot(raw_weights)
        pc1_raw.name = f"{self.name}_PC1_return"

        self.pc1_returns = pc1_raw
        return self

    @classmethod
    def run_all(cls):
        pipelines = {}
        for name, cfg in CONFIG.items():
            pipelines[name] = cls(
                name=name,
                file_path=cfg['file_path'],
                schemes=cfg.get('schemes')
            ).run()
        return pipelines

    def run(self):
        self.load_returns()
        self.apply_schemes()
        self.run_pca()
        return self

if __name__ == "__main__":
    pipelines = FactorPCA.run_all()
    for name, pipe in pipelines.items():
        print(f"{name}: {pipe.explained_variance_ratio}\n")

