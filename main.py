from Strategies.MACD import implementation as macd
from Strategies.BollingerBands import implementation as bbands
from datetime import datetime
from threading import Thread
import time as t
import pytz

def macd_run(capital = 1000, percent = 0.3, init = False):
    if init:
        macd.macd_init_portfolio(capital, percent)
    
    macd.macd()

def bbands_run(capital = 1000, percent = 0.4):
    tz = pytz.timezone('US/Eastern')
    bp = capital * percent
    print(datetime.now(tz).hour, datetime.now(tz).minute)
    time = [datetime.now(tz).hour, datetime.now(tz).minute]
    while (time[0] >= 9 ) and (time[0] < 16):
        time = [datetime.now(tz).hour, datetime.now(tz).minute]
        if time[1] == 26 or time[1] == 56:
            print("starting process")
            bbands.bbands(bp)
            print("just ran",datetime.now(tz).hour, datetime.now(tz).minute)
            t.sleep(61)
    print("market is closed")

def run():
    tz = pytz.timezone('US/Eastern')
    time = [datetime.now(tz).hour, datetime.now(tz).minute]
    
    while True:
        time = [datetime.now(tz).hour, datetime.now(tz).minute]
        if (time[0] == 9 and time[1] == 2) and (datetime.now(tz).weekday() < 5):
            
            Thread(target=bbands_run).start()
            macd_run()
        
        
            
