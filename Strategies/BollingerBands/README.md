# Bollinger Bands Trading Strategy
Bollinger Bands (BBands) is a technical indicator based on using a simple moving average given a number of periods (typically 20) and set amount of standard deviations (typically 2) to construct upper and lower bounds of a stocks price level. It is powerful because it adjusts according to volatility swings due to the use of standard deviation in its calculation.

## Initialization
The BBands trading strategy doesn't initialize a set portfolio and instead only trades from a list of 25-30 high growth yet stable stocks.

## Trades
The BBands strategy executes once every half an hour starting at 9:30 AM EST and ending at 4:00 PM EST. To perform its calculation it first determines a composite indicator using a stocks price, upper BBand, and lower BBand, called the B%. The B% is calculated as follows: 
```
B% = (Price - Lower Band ) / (Upper Band - Lower Band )
```
If this value is below a certain threshold (default 0.3), then it generates BUY signal. If the value is above a certain value (default 0.7), then it generates a SELL signal. Values in between the BUY and SELL threshold require no action. Once the algorithim determines an action, it then determines a factor (f) based on the value of B% using the following formula:
```
f = 1 + ( |B% - Threshold(BUY or SELL)| / Threshold )
```
It then uses this factor to determine a value to trade for the given stock using the following formula:
```
Trade Value = 0.04 * Buying Power * (Stock Market Cap / Average Market Cap ) * f
```
Note: If a sell signal is given to position that doesn't exist, the algorithm will ignore it.

## Setup
To set up the BBands strategy after initializing the repository, first ```cd TradingBot``` then run ```python3 -c "from main import bbands_run; bbands_run(capital, percent)``` where capital is your portfolio size and percent is the percent of portfolio being allocated to this strategy.


