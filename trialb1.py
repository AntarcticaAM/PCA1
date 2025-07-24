# trialb1.py  — export PC1 returns, month-end aligned & forward-filled

import pandas as pd
import numpy as np

# ---- 1) Load/concat your PC1 series (replace these imports with yours) ----
from PCAgrowth      import pc1_returns_growth
from PCAvalue       import pc1_returns_value
from PCAquality     import pc1_returns_quality
from PCAinflation   import pc1_returns_inflation
from PCAcommodity   import pc1_returns_commodity
from PCAdenfensive  import pc1_returns_defensive   # check exact filename/var
from PCAgrowded     import pc1_returns_crowded
from PCArealestate  import pc1_returns_realestate
from PCAshortvol    import pc1_returns_shortvol
from PCAsize        import pc1_returns_size
from PCAmomentum    import pc1_returns_momentum  # check exact filename/var
# add any others…

pc1_df = pd.concat(
    [
        pc1_returns_growth.rename('growth'),
        pc1_returns_value.rename('value'),
        pc1_returns_quality.rename('quality'),
        pc1_returns_inflation.rename('inflation'),
        pc1_returns_commodity.rename('commodity'),
        pc1_returns_defensive.rename('defensive'),
        pc1_returns_crowded.rename('crowded'),
        pc1_returns_realestate.rename('realestate'),
        pc1_returns_shortvol.rename('shortvol'),
        pc1_returns_size.rename('size'),
        pc1_returns_momentum.rename('momentum'),
    ],
    axis=1
)

# ---- 2) Clean index & values ----
pc1_df.index = pd.to_datetime(pc1_df.index)
pc1_df = pc1_df[~pc1_df.index.duplicated(keep='last')].sort_index()
pc1_df = pc1_df.replace([np.inf, -np.inf], np.nan)

# ---- 3) Month-end align & forward fill (EASIEST FIX) ----
# Take the last available obs each month, then ffill to fill gaps
monthly_last   = pc1_df.resample('M').last()
monthly_filled = monthly_last.ffill()

# Optional: limit how far you forward-fill
# monthly_filled = monthly_last.ffill(limit=3)

# ---- 4) (Optional) Rescale if some factors look like % instead of decimals ----
# Decide per column: if median abs value > 1 => divide by 100
scales = {}
for c in monthly_filled.columns:
    med = monthly_filled[c].abs().median()
    scales[c] = 100.0
monthly_filled = monthly_filled.div(pd.Series(scales))
print("Applied scales:", scales)

# ---- 5) Save ----
out_path = r"C:\repos\factors\pc1_returns_monthly_filled.xlsx"
monthly_filled.to_excel(out_path)
print(f"Saved to {out_path}")

