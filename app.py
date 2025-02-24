import os, csv
import talib
import yfinance as yf
import pandas
from flask import Flask, request, render_template
from patterns_jd import candlestick_patterns
import config as c
import cs_utils as csu
from jd.us01_bullish_crossover_macd import get_charts


app = Flask(__name__)

@app.route('/snapshot')
def snapshot():
    try:
        csu.snapshot()
        return render_template('success.html', message=request)
    except Exception as e:
        return render_template('failure.html', message=e.args[1])

@app.route('/csp')
def csp(): #cs patterns
    # pattern  = request.args.get('pattern', False)
    pattern = 'CDL3INSIDE' # Three Inside Up/Down
    stocks = {}

    with open(fr'{c.DATA_DIR}\symbols.csv') as f:
        for row in csv.reader(f):
            stocks[row[0]] = {'company': row[1]}

    if pattern:
        for filename in os.listdir(fr'{c.DATA_DIR}\daily'):
            print(f'filename : {filename}')
            df = pandas.read_csv(fr'{c.DATA_DIR}\daily\{filename}')
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

@app.route('/us01')
def us01(): # us01 : last one week bullish crossover in day chart

    print('app.us01.step01')
    # candlestick_patterns = us01_main(request.args.get('ticker', False))

    symb_chrt_dict = get_charts()

    pass
    return render_template('us01.html', symb_chrt_dict=symb_chrt_dict)

    #
    #
    #
    # pattern = 'CDL3INSIDE'  # Three Inside Up/Down
    # stocks = {}
    #
    # with open(fr'{c.DATA_DIR}\symbols.csv') as f:
    #     for row in csv.reader(f):
    #         # stocks[row[0]] = {'company': row[1]}
    #         stocks[row[0]] = row[1]
    #
    # if False: #pattern:
    #     for filename in os.listdir(fr'{c.DATA_DIR}\daily'):
    #         print(f'filename : {filename}')
    #         df = pandas.read_csv(fr'{c.DATA_DIR}\daily\{filename}')
    #         pattern_function = getattr(talib, pattern)
    #         symbol = filename.split('.')[0]
    #
    #         try:
    #             results = pattern_function(df['Open'], df['High'], df['Low'], df['Close'])
    #             last = results.tail(1).values[0]
    #
    #             if last > 0:
    #                 stocks[symbol][pattern] = 'bullish'
    #             elif last < 0:
    #                 stocks[symbol][pattern] = 'bearish'
    #             else:
    #                 stocks[symbol][pattern] = None
    #         except Exception:
    #             print('failed on filename: ', filename)
    #
    # return render_template('us01.html', candlestick_patterns=candlestick_patterns, stocks=stocks, pattern=pattern)



if __name__ == '__main__':
    app.run(debug=True)
    # index()