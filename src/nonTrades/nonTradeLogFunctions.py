from src.config import DATA_DIR
import os
import json
from pathlib import Path
import pandas as pd


def get_full_nontradelog_path():
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    start_date = data.get('start_date')
    end_date = data.get('end_date')

    filename = f"allnonTrades_{start_date}_to_{end_date}_doctest2.csv"
    full_nontradelog_path = os.path.join(DATA_DIR, 'nonTradeData', filename)

    return full_nontradelog_path


def remove_non_trades(identifier):
    full_nontradelog_path = get_full_nontradelog_path()

    df = pd.read_csv(full_nontradelog_path)
    df_filtered = df[df['Identifier'] != identifier]

    df_filtered.to_csv(full_nontradelog_path, index=False)
    print(f"non trades with identifier '{identifier}' have been removed.")


def nonlog_to_json(log_file_path, log_entries):
    """
    Appends a list of non-trade entries to a specified JSON log file, creating or resetting it if necessary.

    This function checks if the specified log file exists and contains valid JSON. If so, it loads the existing log data,
    appends the new entries to it, and then writes the updated data back to the file. If the file doesn't exist or contains invalid JSON,
    it starts with an empty log and adds the new entries.

    Args:
        log_file_path (str or Path): Path to the non-trade log file. Can be a string or a Path object.
        log_entries (list): A list of non-trade entries (dictionaries) to log.
    """
    # Convert string path to Path object if necessary
    log_file_path = Path(log_file_path) if isinstance(log_file_path, str) else log_file_path

    # If the file exists and is not empty, load its content. Otherwise, start with an empty list.
    if log_file_path.is_file() and os.path.getsize(log_file_path) > 0:
        with open(log_file_path, 'r') as file:
            try:
                log_data = json.load(file)
            except json.JSONDecodeError:
                log_data = []  # Reset if the file content is not valid JSON
    else:
        log_data = []

    # Extend the log data with the new entries
    log_data.extend(log_entries)

    # Write the updated log data back to the file
    with open(log_file_path, 'w') as file:
        json.dump(log_data, file, indent=4)



def save_nontradelog(non_trade_log):
    """
    Saves the non-trade log to a CSV file, appending to the existing log if it exists.

    Args:
        non_trade_log (pd.DataFrame): The DataFrame containing the non-trade log data.
    """
    new_non_trades_df = non_trade_log.get_non_trade_dataframe()
    full_nontradelog_path = get_full_nontradelog_path()

    # Append new non-trade data to the existing file
    new_non_trades_df.to_csv(full_nontradelog_path, mode='a', header=not os.path.exists(full_nontradelog_path), index=False)


def update_nontrade_index(full_nontradelog_path):
    if os.path.exists(full_nontradelog_path):
        nontradelog_df = pd.read_csv(full_nontradelog_path)

        # Ensure 'TradeIndex' is a column and update it
        nontradelog_df.reset_index(drop=True, inplace=True)
        nontradelog_df['TradeIndex'] = nontradelog_df.index + 1

        # Save the updated non-trade log
        nontradelog_df.to_csv(full_nontradelog_path, index=False)

def extract_nontrades(identifier=None, strategy=None, sort_by='EndDate', stock_name=None, trade_type=None):
    """
    Extracts trades from a trade log based on specified criteria and returns a sorted DataFrame of these trades.

    This function filters trades in a trade log by various criteria including identifier, strategy, stock name, and trade type.
    The filtered trades are then sorted based on a specified column. At least one of 'identifier' or 'strategy' must be provided.

    Args:
        identifier (str, optional): The identifier to filter trades. Defaults to None.
        strategy (str, optional): The strategy to filter trades. Defaults to None.
        sort_by (str): The column name to sort the extracted trades by. Defaults to 'EndDate'.
        stock_name (str, optional): The stock name to further filter trades. Defaults to None.
        trade_type (str, optional): The type of trade to further filter. Defaults to None.

    Returns:
        pandas.DataFrame: A DataFrame containing the sorted, filtered trades.

    Raises:
        ValueError: If neither 'identifier' nor 'strategy' is provided.

    """
    # Check that at least one of identifier or strategy is provided
    if identifier is None and strategy is None:
        raise ValueError("At least one of 'identifier' or 'strategy' must be provided")

    full_tradelog_path = get_full_nontradelog_path()
    df = pd.read_csv(full_tradelog_path)

    # Convert 'StartDate' and 'EndDate' to datetime
    df['StartDate'] = pd.to_datetime(df['StartDate'], format='%Y%m%d')
    df['EndDate'] = pd.to_datetime(df['EndDate'], format='%Y%m%d')

    # Initialize the filter
    filter_condition = pd.Series([False] * len(df))

    # Apply identifier filter if provided
    if identifier:
        filter_condition |= (df['Identifier'] == identifier)

    # Apply strategy filter if provided
    if strategy and not identifier:
        filter_condition |= (df['Strategy'] == strategy)

    # Apply the filter
    df_filtered = df[filter_condition]

    # Additional filters for stock name and trade type
    if stock_name:
        df_filtered = df_filtered[df_filtered['Symbol'] == stock_name]
    if trade_type:
        df_filtered = df_filtered[df_filtered['TradeType'] == trade_type]

    # Sort the filtered DataFrame
    df_sorted = df_filtered.sort_values(by=sort_by)

    # Return the sorted DataFrame
    return df_sorted


def remove_non_trades(identifier):
    """
    Removes non-trades with a specific identifier from the non-trade log file.

    This function reads the non-trade log file, filters out all non-trades with the given identifier,
    and then saves the updated log back to the file. The function relies on 'get_full_nontradelog_path'
    to determine the path of the non-trade log file.

    Args:
        identifier (str): The identifier used to filter out non-trades. Non-trades with this identifier will be removed from the log.
    """

    full_nontradelog_path = get_full_nontradelog_path()  # Function to get the path of the non-trade log

    df = pd.read_csv(full_nontradelog_path)

    # Filter out the rows where 'Identifier' column matches the identifier
    df_filtered = df[df['Identifier'] != identifier]

    # Save the filtered DataFrame back to the CSV
    df_filtered.to_csv(full_nontradelog_path, index=False)
    print(f"Non-trades with identifier '{identifier}' have been removed.")


#  Removes from file starting wil allnonTrades
# identifier_to_remove = 'NonTradetest1turtles_34_33_33'
# remove_non_trades(identifier_to_remove)