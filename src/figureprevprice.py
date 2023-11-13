from config import DATA_DIR
import os
import pandas as pd


path = os.path.join(DATA_DIR, 'tradeData', 'allTrades_20100104_to_20201231test.csv')


df = pd.read_csv(path)


for v in df.iloc[100]:
    print(v)