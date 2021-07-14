# ========= PLEASE READ CAREFULLY ==========
# Code credits to Algovibes
# Youtube Channel: 
# https://www.youtube.com/channel/UC87aeHqMrlR6ED0w2SVi5nw
# How to build a RSI Trading Strategy and Backtest over 500 stocks in Python [70% Winning Rate]
# https://www.youtube.com/watch?v=pB8eJwg7LJU
# Disclaimer: This code is no Investment advice and is only for educational and entertainment purposes.
# ===========================================
# ===========================================

# pandas for data handling
import pandas as pd

# yfinance to get stock prices on the internet
import yfinance as yf

# matplotlib for some visualizations
import matplotlib.pyplot as plt

# 'OPTIONAL' turning off some warnings
pd.options.mode.chained_assignment = None

# read_html function from pandas to get ticket symbols of S&P500 companies
tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]


# transform symbol column to list  
tickers = tickers.Symbol.to_list()

# replace invalid data containing dot, replacing it for dash
tickers = [i.replace('.', '-') for i in tickers]

# get rid of ticket symbol that causing errors by their index
tickers.pop(474)
tickers.pop(489)

# function to calculate the RSI for particular assets
def RSIcalc(asset):
    # define data-frame function using yfinance library 
    # to a download function for the asset 'ticker symbol' and the start date
    df = yf.download(asset, start='2011-01-01')
    # creating a column 200-day moving average
    df['MA200'] = df['Adj Close'].rolling(window=200).mean()
    # Calculate the relative returns
    # getting daily|relative returns
    df['price change'] = df['Adj Close'].pct_change()
    # defining up moves column
    df['Upmove'] = df['price change'].apply(lambda x: x if x > 0 else 0)
    # defining the down moves column
    df['Downmove'] = df['price change'].apply(lambda x: abs(x) if x < 0 else 0)
    # average up moves
    df['avg Up'] = df['Upmove'].ewm(span=19).mean()
    # average down moves
    df['avg Down'] = df['Downmove'].ewm(span=19).mean()
    # reasigning NaN values
    df = df.dropna()
    # Calculate RS
    df['RS'] = df['avg Up']/df['avg Down']
    # defining RSI value
    df['RSI'] = df['RS'].apply(lambda x: 100-(100/(x+1)))
    # defining buying signals 
    df.loc[(df['Adj Close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
    # defining non buying signals
    df.loc[(df['Adj Close'] < df['MA200']) | (df['RSI'] > 30), 'Buy'] = 'No'
    return df
# print(RSIcalc(tickers[0]))

# creating a new function to get signals from buying & selling dates
def getSignals(df):
    Buying_dates = []
    Selling_dates = []
    # looping through rows
    for i in range(len(df) - 11):
        # condition for date's buying signal in the loop
        if "Yes" in df['Buy'].iloc[i]:
            # append row names to my buying dates
            Buying_dates.append(df.iloc[i+1].name)
            # define selling date 
            for j in range(1, 11):
                # when RSI not exceed 40 over next 10 days
                if df['RSI'].iloc[1 + j] > 40:
                    # appending timestamp's selling dates
                    Selling_dates.append(df.iloc[i+j+1].name)
                    # exceeding 40 we exit the trade
                    break
                # selling after 10 trading days
                elif j == 10:
                    # appending selling dates to the never exceeding 40 loop results
                    Selling_dates.append(df.iloc[i+j+1].name)
    # returning buying & sellling dates        
    return Buying_dates, Selling_dates

# testing functions
frame = RSIcalc(tickers[0])
# getting timestamp signals
buy, sell = getSignals(frame)
# print(buy)

# visualize the function ploting it
plt.figure(figsize=(12, 5))
plt.scatter(frame.loc[buy].index, frame.loc[buy]['Adj Close'], marker= '^', c='g')
plt.plot(frame['Adj Close'], alpha=0.7)

# calculate profits using our frame
Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
# print(Profits)

# calculate the winning rate
# get win value
wins = [i for i in Profits if i > 0]
# getting a winning rate
len(wins)/len(Profits)
# trade's winning moments in +10 years
len(Profits)

# create empty list to store all those signals & profits 
matrixSignals = []
matrixProfits = []

# loop for getting profits for all those assets
for i in range(len(tickers)):
    # create frame iterating trough tickers symbols
    frame = RSIcalc(tickers[1])
    # defining buying & selling signals and taking the frame
    buy, sell = getSignals(frame)
    # calculating the profits as above
    Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
    # appending the buy to matrix-signal
    matrixSignals.append(buy)
    # appending the profits to matrix-profits
    matrixProfits.append(Profits)
    # print(matrixSignals)
    # print(matrixProfits)
    len(matrixProfits)
    
    # create an empty list for all profits
    allProfit = []
    
    # loop through metric's profits
    for i in matrixProfits:
        # in matrixProfits is a nested array to loop through
        # with the actual profits
        for e in i:
            # append those to the all profit list
            allProfit.append(e)            
    # print(allProfit)
    
    # calculate our wins in allprofits
    wins = [i for i in allProfit if i > 0]
    
    # getting the overall wing rate
    len(wins)/len(allProfit)
    
    # plotting overall results
    plt.hist(allProfit, bins=100)
    plt.show()
    
    # get the signals on 2021
    for i in matrixSignals:
        for e in i:
            if e.year == 2021:
                print(e)