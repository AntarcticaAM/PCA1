# betas_per_fund.py remove defensive other wise not enough data
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
import statsmodels.api as sm
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
import statsmodels.api as sm
from statsmodels.tools import add_constant
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import BaseCrossValidator

# ---------- paths ----------
FACTORS_PATH = r"C:\repos\factors\pc1_returns_monthly_filled.xlsx"
FUNDS_PATH   = r"C:\repos\factors\johnjohn_funds_performance.xlsx"
OUT_PATH     = r"C:\repos\factors\fund_betas_all_factors3.xlsx"

class ExpandingWindowCV(BaseCrossValidator):
    """
    Expanding window CV:
      - First train window length = min_train
      - Test window length = test_size
      - Step forward by 'step' each fold
    """
    def __init__(self, test_size=12, min_train=36, step=None):
        self.test_size = test_size
        self.min_train = min_train
        self.step = step or test_size

    def split(self, X, y=None, groups=None):
        n = len(X)
        start = self.min_train
        while start + self.test_size <= n:
            train_idx = np.arange(0, start)
            test_idx  = np.arange(start, start + self.test_size)
            yield train_idx, test_idx
            start += self.step

    def get_n_splits(self, X=None, y=None, groups=None):
        # optional
        n = len(X)
        cnt = 0
        start = self.min_train
        while start + self.test_size <= n:
            cnt += 1
            start += self.step
        return cnt
    

def pick_k_pcr(X_std, y, cv, k_grid):
    """Return best k using TS-CV MSE."""
    mse_by_k = {}
    for k in k_grid:
        pca = PCA(n_components=k).fit(X_std)
        Z = pca.transform(X_std)
        fold_mse = [
            mean_squared_error(y[tr], sm.OLS(y[tr], add_constant(Z[tr])).fit().predict(add_constant(Z[te])))
            for tr, te in cv.split(Z)
        ]
        mse_by_k[k] = np.mean(fold_mse)
    return min(mse_by_k, key=mse_by_k.get)

def load_factors(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, index_col=0, parse_dates=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.replace([np.inf, -np.inf], np.nan).dropna(how='all')
    df = df[~df.index.duplicated(keep='last')].sort_index()
    
    return df


def load_fund_returns(path: str) -> pd.DataFrame:
    prices = pd.read_excel(path, index_col=0, parse_dates=True)
    prices = prices.apply(pd.to_numeric, errors='coerce')
    prices = prices.replace([np.inf, -np.inf], np.nan)
    prices = prices[~prices.index.duplicated(keep='last')].sort_index()

    # Convert to monthly returns using month-end last price
    return prices.dropna(how='all')


def compute_betas_for_all(factors_df: pd.DataFrame,
                          fund_rets: pd.DataFrame,
                          method: str = "ols",
                          n_components: int | None = None,
                          cv_test: int = 12,
                          min_train: int = 36,
                          pls_scale_y: bool = True) -> pd.DataFrame:
    """
    method = 'ols' or 'ridge'
    Ridge uses cross-validated alpha over a logspace grid.
    """
    # -------------- align --------------
    all_df = pd.concat([factors_df, fund_rets], axis=1, join='inner').dropna(how='any')
    factor_cols = factors_df.columns.tolist()
    funds = fund_rets.columns

    betas = {}

    if method.lower() == "ols":
        X = sm.add_constant(all_df[factor_cols]).astype(float)
        for fund in funds:
            y = all_df[fund].astype(float)
            if y.std() < 1e-12:
                continue
            model = sm.OLS(y, X, missing='drop').fit()
            betas[fund] = model.params.drop('const').replace([np.inf, -np.inf], np.nan)
    elif method.lower() == "ridge":
        # Standardize X so Ridge penalises all factors fairly
        scaler = StandardScaler()
        X_std = scaler.fit_transform(all_df[factor_cols])
        # No constant with Ridge (centered by scaler). If you want an intercept, RidgeCV has fit_intercept arg.
        cv = ExpandingWindowCV(test_size=cv_test, min_train=min_train)
        alphas = np.logspace(-4, 4, 150)
        for fund in funds:
            y = all_df[fund].astype(float).values
            if y.std() < 1e-12:
                continue
            ridge = RidgeCV(alphas=alphas, cv=cv, fit_intercept=True)
            ridge.fit(X_std, y)
            coefs_std = ridge.coef_
            # Undo standardization: β_orig = β_std / σ_X  (intercept handled by model.intercept_)
            beta_orig = pd.Series(coefs_std / scaler.scale_, index=factor_cols)
            betas[fund] = beta_orig.replace([np.inf, -np.inf], np.nan)
    elif method.lower() == "pcr":
        scaler = StandardScaler()
        X_std  = scaler.fit_transform(all_df[factor_cols].astype(float))

    # choose k once (or pass it)
        if n_components is None:
            cv      = ExpandingWindowCV(test_size=cv_test, min_train=min_train)
            k_grid  = range(1, min(len(factor_cols), 6) + 1)
            y_ref   = all_df[funds[0]].astype(float).values
            k       = pick_k_pcr(X_std, y_ref, cv, k_grid)
        else:
            k = n_components

        pca   = PCA(n_components=k).fit(X_std)
        Z     = pca.transform(X_std)
        Zc    = add_constant(Z)

        for fund in funds:
            y = all_df[fund].astype(float).values
            if y.std() < 1e-12: 
                continue
            coef_scores = sm.OLS(y, Zc).fit().params[1:]          # drop const
            betas_orig  = (pca.components_.T @ coef_scores) / scaler.scale_
            betas[fund] = pd.Series(betas_orig, index=factor_cols)
            for fund in funds:
                y = all_df[fund].astype(float)
                if y.std() < 1e-12:
                    continue
            # regress y on scores
                Zc = sm.add_constant(Z)
                res = sm.OLS(y, Zc).fit()
            # map back: beta_orig = P * beta_scores / scale
                beta_scores = res.params.drop('const').values  # length k
                beta_orig = pca.components_.T @ beta_scores
                beta_orig = beta_orig / scaler.scale_
                betas[fund] = pd.Series(beta_orig, index=factor_cols)
    elif method.lower() == "pls":
        scaler_x = StandardScaler()
        X_std = scaler_x.fit_transform(all_df[factor_cols])

        # y scaling optional
        if pls_scale_y:
            scaler_y = StandardScaler()

        k = n_components or min(len(factor_cols), 5)
        for fund in funds:
            y = all_df[fund].astype(float).values.reshape(-1, 1)
            if y.std() < 1e-12:
                continue

            if pls_scale_y:
                y_std = scaler_y.fit_transform(y)
            else:
                y_std = y

            pls = PLSRegression(n_components=k)
            pls.fit(X_std, y_std)

            # Coefs in standardized X (and maybe y); undo
            coef_std = pls.coef_.ravel()
            beta_orig = coef_std / scaler_x.scale_
            if pls_scale_y:
                beta_orig *= scaler_y.scale_[0]  # if y scaled

            betas[fund] = pd.Series(beta_orig, index=factor_cols)
    elif method.lower() == "robust":
        X = add_constant(all_df[factor_cols].astype(float))
        for fund in funds:
            y = all_df[fund].astype(float)
            if y.std() < 1e-12:
                continue
        # Huber loss; you can swap HuberT() with TukeyBiweight() etc.
            rlm = sm.RLM(y, X, M=sm.robust.norms.HuberT())
            res = rlm.fit()
            betas[fund] = res.params.drop('const').replace([np.inf, -np.inf], np.nan)

    else:
        raise ValueError("method must be 'ols', 'ridge', 'pcr', or 'pls'")

    return pd.DataFrame.from_dict(betas, orient='index')


def main():
    factors_df = load_factors(FACTORS_PATH)
    fund_rets  = load_fund_returns(FUNDS_PATH)

    # pick which estimator you want:
    beta_matrix_ols = compute_betas_for_all(factors_df, fund_rets, method="ols")
    beta_matrix_ridge = compute_betas_for_all(factors_df, fund_rets, method="ridge",cv_test=12, min_train=36)
    beta_matrix_pcr = compute_betas_for_all(factors_df, fund_rets, method="pcr", n_components=3, cv_test=12, min_train=36)
    beta_matrix_pls = compute_betas_for_all(factors_df, fund_rets, method="pls")
    beta_matrix_robust = compute_betas_for_all(factors_df, fund_rets, method="robust")

    print("\n=== OLS Betas ===")
    print(beta_matrix_ols.round(6))
    print("\n=== Ridge Betas ===")
    print(beta_matrix_ridge.round(6))
    print("\n=== PCR Betas ===")
    print(beta_matrix_pcr.round(6))
    print("\n=== PLS Betas ===")
    print(beta_matrix_pls.round(6))
    print("\n=== Robust Betas ===")
    print(beta_matrix_robust.round(6))

    betas = {
        "OLS":   beta_matrix_ols,
        "Ridge": beta_matrix_ridge,
        "PCR":   beta_matrix_pcr,
        "PLS":   beta_matrix_pls,
        "Robust": beta_matrix_robust,
}

    out_path = r"C:\repos\factors\betas_all_methods2.xlsx"
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as w:
        for name, df in betas.items():
            df.to_excel(w, sheet_name=name)


if __name__ == "__main__":
    main()

