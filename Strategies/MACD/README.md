# MACD Trading Strategy

MACD stands for moving average convergence/divergence. It is a momentum based technical indicator that returns the different between long term and short term exponential moving average. In this case, the MACD strategy is longer term hedge against the more riskier strategies in the portfolio, and therefore uses 26-day and 12-day as the long and short term averages respectively. 

## Initialization
As a longer term strategy, the initial setup for the MACD strategy requires an initial portfolio consisting of every stock in the SP-100, with positions bought based on market capitalization.

## Trades
The MACD trades once every day. To begin, it creates a table with each stocks current MACD and Signal (the MACD for an arbitrary signal value, in this case 9-day). In technical analysis, a stock is considered a BUY if the MACD is higher than the Signal. Therefore, each day, the difference in percentage from a stocks MACD and Signal is used to determine the percent-change in position for the stock. 

## Setup
To run MACD after initializing the repository, first determine total portfolio size (capital) and the percent of the portfolio that will be invested in the MACD strategy. Since the MACD strategy is relatively buy heavy, the initial chosen percentage should be roughly half of the intended percentage used for this strategy. Then ```cd TradingBot ``` and run ```python3 -c "from main import macd_run; macd_run(capital, percent, True)" ```. This will initialize your MACD portfolio and then run ```python3 -c "from main import macd_run; macd_run()" ``` to change positions daily. Note, the default values for the strategy is $1000 of capital at 20%.
