# Bollinger Naive Algorithm Documentation

This documentation provides an overview of the `BollingerNaive` class and the associated `BollingerBands` class used for implementing a simple trading algorithm based on Bollinger Bands.

![Screenshot (59)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/ff30db69-fe24-4ef5-bfdb-f6987384d991)
![Screenshot (60)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/7a509e6b-034f-4c43-b144-a78ab60c796b)



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

Bands are calculated as follows (Bperiods = 19 -> N = 20)
- Middle Band (MB): `MB = (Sum of Close Prices over last N periods) / N`
- Standard Deviation (SD): `SD = sqrt( (Sum of (Close - MB)^2 over last N periods) / N )`
- Upper Band (UB): `UB = MB + (1.96 * SD)`
- Lower Band (LB): `LB = MB - (1.96 * SD)`
- Upper Band 3 Standard Deviations (UB3SD): `UB3SD = MB + (2.96 * SD)`
- Lower Band 3 Standard Deviations (LB3SD): `LB3SD = MB - (2.96 * SD)`


## Trade Analysis Results Summary(Dynamic SL)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `125,554`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `62.65%`

**Performance Indicators**
- **Average Trade Return**: `0.624%`
- **Average Win on Trades**: `5.14%`
- **Average Loss on Trades**: `-7.00%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `18 days, 22 hours, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `78417.35%`



### Initialization

```python
bollinger_trader = BollingerNaive(self, stock_name, band_data_name='Default', identifier=-1, time_period='Daily', reset_indexes=False, step=0, moving_stop_loss=True)
```



# Bollinger Bands Calculation

## Overview
This script defines a class `BollingerBands` for calculating and visualizing Bollinger Bands for stock trading data. Bollinger Bands are a volatility indicator that consists of a Simple Moving Average (SMA) and two standard deviation lines, one above and one below the SMA. This script provides functionality for individual stock analysis as well as batch processing of multiple stocks.

You can customize the timeframe / Bperiods

## Class `BollingerBands`

### Initialization / Running

```python
bollinger = BollingerBands(data_directory, Bperiods=19, name='Default')
bollinger.calculate_all_bands()
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
    
