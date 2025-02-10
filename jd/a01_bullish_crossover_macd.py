import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate MACD
def calculate_macd(data, short_window=12, long_window=26, signal_window=9):
    data['MACD'] = data['Close'].ewm(span=short_window, adjust=False).mean() - data['Close'].ewm(span=long_window, adjust=False).mean()
    data['Signal'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    return data

# Function to identify bullish crossovers
def identify_bullish_crossovers(data):
    data['Crossover'] = (data['MACD'] > data['Signal']) & (data['MACD'].shift(1) <= data['Signal'].shift(1))
    return data

# Download stock data for the last month
ticker = 'AAPL'  # Change to your desired stock ticker
data = yf.download(ticker, period='6mo', interval='1d')

# Calculate MACD and Signal Line
data = calculate_macd(data)

# Identify Bullish Crossovers
data = identify_bullish_crossovers(data)

# Filter for the last 7 days
last_7_days = data.tail(150)

# Plot MACD and Bullish Crossovers
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['MACD'], label='MACD', color='blue')
plt.plot(data.index, data['Signal'], label='Signal Line', color='red')
# plt.scatter(last_7_days.index, last_7_days['MACD'][last_7_days['Crossover']], color='green', label='Bullish Crossover', marker='o', s=100)
plt.scatter(last_7_days['MACD'][last_7_days['Crossover']].index, last_7_days['MACD'][last_7_days['Crossover']], color='green', label='Bullish Crossover', marker='o', s=100)

plt.legend(loc='upper left')
plt.title(f'{ticker} MACD Bullish Crossovers - Last 6 Months - Daywise')
plt.show()

# Display the results
print("Bullish Crossovers in the last 7 days:")
print(last_7_days[last_7_days['Crossover']])
