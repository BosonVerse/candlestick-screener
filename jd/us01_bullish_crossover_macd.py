import os
import pandas as pd
import config as c
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from cs.util_html import us01_get_tr

# Function to calculate MACD

# Title         : MACD Bullish Crossover Search
# Objective     : Identify stocks that made bullish crossover in last one week in a day chart.


# tradingview       : short_window=8, long_window=16, signal_window=11
# copilot/bloomberg : short_window=12, long_window=26, signal_window=9
# def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
#     data['MACD'] = data['Close'].ewm(span=short_window, adjust=False).mean() - data['Close'].ewm(span=long_window, adjust=False).mean()
#     data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
#     return data

# Function to identify bullish crossovers
# def identify_bullish_crossovers(data):
#     data['MACD_S1'] = data['MACD'].shift(1)
#     data['Signal_S1'] = data['Signal'].shift(1)
#     data['CrossoverBL'] = (data['MACD'] > data['Signal']) & (data['MACD'].shift(1) <= data['Signal'].shift(1))
#     # data['CrossoverBR'] = not ((data['MACD'] > data['Signal']) & (data['MACD'].shift(1) <= data['Signal'].shift(1)))
#     return data


def get_charts():

    df_combined = pd.DataFrame()

    for filename in os.listdir(fr'{c.DATA_DIR}\daily'):

        # candlestick_patterns[filename] = (os.path.splitext(filename)[0]).split('_')[0]
        print(f'Reading filename : {filename}')
        data = pd.read_csv(fr'{c.DATA_DIR}\daily\{filename}')

        data['ticker'] = (os.path.splitext(filename)[0]).split('_')[0]

        # Calculate MACD
        short_window, long_window, signal_window = 12, 26, 9
        data['MACD'] = (data['Close'].ewm(span=short_window, adjust=False).mean() -
                        data['Close'].ewm(span=long_window, adjust=False).mean())
        data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()

        # Identify Bullish Crossovers
        data['CrossoverBL'] = (data['MACD'] > data['Signal']) & (data['MACD'].shift(1) <= data['Signal'].shift(1))

        # Append all the tickers
        df_combined = pd.concat([df_combined, data], axis=0, ignore_index=True)

    symb_chrt_dict = us01_get_tr(df_combined, dt_start='2024-09-30', dt_end='2025-02-07')
    # symb_chrt_dict = {'symbol1': 'chart1', 'symbol2': 'char2'}
    return symb_chrt_dict




# def us01_main_x():
#
#     print('us01_bullish_crossover_macd.us01_main.step01')
#     # Download stock data for the last month
#     # ticker = 'AAPL'  # Change to your desired stock ticker
#     # data_yf = yf.download(ticker, period='6mo', interval='1d', multi_level_index=False)
#     # data = calculate_macd(data_yf)
#
#     df_combined = pd.DataFrame()
#
#     candlestick_patterns = {}
#     #
#     # for filename in os.listdir(fr'{c.DATA_DIR}\daily'):
#     #     candlestick_patterns[filename] = (os.path.splitext(filename)[0]).split('_')[0]
#     #     pass
#     # return candlestick_patterns
#
#     for filename in os.listdir(fr'{c.DATA_DIR}\daily'):
#
#         candlestick_patterns[filename] = (os.path.splitext(filename)[0]).split('_')[0]
#         print(f'filename : {filename}')
#         data = pd.read_csv(fr'{c.DATA_DIR}\daily\{filename}')
#
#         data['ticker'] = (os.path.splitext(filename)[0]).split('_')[0]
#
#         # Calculate MACD
#         short_window, long_window, signal_window = 12, 26, 9
#         data['MACD'] = (data['Close'].ewm(span=short_window, adjust=False).mean() -
#                         data['Close'].ewm(span=long_window, adjust=False).mean())
#         data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
#
#         # Identify Bullish Crossovers
#         data['Crossover'] = (data['MACD'] > data['Signal']) & (data['MACD'].shift(1) <= data['Signal'].shift(1))
#
#         # Append all the tickers
#         df_combined = pd.concat([df_combined, data], axis=0, ignore_index=True)
#
#     create_html_output(df_combined)
#
#
#     return candlestick_patterns