
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
        self.df_raw             = None
        self.df_after_schemes   = None
        self.all_scheme_members = set()

    def load_returns(self):
        df = pd.read_excel(
            self.path,
            header=0,
            skiprows=self.skiprows,
            index_col=self.index_col,
            parse_dates=True
        )
        if CONFIG[self.name].get("input_is_returns", False):
            returns = df.apply(pd.to_numeric, errors="coerce").ffill()
        else:
            returns = df.apply(pd.to_numeric, errors="coerce").pct_change(fill_method=None).ffill()

    # drop rows with any zero
        returns = returns[(returns != 0).all(axis=1)]

    # store BOTH
        self.df_raw = returns.copy()
        self.df     = returns

    def apply_schemes(self):
        """
        Build each aggregate in self.schemes and KEEP every column that is not part of any scheme.
        Result stored in self.df_after_schemes.
        """
    # If no schemes, just forward the raw df
        if not getattr(self, "schemes", None):
            self.df_after_schemes = self.df_raw.copy()
            self.all_scheme_members = set()
            return

        df = self.df_raw.copy()
        new_cols = {}
        members  = set()

        for new_name, weight_dict in self.schemes.items():
        # weight_dict is {ticker: weight_series}
            w = pd.DataFrame(weight_dict)

        # Align rows (dates) and normalize each row to sum to 1
            w = w.reindex(df.index).div(w.sum(axis=1), axis=0)

            missing = [c for c in w.columns if c not in df.columns]
            if missing:
                raise ValueError(f"[{self.name}] Missing tickers for scheme '{new_name}': {missing}")

            agg = (df[w.columns] * w).sum(axis=1)
            new_cols[new_name] = agg
            members.update(w.columns)

        passthrough_cols = [c for c in df.columns if c not in members]

        self.df_after_schemes = pd.concat(
            [df[passthrough_cols]] + [s.rename(k) for k, s in new_cols.items()],
            axis=1
        )

        self.all_scheme_members = members

    # ---------- sanity checks ----------
        lost = set(df.columns) - set(self.df_after_schemes.columns) - members
        if lost:
            print(f"[{self.name}] WARNING: lost non-scheme cols: {sorted(lost)}")

    # Quick report
        print(f"[{self.name}] schemes applied: {list(self.schemes.keys())}")
        print(f"[{self.name}] #scheme members: {len(members)}  | passthrough kept: {len(passthrough_cols)}")
        print(f"[{self.name}] final cols: {len(self.df_after_schemes.columns)}")

    def run_pca(self):
        df = self.df_after_schemes.dropna()

        scaler = StandardScaler()
        X_std  = scaler.fit_transform(df)

        pca = PCA().fit(X_std)

    # Store scores (optional)
        self.scores = pd.DataFrame(pca.transform(X_std),
                               index=df.index,
                               columns=[f"PC{i+1}" for i in range(pca.n_components_)])

        self.explained_variance_ratio = pd.Series(
            pca.explained_variance_ratio_,
            index=self.scores.columns,
            name=f"{self.name}_explained_variance_ratio"
        )

    # Reconstruct PC1 on raw scale
        loadings    = pca.components_[0]
        raw_weights = loadings / scaler.scale_
        pc1_raw     = df.dot(raw_weights)

        self.pc1_returns = pc1_raw.rename(f"{self.name}_PC1_return")

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
        print(f"{name}: {pipe.pc1_returns}\n")

pipelines = FactorPCA.run_all()

pc1_df = pd.concat(
    [p.pc1_returns.rename(name) for name, p in pipelines.items()],
    axis=1
)
out_path = r"C:\repos\factors\pc1_returns.xlsx"
pc1_df.to_excel(out_path)
print(f"PC1 returns saved to {out_path}")