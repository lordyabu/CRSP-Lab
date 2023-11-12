from dataclasses import dataclass

import pandas as pd
import numpy as np
import time
# Load your data
df = pd.read_csv("C:/Users/theal/Documents/CrspData/priceDataOHLCSplitTest/AAPL.csv")


df['Rolling_Max_10'] = df['High'].shift(1).rolling(window=10).max()
df['Rolling_Min_10'] = df['Low'].shift(1).rolling(window=10).min()
df['Rolling_Max_20'] = df['High'].shift(1).rolling(window=20).max()
df['Rolling_Min_20'] = df['Low'].shift(1).rolling(window=20).min()
df['Rolling_Max_55'] = df['High'].shift(1).rolling(window=55).max()
df['Rolling_Min_55'] = df['Low'].shift(1).rolling(window=55).min()



df.to_csv('AAPLTurtle.csv')

