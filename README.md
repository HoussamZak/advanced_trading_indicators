# stateOfTheArt_trading_indicators
New powerful trading indicators functions to generate indicators and/or signals on your dataframes.

-----------------------------------------------------------------------------------------------

Relative Vigor Index - RVI

-----------------------------------------------------------------------------------------------

Diparity Index 
- dataframe with at least a Close or price column 
- default parameters:
    _lookback = 14

-----------------------------------------------------------------------------------------------

Trend Exhaustion indicator:
- dataframe with at least a Close or price column 
- default parameters:
    _lookback = 21
    _buy_thrshld = 15
    _sell_thrshld = -20

-----------------------------------------------------------------------------------------------

Aaron Oscillator, a modified version of Aaron Up and Aaron Down indicators, is used to identify 
the start of new trends and their strength by measuring elapsed time in between highs and lows
over a specific period of time. 

High Aaron Oscillator indicates strong upward trend while low value is indicative of a strong 
downtrend, values > + 50 => strong bullish momentum , values < -50 => strong bearish momentum.

Aaron Oscillator, default period = 25.

-----------------------------------------------------------------------------------------------

Choppiness Index

-----------------------------------------------------------------------------------------------

Trend Exhaustion