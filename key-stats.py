import pandas as pd
import os
import time
from datetime import datetime

# Taken from http://pythonprogramming.net/static/downloads/machine-learning-data/intraQuarter.zip
path = '/Users/James/Dropbox/Projects/sklearn/intraQuarter'

def Key_Stats(gather = "Total Debt/Equity (mrq)"):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    # print stock_list

    for stock_dir in stock_list[1:]:
        stock_files = os.listdir(stock_dir)
        ticker = stock_dir.split('/')[-1]
        if len(stock_files) > 0:
            for stock_file in stock_files:
                date_stamp = datetime.strptime(stock_file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # # time stamp
                # print date_stamp, unix_time

                stock_file_path = stock_dir + '/' + stock_file
                print stock_file_path

                source = open(stock_file_path, 'r').read()
                # print source

                if gather + ':</td>' in source:
                    value = source.split(gather + ':</td>')[1].split('<td class="yfnc_tabledata1">')[1].split('</td>')[0]
                else:
                    value = 'N/A'
                print ticker + ':' + value

            time.sleep(15)

Key_Stats()
