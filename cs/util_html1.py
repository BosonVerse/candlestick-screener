import os

import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
from datetime import datetime, timedelta

import config as c

def create_html_output(df_macd, ticker=None, dt_start=None, dt_end=None):

    dt_start = datetime.strptime(dt_start, "%Y-%m-%d").date()
    dt_end = datetime.strptime(dt_end, "%Y-%m-%d").date()
    df_macd['Date'] = pd.to_datetime(df_macd['Date']).dt.date

    symbols_df = pd.read_csv(fr'{c.DATA_DIR}\symbols.csv', names=['ticker', 'stock_name'])
    if ticker is not None: symbols_df = symbols_df[symbols_df.ticker == ticker]
    df_macd = df_macd.merge(symbols_df, how='inner', on='ticker')

    df_macd['MgtS'] = (df_macd['MACD'] >= df_macd['Signal'])


    output_filename = 'output'

    html_content = """
    <html>
    <head>
        <title>MACD - Bullish Crossovers</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 10px;
            }
        </style>
    </head>
    <body>
        <table>
            <tr>
                <th>Values</th>
                <th>Plot</th>
            </tr>
    """
    # df_macd['Date'] = pd.to_datetime(df_macd['Date'])

    for ticker in df_macd.ticker.unique():

        print(f'Generating html for {ticker}')

        # assignments
        df_data = df_macd[(df_macd.ticker == ticker) & (df_macd['Date'] >= dt_start) & (df_macd['Date'] <= dt_end)]
        stock_name = df_macd['stock_name'][df_macd.ticker == ticker].values[0]

        if dt_start is None or dt_end is None:
            dt_start = datetime(df_data.Date.min())
            dt_end = datetime(df_data.Date.max())

        # xticks = df_data.Date.dt.strftime('%m%d').to_list()
        xticks = pd.to_datetime(df_data['Date']).dt.strftime('%Y%m').to_list()
        # xticks, dt_curr = [], df_data.Date.min()
        # while dt_curr <= df_data.Date.max():
        #     xticks.append(dt_curr.strftime("%m%d"))
        #     dt_curr += timedelta(days=1)

        # code logic
        plt.figure(figsize=(10, 4))
        plt.plot(df_data.index, df_data['MACD'], label='MACD', color='blue')
        plt.plot(df_data.index, df_data['Signal'], label='Signal Line', color='red')
        # plot lines to understand more
        # plt.plot(df_data.index, df_data['MACD_S1'], label='MACD_S1', color='green')
        # plt.plot(df_data.index, df_data['Signal_S1'], label='Signal_S1', color='orange')


        # todo : below will plot only the first point label. Change to label all points.
        for i in range(len(df_data['Date'][df_data['CrossoverBL']].values)):
            plt.annotate(df_data['Date'][df_data['CrossoverBL']].values[i],
                         (df_data['MACD'][df_data['CrossoverBL']].index.values[i], df_data['MACD'][df_data['CrossoverBL']].values[i]),
                         textcoords="offset points",
                         xytext=(-10, 3),
                         ha='left',
                         rotation=90
                         )

        # # Set the x-ticks to be the date values
        # ax = plt.gca()
        # ax.set_xticks(df_data['Date'])
        #
        # # Optionally, format the dates on the x-axis
        # ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        # ax.set_xticklabels(df_data['Date'].dt.strftime('%Y-%m-%d'), rotation=90)

        plt.xticks(df_data.index, xticks, rotation='vertical')

        # # Get the current axis
        # ax = plt.gca()
        # # x_ticks = pd.to_datetime(df_data.Date).dt.strftime('%Y-%m-%d').to_list()
        # # Set custom ticks on the x-axis and y-axis
        # ax.set_xticks(xticks)  # Custom ticks for x-axis

        # Optionally, set labels for the ticks
        # ax.set_xticklabels(xticks, rotation=90)

        # plt.gca().set_xticklabels(df_data.Date, rotation=90)
        # plt.xticks(rotation=270)
        # plt.xlabel(df_data.Date)

        plt.legend(loc='upper left')
        plt.title(f'MACD Bullish Crossovers - {ticker } - {dt_start} to {dt_end}')
        plt.grid(which='major', linestyle='--', linewidth='0.1', color='gray')

        # plt.minorticks_on()
        # # Enable minor gridlines
        # plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

        # Save plot to a string in base64 format
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')


        # Add rows to HTML content
        co_dates = next((date for date in pd.to_datetime(df_data['Date'][df_data.CrossoverBL]).dt.strftime('%Y-%m-%d')), '')

        html_content += f"""
            <tr>
                <td>{stock_name} - {ticker}{os.linesep}{co_dates}</td>
                <td><img src="data:image/png;base64,{img_str}" /></td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    # save raw data
    #df_data.to_csv(f'{output_filename}.csv')
    # save html_content
    with open(f'{output_filename}.html', 'w') as f:
        f.write(html_content)