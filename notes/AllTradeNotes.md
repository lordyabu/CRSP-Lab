# Algorithm Notes

## Bollinger Naive 1
![Screenshot (59)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/ff30db69-fe24-4ef5-bfdb-f6987384d991)
![Screenshot (60)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/7a509e6b-034f-4c43-b144-a78ab60c796b)

The Naive strategy enters on band highs/lows and exits on middle band / stop loss triggered at 3SD
Bollinger 1 is only able to trade 1 unit at a time

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
- **Total Number of Trades**: `125,554`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `62.21%`

**Performance Indicators**
- **Average Trade Return**: `0.595%`
- **Average Win on Trades**: `5.09%`
- **Average Loss on Trades**: `-6.86%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `18 days, 22 hours, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `74743.49%`


## Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `125,554`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `62.21%`

**Performance Indicators**
- **Average Trade Return**: `0.20%`
- **Average Win on Trades**: `4.45%`
- **Average Loss on Trades**: `-7.93%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `18 days, 22 hours, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `24,521.90%`


## LONG Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Not factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `58,449`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `65.79%`

**Performance Indicators**
- **Average Trade Return**: `0.86%`
- **Average Win on Trades**: `5.14%`
- **Average Loss on Trades**: `-7.43%`
- **Maximum Trade Duration**: `127 days`
- **Average Trade Duration**: `17 days, 11 hours, 12 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `50,401.13%`


## LONG Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `58,449`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `65.79%`

**Performance Indicators**
- **Average Trade Return**: `0.46%`
- **Average Win on Trades**: `4.52%`
- **Average Loss on Trades**: `-8.60%`
- **Maximum Trade Duration**: `127 days`
- **Average Trade Duration**: `17 days, 11 hours, 12 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `27,021.53%`



## SHORT Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Not factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `67,105`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `59.01%`

**Performance Indicators**
- **Average Trade Return**: `0.36%`
- **Average Win on Trades**: `5.05%`
- **Average Loss on Trades**: `-6.46%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `20 days, 6 hours, 2 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `24,343.37%`


## SHORT Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Trades**: `67,105`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `59.01%`

**Performance Indicators**
- **Average Trade Return**: `-0.04%`
- **Average Win on Trades**: `4.34%`
- **Average Loss on Trades**: `-7.44%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `20 days, 6 hours, 2 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `-2,499.63%`


![Screenshot (78)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/e36f0c5b-afe8-4de3-8c1a-c2b383d5196c)



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



## LONG Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Not factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded**: `156,708`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `65.70%`

**Performance Indicators**
- **Average Trade Return**: `0.99%`
- **Average Win on Trades**: `5.74%`
- **Average Loss on Trades**: `-8.21%`
- **Maximum Trade Duration**: `128 days`
- **Average Trade Duration**: `9 days, 0 hours, 17 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `155,170.38%`



## LONG Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded**: `156,708`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `65.70%`

**Performance Indicators**
- **Average Trade Return**: `0.71%`
- **Average Win on Trades**: `5.34%`
- **Average Loss on Trades**: `-9.02%`
- **Maximum Trade Duration**: `128 days`
- **Average Trade Duration**: `9 days, 0 hours, 17 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `111,928.22%`




## SHORT Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Not factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded**: `193,838`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `60.07%`

**Performance Indicators**
- **Average Trade Return**: `0.48%`
- **Average Win on Trades**: `5.04%`
- **Average Loss on Trades**: `-6.42%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `21 days, 14 hours, 1 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `93,346.58%`



## SHORT Trade Analysis Results Summary(Dynamic SL; Enter/Exit at open; Factoring in trade costs) 


**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded**: `193,838`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `60.07%`

**Performance Indicators**
- **Average Trade Return**: `0.1`%`
- **Average Win on Trades**: `4.59%`
- **Average Loss on Trades**: `-7.10%`
- **Maximum Trade Duration**: `170 days`
- **Average Trade Duration**: `21 days, 14 hours, 1 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `40,957.47%`



![Screenshot (62)](https://github.com/lordyabu/CRSP-Lab/assets/92772420/70e99f04-5584-4034-8c8b-28730d00c149)


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



## LONG Trade Analysis Results Summary(Enter/Exit on Close; Not factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `252,693`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `38.28%`

**Performance Indicators**
- **Average Trade Return**: `0.45%`
- **Average Win on Trades**: `9.71%`
- **Average Loss on Trades**: `-5.32%`
- **Maximum Trade Duration**: `362 days`
- **Average Trade Duration**: `35 days, 13 hours, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `113513.61%`



## LONG Trade Analysis Results Summary(Enter/Exit on Open; Factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `252,693`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `38.28%`

**Performance Indicators**
- **Average Trade Return**: `.21%`
- **Average Win on Trades**: `9.08%`
- **Average Loss on Trades**: `-5.71%`
- **Maximum Trade Duration**: `362 days`
- **Average Trade Duration**: `33 days, 55 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `52,194.07%`



## SHORT Trade Analysis Results Summary(Enter/Exit on Close; Not factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `171,763`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `29.97%`

**Performance Indicators**
- **Average Trade Return**: `-.13%`
- **Average Win on Trades**: `14.88%`
- **Average Loss on Trades**: `-6.57%`
- **Maximum Trade Duration**: `323 days`
- **Average Trade Duration**: `29 days, 7 hours, 11 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `-21,674.03%`



## SHORT Trade Analysis Results Summary(Enter/Exit on Open; Factoring in trade costs)

**Analysis Period**
- **Start Date**: `2010-01-04`
- **End Date**: `2020-12-31`
- **Total Duration**: `4014 days`

**Trading Metrics**
- **Total Number of Units Traded(not the same as number of trades)**: `171,763`
- **Number of Different Stocks Traded**: `1120`
- **Win Rate**: `29.97%`

**Performance Indicators**
- **Average Trade Return**: `-.38%`
- **Average Win on Trades**: `14.02%`
- **Average Loss on Trades**: `-6.94%`
- **Maximum Trade Duration**: `323 days`
- **Average Trade Duration**: `29 days, 7 hours, 11 minutes`

**Overall Returns**
- **Total Return (Weighted Equally per Trade)**: `-65,663.74%`