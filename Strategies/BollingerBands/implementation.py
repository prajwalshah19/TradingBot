import pandas as pd
import requests
import time
import datetime
import pytz
from pathlib import Path
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from General.helper import rb_login, alpaca_login, create_batches, get_ask_price


from Secrets.keys import TWELVEDATA_KEY

def newTable(table, batch):
    rb_login()
    url = f'https://api.twelvedata.com/bbands?symbol={batch}&interval=30min&apikey={TWELVEDATA_KEY}'

    data = requests.get(url).json()

    for ticker in data:
        try:
            
            upper = float(data[ticker]['values'][0]['upper_band'])
        except KeyError:
            break
        lower = float(data[ticker]['values'][0]['lower_band'])
        mid = data[ticker]['values'][0]['middle_band']
        price = get_ask_price(ticker)
        bp = ((price -lower) / (upper-lower))
        table.loc[len(table.index)] = [ticker, upper, lower, bp]

def bbands_data():
    stocks = pd.read_csv('General/Data/high_growth25.csv')
    my_cols = ['Ticker', 'Upper', 'Lower', 'BBands%']
    final_df = pd.DataFrame(columns = my_cols)
    batches = create_batches(stocks['Ticker'], 8)
    for item in batches:
        newTable(final_df, item)
        time.sleep(61)
    filepath = Path(f'./Strategies/BollingerBands/Data/{datetime.date.today()}bbands_data.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    final_df.to_csv(filepath) 

def bbands(bp):
    rb_login()
    client = alpaca_login()
    cols = ['Ticker', 'Side', 'Value$']
    table = pd.DataFrame(columns = cols)
    tz = pytz.timezone('US/Eastern')
    bbands_data()
    stocks = pd.read_csv(f'Strategies/BollingerBands/Data/{datetime.date.today()}bbands_data.csv')
    mCaps = pd.read_csv('General/Data/high_growth25_marketCap.csv')
    average_mCap = mCaps['Market Cap'].mean()
    side = ""
    #print(average_mCap)
    for i in range(len(stocks["Ticker"])):
        price = get_ask_price(stocks["Ticker"][i])
        
        if stocks["BBands%"][i] < 0.3:
            side = "buy"
            factor = 1 + (abs(stocks["BBands%"][i] - 0.3))/0.3
            
        elif stocks["BBands%"][i] > 0.7:
            side = "sell"
            factor = 1 + (abs(stocks["BBands%"][i] - 0.7))/0.7
            
        else:
            continue
        val = bp * (mCaps["Market Cap"][i] / average_mCap) * .04 * factor
        
        if val > 1:
            if stocks["BBands%"][i] < 0.3:
                data = MarketOrderRequest(
                        symbol = stocks["Ticker"][i],
                        qty = val / price,
                        side = OrderSide.BUY ,
                        time_in_force = TimeInForce.DAY
                            )
                order = client.submit_order(order_data = data)
                table.loc[len(table.index)] = [stocks["Ticker"][i], side, val]
                print(stocks["Ticker"][i], side, val)
            else:
                try:
                    pos = float(client.get_open_position(stocks["Ticker"][i]).qty)
                    quant = (val / price) if val < pos else (pos/price)
                    data = MarketOrderRequest(
                        symbol = stocks["Ticker"][i],
                        qty = quant,
                        side = OrderSide.SELL ,
                        time_in_force = TimeInForce.DAY
                            )
                    order = client.submit_order(order_data = data)
                    table.loc[len(table.index)] = [stocks["Ticker"][i], side, val]
                    print(stocks["Ticker"][i], side, val)
                except Exception as e:
                    print(stocks["Ticker"][i], "no open position to sell from, exception -->", e)
    filepath = Path(f'./Strategies/BollingerBands/Logs/{datetime.datetime.now(tz)}bbands_trades.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    table.to_csv(filepath) 

        
        
        
        


    
        






            