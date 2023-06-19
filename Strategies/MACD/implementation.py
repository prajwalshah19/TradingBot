
import pandas as pd
import requests
import time
import datetime
from pathlib import Path
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce


from General.helper import rb_login, alpaca_login, create_batches, get_ask_price


from Secrets.keys import TWELVEDATA_KEY



def newTable(table, batch):
    url = f'https://api.twelvedata.com/macd?symbol={batch}&interval=1day&apikey={TWELVEDATA_KEY}'

    data = requests.get(url).json()

    for ticker in data:
        try:
            macd = data[ticker]['values'][0]['macd']
        except KeyError:
            break
        signal = data[ticker]['values'][0]['macd_signal']
        hist = data[ticker]['values'][0]['macd_hist']

        table.loc[len(table.index)] = [ticker, macd, signal, hist]
 




def macd_data():
    stocks = pd.read_csv('./General/Data/sp_100_stocks.csv')
    my_cols = ['Ticker', 'MACD', 'Signal', 'Hist']
    final_df = pd.DataFrame(columns = my_cols)
    batches = create_batches(stocks['Ticker'], 8)
    for item in batches:
        newTable(final_df, item)
        time.sleep(61)
    filepath = Path(f'./Strategies/MACD/Logs/{datetime.date.today()}macd_trades.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    final_df.to_csv(filepath)  

def make_macd_port(capital, percent):
    bp = capital * percent
    stocks = pd.read_csv('General/Data/marketCap.csv')
    #display(stocks)
    total = stocks['Market Cap'].sum()
    #print(total)
    cols = ['Ticker', 'Value Bought']
    newPort = pd.DataFrame(columns = cols)
    
    for i in range(len(stocks['Ticker'])):
        #print(stocks["Ticker"][i], stocks['Market Cap'][i])
        val = ((stocks['Market Cap'][i]) / total) * bp
        newPort.loc[len(newPort.index)] = [stocks["Ticker"][i], val]
    #display(newPort)
    filepath = Path(f'Strategies/MACD/Data/macd_init_port.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    newPort.to_csv(filepath)  



#TRADING METHODS
def macd_init_portfolio(capital, percent):
    make_macd_port(capital, percent)
    stocks = pd.read_csv("Strategies/MACD/Data/macd_init_port.csv")
    rb_login()
    client = alpaca_login()
    c = 0
    for i in range(len(stocks["Ticker"])):
        print(stocks["Ticker"][i])
        
        price = get_ask_price((stocks["Ticker"][i]).replace(",", ""))
        #print(type(price))
        quant = (stocks["Value Bought"][i]) / price
        if(price * quant) > 1:
            data = MarketOrderRequest(
                symbol = (stocks["Ticker"][i]).replace(",", ""),
                qty = quant,
                side = OrderSide.BUY,
                time_in_force = TimeInForce.DAY
            )
            order = client.submit_order(order_data = data)
        else:
            print((stocks["Ticker"][i]).replace(",", ""), "quant too low")
            c += 1
    print("MCAP Weighted SP-100 portfolio initialized", c)

def macd():
    macd_data(1000, .2)
    rb_login()
    client = alpaca_login()
    stocks = pd.read_csv(f'./Strategies/MACD/Logs/{datetime.date.today()}macd_trades.csv')
    #totalComposite = (stocks['MACD'].sum() - stocks['Signal'].sum() ) + stocks['Hist'].sum()
    #positions = client.get_all_positions()
    sum = 0
    for i in range(len(stocks["Ticker"])):
        price = get_ask_price(stocks["Ticker"][i])
        #composite = (stocks['MACD'][i] - stocks['Signal'][i]) + stocks['Hist'][i]
        percentChange = (stocks['MACD'][i] - stocks['Signal'][i]) / stocks['MACD'][i]
        try: 
            position = float(client.get_open_position(stocks["Ticker"][i]).qty)
            
            print(stocks["Ticker"][i], position * price, percentChange * position * price)
            sum += (percentChange * position * price)
            if abs(percentChange * position * price ) > 1:
                data = MarketOrderRequest(
                    symbol = stocks["Ticker"][i],
                    qty = abs(position * percentChange),
                    side = OrderSide.BUY if (percentChange > 0) else OrderSide.SELL,
                    time_in_force = TimeInForce.DAY
                    )
                order = client.submit_order(order_data = data)


                print(stocks["Ticker"][i], "done", "bought" if (percentChange > 0) else "sold")
            else:
                print(stocks["Ticker"][i], "quant too low")
        except:
            print(stocks["Ticker"][i], "position doesn't exist")


    print("Changed Positions based on Daily MACD composite score, net traded volume -->", sum)