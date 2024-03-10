import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

#------------------------- Choppiness Index -------------------------

def calc_true_range(data):
    #-- all column names lowercase
    data.columns = map(str.lower, data.columns)

    return np.maximum.reduce([
        data['high'] - data['low'],
        abs(data['high'] - data['close'].shift()),
        abs(data['low'] - data['close'].shift())
        ])

#-- Change window_size value at your own discretion
#-- 14 is common window chosen in ATR calculation

def chopp_idx_signals(data):
    #-- all column names lowercase
    data.columns = map(str.lower, data.columns)
    window_size = 14
    #-- Calculate ATR, highest high, lowest low & choppiness index
    data['true_range'] = calc_true_range(data)
    data['ATR'] = data['true_range'].rolling(window = window_size).mean()
    data['highest_high'] = data['high'].rolling(window =window_size).max()
    data['lowest_low'] = data['low'].rolling(window =window_size).min()
    #-- Choppiness Index
    data['sum_true_range'] = data['true_range'].rolling(window = window_size).sum()
    data['range'] = data['highest_high'] - data['lowest_low']
    data['chop'] = 100 * np.log10(data['sum_true_range'] / data['range']) /np.log10(window_size)
    data['chop'] = data['chop'].clip(lower = 0, upper = 100)
    #-- buy & sell signals based on Choppiness Index
    data['chop_lag1'] = data['chop'].shift()
    data['signal'] = np.where((data['chop'] < 30) & (data['chop_lag1'] >= 30), "Buy Signal",
                              np.where((data['chop'] > 60 ) & (data['chop_lag1'] <= 60),"Sell Signal", "Neutral"))
    return data


#------------------------- Disparity Index -------------------------

def disparity_index(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)
    #-- renaming price column if price column present
    data = data.rename(columns={'price': 'close'})
    data = data.rename(columns={'prices': 'close'})
    #-- default lookback value
    lookback = 14
    
    data['mov_avg'] = data['close'].rolling(lookback).mean()
    data['disp'] = ((data['close'] - data['mov_avg'] )/ data['mov_avg']) * 100

    buy_prices = []
    sell_prices = []
    disp_signal = []
    signal = 0
    # data.dropna(inplace = True)

    for i in range(len(data['close'])):
        if data['disp'].iloc[i - 4] < 0 and data['disp'].iloc[i - 3] < 0 and data['disp'].iloc[i - 2]<0 and data['disp'].iloc[i-1]<0 and data['disp'].iloc[i] > 0:
            if signal != 1:
                buy_prices.append(data['close'].iloc[i])
                sell_prices.append(np.nan)
                signal = 1 
            else:
                buy_prices.append(np.nan)
                sell_prices.append(np.nan)
                disp_signal.append(0)

        elif data['disp'].iloc[i - 4] > 0 and data['disp'].iloc[i - 3] > 0 and data['disp'].iloc[i - 2]>0 and data['disp'].iloc[i-1]>0 and data['disp'].iloc[i] < 0:
            if signal != -1:
                buy_prices.append(np.nan)
                sell_prices.append(data['close'].iloc[i])
                signal = -1
                disp_signal.append(signal)
            else:
                buy_prices.append(np.nan)
                sell_prices.append(np.nan)
                disp_signal.append(0)
        else:
            buy_prices.append(np.nan)
            sell_prices.append(np.nan)
            disp_signal.append(0)
    #-- appending generated signals series to dataframe 
    # data['signal'] = disp_signal
    # data['buy_price'] =  buy_prices
    # data['sell_price'] = sell_prices
    return data , disp_signal, buy_prices, sell_prices

#-- deploying trading/strategy logic and plotting
def disparity_strategy_and_plot(data):

    # buy_prices, sell_prices, _ = disparity_index(data['close'])

    # Plotting the buy and sell signals along with DI
    fig, ax = plt.subplots(2, 1, figsize=(15, 8), gridspec_kw={'height_ratios': [2, 1]})
    
    # Plotting the stock price and signals
    ax[0].plot(data['close'], label='Close Price', alpha=0.5)
    ax[0].scatter(data.index, data['buy_price'], label='Buy Signal', marker='^', color='green', s=100)
    ax[0].scatter(data.index, data['sell_price'], label='Sell Signal', marker='v', color='red', s=100)
    ax[0].set_title(' - Buy & Sell Signals')
    ax[0].set_ylabel('Price')
    ax[0].legend()

    # Plotting the Disparity Index with bars
    ax[1].bar(data.index, data['disp'], color=np.where(data['disp'] >= 0, '#26a69a', '#ef5350'))
    ax[1].axhline(0, color='gray', linestyle='--')  # Add a line at zero
    ax[1].set_title(' - 14-Period Disparity Index')
    ax[1].set_xlabel('Date')
    ax[1].set_ylabel('Disparity Index (%)')

    plt.tight_layout()
    plt.show()


#------------------------- Trend Exhaustion -------------------------

def trend_exhaustion(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)
    lookback = 21
    buy_thrshld = 15
    sell_thrshld = -20
    #-- moving average
    movavg =data['close'].rolling(window = lookback).mean()
    #-- time spent above mean
    above_M = np.where(data['close'] > movavg, 1, 0)
    for i in range(1, len(above_M)):
        if above_M[i] == 1:
            above_M[i] += above_M[i-1]
    
    #-- time spent below mean
    below_M = np.where(data['close'] <  movavg, -1, 0)
    for i in range(1, len(below_M)):
        if below_M[i] == -1:
            below_M[i] += below_M[i - 1]
    
    #-- generatingsignals
    signals = pd.Series(0, index = data.index)
    signals[below_M <= sell_thrshld] = 1 #-- buy long signal
    signals[above_M >= buy_thrshld] = -1 #-- sell short signal
    return pd.DataFrame({
        'close' : data['close'],
        'mov_avg' : movavg,
        'above_mean' : pd.Series(above_M, index = data.index),
        'below_mean' : pd.Series(below_M, index = data.index),
        'signal': signals
    })
#-- Plotting with trendExhaustion 

def plot_stock_with_trendExhaustion(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)
    ax1.plot(data['close'], label='Close Price', color='blue')
    ax1.plot(data['mov_avg'], label='Moving Average', color='red')
    ax1.scatter(data.index, data['close'].where(data['signal']==1), color='green', marker='^', alpha=1, s =100)
    ax1.scatter(data.index, data['close'].where(data['signal']==-1), color='red', marker='v', alpha=1, s = 100)
    ax1.legend(loc='upper left')
    ax1.set_ylabel('Price')
    ax1.grid(True)

    ax2.plot(data['above_mean'], label='Time Spent Above Mean', color='green')
    ax2.plot(data['below_mean'], label='Time Spent Below Mean', color='red')
    ax2.legend(loc='upper left')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Time Spent')
    ax2.grid(True)

    plt.title('Time Spent Above or Below Mean,  Signals')
    plt.tight_layout()
    plt.show()

#------------------------- Relative Vigor Index -----------------------
    
def rvi_signals(data, period = 10):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)

    numerator = data['close'] - data['open']
    denominator = data['high'] - data['low']
    data['rvi'] = (numerator.rolling(window = period).mean() /
                   denominator.rolling(window = period).mean())
    data['rvi_signal'] = data['rvi'].rolling(window = period).mean()
    data['buy_long'] = ((data['rvi'] > data['rvi_signal']) & (data['rvi'].shift(1) <= data['rvi_signal'].shift(1)))
    data['sell_short'] = ((data['rvi'] < data['rvi_signal']) & (data['rvi'].shift(1) >= data['rvi_signal'].shift(1)))
    return data 

def plot_stock_with_rvi(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 10), gridspec_kw={'height_ratios': [2, 1]})
    # Stock price plot with buy and sell signals
    ax1.plot(data['close'], label='Close Price', color='blue')
    ax1.scatter(data.index[data['buy_long']], data['close'][data['buy_long']], label='Buy Signal', marker='^', color='green', alpha=1)
    ax1.scatter(data.index[data['sell_short']], data['close'][data['sell_short']], label='Sell Signal', marker='v', color='red', alpha=1)
    ax1.set_title('Relative Vigor Index, Stock Price ')
    ax1.set_ylabel('Price')
    ax1.legend()

    # RVI plot with buy and sell signals
    ax2.plot(data['rvi'], label='RVI', color='green')
    ax2.plot(data['rvi_signal'], label='Signal Line', color='red', linestyle='--')
    ax2.scatter(data.index[data['buy_long']], data['rvi'][data['buy_long']], label='Buy Signal', marker='^', color='blue', alpha=1)
    ax2.scatter(data.index[data['sell_short']], data['rvi'][data['sell_short']], label='Sell Signal', marker='v', color='orange', alpha=1)
    ax2.set_title('Relative Vigor Index (RVI) with Signals')
    ax2.set_ylabel('RVI')
    ax2.legend()

    plt.tight_layout()
    plt.show()

#------------------------- DeMarker Indicator -------------------------

def demarker_indc(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)

    period = 9
    data['deMAX'] = 0
    data['deMIN'] = 0
    for i in range(1, len(data)):
        if data['close'][i] > data['close'][i - 1]:
            data['deMAX'][i] = data['close'][i] - data['close'][i-1]
        elif data['close'][i] < data['close'][i - 1]:
            data['deMIN'][i] = data['close'][i - 1] -data['close'][i]

    data['deMM'] = data['deMAX'].rolling(window = period).mean()
    data['deMN'] = data['deMIN'].rolling(window = period).mean()
    data['deMarker'] = data['deMN'] / (data['deMM'] + data['deMN'])

    #-- Buy & Sell Signals to dataframe
    data['buy_long'] = (data['deMarker'] < 0.275) & (data['deMarker'].shift(1) >= 0.3)
    data['sell_short'] = (data['deMarker'] > 0.725) & (data['deMarker'].shift(1) <= 0.7)
    return data

def plot_with_demarker(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8))
    # Stock price with buy and sell signals
    ax1.plot(data['close'], label='Close Price', alpha=0.5)
    ax1.scatter(data.index[data['buy_long']], data['close'][data['buy_long']], label='Buy Signal', marker='^', color='green', s=100)
    ax1.scatter(data.index[data['sell_short']], data['close'][data['sell_short']], label='Sell Signal', marker='v', color='red', s=100)
    ax1.set_title('Price Chart with Buy and Sell Signals')
    ax1.set_ylabel('Price')
    ax1.legend()

    # DeMarker Indicator
    ax2.plot(data['deMarker'], label='DeMarker', color='blue')
    ax2.axhline(0.7, color='red', linestyle='--', label='Overbought Threshold (0.725)')
    ax2.axhline(0.3, color='green', linestyle='--', label='Oversold Threshold (0.275)')
    ax2.set_title('DeMarker Indicator')
    ax2.set_ylabel('DeMarker Value')
    ax2.legend()

    plt.tight_layout()
    plt.show()


#------------------------- Aaron Indicator -------------------------
    
def aaron_indicator(data):
    #-- ensuring that all column names lowercase
    data.columns = map(str.lower, data.columns)

    period = 25
    aaron_up = 100 * (data['high'].rollling(period + 1).apply(np.argmax, raw = True) / period)
    aaron_down = 100 * (data['low'].rolling(period + 1).apply(np.argmin, raw = True) / period)
    # aaron_oscillator = aaron_up - aaron_down 
    data['aaron_osc'] = aaron_up - aaron_down 

    #-- Buy & Sell Signals to dataframe
    data['buy_long'] = (data['aaron_osc'] > 0) & (data['aaron_osc'].shift(1) <= 0)
    data['sell_short'] = (data['aaron_osc'] < 0) & (data['aaron_osc'].shift(1) >= 0)


def plot_with_aroon_indicator(data):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 8), sharex=True)
    
    ax1.plot(data.index, data['close'], label='Close Price', color='blue')
    ax1.plot(data.index['buy_long'], data.loc['buy_long']['close'], '^', markersize=10, color='g', label='Buy Signal')
    ax1.plot(data.index['sell_short'], data.loc['sell_short']['close'], 'v', markersize=10, color='r', label='Sell Signal')
    ax1.set_ylabel("Close Price")
    ax1.legend()
    
    ax2.plot(data.index, label='Aroon Oscillator', color='purple')
    ax2.axhline(0, linestyle='--', color='black')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Aroon Oscillator")
    ax2.legend()
    
    for signal_date in data.index['buy_long']:
        ax1.axvline(signal_date, color='g', linestyle='--', alpha=0.5)
        ax2.axvline(signal_date, color='g', linestyle='--', alpha=0.5)
    
    for signal_date in data.index['sell_short']:
        ax1.axvline(signal_date, color='r', linestyle='--', alpha=0.5)
        ax2.axvline(signal_date, color='r', linestyle='--', alpha=0.5)
    
    plt.show()
