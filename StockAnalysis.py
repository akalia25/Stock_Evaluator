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
    return stock_appraisal


def main():
    stocks = user_input().split(',')
    stocks = cleanse_stocks(stocks)
    stocks_df = historical_data(stocks)
    stock_appraisal_z_value(stocks_df)


if __name__ == '__main__':
    main()
