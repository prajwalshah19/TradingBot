# TradingBot

This is a stock market trading bot that aims to utilize various methods of technical analysis to buy and sell securities with the intent of outperforming the market. 

## Overview

This bot operates by implementing numerous techinical trading strategies that operate independently of each other. The end user will eventually be able to designate how much of each strategy is utlized in their portfolio. The project utilizes the various API's and packages to get data and execute trades.

| Source        | Purpose       |
| ------------- | ------------- |
| TwelveData API   | Get real time technical indicators for analysis.  |
| YFinance Package (temporary) | Get more static stock data for initialization (such as market capitalization). |
| Alpaca API       | Read current positions and execute paper trades.  |
| RobinStocks Package | Get real time stock prices (temporary) and execute real money trades (coming soon).  |

Below is how the project is setup:
```
/TradingBot
  /General
    /Data
      {CSVs containing general stock information}
    - helper.py
  /Strategies
    /Algo Trading Strategy 
      /Data
        {CSVs containing strategy specfic stock information}
      /Logs
        {CSVs containing day-to-day trade information}
      -implementation.py 
  /Secrets
    -keys.py
  -main.py
  -requirements.txt

```

## Modules

| Name | Purpose |
| ------------- | ------------- |
| General  | Contains general stock information and helper methods to assist with algorithm implementation.  |
| Strategies  | Contains each trading strategy and implementation  |
| main.py (coming soon) | Contains interface for end user to view all trading strategies and build their portfolio.  |
| requirements.txt  | Contains all dependencies. |
| Secrets  | Contains api keys. |

## Setup

1. Clone repository onto local machine ```git clone https://github.com/prajwalshah19/TradingBot.git``` 
2. Navigate to directory ```cd TradingBot ```
3. Install Dependencies ```pip install -r requirements.txt```
4. Open ```Secrets-Demo```, update the keys in ```keys.py``` and rename ```Secrets-Demo``` to ```Secrets```

Note: If your local machine is runnig Python 3.11, please set up a virtual environment with Python 3.10 to ensure dependency compatibility.

## Usage

Coming Soon

## Dependencies 

Trading bot uses the following packages 

* ```pandas``` and ```numpy``` for data analysis and csv formatting.
* ```requests``` for making API calls to the TwevleData API
* ```alpaca-py``` for executing paper trades.
* ```yfinance``` as a temporary solution for getting stock data.
* ```robin-stocks``` to access stock information and eventually execute real money trades.
* ```time```, ```datetime```, ```pathlib```, and ```aiohttp``` for other administrative tasks.

## Contributions

Contributions are welcome and encouraged. Please fork and make changes. For anyone with experience in algorithmic trading, feel free to implement your own strategy!

Pull requests are welcomed.

## License
MIT License




