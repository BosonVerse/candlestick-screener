import os, csv
import talib
import yfinance as yf
import pandas
from flask import Flask, request, render_template
from patterns import candlestick_patterns


dataset_symbols = r'datasets/symbolsNSE.csv'
dataset_daily = r'datasets/dailyNSE'

app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    with open(dataset_symbols) as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            data = yf.download(symbol, start="2020-01-01", end="2020-08-01")
            # data.to_csv(f'{dataset_daily}/{symbol}.csv'.format(dataset_daily, symbol))
            data.to_csv(f'{dataset_daily}/{symbol}.csv')

    return {
        "code": "success"
    }

@app.route('/')
def index():
    # pattern  = request.args.get('pattern', False)
    pattern = 'CDL3INSIDE' # Three Inside Up/Down
    stocks = {}

    with open(dataset_symbols) as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        for filename in os.listdir(f'{dataset_daily}'):
            print(f'filename : {filename}')
            # df = pandas.read_csv(f'{dataset_daily}/{filename}'.format(filename))
            df = pandas.read_csv(f'{dataset_daily}/{filename}')
            pattern_function = getattr(talib, pattern)
            symbol = filename.split('.')[0]

            try:
                results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
                last = results.tail(1).values[0]

                if last > 0:
                    stocks[symbol][pattern] = 'bullish'
                elif last < 0:
                    stocks[symbol][pattern] = 'bearish'
                else:
                    stocks[symbol][pattern] = None
            except Exception:
                print('failed on filename: ', filename)

    return render_template('index.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)

@app.route('/')
def health():
    return render_template('health.html', message=request)

if __name__ == '__main__':
    app.run(debug=True)
    # index()