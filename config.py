import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

global APP_VARIABLES
APP_VARIABLES = ['BASE_DIR', 'DATA_DIR','API_KEY_CS']

load_dotenv(find_dotenv(usecwd=True))

globals()['BASE_DIR'] = os.getenv('BASE_DIR')

for key, value in os.environ.items():
    if key in APP_VARIABLES : globals()[key] = value
