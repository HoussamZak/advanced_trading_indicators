import numpy as np 
import pandas as pdf


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

def disp_idx(data, lookback):
    ma = data.rolling(lookback).mean()
    return ((data - ma)/ma) * 100

def implement_disp_strat(prices, disp):
    buy_price = []
    sell_price = []
    disp_signal = []
    signal = 0
    for i in range(len(prices)):
        if disp[i - 4] < 0 and disp[i - 3] < 0 and disp[i - 2] < 0 and disp[i - 1] < 0 and disp[i] > 0 :
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1 
                disp_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                disp_signal.append(0)
        elif disp[i-4] > 0 and disp[i-3]>0 and disp[i-2]>0 and disp[i-1]>0 and disp[i] < 0:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                disp_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                disp_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            disp_signal.append(0)

def disparity_idx_indc(data):
        buy_price, sell_price, _ = implement_disp_strat(data['close'], data['disp_14'])
        return buy_price, sell_price,data 
    