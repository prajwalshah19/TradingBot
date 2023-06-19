from Strategies.MACD import implementation as macd
from Strategies.BollingerBands import implementation as bbands
from datetime import datetime

def macd_run(capital = 1000, percent = 0.2, init = False):
    if init:
        macd.macd_init_portfolio(capital, percent)
    else:
        macd.macd()

def bbands_run(capital = 1000, percent = 0.2):
    bp = capital * percent
    #print(datetime.now().hour, datetime.now().minute)
    time = [datetime.now().hour, datetime.now().minute]
    while (time[0] > 9 and time[1] > 30) and (time[0] < 16):
        time = [datetime.now().hour, datetime.now().minute]
        if time[1] == 26 or time[0] == 0:
            print("starting process")
            bbands.bbands()
            print("just ran",datetime.now().hour, datetime.now().minute)
    print("market is closed")
