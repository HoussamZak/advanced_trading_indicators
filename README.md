# stateOfTheArt_trading_indicators
Powerful trading indicators functions to generate indicators and/or signals on your dataframes.

Each indicator comes with a function to add indicator and signals to a dataframe along with
a plotting function to visualize Buy-Long, Sell-Short entries on price chart.



Relative Vigor Index - RVI:
- functions:    rvi_signals & plot_stock_with_rvi
- have a ready dataframe with at least a Close or price column 

This index measures the strength of current trend by comparing the closing to the opening price within
a specific period. The idea is backed by calculation checking that in a strong bullish trend prices do
tend to close near the high/max point of the period while in a strong bearish trend prices do tend to 
close near the low/min of the window period. RVI, in plotting function, is shown as a red line labelled
signal line along which crossovers can indicate Long or Short entries. 
Ideally, RVI is best used in combination with a moving average to better assess and label market trend.

-----------------------------------------------------------------------------------------------

DeMarker Indicaor:

- functions: demarker_indc & plot_with_demarker
- have a ready dataframe with at least a Close or price column 

The DeMarker Indicator identifies potential buying or selling opportunities when price reaches exhaustion levels, 
thus signaling market tops and bottoms. It is calculated based on the demands of the high and low prices
given a particular period. 




-----------------------------------------------------------------------------------------------

Trend Exhaustion indicator: 
    
- functions: trend_exhaustion & plot_stock_with_trendExhaustion
- have a ready dataframe with at least a Close or price column 
- default parameters:
    _lookback = 21
    _buy_thrshld = 15
    _sell_thrshld = -20

In order to assess the exhaustion and potential subsequent reversal of a trend we can rely on 
the Trend Exhaustion Indicator. It usually would look at strong divergences in indicator like RSI 
and/or divergences in Volume while our code considers the time spent above or below the mean to generate
buy or sell signals.

-----------------------------------------------------------------------------------------------
Aaron Oscillator

- functions:   
- have a ready dataframe with at least a Close or price column 
- default period = 25

Aaron Oscillator, a modified version of Aaron Up and Aaron Down indicators, is used to identify 
the start of new trends and their strength by measuring elapsed time in between highs and lows
over a specific period of time. 

High Aaron Oscillator indicates strong upward trend while low value is indicative of a strong 
downtrend, values > + 50 => strong bullish momentum , values < -50 => strong bearish momentum.

-----------------------------------------------------------------------------------------------

Choppiness Index: 

- function: chopp_idx_signals 
- have a ready dataframe with at least a Close or price column 
- window_size = 14

To distinguish between trendin and ranging markets we can use Choppiness Index which measures 
the degree of volatility by using a logarithmic formula that compares the sum of TrueRange over
a set number of selected periods to the set of market Highs & Lows during the same period. CI can
be used to determine whether it is best to deploy trend-following strategies or range-trading ones.

-----------------------------------------------------------------------------------------------

