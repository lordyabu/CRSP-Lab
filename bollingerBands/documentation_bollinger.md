# Bollinger Naive Algorithm Documentation

This documentation provides an overview of the `BollingerNaive` class and the associated `BollingerBands` class used for implementing a simple trading algorithm based on Bollinger Bands.




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

## Class: BollingerNaive

The `BollingerNaive` class inherits from `StockAlgorithmDaily` and implements a naive trading strategy based on Bollinger Bands.

The Naive strategy enters on band highs/lows and exits on middle band / stop loss triggered at 3SD

### Initialization

```python
bollinger_trader = BollingerNaive(self, stock_name, band_data_name='Default', identifier=-1, time_period='Daily', reset_indexes=False, step=0)
```



# Bollinger Bands Calculation and Visualization

## Overview
This script defines a class `BollingerBands` for calculating and visualizing Bollinger Bands for stock trading data. Bollinger Bands are a volatility indicator that consists of a Simple Moving Average (SMA) and two standard deviation lines, one above and one below the SMA. This script provides functionality for individual stock analysis as well as batch processing of multiple stocks.

You can customize the timeframe / Bperiods

## Class `BollingerBands`

### Initialization

```python
bollinger = BollingerBands(data_directory, Bperiods=19, name='Default')
```


Notes. 
- All values are currently being calculated using Return data instead of RAW price data
- OHLC is calculated from 5min return data
- PnL is calculated off of Return instead of OHLC Close (Which should give more accurate return data)

Values Tested for:
- IDENTIFER: PASS
- STRATEGY: PASS
- TIME_PERIOD: PASS
- STOCK_NAME: PASS
- ENTER_PRICE: PASSING FOR RETURN
- EXIT_PRICE: PASSING FOR RETURN
- PNL: PASSING FOR RETURN
- START_DATE: PASS
- END_DATE: PASS
- TRADE_TYPE: PASS
- LEVERAGE: PASS
- START_TIME: NA
- END_TIME: NA
    
