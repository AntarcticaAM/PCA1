import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.model_selection import BaseCrossValidator
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
import statsmodels.api as sm
from statsmodels.robust.robust_linear_model import RLM
from sklearn.feature_selection import (
    SelectKBest, SelectPercentile, f_regression
)

# ---------- helpers ----------

class ExpandingWindowCV(BaseCrossValidator):
    """Time-series CV: expanding train, fixed-size test."""
    def __init__(self, test_size=12, min_train=36, step=None):
        self.test_size  = test_size
        self.min_train  = min_train
        self.step       = step or test_size
    def split(self, X, y=None, groups=None):
        n = len(X)
        start = self.min_train
        while start + self.test_size <= n:
            yield np.arange(start), np.arange(start, start + self.test_size)
            start += self.step
    def get_n_splits(self, X=None, y=None, groups=None):
        n = len(X)
        start = self.min_train
        c = 0
        while start + self.test_size <= n:
            c += 1
            start += self.step
        return c

def oos_r2(y_true, y_pred):
    """Out-of-sample R² (aka Q²)."""
    return 1 - mean_squared_error(y_true, y_pred) / np.var(y_true, ddof=1)

def pick_k_pcr(X_std, y, cv, k_grid):
    """Choose k for PCR via TS-CV MSE."""
    best_k, best_mse = None, np.inf
    for k in k_grid:
        pca = PCA(n_components=k).fit(X_std)
        Z   = pca.transform(X_std)
        fold_mse = []
        for tr, te in cv.split(Z):
            res = sm.OLS(y[tr], sm.add_constant(Z[tr])).fit()
            y_hat = res.predict(sm.add_constant(Z[te]))
            fold_mse.append(mean_squared_error(y[te], y_hat))
        mse = np.mean(fold_mse)
        if mse < best_mse:
            best_mse, best_k = mse, k
    return best_k

def pick_k_pls(X_std, y, cv, k_grid, scale_y=True):
    """Choose n_components for PLS via TS-CV MSE."""
    best_k, best_mse = None, np.inf
    for k in k_grid:
        fold_mse = []
        for tr, te in cv.split(X_std):
            pls = PLSRegression(n_components=k, scale=scale_y)
            pls.fit(X_std[tr], y[tr])
            y_hat = pls.predict(X_std[te]).ravel()
            fold_mse.append(mean_squared_error(y[te], y_hat))
        mse = np.mean(fold_mse)
        if mse < best_mse:
            best_mse, best_k = mse, k
    return best_k

# ---------- main worker ----------

def compute_betas_for_all(factor_df, fund_df,
                          method="ols",
                          n_components=None,
                          pls_scale_y=True,
                          cv_test=12,
                          min_train=36,
                          return_metrics=False):
    """
    Returns:
        beta_df  (DataFrame)
        metric_df (DataFrame) if return_metrics=True
    """
    # line up dates
    df_all = pd.concat([factor_df, fund_df], axis=1).dropna(how='any')
    factor_cols = factor_df.columns.tolist()
    funds       = fund_df.columns.tolist()

    betas   = {}
    metrics = {}

    if method.lower() == "ols":
        X = sm.add_constant(df_all[factor_cols]).astype(float)
        for f in funds:
            y  = df_all[f].astype(float)
            if y.std() < 1e-12:  # skip flat
                continue
            res = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags':3})
            betas[f] = res.params.drop('const')
            if return_metrics:
                metrics[f] = {"R2_in": res.rsquared, "R2_adj": res.rsquared_adj}

    elif method.lower() == "robust":
        X = sm.add_constant(df_all[factor_cols]).astype(float)
        for f in funds:
            y = df_all[f].astype(float)
            if y.std() < 1e-12:
                continue
            res = RLM(y, X, M=sm.robust.norms.HuberT()).fit()
            betas[f] = res.params.drop('const')
            if return_metrics:
                # pseudo R² = 1 - RSS/TSS
                rss = np.sum(res.resid ** 2)
                tss = np.sum((y - y.mean()) ** 2)
                metrics[f] = {"R2_pseudo": 1 - rss/tss}

    elif method.lower() == "ridge":
        scaler = StandardScaler()
        X_std  = scaler.fit_transform(df_all[factor_cols].astype(float))
        cv     = ExpandingWindowCV(test_size=cv_test, min_train=min_train)
        splits = list(cv.split(X_std))

        alphas = np.logspace(-4, 4, 100)

        for f in funds:
            y = df_all[f].astype(float).values
            if y.std() < 1e-12:
                continue

            # choose alpha by TS-CV
            best_a, best_mse = None, np.inf
            for a in alphas:
                yhat_oos, ytrue_oos = [], []
                for tr, te in splits:
                    model = Ridge(alpha=a, fit_intercept=True)
                    model.fit(X_std[tr], y[tr])
                    yhat_oos.append(model.predict(X_std[te]))
                    ytrue_oos.append(y[te])
                mse = mean_squared_error(np.concatenate(ytrue_oos),
                                         np.concatenate(yhat_oos))
                if mse < best_mse:
                    best_mse, best_a = mse, a

            final = Ridge(alpha=best_a, fit_intercept=True).fit(X_std, y)
            coef_std = final.coef_
            betas[f] = pd.Series(coef_std / scaler.scale_, index=factor_cols)

            if return_metrics:
                # in-sample
                r2_in = final.score(X_std, y)
                # oos
                yhat_oos, ytrue_oos = [], []
                for tr, te in splits:
                    m = Ridge(alpha=best_a, fit_intercept=True).fit(X_std[tr], y[tr])
                    yhat_oos.append(m.predict(X_std[te]))
                    ytrue_oos.append(y[te])
                yhat_oos = np.concatenate(yhat_oos)
                ytrue_oos= np.concatenate(ytrue_oos)
                metrics[f] = {"R2_in": r2_in,
                              "R2_oos": oos_r2(ytrue_oos, yhat_oos),
                              "alpha": best_a}

    elif method.lower() == "pcr":
        scaler = StandardScaler()
        X_std  = scaler.fit_transform(df_all[factor_cols].astype(float))
        cv     = ExpandingWindowCV(test_size=cv_test, min_train=min_train)

        # pick k once (cheap & consistent). You can loop per fund if needed.
        if n_components is None:
            y_ref  = df_all[funds[0]].astype(float).values
            k_grid = range(1, min(len(factor_cols), 6) + 1)
            k      = pick_k_pcr(X_std, y_ref, cv, k_grid)
        else:
            k = n_components

        pca = PCA(n_components=k).fit(X_std)
        Z   = pca.transform(X_std)
        Zc  = sm.add_constant(Z)

        splits = list(cv.split(Z))

        for f in funds:
            y = df_all[f].astype(float).values
            if y.std() < 1e-12:
                continue
            res = sm.OLS(y, Zc).fit()
            scores = res.params[1:]  # drop const
            beta_orig = (pca.components_.T @ scores) / scaler.scale_
            betas[f]  = pd.Series(beta_orig, index=factor_cols)

            if return_metrics:
                # IS metrics
                rss = np.sum(res.resid ** 2)
                tss = np.sum((y - y.mean()) ** 2)
                r2_in = 1 - rss / tss

                # OOS metrics
                yhat_oos, ytrue_oos = [], []
                for tr, te in splits:
                    res_tr = sm.OLS(y[tr], sm.add_constant(Z[tr])).fit()
                    yhat_oos.append(res_tr.predict(sm.add_constant(Z[te])))
                    ytrue_oos.append(y[te])
                yhat_oos = np.concatenate(yhat_oos)
                ytrue_oos= np.concatenate(ytrue_oos)
                metrics[f] = {"R2_in": r2_in,
                              "R2_oos": oos_r2(ytrue_oos, yhat_oos),
                              "k": k}

    elif method.lower() == "pls":
        scaler = StandardScaler()
        X_std  = scaler.fit_transform(df_all[factor_cols].astype(float))
        cv     = ExpandingWindowCV(test_size=cv_test, min_train=min_train)
        splits = list(cv.split(X_std))

        # pick k once
        if n_components is None:
            y_ref  = df_all[funds[0]].astype(float).values
            k_grid = range(1, min(len(factor_cols), 6) + 1)
            k      = pick_k_pls(X_std, y_ref, cv, k_grid, scale_y=pls_scale_y)
        else:
            k = n_components

        for f in funds:
            y = df_all[f].astype(float).values
            if y.std() < 1e-12:
                continue

            pls = PLSRegression(n_components=k, scale=pls_scale_y)
            pls.fit(X_std, y)
            # map PLS coef back to original scale
            coef_std = pls.coef_.ravel()
            betas[f] = pd.Series(coef_std / scaler.scale_, index=factor_cols)

            if return_metrics:
                # In-sample R2
                yhat_in = pls.predict(X_std).ravel()
                r2_in   = 1 - mean_squared_error(y, yhat_in) / np.var(y, ddof=1)
                # OOS R2
                yhat_oos, ytrue_oos = [], []
                for tr, te in splits:
                    m = PLSRegression(n_components=k, scale=pls_scale_y).fit(X_std[tr], y[tr])
                    yhat_oos.append(m.predict(X_std[te]).ravel())
                    ytrue_oos.append(y[te])
                yhat_oos = np.concatenate(yhat_oos)
                ytrue_oos= np.concatenate(ytrue_oos)
                metrics[f] = {"R2_in": r2_in,
                              "R2_oos": oos_r2(ytrue_oos, yhat_oos),
                              "k": k}

    elif method.lower() in ("select_kbest", "kbest"):
        # choose K (or pass in as an extra arg)
        K = min(5, len(factor_cols))  
        for fund in funds:
            y = df_all[fund].astype(float)
            if np.nanstd(y) < 1e-12:
                continue

            X_df = df_all[factor_cols].astype(float)
            selector = SelectKBest(score_func=f_regression, k=K)
            selector.fit(X_df, y)

            kept = X_df.columns[selector.get_support()]
            X_sel = sm.add_constant(X_df[kept])
            res   = sm.OLS(y, X_sel).fit()

            # build full‐length beta vector
            beta_full = pd.Series(0.0, index=factor_cols)
            beta_full[kept] = res.params[kept]
            betas[fund]     = beta_full

            if return_metrics:
                metrics[fund] = {
                    "R2_in": res.rsquared,
                    "K": len(kept)
                }

    # ── NEW: SelectPercentile (top P% ANOVA features) ──
    elif method.lower() in ("select_percentile", "percentile"):
        P = 50  # top 50%; you can make this an argument
        for fund in funds:
            y = df_all[fund].astype(float)
            if np.nanstd(y) < 1e-12:
                continue

            X_df = df_all[factor_cols].astype(float)
            selector = SelectPercentile(score_func=f_regression,
                                        percentile=P)
            selector.fit(X_df, y)

            kept = X_df.columns[selector.get_support()]
            X_sel = sm.add_constant(X_df[kept])
            res   = sm.OLS(y, X_sel).fit()

            beta_full = pd.Series(0.0, index=factor_cols)
            beta_full[kept] = res.params[kept]
            betas[fund]     = beta_full

            if return_metrics:
                metrics[fund] = {
                    "R2_in": res.rsquared,
                    "percentile": P
                }

    else:
        raise ValueError(f"Unknown method {method}")

    beta_df = pd.DataFrame.from_dict(betas, orient='index')
    if return_metrics:
        metric_df = pd.DataFrame(metrics).T
        return beta_df, metric_df
    return beta_df
def main():

    factor_path = r"C:\repos\factors\pc1_returns_monthly_filled.xlsx"
    fund_path   = r"c:\repos\theexcels\johnjohn_funds_performance.xlsx"
    out_path    = r"C:\repos\factors\betas_all_methods3.xlsx"


    factors_df = pd.read_excel(factor_path, index_col=0, parse_dates=True)
    fund_rets  = pd.read_excel(fund_path,   index_col=0, parse_dates=True)

    # Make sure columns are strings (sometimes Excel gives weird types)
    factors_df.columns = factors_df.columns.astype(str)
    fund_rets.columns  = fund_rets.columns.astype(str)


    # (compute_betas_for_all will concat & dropna again,
    #  but we can clean early to get identical samples across methods)
    aligned = pd.concat([factors_df, fund_rets], axis=1)
    aligned = aligned.dropna(how='any')
    factors_df = aligned[factors_df.columns]
    fund_rets  = aligned[fund_rets.columns]

    beta_ols,  met_ols  = compute_betas_for_all(factors_df, fund_rets,
                                                method="ols", return_metrics=True)

    beta_rob,  met_rob  = compute_betas_for_all(factors_df, fund_rets,
                                                method="robust", return_metrics=True)

    beta_rdg,  met_rdg  = compute_betas_for_all(factors_df, fund_rets,
                                                method="ridge",
                                                cv_test=12, min_train=36,
                                                return_metrics=True)

    beta_pcr,  met_pcr  = compute_betas_for_all(factors_df, fund_rets,
                                                method="pcr",
                                                n_components=3,   # auto-pick k
                                                cv_test=12, min_train=36,
                                                return_metrics=True)

    beta_pls,  met_pls  = compute_betas_for_all(factors_df, fund_rets,
                                                method="pls",
                                                n_components=3,   # auto-pick k
                                                cv_test=12, min_train=36,
                                                return_metrics=True)
    beta_kbest, met_kbest = compute_betas_for_all(factors_df, fund_rets,
                                                  method="select_kbest",
                                                  return_metrics=True)
    beta_percentile, met_percentile = compute_betas_for_all(factors_df, fund_rets,
                                                             method="select_percentile",
                                                             return_metrics=True)

    with pd.ExcelWriter(out_path) as w:
        beta_ols.to_excel(w,   "OLS_betas")
        met_ols.to_excel(w,    "OLS_metrics")

        beta_rob.to_excel(w,   "ROBUST_betas")
        met_rob.to_excel(w,    "ROBUST_metrics")

        beta_rdg.to_excel(w,   "RIDGE_betas")
        met_rdg.to_excel(w,    "RIDGE_metrics")

        beta_pcr.to_excel(w,   "PCR_betas")
        met_pcr.to_excel(w,    "PCR_metrics")

        beta_pls.to_excel(w,   "PLS_betas")
        met_pls.to_excel(w,    "PLS_metrics")

        beta_kbest.to_excel(w, "KBest_betas")
        met_kbest.to_excel(w,  "KBest_metrics")

        beta_percentile.to_excel(w, "Percentile_betas")
        met_percentile.to_excel(w, "Percentile_metrics")

    print(f"Saved all betas & metrics to: {out_path}")


if __name__ == "__main__":
    main()

