from helperClasses.extractTrades import extract_trades
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
def get_trade_stats(trades):
    # Calculate durations
    trades['TradeDuration'] = trades['EndDate'] - trades['StartDate']

    # Calculate stats
    start_date = trades['StartDate'].min()
    end_date = trades['EndDate'].max()
    duration = end_date - start_date
    total_trades = len(trades)
    unique_stocks = trades['Symbol'].nunique()
    winning_trades = trades[trades['PnL'] > 0]
    losing_trades = trades[trades['PnL'] < 0]
    win_rate = (len(winning_trades) / total_trades) * 100
    best_trade = winning_trades['PnL'].max()
    worst_trade = losing_trades['PnL'].min()
    avg_win = winning_trades['PnL'].mean()
    avg_loss = losing_trades['PnL'].mean()
    avg_trade = trades['PnL'].mean()
    max_trade_duration = trades['TradeDuration'].max()
    avg_trade_duration = trades['TradeDuration'].mean()
    total_return = trades['PnL'].sum()

    # Print stats
    print(f"Start: {start_date}")
    print(f"End: {end_date}")
    print(f"Duration: {duration}")
    print(f"# Trades: {total_trades}")
    print(f"# Different Stocks: {unique_stocks}")
    print(f"Win Rate [%]: {win_rate}")
    print(f"Best Trade [%]: {best_trade}")
    print(f"Worst Trade [%]: {worst_trade}")
    print(f"Avg. Win [%]: {avg_win}")
    print(f"Avg. Loss [%]: {avg_loss}")
    print(f"Avg. Trade [%]: {avg_trade}")
    print(f"Max. Trade Duration: {max_trade_duration}")
    print(f"Avg. Trade Duration: {avg_trade_duration}")
    print(f"Total Return [$] (Using each trade = $1): {total_return}")


def plot_wins_and_losses(trades):
    # Sample 100 random trades if the total number of trades is more than 100
    if len(trades) > 100:
        trades_sample = trades.sample(n=100, random_state=1)  # random_state for reproducibility
    else:
        trades_sample = trades

    # Separate winning and losing trades
    winning_trades = trades_sample[trades_sample['PnL'] > 0]
    losing_trades = trades_sample[trades_sample['PnL'] < 0]

    # Plotting
    plt.figure(figsize=(10, 6))

    # Plot winning trades in green
    plt.scatter(winning_trades['EndDate'], winning_trades['PnL'], color='green', label='Winning Trades')

    # Plot losing trades in red
    plt.scatter(losing_trades['EndDate'], losing_trades['PnL'], color='red', label='Losing Trades')

    # Adding labels and title
    plt.xlabel('Time')
    plt.ylabel('Trade Wins/Losses')
    plt.title('Sample of 100 Trade Wins and Losses Over Time')
    plt.legend()

    # Display the plot
    plt.show()

# Usage
trades_df = extract_trades('test1', 'EndDate')
get_trade_stats(trades_df)
plot_wins_and_losses(trades_df)
