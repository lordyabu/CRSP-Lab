# Project Structure
Check /notes for high level documentation notes
## Key Files
- Data Examination and Main Execution
  - [main.py](/src/main.py) - Runs the data preprocessing / trades - (Set flags for each operation)
  - [examine_data.py](/src/examine_data.py) - Aggregates the Trade Analysis section below

- Matlab and Major operations
  - [getindividualstocks.m](/src/matlabExtraction/getindivudalstocks.m) - Converts Rosettaupdated to individual csvs
  - [majorOperations.py](/src/helperFunctions/dataPreprocessing/majorOperations.py) - Applies major operations to dataset

- OHLC Calculations
  - [getOHLCfrom5minRet.py](/src/helperFunctions/dataPreprocessing/getOHLCfrom5MinRet.py) - Calculates OHLC from 5min return data


- Timespan
  - [findTimespanStocks.py](/src/helperFunctions/dataPreprocessing/findTimespanStocks.py) - Gets valid stocks for specified timespan


- Bollinger Bands Analysis
  - [bollingerNaive.py](/src/bollingerBands/bollingerNaive.py) - Trader class for bollinger
  - [calculateBands.py](/src/bollingerBands/calculateBands.py) - Calculates / Saves bands for bollinger

- Turtle Trading Strategy
  - [turtleNaive.py](/src/turtles/turtleNaive.py) - Trader class for turtles
  - [calculateWindows.py](/src/turtles/calculateWindows.py) - Calculates / Saves windows for turtle

- Trade Analysis
  - [getStats.py](/src/tradeAnalysis/getStats.py) - Get basic trade stats
  - [getGraphs.py](/src/tradeAnalysis/getGraphs.py) - Get basic trade graphs
  - [graphBollingerTrades.py](/src/bollingerBands/analysis/graphBollingerTrades.py) - Get detailed graph with bollinger trade points
  - [graphTurtleTrades.py](/src/turtles/analysis/graphTurtleTrades.py) - Get detailed graph with turtle trade points

    