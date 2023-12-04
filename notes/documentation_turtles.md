# Turtle Trading Algorithm Documentation
This documentation provides an overview of the Turtle class and the associated Box class used for implementing the Turtle Trading algorithm, a famous method in financial markets trading.

![Screenshot (62)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/70e99f04-5584-4034-8c8b-28730d00c149)


Turtle Trading Algorithm Documentation
This documentation provides an overview of the Turtle class and the associated Box class used for implementing the Turtle Trading algorithm, a famous method in financial markets trading.

## Modules and Dependencies
- `pandas`: For data manipulation and analysis.
- `os`: To interact with the operating system, mainly for file and directory operations.
- `json`: To work with JSON data.
- `numpy`: For numerical operations.
- `math`: Provides access to mathematical functions.
- `matplotlib`: For plotting graphs and charts.
- `concurrent.futures`: For parallel execution of tasks.
- `tqdm`: For displaying progress bars.
- `config`: Contains configuration variables like `DATA_DIR`.

## Class: Turtle

The `TurtleNaive` class inherits from `StockAlgorithmDaily` and implements a naive trading strategy based on the turtles.

Key aspects of the strategy include:

Entry based on 20-day highs or lows.
Exit on 10-day highs or lows, opposite to the entry condition.


## Trade Analysis Results Summary(Enter/Exit on Open; Not factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `424,456`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `34.92%`

**Performance Indicators**
- **Average Trade Return**: `0.21%`
- **Average Win on Trades**: `11.5%`
- **Average Loss on Trades**: `-5.86%`
- **Maximum Trade Duration**: `362 days`
- **Average Trade Duration**: `33 days, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `91839.57%`


## Trade Analysis Results Summary(Enter/Exit on Open; Factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `424,456`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `34.92%`

**Performance Indicators**
- **Average Trade Return**: `-.03%`
- **Average Win on Trades**: `10.79%`
- **Average Loss on Trades**: `-6.24%`
- **Maximum Trade Duration**: `362 days`
- **Average Trade Duration**: `33 days, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `-13,469.67%`


## Trade Analysis Results Summary(Enter/Exit on Close; Not factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `424,456`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `34.56%`

**Performance Indicators**
- **Average Trade Return**: `0.21%`
- **Average Win on Trades**: `11.7%`
- **Average Loss on Trades**: `-5.87%`
- **Maximum Trade Duration**: `362 days`
- **Average Trade Duration**: `33 days, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `90246.35%`



### Initialization / Running
```python
turtle_trader = TurtleNaive(self, stock_name, rolling_window_name='Default', identifier=-1, time_period='Daily', reset_indexes=False, step=0)
```

# Turtles Window Calculation

## Overview
This script defines a class `TurtleWindows` for calculating and visualizing Turtle windows for stock trading data.

You can customize the timeframe / Bperiods

## Class `TurtleWindows`

### Initialization / Running

```python
turtle_windows = TurtleWindows(data_directory)
turtle_windows.calculate_all_windows()
```
Notes.
- OHLC is calculated from 5min return data

Values Tested for:
- IDENTIFER: PASS
- STRATEGY: PASS
- TIME_PERIOD: PASS
- STOCK_NAME: PASS
- ENTER_PRICE: PASS
- EXIT_PRICE: PASS
- PNL: PASS
- START_DATE: PASS
- END_DATE: PASS
- TRADE_TYPE: PASS
- LEVERAGE: PASS
- START_TIME: NA
- END_TIME: NA
