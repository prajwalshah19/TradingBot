from Strategies.MACD import implementation as macd
from Strategies.BollingerBands import implementation as bbands
from datetime import datetime
import pytz

def macd_run(capital = 1000, percent = 0.2, init = False):
    if init:
        macd.macd_init_portfolio(capital, percent)
    else:
        macd.macd()

def bbands_run(capital = 1000, percent = 0.2):
    tz = pytz.timezone('US/Eastern')
    bp = capital * percent
    print(datetime.now(tz).hour, datetime.now(tz).minute)
    time = [datetime.now(tz).hour, datetime.now(tz).minute]
    while (time[0] > 9 and time[1] > 30) and (time[0] < 16):
        time = [datetime.now(tz).hour, datetime.now(tz).minute]
        if time[1] == 26 or time[0] == 56:
            print("starting process")
            bbands.bbands()
            print("just ran",datetime.now(tz).hour, datetime.now(tz).minute)
    print("market is closed")
