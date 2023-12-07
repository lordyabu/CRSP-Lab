# This script focuses on trading data analysis, featuring a collection of functions for evaluating trading strategies.
# 'get_trade_stats' calculates various statistics for trades within a specific date range.
# 'plot_wins_and_losses' visually represents 100 sample trades, providing insights into trade performance over time.
# 'rank_stocks_by_pnl' ranks stocks based on their profitability, assisting in identifying the most and least successful stocks in a trading strategy.


from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
import matplotlib.pyplot as plt
import pandas as pd
import json
from tqdm import tqdm
from src.config import DATA_DIR
import os


def get_trade_stats(trades, start_date, end_date, selection_type='EndDate'):
    """
    Calculates various statistics for a given set of trades within a specified date range.

    Args:
        trades (pd.DataFrame): DataFrame containing trade data.
        start_date (str): The start date for the trade analysis.
        end_date (str): The end date for the trade analysis.

    Returns:
        dict: A dictionary containing calculated trade statistics.
    """
    # Filter trades by date range
    trades = trades[(trades[selection_type] >= start_date) & (trades[selection_type] <= end_date)]

    # Calculate durations
    trades['TradeDuration'] = trades['EndDate'] - trades['StartDate']

    # Calculate stats
    start_date = trades['StartDate'].min()
    end_date = trades['EndDate'].max()
    duration = end_date - start_date
    total_trades = len(trades)
    unique_stocks = trades['Symbol'].nunique()
    winning_trades = trades[trades['PnL%'] > 0]
    losing_trades = trades[trades['PnL%'] < 0]
    win_rate = (len(winning_trades) / total_trades) * 100
    avg_win = winning_trades['PnL%'].mean()
    avg_loss = losing_trades['PnL%'].mean()
    median_win = winning_trades['PnL%'].median()
    median_loss = losing_trades['PnL%'].median()
    avg_trade = trades['PnL%'].mean()
    median_trade = trades['PnL%'].median()
    total_return = trades['PnL'].sum()
    total_return_percent = trades['PnL%'].sum()
    min_exit_price_idx = trades['ExitPrice'].idxmin()
    min_enter_price_idx = trades['EnterPrice'].idxmin()
    min_pnl_percent_idx = trades['PnL%'].idxmin()
    max_pnl_percent_idx = trades['PnL%'].idxmax()
    longest_trade_duration = trades['TradeDuration'].max()
    shortest_trade_duration = trades['TradeDuration'].min()
    average_trade_duration = trades['TradeDuration'].mean()

    # Calculate stats including transaction costs
    total_transaction_cost_percent = trades['TransactionCost%'].sum()
    avg_trade_with_transaction_cost = (total_return_percent - total_transaction_cost_percent) / total_trades
    avg_win_with_transaction_cost = (avg_win * len(winning_trades) - total_transaction_cost_percent) / len(winning_trades)
    avg_loss_with_transaction_cost = (avg_loss * len(losing_trades) - total_transaction_cost_percent) / len(losing_trades)
    median_win_with_transaction_cost = median_win - (total_transaction_cost_percent / len(winning_trades))
    median_loss_with_transaction_cost = median_loss - (total_transaction_cost_percent / len(losing_trades))

    # Print stats
    print(f"Start: {start_date}")
    print(f"End: {end_date}")
    print(f"Duration: {duration}")
    print(f"# Trades: {total_trades}")
    print(f"# Different Stocks: {unique_stocks}")
    print(f"Win Rate [%]: {win_rate}")
    print(f"Avg. Trade [%]: {avg_trade}")
    print(f"Avg. Trade [%] (including Transaction Cost): {avg_trade_with_transaction_cost}")
    print(f"Median Trade [%]: {median_trade}")
    print(f"Avg. Win [%]: {avg_win}")
    print(f"Avg. Win [%] (including Transaction Cost): {avg_win_with_transaction_cost}")
    print(f"Median Win [%]: {median_win}")
    print(f"Median Win [%] (including Transaction Cost): {median_win_with_transaction_cost}")
    print(f"Avg. Loss [%]: {avg_loss}")
    print(f"Avg. Loss [%] (including Transaction Cost): {avg_loss_with_transaction_cost}")
    print(f"Median Loss [%]: {median_loss}")
    print(f"Median Loss [%] (including Transaction Cost): {median_loss_with_transaction_cost}")
    print(f"Total Return [%] (Where every trade is weighted equally): {total_return_percent}")
    print(f"Total Return [%] (including Transaction Cost): {total_return_percent - total_transaction_cost_percent}")
    print(f"Minimum Exit Price: {trades['ExitPrice'].min()}, Index: {min_exit_price_idx}")
    print(f"Minimum Enter Price: {trades['EnterPrice'].min()}, Index: {min_enter_price_idx}")
    print(f"Minimum PnL%: {trades['PnL%'].min()}, Index: {min_pnl_percent_idx}")
    print(f"Maximum PnL%: {trades['PnL%'].max()}, Index: {max_pnl_percent_idx}")
    print(f"Longest Trade Duration: {longest_trade_duration}")
    print(f"Shortest Trade Duration: {shortest_trade_duration}")
    print(f"Average Trade Duration: {average_trade_duration}")

    return {
        "Start": start_date,
        "End": end_date,
        "Duration": duration,
        "# Trades": total_trades,
        "# Different Stocks": unique_stocks,
        "Win Rate [%]": win_rate,
        "Avg. Trade [%]": avg_trade,
        "Avg. Trade [%] (including Transaction Cost)": avg_trade_with_transaction_cost,
        "Median Trade [%]": median_trade,
        "Avg. Win [%]": avg_win,
        "Avg. Win [%] (including Transaction Cost)": avg_win_with_transaction_cost,
        "Median Win [%]": median_win,
        "Median Win [%] (including Transaction Cost)": median_win_with_transaction_cost,
        "Avg. Loss [%]": avg_loss,
        "Avg. Loss [%] (including Transaction Cost)": avg_loss_with_transaction_cost,
        "Median Loss [%]": median_loss,
        "Median Loss [%] (including Transaction Cost)": median_loss_with_transaction_cost,
        "Total Return [%]": total_return_percent,
        "Total Return [%] (including Transaction Cost)": total_return_percent - total_transaction_cost_percent,
        "Longest Trade Duration": longest_trade_duration,
        "Shortest Trade Duration": shortest_trade_duration,
        "Average Trade Duration": average_trade_duration
    }


def get_trade_stats_cost_filter(trades, start_date, end_date, selection_type='EndDate', include_costs=False):
    """
    Calculates various statistics for a given set of trades within a specified date range,
    optionally including transaction costs.
    """
    filtered_trades = trades[(trades[selection_type] >= start_date) & (trades[selection_type] <= end_date)]

    # Calculate the trade duration in days
    filtered_trades['TradeDuration'] = (filtered_trades['EndDate'] - filtered_trades['StartDate']).dt.days

    total_trades = len(filtered_trades)
    unique_stocks = filtered_trades['Symbol'].nunique()
    winning_trades = filtered_trades[filtered_trades['PnL%'] > 0]
    losing_trades = filtered_trades[filtered_trades['PnL%'] < 0]
    win_rate = (len(winning_trades) / total_trades) * 100 if total_trades > 0 else 0
    avg_win = winning_trades['PnL%'].mean() if not winning_trades.empty else 0
    avg_loss = losing_trades['PnL%'].mean() if not losing_trades.empty else 0
    total_return_percent = filtered_trades['PnL%'].sum()

    # Calculate stats including transaction costs
    if include_costs:
        total_transaction_cost_percent = filtered_trades['TransactionCost%'].sum()
        avg_win_with_transaction_cost = (avg_win * len(winning_trades) - total_transaction_cost_percent) / len(winning_trades) if len(winning_trades) > 0 else 0
        avg_loss_with_transaction_cost = (avg_loss * len(losing_trades) - total_transaction_cost_percent) / len(losing_trades) if len(losing_trades) > 0 else 0
        avg_win = avg_win_with_transaction_cost
        avg_loss = avg_loss_with_transaction_cost
        total_return_percent -= total_transaction_cost_percent

    # Assembling the stats dictionary
    stats = {
        "Total Units Traded": total_trades,
        "Different Stocks": unique_stocks,
        "Win Rate": f"{round(win_rate, 2)}%",
        "Avg. Trade Return": f"{round(total_return_percent / total_trades if total_trades > 0 else 0, 2)}%",
        "Avg. Win on Trades": f"{round(avg_win, 2)}%",
        "Avg. Loss on Trades": f"{round(avg_loss, 2)}%",
        "Max Trade Duration": f"{filtered_trades['TradeDuration'].max()} days",
        "Avg. Trade Duration": f"{round(filtered_trades['TradeDuration'].mean(), 2)} days",
        "Total Return": f"{round(total_return_percent, 2)}%"
    }

    return stats






def plot_wins_and_losses(trades, start_date, end_date):
    """
    Plots sample of 100 trades over the timespan

    Args:
        trades (pd.DataFrame): DataFrame containing trade data.
        start_date (str): The start date for plotting the data.
        end_date (str): The end date for plotting the data.
    """
    trades = trades[(trades['EndDate'] >= start_date) & (trades['EndDate'] <= end_date)]

    # Sample 100 random trades if the total number of trades is more than 100
    if len(trades) > 100:
        trades_sample = trades.sample(n=100)
    else:
        trades_sample = trades

    # Separate winning and losing trades
    winning_trades = trades_sample[trades_sample['PnL'] > 0]
    losing_trades = trades_sample[trades_sample['PnL'] < 0]

    plt.figure(figsize=(14, 7))

    # Plot winning trades in green ($ and %)
    plt.scatter(winning_trades['EndDate'], winning_trades['PnL%'], color='lightgreen', label='Winning Trades [%]',
                alpha=1)

    # Plot losing trades in red ($ and %)
    plt.scatter(losing_trades['EndDate'], losing_trades['PnL%'], color='pink', label='Losing Trades [%]', alpha=1)

    # Adding labels and title
    plt.xlabel('Time')
    plt.ylabel('Trade Wins/Losses ($ and %)')
    plt.title('Sample of 100 Trade Wins and Losses Over Time')
    plt.legend()

    # Display the plot
    plt.show()


def rank_stocks_by_pnl(identifier, start_date, end_date):
    """
    Ranks stocks by total profit and loss (PnL) within a specified date range.

    Args:
        identifier (str): Identifier for filtering trades.
        start_date (str): The start date for the trade analysis.
        end_date (str): The end date for the trade analysis.

    Returns:
        pd.DataFrame: DataFrame containing stocks ranked by total PnL.
    """
    json_file_path = os.path.join(DATA_DIR, 'helperData', 'valid_stock_filenames.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    valid_stocks = data.get('valid_files')
    valid_stocks = [stock.replace('.csv', '') for stock in valid_stocks]

    stats_list = []

    for stock in tqdm(valid_stocks, desc='Processing stocks'):
        trades_df = extract_trades(identifier, 'EndDate', stock_name=stock)
        stats = get_trade_stats(trades_df, start_date, end_date)

        stats['Stock'] = stock
        stats_list.append(stats)

    # Create DataFrame from stats list
    stats_df = pd.DataFrame(stats_list)

    # Rank stocks by 'Total Return [%]'
    ranked_stocks = stats_df.sort_values(by='Total Return [%]', ascending=False)
    return ranked_stocks


import pandas as pd

def create_excel_report(identifier):
    # Extract trade data
    overall_trades = extract_trades(sort_by='EndDate', identifier=identifier)
    long_trades = extract_trades(sort_by='EndDate', identifier=identifier, trade_type='long')
    short_trades = extract_trades(sort_by='EndDate', identifier=identifier, trade_type='short')

    # Define date range
    start_date = '20181001'
    end_date = '20201231'

    # Prepare a DataFrame to store all stats
    all_stats = []

    # Get statistics for each trade type and for each cost scenario
    for trade_type, trades in [('Overall', overall_trades), ('Long', long_trades), ('Short', short_trades)]:
        for cost_label, include_costs in [('Without Costs', False), ('With Costs', True)]:
            stats = get_trade_stats_cost_filter(trades, start_date, end_date, include_costs=include_costs, selection_type='StartDate')
            stats['Trade Type'] = trade_type
            stats['Cost Scenario'] = cost_label
            all_stats.append(stats)

    # Combine all stats into a single DataFrame
    combined_df = pd.DataFrame(all_stats)

    # Reorder columns to put 'Trade Type' first
    column_order = ['Trade Type', 'Cost Scenario'] + [col for col in combined_df if col not in ['Trade Type', 'Cost Scenario']]
    combined_df = combined_df[column_order]

    # Write to Excel
    combined_df.to_excel(f"{identifier}_combined_trade_stats.xlsx", index=False)

create_excel_report("test1turtles")
