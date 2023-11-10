from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
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
    avg_win_percent = winning_trades['PnL%'].mean()  # Average win percentage
    avg_loss_percent = losing_trades['PnL%'].mean()  # Average loss percentage
    avg_trade = trades['PnL'].mean()
    avg_trade_percent = trades['PnL%'].mean()
    max_trade_duration = trades['TradeDuration'].max()
    avg_trade_duration = trades['TradeDuration'].mean()
    total_return = trades['PnL'].sum()
    total_return_percent = trades['PnL%'].sum()  # Total return percentage

    # Print stats
    print(f"Start: {start_date}")
    print(f"End: {end_date}")
    print(f"Duration: {duration}")
    print(f"# Trades: {total_trades}")
    print(f"# Different Stocks: {unique_stocks}")
    print(f"Win Rate [%]: {win_rate}")
    print(f"Avg. Trade [%]: {avg_trade_percent}")
    print(f"Avg. Win [%]: {avg_win_percent}")
    print(f"Avg. Loss [%]: {avg_loss_percent}")
    # print(f"Best Trade [$]: {best_trade}")
    # print(f"Worst Trade [$]: {worst_trade}")
    # print(f"Avg. Trade [$]: {avg_trade}")
    # print(f"Avg. Win [$]: {avg_win}")
    # print(f"Avg. Loss [$]: {avg_loss}")
    print(f"Max. Trade Duration: {max_trade_duration}")
    print(f"Avg. Trade Duration: {avg_trade_duration}")
    # print(f"Total Return [$] (Using each trade = 1 share): {total_return}")
    print(f"Total Return [%] (Where every trade is weighted equally): {total_return_percent}")

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

# Usage
trades_df = extract_trades('test1', 'EndDate')
get_trade_stats(trades_df)
plot_wins_and_losses(trades_df)
