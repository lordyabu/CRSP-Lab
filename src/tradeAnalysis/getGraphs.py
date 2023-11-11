import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades


def plot_log_return_histogram(trades):
    trades['LogReturn'] = np.log(trades['PnL%'] / trades['PnL%'].shift(1))
    trades['LogReturn'].hist(bins=50, alpha=0.6, color='blue')
    plt.title('Log Return Histogram')
    plt.xlabel('Log Return')
    plt.ylabel('Frequency')
    plt.show()


def plot_cumulative_returns(trades):
    trades['CumulativeReturn'] = (1 + trades['PnL%']).cumprod()
    trades['CumulativeReturn'].plot(figsize=(14, 7))
    plt.title('Cumulative Returns Over Time')
    plt.xlabel('Time')
    plt.ylabel('Cumulative Return')
    plt.show()


def plot_log_cumulative_returns(trades):
    trades['LogCumulativeReturn'] = np.log(1 + trades['PnL%']).cumsum()
    trades['LogCumulativeReturn'].plot(figsize=(14, 7))
    plt.title('Log Cumulative Returns')
    plt.xlabel('Time')
    plt.ylabel('Log Cumulative Return')
    plt.show()


def plot_rolling_volatility(trades):
    trades['RollingVol'] = trades['PnL%'].rolling(window=126).std() * np.sqrt(126)  # Assuming 21 trading days in a month
    trades['RollingVol'].plot(figsize=(14, 7))
    plt.title('6-Month Rolling Volatility')
    plt.xlabel('Time')
    plt.ylabel('Volatility')
    plt.show()


def plot_rolling_sharpe_ratio(trades):
    trades['RollingSharpe'] = trades['PnL%'].rolling(window=126).mean() / trades['PnL%'].rolling(window=126).std()
    trades['RollingSharpe'].plot(figsize=(14, 7))
    plt.title('6-Month Rolling Sharpe Ratio')
    plt.xlabel('Time')
    plt.ylabel('Sharpe Ratio')
    plt.show()


# For this, you need a drawdown calculation function. This is a simplified version.
def calculate_drawdowns(trades):
    trades['Peak'] = trades['CumulativeReturn'].cummax()
    trades['Drawdown'] = (trades['CumulativeReturn'] - trades['Peak']) / trades['Peak']
    return trades.sort_values('Drawdown').head(5)

def plot_top_drawdowns(trades):
    top_drawdowns = calculate_drawdowns(trades)
    top_drawdowns['Drawdown'].plot(kind='bar')
    plt.title('Top 5 Drawdown Periods')
    plt.xlabel('Time')
    plt.ylabel('Drawdown')
    plt.show()


def plot_underwater_chart(trades):
    drawdowns = calculate_drawdowns(trades)
    drawdowns['Drawdown'].plot(figsize=(14, 7))
    plt.title('Underwater Plot')
    plt.xlabel('Time')
    plt.ylabel('Drawdown')
    plt.fill_between(drawdowns.index, drawdowns['Drawdown'], color='blue', alpha=0.3)
    plt.show()


def plot_monthly_returns(trades):
    trades['Month'] = trades['EndDate'].dt.to_period('M')
    monthly_returns = trades.groupby('Month')['PnL%'].sum()
    monthly_returns.plot(kind='bar', figsize=(14, 7))
    plt.title('Monthly Returns')
    plt.xlabel('Month')
    plt.ylabel('Total Return %')
    plt.show()


def plot_annual_returns(trades):
    trades['Year'] = trades['EndDate'].dt.to_period('Y')
    annual_returns = trades.groupby('Year')['PnL%'].sum()
    annual_returns.plot(kind='bar', figsize=(14, 7))
    plt.title('Annual Returns')
    plt.xlabel('Year')



def plot_distribution_of_monthly_returns(trades):
    trades['Month'] = trades['EndDate'].dt.to_period('M')
    monthly_returns = trades.groupby('Month')['PnL%'].sum()
    monthly_returns.hist(bins=50, alpha=0.6, color='green')
    plt.title('Distribution of Monthly Returns')
    plt.xlabel('Monthly Return %')
    plt.ylabel('Frequency')
    plt.show()



def plot_return_quantiles(trades):
    quantiles = trades['PnL%'].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
    quantiles.plot(kind='bar')
    plt.title('Return Quantiles')
    plt.xlabel('Quantile')
    plt.ylabel('PnL %')
    plt.show()



def plot_transaction_time_distribution(trades):
    trades['Time'] = trades['StartDate'].dt.hour + trades['StartDate'].dt.minute / 60
    trades['Time'].hist(bins=24, alpha=0.6, color='purple')
    plt.title('Transaction Time Distribution')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Frequency')
    plt.show()


trades_df = extract_trades('test1', 'EndDate')

print(max(trades_df['PnL%']))

plot_log_return_histogram(trades_df)