import pandas as pd
from config import DATA_DIR
import os

full_tradelog_path = os.path.join(DATA_DIR, 'tradeData', 'allTrades.csv')


def remove_trades(identifier):
    df = pd.read_csv(full_tradelog_path)

    # Filter out the rows where 'Identifier' column matches the identifier
    df_filtered = df[df['Identifier'] != identifier]

    # Save the filtered DataFrame back to the CSV
    df_filtered.to_csv(full_tradelog_path, index=False)
    print(f"Trades with identifier '{identifier}' have been removed.")


# Usage example
identifier_to_remove = 'test1'
remove_trades(identifier_to_remove)
