def marketAnalysis(client,cryptoCurrency):
    import statsmodels.api as sm
    import pandas as pd
    import numpy as np
    import statistics

    #
    longTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=10080)["bid"]
    mediumTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=1440)["bid"]
    shortTermPrices=client.get_prices(market=cryptoCurrency+'CLP',timeframe=60)["bid"]

    #
    dataLong=pd.DataFrame(longTermPrices)
    dataMedium=pd.DataFrame(mediumTermPrices)
    dataShort=pd.DataFrame(shortTermPrices)

    #
    CRY_meanValue=statistics.mean(dataLong['close_price'].values.astype(np.float))
    CRY_standardDeviation=statistics.stdev(dataLong['close_price'].values.astype(np.float))

    #
    dataMedium['candle_date']=[i for i in range(1,len(dataMedium['candle_date'])+1)]
    y=dataMedium['close_price'].astype(np.float)
    x=sm.add_constant(dataMedium['candle_date'])
    model=sm.OLS(y,x).fit()
    mediumIntercept=model.params[0]
    mediumSlope=model.params[1]

    #
    dataShort['candle_date']=[i for i in range(1,len(dataShort['candle_date'])+1)]
    y=dataShort['close_price'].astype(np.float)
    x=sm.add_constant(dataShort['candle_date'])
    model=sm.OLS(y,x).fit()
    shortIntercept=model.params[0]
    shortSlope=model.params[1]

    #
    if mediumSlope>0 and shortSlope<0:
        doBuy=True
        doSell=False
    elif mediumSlope<0 and shortSlope>0:
        doBuy=False
        doSell=True
    else:
        doBuy=False
        doSell=False

    return doBuy,doSell,CRY_meanValue,CRY_standardDeviation
