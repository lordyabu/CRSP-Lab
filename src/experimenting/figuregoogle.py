from config import OHLC_DATA_DIR
import os
import pandas as pd

path = os.path.join(OHLC_DATA_DIR, 'GOOG.csv')
df = pd.read_csv(path)

# List to store dates of rows where any of the specified columns have NaN values
dates_with_nans = []

# Columns to check for NaN values
nan_check_columns = ['Open', 'High', 'Low', 'Close', 'PRC', 'OPENPRC', 'RET']

for i, row in df.iterrows():
    # Check if any of the specified columns have NaN value in the current row
    if row[nan_check_columns].isnull().any():
        dates_with_nans.append(row['date'])

# Now, dates_with_nans contains the dates of all rows where any of the specified columns have NaN values
print("Dates with NaNs in specified columns:", dates_with_nans)
