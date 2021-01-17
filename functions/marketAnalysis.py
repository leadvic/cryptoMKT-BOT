def marketAnalysis(client,cryptoCurrency,initialInvestemnt,CLP_available,CRY_available):
    import statsmodels.api as sm
    from data import infoCRY
    import pandas as pd
    import numpy as np
    import statistics

    # Last Price
    lastPrice=float(client.get_ticker(market=cryptoCurrency+'CLP')["data"][0]["last_price"])

    # Get prices in the long, medium,short and ultra-short term
    longTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=10080)["bid"]
##    mediumTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=1440)["bid"]
##    shortTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=60)["bid"]
    ultraShortTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=15)["bid"]

    # Prices are stored as DataFame from the oldest to the newest
    dataLong=pd.DataFrame(longTermPrices).sort_values(by='candle_date', ascending=True)
##    dataMedium=pd.DataFrame(mediumTermPrices).sort_values(by='candle_date', ascending=True)
##    dataShort=pd.DataFrame(shortTermPrices).sort_values(by='candle_date', ascending=True)
    dataUltraShort=pd.DataFrame(ultraShortTermPrices).sort_values(by='candle_date', ascending=True)
    dataUltraShort.at[-1,:]=lastPrice

    # Calculation of the long-term mean and standard deviation
    CRY_meanValue=statistics.mean(dataLong['close_price'].values.astype(np.float))
    CRY_standardDeviation=statistics.stdev(dataLong['close_price'].values.astype(np.float))

    # Calculation of the medium-term least squares intercept ans slope
##    dataMedium['candle_date']=[i for i in range(1,len(dataMedium['candle_date'])+1)]
##    y=dataMedium['close_price'].astype(np.float)
##    x=sm.add_constant(dataMedium['candle_date'])
##    model=sm.OLS(y,x).fit()
##    mediumIntercept=model.params[0]
##    mediumSlope=model.params[1]

    # Calculation of the short-term least squares intercept ans slope
##    dataShort['candle_date']=[i for i in range(1,len(dataShort['candle_date'])+1)]
##    y=dataShort['close_price'].astype(np.float)
##    x=sm.add_constant(dataShort['candle_date'])
##    model=sm.OLS(y,x).fit()
##    shortIntercept=model.params[0]
##    shortSlope=model.params[1]

    # Calculation of the ultra-short-term least squares intercept ans slope
    dataUltraShort['candle_date']=[i for i in range(1,len(dataUltraShort['candle_date'])+1)]
    y=dataUltraShort['close_price'].astype(np.float)
    x=sm.add_constant(dataUltraShort['candle_date'])
    model=sm.OLS(y,x).fit()
    ultraShortIntercept=model.params[0]
    ultraShortSlope=model.params[1]

    # Decision to buy or sell
    if ultraShortSlope<0 or lastPrice<CRY_meanValue-CRY_standardDeviation*0.6:
        doBuy=True
        doSell=False
    elif ultraShortSlope>0 or lastPrice>CRY_meanValue+CRY_standardDeviation*0.6:
        doBuy=False
        doSell=True
    else:
        doBuy=False
        doSell=False

    # How much should be bought or sold
    if CLP_available>=initialInvestemnt*0.2:
        if initialInvestemnt*0.01>=infoCRY.minAmountCRY[cryptoCurrency]:
            minCLP=initialInvestemnt*0.01
        elif initialInvestemnt*0.1>=infoCRY.minAmountCRY[cryptoCurrency]:
            minCLP=initialInvestemnt*0.1
        else:
            print("Insufficient Funds Available")

    elif CLP_available>=infoCRY.minAmountCRY[cryptoCurrency]*10:
        minCLP=CLP_available*0.1
    else:
        minCLP=CLP_available

    minCRY=minCLP/lastPrice

    return doBuy,doSell,minCLP,minCRY
