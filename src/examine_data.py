from src.tradeAnalysis.getGraphs import plot_everything
from src.tradeAnalysis.getStats import get_trade_stats, plot_wins_and_losses
from src.helperFunctions.dataAnalysis.extractTrades import extract_trades
from src.turtles.analysis.graphTurtleTrades import graph_window_turtle
from src.bollingerBands.analysis.graphBollingerTrades import graph_window_bollinger

import warnings
warnings.filterwarnings('ignore')

# Strategies: bollinger_naive_dynamic_sl, turtle_naive

trades_df = extract_trades(strategy='turtle_naive', trade_type='short', sort_by='EndDate')

start_date = '2015-01-04'
end_date = '2020-12-31'

# plot_everything(trades_df, start_date, end_date)


# get_trade_stats(trades_df, start_date, end_date)


# plot_wins_and_losses(trades_df, start_date, end_date)

start_date_window = '2010-10-11'
end_date_window = '2011-12-31'
graph_window_bollinger(start_date_window, end_date_window, 'AAPL', 'bollinger_naive_dynamic_sl')

start_date_window = '2018-10-11'
end_date_window = '2020-12-31'
# graph_window_turtle(start_date_window, end_date_window, 'AAPL', 'turtle_naive')