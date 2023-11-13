from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
import matplotlib.pyplot as plt
from src.helperFunctions.dataAnalysis.filterBadTrades import remove_naive
import pandas as pd
import json
from tqdm import tqdm
from src.config import DATA_DIR
import os
def get_trade_stats(trades, start_date, end_date):
    # Calculate durations
    trades = trades[(trades['EndDate'] >= start_date) & (trades['EndDate'] <= end_date)]


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
    median_win = winning_trades['PnL%'].median()  # Median win
    median_loss = losing_trades['PnL%'].median()  # Median loss
    avg_trade = trades['PnL%'].mean()
    median_trade = trades['PnL%'].median()  # Median trade
    total_return = trades['PnL'].sum()
    total_return_percent = trades['PnL%'].sum()  # Total return percentage

    # Print stats
    print(f"Start: {start_date}")
    print(f"End: {end_date}")
    print(f"Duration: {duration}")
    print(f"# Trades: {total_trades}")
    print(f"# Different Stocks: {unique_stocks}")
    print(f"Win Rate [%]: {win_rate}")
    print(f"Avg. Trade [%]: {avg_trade}")
    print(f"Median Trade [%]: {median_trade}")
    print(f"Avg. Win [%]: {avg_win}")
    print(f"Median Win [%]: {median_win}")
    print(f"Avg. Loss [%]: {avg_loss}")
    print(f"Median Loss [%]: {median_loss}")
    print(f"Total Return [%] (Where every trade is weighted equally): {total_return_percent}")

    return {
        "Start": start_date,
        "End": end_date,
        "Duration": duration,
        "# Trades": total_trades,
        "# Different Stocks": unique_stocks,
        "Win Rate [%]": win_rate,
        "Avg. Trade [%]": avg_trade,
        "Median Trade [%]": median_trade,
        "Avg. Win [%]": avg_win,
        "Median Win [%]": median_win,
        "Avg. Loss [%]": avg_loss,
        "Median Loss [%]": median_loss,
        "Total Return [%]": total_return_percent
    }

def plot_wins_and_losses(trades):
    # Sample 100 random trades if the total number of trades is more than 100
    if len(trades) > 100:
        trades_sample = trades.sample(n=100)
    else:
        trades_sample = trades

    # Separate winning and losing trades
    winning_trades = trades_sample[trades_sample['PnL'] > 0]
    losing_trades = trades_sample[trades_sample['PnL'] < 0]

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot winning trades in green ($ and %)
    plt.scatter(winning_trades['EndDate'], winning_trades['PnL%'], color='lightgreen', label='Winning Trades [%]', alpha=1)

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


# Usage
trades_df = extract_trades('test6turtle', 'EndDate', stock_name='LNC')



# Define your start and end dates
start_date = '2010-01-04'
end_date = '2020-12-31'
# Call the function with the date range
a = get_trade_stats(trades_df, start_date, end_date)

min_exit_price_idx = trades_df['ExitPrice'].idxmin()
min_enter_price_idx = trades_df['EnterPrice'].idxmin()
min_pnl_percent_idx = trades_df['PnL%'].idxmin()
max_pnl_percent_idx = trades_df['PnL%'].idxmax()

# Print the minimum values and their corresponding indices
print(f"Minimum Exit Price: {trades_df['ExitPrice'].min()}, Index: {min_exit_price_idx}")
print(f"Minimum Enter Price: {trades_df['EnterPrice'].min()}, Index: {min_enter_price_idx}")
print(f"Minimum PnL%: {trades_df['PnL%'].min()}, Index: {min_pnl_percent_idx}")

# Print the maximum PnL% and its corresponding index
print(f"Maximum PnL%: {trades_df['PnL%'].max()}, Index: {max_pnl_percent_idx}")


df = rank_stocks_by_pnl('test6turtle', start_date, end_date)

df.to_csv('turtle_rankings.csv')