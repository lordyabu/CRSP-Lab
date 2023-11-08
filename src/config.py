import os

# Assuming your Documents folder is in the standard location for your OS
# For Windows
DATA_DIR = os.path.expanduser("~/Documents/dataEnsembleLegends")

# For MacOS and Linux
# DATA_DIR = os.path.expanduser("~/Documents/dataEnsembleLegends")

# You can then use this in your scripts like so:
# file_path = os.path.join(DATA_DIR, 'your_data_file.csv')
