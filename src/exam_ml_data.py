# This script is designed to analyze and visualize trading strategies, focusing on the ML trades
# See examine_data for a more complete description as this is essentially a replica.

from src.tradeAnalysis.getStats import get_trade_stats, plot_wins_and_losses
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades, extract_trades_auxillary, extract_ml_trades
from src.tradeAnalysis.getGraphs import plot_everything

import warnings
warnings.filterwarnings('ignore')

# Strategies: bollinger_naive_dynamic_sl, turtle_naive, box_naive
trades_df = extract_ml_trades(sort_by='EndDate', identifier='Naive Bayes_34_33_33_test1mlbollinger22', trade_type='long')



start_date = '20100104'
end_date = '20201231'

# Analysis and Visualization Section
# -----------------------------------

# Plot various graphs for the trading strategy
# Uncomment the line below to execute
plot_everything(trades_df, start_date, end_date)

# Get and print trade statistics
# Uncomment the line below to execute
get_trade_stats(trades_df, start_date, end_date, selection_type='EndDate')

# Plot wins and losses
# Uncomment the line below to execute
# plot_everything(trades_df, start_date, end_date)

# Bollinger Bands Analysis
# ------------------------

start_date_window_boll = '2010-10-11'
end_date_window_boll = '2011-12-31'
# Visualize Bollinger Bands trades for a specific window
# Uncomment the line below to execute
# graph_window_bollinger(start_date_window_boll, end_date_window_boll, 'AAPL', 'bollinger_naive_dynamic_sl')

# Turtle Trading Strategy Analysis
# ---------------------------------

start_date_window_turtle = '2018-10-11'
end_date_window_turtle = '2020-12-31'
# Visualize Turtle trades for a specific window
# Uncomment the line below to execute
# graph_window_turtle(start_date_window_turtle, end_date_window_turtle, 'AAPL', 'turtle_naive')
# ---------------------------------