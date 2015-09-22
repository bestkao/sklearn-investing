import pandas as pd
import os
from time import mktime
from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib import style
style.use('dark_background')

import re

# Taken from http://pythonprogramming.net/static/downloads/machine-learning-data/intraQuarter.zip
path = '/Users/James/Dropbox/Projects/sklearn/intraQuarter'


def Key_Stats(gather = "Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date', 'Unix', 'Ticker', 'DE Ratio',
                                 'Price', 'stock_p_change', 'SP500', 'sp500_p_change',
                                 'Difference', 'Status'])
    # Taken from https://www.quandl.com/data/YAHOO/INDEX_GSPC-S-P-500-Index
    sp500_df = pd.DataFrame.from_csv('YAHOO-INDEX_GSPC.csv')
    ticker_list = []

    for stock_dir in stock_list[1:100]:
        stock_files = os.listdir(stock_dir)
        ticker = stock_dir.split('/')[-1]
        ticker_list.append(ticker)

        starting_stock_price = False
        starting_sp500_value = False

        if len(stock_files) > 0:
            for stock_file in stock_files:
                date_stamp = datetime.strptime(stock_file, '%Y%m%d%H%M%S.html')
                unix_time = mktime(date_stamp.timetuple())
                stock_file_path = stock_dir + '/' + stock_file
                source = open(stock_file_path, 'r').read()

                try:
                    try:
                        de_ratio = source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0]
                        if de_ratio == 'N/A': pass
                        else: de_ratio = float(de_ratio)
                    except Exception as e:
                        try:
                            de_ratio = source.split(gather + ':</td>\n<td class="yfnc_tabledata1">')[1].split('</td>')[0]
                            if de_ratio == 'N/A': pass
                            else: de_ratio = float(de_ratio)
                        except Exception as e:
                            try:
                                de_ratio = source.split(gather + ':</td>\n<td class="yfnc_tabledata1" width="75%">')[1].split('</td>')[0]
                                if de_ratio == 'N/A': pass
                                else: de_ratio = float(de_ratio)
                            except Exception as e:
                                try:
                                    de_ratio = source.split(gather + ':</td><td class="yfnc_tabledata1" width="75%">')[1].split('</td>')[0]
                                    if de_ratio == 'N/A': pass
                                    else: de_ratio = float(de_ratio)
                                except:
                                    print 'wtf de ratio lol', ticker, stock_file, de_ratio

                    try:
                        sp500_date = datetime.fromtimestamp(unix_tim).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df.index == sp500_date]
                        sp500_value = float(row['Adjusted Close'])
                    except: # Weekends / Single Day Holidays (-3 days)
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row = sp500_df[sp500_df.index == sp500_date]
                        sp500_value = float(row['Adjusted Close'])

                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        try:
                            stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]
                            # print stock_price
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            # print stock_price
                        except Exception as e:
                            try:
                                stock_price = source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0]
                                # print stock_price
                                stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                                stock_price = float(stock_price.group(1))
                                # print stock_price
                            except Exception as e:
                                print 'wtf stock price lol', ticker, stock_file, de_ratio
                                # time.sleep(5)

                    # set if we dont have one
                    if not starting_stock_price: starting_stock_price = stock_price
                    if not starting_sp500_value: starting_sp500_value = sp500_value

                    stock_p_change = (stock_price - starting_stock_price) / starting_stock_price * 100
                    sp500_p_change = (sp500_value - starting_sp500_value) / starting_sp500_value * 100

                    location = len(df['Date'])

                    difference = stock_p_change-sp500_p_change
                    if difference > 0: status = "outperform"
                    else:              status = "underperform"

                    df = df.append({'Date'           : date_stamp,
                                    'Unix'           : unix_time,
                                    'Ticker'         : ticker,
                                    'DE Ratio'       : de_ratio,
                                    'Price'          : stock_price,
                                    'stock_p_change' : stock_p_change,
                                    'SP500'          : sp500_value,
                                    'sp500_p_change' : sp500_p_change,
                                    'Difference'     : difference,
                                    'Status'         : status},
                                   ignore_index = True)
                except Exception as e:
                    pass
                    # print str(e)

    for each_ticker in ticker_list:
        try:
            plot_df = df[df['Ticker'] == each_ticker]
            plot_df = plot_df.set_index(['Date'])

            if plot_df['Status'][-1] == 'underperform':
                color = 'r'
            else:
                color = 'g'

            plot_df['Difference'].plot(label = each_ticker, color=color)
            plt.legend()
        except:
            pass

    plt.show()
    save = gather.replace(' ','').replace('(','').replace(')','').replace('/','') + '.csv'
    print(save)
    df.to_csv(save)

Key_Stats()
