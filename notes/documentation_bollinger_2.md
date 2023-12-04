# Bollinger Naive Algorithm Documentation

This documentation provides an overview of the `BollingerNaiveTwo` class and the associated `BollingerBands` class used for implementing a simple trading algorithm based on Bollinger Bands.

![Screenshot (78)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/e36f0c5b-afe8-4de3-8c1a-c2b383d5196c)



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

The `BollingerNaiveTwo` class inherits from `StockAlgorithmDaily` and implements a naive trading strategy based on Bollinger Bands.

The Naive strategy enters on band highs/lows and exits on middle band / stop loss triggered at 3SD.

The difference between this and the other is that it is capable of trading multiple units at a time

Bands are calculated as follows (Bperiods = 19 -> N = 20)
- Middle Band (MB): `MB = (Sum of Close Prices over last N periods) / N`
- Standard Deviation (SD): `SD = sqrt( (Sum of (Close - MB)^2 over last N periods) / N )`
- Upper Band (UB): `UB = MB + (1.96 * SD)`
- Lower Band (LB): `LB = MB - (1.96 * SD)`
- Upper Band 3 Standard Deviations (UB3SD): `UB3SD = MB + (2.96 * SD)`
- Lower Band 3 Standard Deviations (LB3SD): `LB3SD = MB - (2.96 * SD)`


## Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Not factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded**: `350,546`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `62.59%`

**Performance Indicators**
- **Average Trade Return**: `0.71%`
- **Average Win on Trades**: `5.37%`
- **Average Loss on Trades**: `-7.15%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `20 days, 10 hours, 25 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `248,516.96%`



## Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded**: `350,546`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `62.59%`

**Performance Indicators**
- **Average Trade Return**: `0.44%`
- **Average Win on Trades**: `4.94%`
- **Average Loss on Trades**: `-7.88%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `20 days, 10 hours, 25 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `152,885.69%`

## Trade Analysis Results Summary(Dynamic SL; Enter/Exit at close; Not factoring in trade costs) 



### Initialization

```python
bollinger_trader = BollingerNaiveTwo(self, stock_name, band_data_name='Default', identifier=-1, time_period='Daily', reset_indexes=False, step=0, moving_stop_loss=True)
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
    
