
import robin_stocks.robinhood as rb
from alpaca.trading.client import TradingClient
from Secrets.keys import ALPACA_KEY, ALPACA_SECRET_KEY, RB_USERNAME, RB_PASSWORD
import pathlib as Path
import pandas as pd
import time
import yfinance as yf

def rb_login():
    rb.login(username = RB_USERNAME,
             password = RB_PASSWORD,
             expiresIn = 86400, 
             by_sms=True)

def alpaca_login():
    client = TradingClient(ALPACA_KEY, ALPACA_SECRET_KEY, paper=True)
    return client

def get_ask_price(ticker):
    return float(rb.stocks.get_latest_price(ticker)[0])

def create_batches(info, bsize):
    batches = []
    numBatches = int(info.size / bsize)
    #print(info.size, numBatches)
    for i in range(numBatches):
        
        batch = []
        for j in range(bsize):
            batch.append(info[(i * bsize) + j])
        batches.append(', '.join(batch))
    batches.append(", ".join(info[(info.size - (info.size % bsize)):].tolist()))
    return batches


def update_market_cap():
    stocks = pd.read_csv('General/Data/sp_100_stocks.csv')
    
    my_cols = ['Ticker', 'Market Cap']
    mcap = pd.DataFrame(columns = my_cols)
    batches = create_batches(stocks['Ticker'], 20)
    #print(batches)
    for item in batches:
        print(item.split())
        for ticker in item.split():
            #print(ticker)
            t = ticker.replace(",", "")
            t = t.replace(".", "-")
            stock = yf.Ticker(t).info
            print(ticker.replace(",", ""), stock["marketCap"])
            mcap.loc[len(mcap.index)] = [ticker.replace(",", ""), stock["marketCap"]]
        time.sleep(61)
    filepath = Path.Path(f'General/Data/marketCap.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    mcap.to_csv(filepath)  

