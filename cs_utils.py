import yfinance as yf
# from tradingview_scraper import TradingViewScraper
import config as c

# start_date = '2024-07-01'
# end_date = '2024-12-31'
period='3mo'
interval='1d'

def snapshot():
    # tv_scraper = TradingViewScraper()

    with open(fr'{c.DATA_DIR}\symbols.csv') as f:
        for line in f:
            if "," not in line:
                continue
            symbol = line.split(",")[0]
            print(f'Creating snapshot for {symbol}')
            # data = yf.download(symbol, start=start_date, end=end_date)
            # data.to_csv(f'datasets/daily/{symbol}_dt.csv')
            data = yf.download(symbol, period=period, interval=interval,multi_level_index=False)
            #data.to_csv(f'datasets/daily/{symbol}_yf.csv')
            # data = tv_scraper.fetch_ohlcv(symbol, period='1d', limit=100)
            # data.to_csv(f'datasets/daily/{symbol}_tv.csv')

    return {
        "code": "success"
    }