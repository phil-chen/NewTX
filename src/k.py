''' all operations related to k bar is put here '''
import os
import mtx
import json
from datetime import datetime, timedelta
import time
import FirebaseUtil
import g
import calendar

time_price = dict()
yesterday_time_price = dict()
legal_hour = map(str,range(8,14))
fb = FirebaseUtil.FirebaseUtil()

# TODO: FOR TESTING
TEST_PRICE = 8500

def update_k_60():
    curr_time = time.strftime("%H%M")
    curr_date = time.strftime("%Y%m%d")
    if curr_time.endswith("45") and curr_time[0:2] in legal_hour:
        time_price[curr_time] = mtx.get_price()
        outfile = '../history/' + current_date + '.json'
        with open(outfile, 'w') as outfile:
            json.dump(data, outfile)

def last_trade_date(d):
    # front-end wrapper function
    return last_trade_date_1(d)

def last_trade_date_1(d):
    d = d - timedelta(1)
    while fb.get(str(d).replace('-','/')) == None:
        d = d - timedelta(1)
    return d

def last_trade_date_2(d):
    # TODO: Replace the following code with trial and error.
    # Check whether or not there are prices for yesterday iteratively
    weekend = ['Sunday', 'Saturday']
    d = d - timedelta(1)
    while calendar.day_name[d.weekday()] in weekend:
        d = d - timedelta(1)
    return d

def today():
    return datetime.now().date()

def k_day_trend():
    trade_days = []
    trade_day = today()
    for i in range(1,5):
        trade_day = last_trade_date(trade_day)
        trade_days.append(trade_day)

    print trade_days
    trade_days = map(lambda i: str(i).replace('-','/'), trade_days)
    prices = map(lambda i: int(fb.get(i)), trade_days)
    print prices

    last_4_avg = sum(prices)/len(prices)
    print last_4_avg

    # Derivation:
    # (x1+x2+x3+x4+now)/5 >= (x1+x2+x3+x4)/4 + UP_THRESHOLD
    # 4now >= x1 + x2 + x3 + x4 + 20UP_THRESHOLD
    # now >= last_4_avg + 5UP_THRESHOLD
    curr_price = mtx.get_price_TX()
    if curr_price >= (last_4_avg + 5*g.UP_THRESHOLD):
        return 1
    elif curr_price <= (last_4_avg - 5*g.BOTTOM_THRESHOLD):
        return -1
    else:
        return 0

def update_k_day():
    # front-end wrapper
    return update_k_day_1()

def update_k_day_1():
    access_str = str(last_trade_date(today())).replace('-','/')
    return fb.get(access_str)

def update_k_day_2():
    yesterday_date = datetime.now() - timedelta(1)
    yesterday_str = yesterday_date.strftime("%Y%m%d")
    infile = '../history/' + yesterday_str + '.json'
    while os.path.isfile(infile) != True:
        yesterday_date = yesterday_date - timedelta(1)
        yesterday_str = yesterday_date.strftime("%Y%m%d")
        infile = '../history/' + yesterday_str + '.json'

    print yesterday_date

    with open(infile, 'r') as infile:
        yesterday_time_price = json.loads(infile.read())
    return yesterday_time_price

def k_60_trend():
    # TODO
    return 1

if __name__ == '__main__':
    print k_day_trend()
    # print update_k_day_1()
    print last_trade_date(today())
