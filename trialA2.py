# betas_per_fund.py
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.cross_decomposition import PLSRegression
from sklearn.decomposition import PCA
from statsmodels.tools import add_constant
from sklearn.linear_model import BayesianRidge




# ---------- paths ----------
FACTORS_PATH = r"C:\repos\factors\pc1_returns_monthly_filled.xlsx"
FUNDS_PATH   = r"C:\repos\theexcels\johnjohn_funds_performance.xlsx"
OUT_PATH     = r"C:\repos\factors\fund_betas_all_factors3.xlsx"


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
    n_points = {}

    if method.lower() == "ols":
        X = sm.add_constant(all_df[factor_cols]).astype(float)
        for fund in funds:
            y = all_df[fund].astype(float)
            if y.std() < 1e-12:
                continue
            model = sm.OLS(y, X, missing='drop').fit()
            betas[fund] = model.params.drop('const').replace([np.inf, -np.inf], np.nan)
            n_points[fund] = len(y.dropna())
    elif method.lower() == "ridge":
        # Standardize X so Ridge penalises all factors fairly
        scaler = StandardScaler()
        X_std = scaler.fit_transform(all_df[factor_cols])
        # No constant with Ridge (centered by scaler). If you want an intercept, RidgeCV has fit_intercept arg.
        alphas = np.logspace(-4, 4, 100)
        ridge = RidgeCV(alphas=alphas, fit_intercept=True, cv=None)  # leave-one-block CV is optional
        for fund in funds:
            y = all_df[fund].astype(float).values
            if y.std() < 1e-12:
                continue
            ridge.fit(X_std, y)
            coefs_std = ridge.coef_
            # Undo standardization: β_orig = β_std / σ_X  (intercept handled by model.intercept_)
            beta_orig = pd.Series(coefs_std / scaler.scale_, index=factor_cols)
            betas[fund] = beta_orig.replace([np.inf, -np.inf], np.nan)
            n_points[fund] = np.count_nonzero(~np.isnan(y))
    elif method.lower() == "pcr":
        # Standardize X for PCA/Ridge fairness
        scaler = StandardScaler()
        X_std = scaler.fit_transform(all_df[factor_cols])
        # choose components
        k = n_components or min(len(factor_cols), 5)
        pca = PCA(n_components=k).fit(X_std)
        Z = pca.transform(X_std)  # scores
        Z = pd.DataFrame(Z, index=all_df.index)

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
            n_points[fund] = len(y.dropna())
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
            n_points[fund] = np.count_nonzero(~np.isnan(y))
    elif method.lower() == "bayesian":
        scaler = StandardScaler()
        X_std = scaler.fit_transform(all_df[factor_cols])
        # No constant with BayesianRidge (centered by scaler). If you want an intercept, set fit_intercept=True.
        model = BayesianRidge(fit_intercept=True)
        for fund in funds:
            y = all_df[fund].astype(float).values
            if y.std() < 1e-12:
                continue
            model.fit(X_std, y)
            coefs_std = model.coef_
            # Undo standardization: β_orig = β_std / σ_X  (intercept handled by model.intercept_)
            beta_orig = pd.Series(coefs_std / scaler.scale_, index=factor_cols)
            betas[fund] = beta_orig.replace([np.inf, -np.inf], np.nan)
            n_points[fund] = np.count_nonzero(~np.isnan(y))
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
            n_points[fund] = len(y.dropna())

    else:
        raise ValueError("method must be 'ols', 'ridge', 'pcr', or 'pls'")

    return pd.DataFrame.from_dict(betas, orient='index'), n_points


def main():
    factors_df = load_factors(FACTORS_PATH)
    fund_rets  = load_fund_returns(FUNDS_PATH)

    # pick which estimator you want:
    beta_matrix_ols, n_ols = compute_betas_for_all(factors_df, fund_rets, method="ols")
    beta_matrix_ridge, n_ridge = compute_betas_for_all(factors_df, fund_rets, method="ridge")
    beta_matrix_pcr, n_pcr = compute_betas_for_all(factors_df, fund_rets, method="pcr")
    beta_matrix_pls, n_pls = compute_betas_for_all(factors_df, fund_rets, method="pls")
    beta_matrix_robust, n_robust = compute_betas_for_all(factors_df, fund_rets, method="robust")
    beta_matrix_bayesian, n_bayesian = compute_betas_for_all(factors_df, fund_rets, method="bayesian")

    print("\n=== OLS Betas ===")
    print(beta_matrix_ols.round(6))
    print("Shared data points per fund (OLS):", n_ols)
    print("\n=== Ridge Betas ===")
    print(beta_matrix_ridge.round(6))
    print("Shared data points per fund (Ridge):", n_ridge)
    print("\n=== PCR Betas ===")
    print(beta_matrix_pcr.round(6))
    print("Shared data points per fund (PCR):", n_pcr)
    print("\n=== PLS Betas ===")
    print(beta_matrix_pls.round(6))
    print("Shared data points per fund (PLS):", n_pls)
    print("\n=== Robust Betas ===")
    print(beta_matrix_robust.round(6))
    print("Shared data points per fund (Robust):", n_robust)
    print("\n=== Bayesian Betas ===")
    print(beta_matrix_bayesian.round(6))

    betas = {
        "OLS":   beta_matrix_ols,
        "Ridge": beta_matrix_ridge,
        "PCR":   beta_matrix_pcr,
        "PLS":   beta_matrix_pls,
        "Robust": beta_matrix_robust,
        "Bayesian": beta_matrix_bayesian,
}

    out_path = r"C:\repos\factors\betas_all_methods.xlsx"
    with pd.ExcelWriter(out_path, engine="xlsxwriter") as w:
        for name, df in betas.items():
            df.to_excel(w, sheet_name=name)


if __name__ == "__main__":
    main()

