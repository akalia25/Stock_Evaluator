#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 02:20:38 2020

@author: adityakalia
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as matdates
from scipy.stats import norm
import numpy as np


def user_input():
    """
    This function takes the user's input of what stocks they would like to
    anayze and stores .
    """
    while True:
        try:
            stocks = input("Please enter the stocks you would " +
                           "like to analyze seperated by commas : ")
            if len(stocks) > 0:
                break
        except ValueError:
            pass
        print("Incorrect input please enter your stocks")

    return stocks


def cleanse_stocks(val):
    """
    This function parses the user's input and ensures there are no whitespaces.
    """
    val = [x.strip(' ') for x in val]
    return val


def historical_data(stocks):
    """
    This function uses the Yfinance API and collects the historical data
    of the user inputted and places the data in a dataframe (DF).
    """
    stocks_df = pd.DataFrame()
    for x in stocks:
        try:
            stock = yf.Ticker(x)
            tempdf = stock.history(period='3mo')
            tempdf.loc[:, 'StockName'] = x
            stocks_df = stocks_df.append(tempdf, sort='False')
            stocks_df.loc[:, 'ROI'] = stocks_df['Close'].pct_change()
        except ValueError:
            print("Incorrect stock entered " + x)
            pass
    return stocks_df


def zvalue(series):
    """
    This function takes a series as input and calculates the standard
    deviation, mean, and uses the series last stock price as the x value
    using these values it calculates the z value
    """
    meanVal = series.mean()
    stdVal = series.std()
    mu = series[-1]
    z1 = (mu - meanVal) / stdVal
    return z1


def stock_appraisal_z_value(stocks_df):
    """
    The purpose of this function is to consider the z-value of each stocks
    closing prices and determine what the optimal position for that stock
    is (Hold, Buy, Sell)
    Parameters
    ----------
    stocks_df : Pandas DataFrame
    Contains the pandas DataFrame with all the stocks entered by the user and
    their trading history (close price, volume, date, etc)
    Returns
    -------
    stock_appraisal_z_value_df : Pandas DataFrame
    Uses the stock as the index and the other columns represent the optimal
    position of the stock
    """
    stock_zval = {}
    stock_appraisal = {}
    for stock in stocks_df.StockName.unique():
        series = stocks_df['Close'][(stocks_df.StockName == stock)][-30:]
        z1 = zvalue(series)
        stock_zval[stock] = z1
    for key, value in stock_zval.items():
        if 1 > value > -1:
            stock_appraisal[key] = 'HOLD'
        if value > 1:
            stock_appraisal[key] = 'SELL'
        if value < -1:
            stock_appraisal[key] = 'BUY'
    print(stock_appraisal)
    stock_appraisal_z_value_df = pd.DataFrame(list(stock_appraisal.values()),
                                  columns=['z_value_appraisal'],
                                  index=stock_appraisal.keys())
    return stock_appraisal_z_value_df


def stock_appraisal_moving_average(stocks_df):
    """

    The purpose of this function is to use the stocks closing price to create
    its moving average, and trigger the optimal postion of the stock based on
    how the stocks moving average is progressing

    Parameters
    ----------
    stocks_df : Pandas DataFrame
    Contains the pandas DataFrame with all the stocks entered by the user and
    their trading history (close price, volume, date, etc)
    Returns
    -------
    stock_appraisal_moving_average : Pandas DataFrame
    """
    stock_appraisal = {}
    for stock in stocks_df.StockName.unique():
        df1 = stocks_df[['Close',
                         'StockName']][(stocks_df.StockName == stock)][-30:]
        data = stocks_df['Close'][(stocks_df.StockName == stock)][-30:]
        for moving_average_period in (5, 15, 30):
            moving_average = data.rolling(window=moving_average_period).mean()
            df1.loc[:, 'SMA ' + str(stock) + ' ' + str(
                    moving_average_period)] = moving_average.values
        final_series = df1.iloc[-1, [-1, -2, -3]] - df1.iloc[-1, 0]
        if final_series[0] > 0 and final_series[1] > 0 and final_series[2] > 0:
            stock_appraisal[stock] = 'BUY'
        elif final_series[0] < 0 and final_series[1] < 0 and final_series[2] < 0:
            stock_appraisal[stock] = 'SELL'
        else:
            stock_appraisal[stock] = 'HOLD'
    print(stock_appraisal)
    stock_appraisal_moving_average_df = pd.DataFrame(list(stock_appraisal.values()),
                                  columns=['moving_average_appraisal'],
                                  index=stock_appraisal.keys())
    return stock_appraisal_moving_average_df


def main():
    stocks = user_input().split(',')
    stocks = cleanse_stocks(stocks)
    stocks_df = historical_data(stocks)
    stock_appraisal_z_value(stocks_df)
    stock_appraisal_moving_average(stocks_df)


if __name__ == '__main__':
    main()
