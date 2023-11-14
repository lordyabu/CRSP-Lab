# This script contains a suite of visualization functions for trade data analysis. Each function takes trade data as input
# and creates various plots to analyze different aspects of trading performance. Functions include plotting histograms of
# logarithmic returns, cumulative returns over time, rolling volatility, and Sharpe ratios, as well as drawdowns,
# underwater charts, and distributions of monthly and annual returns.


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_log_return_histogram(trades):
    trades['LogReturn'] = np.log(trades['PnL%'] / trades['PnL%'].shift(1))
    trades = trades.replace([np.inf, -np.inf], np.nan).dropna(subset=['LogReturn'])
    trades['LogReturn'].hist(bins=50, alpha=0.6, color='blue')
    plt.title('Log Realized Return Histogram')
    plt.xlabel('Log Return')
    plt.ylabel('Frequency')
    plt.show()


def plot_cumulative_returns(trades):
    # Sort the DataFrame by 'EndDate' in ascending order
    trades = trades.sort_values(by='EndDate')

    # Calculate the cumulative sum of 'PnL%' at each timestamp
    trades['CumulativeReturn'] = trades['PnL%'].cumsum()

    # Plot the cumulative returns
    plt.figure(figsize=(14, 7))
    plt.plot(trades['EndDate'], trades['CumulativeReturn'])
    plt.title('Cumulative Realized Returns Over Time')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.show()


def plot_cumulative_returns_and_trades(trades):
    trades = trades.sort_values(by='EndDate')

    # Calculate the cumulative sum of 'PnL%'
    trades['CumulativeReturn'] = trades['PnL%'].cumsum()

    # Create a new DataFrame with a continuous date range
    date_range = pd.date_range(start=trades['EndDate'].min(), end=trades['EndDate'].max())
    date_df = pd.DataFrame(date_range, columns=['EndDate'])

    # Merge with the original data
    merged_df = pd.merge(date_df, trades, on='EndDate', how='left')

    # Forward fill the 'CumulativeReturn' to account for dates with no trades
    merged_df['CumulativeReturn'] = merged_df['CumulativeReturn'].ffill()

    # Calculate the cumulative number of trades over time
    merged_df['TradeCount'] = merged_df['PnL%'].notnull().cumsum()

    # Plotting
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Plot cumulative returns
    ax1.plot(merged_df['EndDate'], merged_df['CumulativeReturn'], color='b', label='Cumulative Return', alpha=0.5)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Cumulative Realized Return', color='b')
    ax1.tick_params(axis='y', labelcolor='b')

    # Secondary y-axis for the cumulative number of trades
    ax2 = ax1.twinx()
    ax2.plot(merged_df['EndDate'], merged_df['TradeCount'], color='r', label='Cumulative Number of Trades')
    ax2.set_ylabel('Cumulative Number of Trades Realized', color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    # Add legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Cumulative Realized Returns and Cumulative Number of Realized Trades Over Time')
    plt.show()


def plot_rolling_volatility(trades):
    # Assuming 21 trading days in a month, for a 6-month window
    window_size = 21 * 6

    # Group by 'EndDate' and apply rolling standard deviation
    trades['RollingVol'] = trades.groupby('EndDate')['PnL%'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1).std() * np.sqrt(window_size)
    )

    # Plotting
    trades.plot(x='EndDate', y='RollingVol', figsize=(14, 7))
    plt.title('6-Month Rolling Volatility')
    plt.xlabel('EndDate')
    plt.ylabel('Volatility')
    plt.show()


def plot_rolling_sharpe_ratio(trades):
    # Assuming 21 trading days in a month, for a 6-month window
    window_size = 21 * 6

    # 10yr treasury yield
    risk_free_rate = 0.4

    # Sort trades by 'EndDate'
    trades = trades.sort_values(by='EndDate')

    # Calculate rolling mean and standard deviation of 'PnL%'
    rolling_mean = trades['PnL%'].rolling(window=window_size, min_periods=1).mean()
    rolling_std = trades['PnL%'].rolling(window=window_size, min_periods=1).std().replace(0, 1e-6)

    # Calculate Sharpe Ratio
    trades['RollingSharpe'] = (rolling_mean - risk_free_rate) / rolling_std * np.sqrt(252)

    # Plotting
    trades.iloc[250:].plot(x='EndDate', y='RollingSharpe', figsize=(14, 7))
    plt.title('6-Month Rolling Sharpe Ratio')
    plt.xlabel('EndDate')
    plt.ylabel('Sharpe Ratio')
    plt.show()


def plot_drawdowns_over_time(trades):
    trades = trades.sort_values(by='EndDate')
    trades['CumulativeReturn'] = trades['PnL%'].cumsum()
    trades['Peak'] = trades['CumulativeReturn'].cummax()
    trades['Drawdown'] = (trades['CumulativeReturn'] - trades['Peak']) / trades['Peak']

    # Plotting the entire Drawdown series
    trades.iloc[250:].plot(x='EndDate', y='Drawdown', kind='line')
    plt.title('Drawdown Over Time')
    plt.xlabel('EndDate')
    plt.ylabel('Drawdown')
    plt.show()


def calculate_drawdowns(trades):
    trades = trades.sort_values(by='EndDate')
    trades['CumulativeReturn'] = trades['PnL%'].cumsum()
    trades['Peak'] = trades['CumulativeReturn'].cummax()
    trades['Drawdown'] = (trades['CumulativeReturn'] - trades['Peak']) / trades['Peak']
    return trades


def plot_underwater_chart(trades):
    drawdowns = calculate_drawdowns(trades)
    drawdowns_filtered = drawdowns.iloc[250:]
    drawdowns_filtered.plot(x='EndDate', y='Drawdown', figsize=(14, 7))
    plt.title('Underwater Plot')
    plt.xlabel('EndDate')
    plt.ylabel('Drawdown')
    plt.fill_between(drawdowns_filtered['EndDate'], drawdowns_filtered['Drawdown'], color='blue', alpha=0.3)
    plt.show()


def plot_monthly_returns(trades):
    # Ensure 'EndDate' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(trades['EndDate']):
        trades['EndDate'] = pd.to_datetime(trades['EndDate'])

    # Extract the month from 'EndDate'
    trades['Month'] = trades['EndDate'].dt.to_period('M')

    # Group by month and sum the 'PnL%'
    monthly_returns = trades.groupby('Month')['PnL%'].sum()

    # Plotting
    monthly_returns.plot(kind='bar', figsize=(14, 7))
    plt.title('Monthly Returns')
    plt.xlabel('Month')
    plt.ylabel('Total Return %')
    plt.show()


def plot_annual_returns(trades):
    # Ensure 'EndDate' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(trades['EndDate']):
        trades['EndDate'] = pd.to_datetime(trades['EndDate'])

    # Extract the year from 'EndDate'
    trades['Year'] = trades['EndDate'].dt.to_period('Y')

    # Group by year and sum the 'PnL%'
    annual_returns = trades.groupby('Year')['PnL%'].sum()

    # Plotting
    annual_returns.plot(kind='bar', figsize=(14, 7))
    plt.title('Annual Returns')
    plt.xlabel('Year')
    plt.ylabel('Total Return %')
    plt.show()


def plot_distribution_of_monthly_returns(trades):
    # Ensure 'EndDate' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(trades['EndDate']):
        trades['EndDate'] = pd.to_datetime(trades['EndDate'])

    # Extract the month from 'EndDate'
    trades['Month'] = trades['EndDate'].dt.to_period('M')

    # Group by month and sum the 'PnL%'
    monthly_total_returns = trades.groupby('Month')['PnL%'].sum()

    # Count the number of trades each month
    monthly_trade_counts = trades.groupby('Month').size()

    # Calculate average return per trade for each month
    monthly_avg_returns = monthly_total_returns / monthly_trade_counts

    # Plotting the histogram
    monthly_avg_returns.hist(bins=50, alpha=0.6, color='green')
    plt.title('Distribution of Average Monthly Returns per Trade')
    plt.xlabel('Average Monthly Return(%)')
    plt.ylabel('Frequency')
    plt.show()


def plot_distribution_of_annual_returns(trades):
    # Ensure 'EndDate' is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(trades['EndDate']):
        trades['EndDate'] = pd.to_datetime(trades['EndDate'])

    # Extract the year from 'EndDate'
    trades['Year'] = trades['EndDate'].dt.to_period('Y')

    # Group by year and sum the 'PnL%'
    annual_total_returns = trades.groupby('Year')['PnL%'].sum()

    # Count the number of trades each year
    annual_trade_counts = trades.groupby('Year').size()

    # Calculate average return per trade for each year
    annual_avg_returns = annual_total_returns / annual_trade_counts

    # Plotting the histogram
    annual_avg_returns.hist(bins=50, alpha=0.6, color='green')
    plt.title('Distribution of Average Annual Returns per Trade')
    plt.xlabel('Average Annual Return(%)')
    plt.ylabel('Frequency')
    plt.show()


# Looks good
def plot_return_quantiles(trades):
    # Calculate the desired quantiles of 'PnL%'
    quantiles = trades['PnL%'].quantile([0.1, 0.25, 0.5, 0.75, 0.9])

    # Plotting the quantiles as a bar chart
    quantiles.plot(kind='bar')
    plt.title('Return Quantiles')
    plt.xlabel('Quantile')
    plt.ylabel('PnL %')
    plt.xticks(rotation=0)  # This will ensure quantile labels are horizontal for readability
    plt.show()


def plot_everything(trades_df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the DataFrame for trades within the specified date range
    trades_df = trades_df[(trades_df['EndDate'] >= start_date) & (trades_df['EndDate'] <= end_date)]

    plot_log_return_histogram(trades_df)
    plot_cumulative_returns(trades_df)
    plot_cumulative_returns_and_trades(trades_df)
    plot_rolling_volatility(trades_df)
    plot_rolling_sharpe_ratio(trades_df)
    # plot_drawdowns_over_time(trades_df) - Need to debug
    # plot_underwater_chart(trades_df) - Need to debug
    plot_monthly_returns(trades_df)
    plot_annual_returns(trades_df)
    plot_distribution_of_monthly_returns(trades_df)
    plot_distribution_of_annual_returns(trades_df)
    plot_return_quantiles(trades_df)
