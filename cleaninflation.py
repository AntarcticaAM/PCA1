import pandas as pd

file_path = r"C:\repos\theexcels\inflation_factors_cleaned.xlsx"

df = pd.read_excel(
    file_path,
    header=0,
    skiprows=[1, 2],
    index_col=0,
    parse_dates=True
)

# Find rows with NaN (before ffill)
nan_rows = df.isna().any(axis=1)

# Get the index of the row before each NaN row
donor_indices = df.index[nan_rows].to_list()
donor_indices = [df.index[df.index.get_loc(idx)-1] for idx in donor_indices if df.index.get_loc(idx) > 0]

# Forward fill
df_filled = df.ffill()

# Drop the donor rows
df_cleaned = df_filled.drop(donor_indices)

# (Optional) Remove rows with any 0s
df_cleaned = df_cleaned[(df_cleaned != 0).all(axis=1)]

df_cleaned.to_excel("inflation_factors_cleaned.xlsx")