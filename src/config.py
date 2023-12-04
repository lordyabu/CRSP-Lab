"""
Folder names/locations on your device. Change the names at your convenience.
You must create the folders.
"""

import os

DATA_DIR = os.path.expanduser("~/Documents/CrspData") # Base directory for data
RAW_PRICE_DATA_DIR = os.path.join(DATA_DIR, 'priceDataRAW') # Raw Price Data
PRICE_DATA_DIR = os.path.join(DATA_DIR, 'priceDataMO') # Price data post Major Operations
OHLC_DATA_DIR =  os.path.join(DATA_DIR, 'priceDataOHLC') # Price data post OHLC calculations
FIVE_MIN_DIR = os.path.join(DATA_DIR, 'dataFiveMin', '.csv') # 5 min return data

BOLLINGER_DATA_NAME = 'bollingerData'
BOLLINGER_DATA_DIR = os.path.join(DATA_DIR, BOLLINGER_DATA_NAME)

TURTLE_DATA_NAME = 'turtleData'
TURTLE_DATA_DIR = os.path.join(DATA_DIR, TURTLE_DATA_NAME)

BOX_DATA_NAME = 'boxData'
BOX_DATA_DIR = os.path.join(DATA_DIR, BOX_DATA_NAME)

DEEP_DATA_NAME = 'deepData'
DEEP_DATA_PATH = os.path.join(DATA_DIR, DEEP_DATA_NAME)

TRANSACTION_COST_PCT = .2
TRANSACTION_COST_DOLLAR = 5