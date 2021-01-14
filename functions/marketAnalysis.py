def marketAnalysis(client,cryptoCurrency):
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    import statistics

    lastPrice=float(client.get_ticker(market=cryptoCurrency+'CLP')["data"][0]["last_price"])

    #
    longTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=10080)["bid"]
##    mediumTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=1440)["bid"]
##    shortTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=60)["bid"]
    ultraShortTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=15)["bid"]

    #
    dataLong=pd.DataFrame(longTermPrices).sort_values(by='candle_date', ascending=True)
##    dataMedium=pd.DataFrame(mediumTermPrices).sort_values(by='candle_date', ascending=True)
##    dataShort=pd.DataFrame(shortTermPrices).sort_values(by='candle_date', ascending=True)
    dataUltraShort=pd.DataFrame(ultraShortTermPrices).sort_values(by='candle_date', ascending=True)
    dataUltraShort.at[-1,:]=lastPrice

    #
    CRY_meanValue=statistics.mean(dataLong['close_price'].values.astype(np.float))
    CRY_standardDeviation=statistics.stdev(dataLong['close_price'].values.astype(np.float))

    #
##    dataMedium['candle_date']=[i for i in range(1,len(dataMedium['candle_date'])+1)]
##    y=dataMedium['close_price'].astype(np.float)
##    x=sm.add_constant(dataMedium['candle_date'])
##    model=sm.OLS(y,x).fit()
##    mediumIntercept=model.params[0]
##    mediumSlope=model.params[1]

    #
##    dataShort['candle_date']=[i for i in range(1,len(dataShort['candle_date'])+1)]
##    y=dataShort['close_price'].astype(np.float)
##    x=sm.add_constant(dataShort['candle_date'])
##    model=sm.OLS(y,x).fit()
##    shortIntercept=model.params[0]
##    shortSlope=model.params[1]

    #
    dataUltraShort['candle_date']=[i for i in range(1,len(dataUltraShort['candle_date'])+1)]
    y=dataUltraShort['close_price'].astype(np.float)
    x=sm.add_constant(dataUltraShort['candle_date'])
    model=sm.OLS(y,x).fit()
    ultraShortIntercept=model.params[0]
    ultraShortSlope=model.params[1]

    #
    if ultraShortSlope<0 or lastPrice<CRY_meanValue-CRY_standardDeviation*0.6:
        doBuy=True
        doSell=False
    elif ultraShortSlope>0 or lastPrice>CRY_meanValue+CRY_standardDeviation*0.6:
        doBuy=False
        doSell=True
    else:
        doBuy=False
        doSell=False

    return doBuy,doSell
