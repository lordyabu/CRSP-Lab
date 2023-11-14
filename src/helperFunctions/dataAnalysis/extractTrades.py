# This script defines a function to extract specific trades from a trade log based on various criteria such as identifier,
# strategy, stock name, and trade type. The function allows for sorting the extracted trades and returns the filtered results.

import pandas as pd
from src.helperFunctions.tradeLog.getTradeLogPath import get_full_tradelog_path


def extract_trades(identifier=None, strategy=None, sort_by='EndDate', stock_name=None, trade_type=None):
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

    full_tradelog_path = get_full_tradelog_path()
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
    if strategy:
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
