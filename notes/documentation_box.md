# Box Naive Algorithm Documentation

This documentation provides an overview of the `BollingerNaive` class and the associated `BollingerBands` class used for implementing a simple trading algorithm based on Bollinger Bands.

![Screenshot (65)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/86daad28-b119-4836-ae67-e7e002cabc89)

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

## Class: DarvasTrader

The `DarvasTrader` class inherits from `StockAlgorithmDaily` and implements a naive trading strategy based on Bollinger Bands.

The Naive strategy enters on upper box breaks and exits on lower box breaks
The strategy only goes long

Boxes are calculated as follows
- Find a new 12-month high.
- Find the top of the box, which is the highest high for the next three days (4 days total).
- After finding the top, look for the bottom of the box. It's the lowest low for the next three days (4 days total).
- Once the box is complete, a close above the top of the box signals a buy.
- A close below the bottom of the box is the sell signal. Exit and then go back to step 1.


## Trade Analysis Results Summary(Enter/Exit at open; Not factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `22,129`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `40.25%`

**Performance Indicators**
- **Average Trade Return**: `.25%`
- **Average Win on Trades**: `8.83%`
- **Average Loss on Trades**: `-5.54%`
- **Maximum Trade Duration**: `1113 days`
- **Average Trade Duration**: `46 days, 20 hours, 33 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `5590.63%`


## Trade Analysis Results Summary(Enter/Exit at open; Factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `22,129`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `40.25%`

**Performance Indicators**
- **Average Trade Return**: `-.04%`
- **Average Win on Trades**: `8.09%`
- **Average Loss on Trades**: `-6.04%`
- **Maximum Trade Duration**: `1113 days`
- **Average Trade Duration**: `46 days, 20 hours, 33 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `-989.55%`



### Initialization

```python
box_trader = DarvasTrader(self, stock_name, time_period='Daily', identifier=-1, time_period='Daily', reset_indexes=False, step=0)
```



# Box Calculation

## Overview
This script defines a class `DarvasBoxCalculator` for calculating and visualizing Darvas Boxes for stock trading data. Darvas boxes are used in momentum based strategy on stocks with sharp increases in volume.
It makes the most money off of parabolic price movement which is typically upwards. Using volume helps identify these trends quicker, but the dataset does not have this functionality so it just runs on all stocks.

You can customize the timeframe / Bperiods

## Class `DarvasBoxCalculator`

### Initialization / Running

```python
calculator = DarvasBoxCalculator(data_directory, name='Default')
calculator.calculate_all_stock_boxes()
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
    




































Start: 2010-01-05 00:00:00
End: 2020-12-31 00:00:00
Duration: 4013 days 00:00:00
# Trades: 22129
# Different Stocks: 1117
Win Rate [%]: 39.9566180125627
Avg. Trade [%]: 0.2449405757151263
Median Trade [%]: -1.61
Avg. Win [%]: 8.858820402623856
Median Win [%]: 5.32
Avg. Loss [%]: -5.501350637591507
Median Loss [%]: -4.26
Total Return [%] (Where every trade is weighted equally): 5420.290000000001
Minimum Exit Price: 0.89, Index: 23944
Minimum Enter Price: 0.96, Index: 23944
Minimum PnL%: -83.31, Index: 10193
Maximum PnL%: 190.99, Index: 21460

Process finished with exit code 0
