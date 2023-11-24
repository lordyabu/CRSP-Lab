import pandas as pd
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades

def compare_two():
    trades_one = extract_trades(identifier='test1bollinger')
    trades_two = extract_trades(identifier='test2bollinger')

    cols_to_exclude = ['Identifier', 'TradeIndex']

    # Perform an outer merge on all columns except those to be excluded
    merged_df = pd.merge(trades_one.drop(columns=cols_to_exclude),
                         trades_two.drop(columns=cols_to_exclude),
                         how='outer',
                         indicator=True,
                         left_index=True,
                         right_index=True)

    # Filter rows that are unique to each dataframe
    unique_in_one = merged_df[merged_df['_merge'] == 'left_only']
    unique_in_two = merged_df[merged_df['_merge'] == 'right_only']

    # Re-add the TradeIndex column for printing
    unique_in_one['TradeIndex'] = trades_one['TradeIndex']
    unique_in_two['TradeIndex'] = trades_two['TradeIndex']

    # Print out TradeIndex and DataFrame source for unique rows
    for index, row in unique_in_one.iterrows():
        print(f"TradeIndex: {row['TradeIndex']}, Source: trades_one")

    for index, row in unique_in_two.iterrows():
        print(f"TradeIndex: {row['TradeIndex']}, Source: trades_two")

compare_two()
