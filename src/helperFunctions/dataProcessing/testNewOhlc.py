from src.config import DATA_DIR, PRICE_DATA_DIR
import os
import pandas as pd

date_do = 20201231
stock_name = 'AAPL'


our_data = os.path.join(DATA_DIR, 'priceData', 'AAPL.csv')
five_min_directory = os.path.join(DATA_DIR, 'dataFiveMin', '.csv')
five_file_path = os.path.join(five_min_directory, f"Day_{date_do}.csv")


our_data_df = pd.read_csv(our_data)
five_min_df = pd.read_csv(five_file_path, usecols=[stock_name])


# Find the row in our_data_df where the 'Day' column matches date_our
matching_row = our_data_df[our_data_df['date'] == date_do]

# Check if there's a matching row
if not matching_row.empty:
    # Retrieve the 'Open' and 'Close' values (assuming these represent 'OPENPRC' and 'PRC')
    open_prc = matching_row['OPENPRC'].iloc[0]
    prc = matching_row['PRC'].iloc[0]  # Assuming 'Close' is the 'PRC'

    print(f"OPENPRC: {open_prc}, PRC: {prc}")
else:
    print(f"No data found for date: {date_do}")

# Okay so ours matches historical

curr_price = open_prc
prices = [curr_price]
for i, row in five_min_df.iterrows():
    curr_price *= (1 + row['AAPL'])
    prices.append(curr_price)

for p in prices:
    print(p)

print(min(prices), max(prices))

