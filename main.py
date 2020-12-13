def main(api_key,api_secret,cryptoCurrency,minCLP):
    from cryptomarket.exchange.client import Client
    from marketAnalysis import marketAnalysis
    from sell import sell
    from buy import buy
    import time

    # Start counting the program execution time
    startTime=time.time()

    # Connection as the client
    print("Connecting")
    client=Client(api_key,api_secret)

    while True:

        # CLP available
        CLP_available=float(client.get_balance()[3]["available"])

        # CryptoCurrency (CRY) available
        for currency in client.get_balance()["data"]:
            if currency["wallet"]==cryptoCurrency:
                CRY_available=float(currency["available"])
                break

        # Market Analysis
        print("Analising")
        doBuy,doSell,CRY_mean,CRY_stDev=marketAnalysis(client,cryptoCurrency)

        # Minimum amount of CryptoCurrency needed to trade
        minCRY=minCLP/float(client.get_ticker(market=cryptoCurrency+'CLP')[0]["last_price"])

        # Buy, Sell, Pass, Exit
        if CLP_available>=minCLP and doBuy:
            #Buy CryptoCurrency
            print("Buying")
            buy(client,cryptoCurrency,minCLP)

        elif CRY_available>=minCRY and doSell:
            #Sell CryptoCurrency
            print("Selling")
            sell(client,cryptoCurrency,minCRY)

        elif CLP_available<minCLP and CRY_available<minCRY:
            #Exit Program
            print("Exiting")
            raise SyntaxError('MUHAHA THIS IS AN ERROR')
            return None

        else: #doBuy & doSell
            #Wait for a while
            print("Waiting")
            time.sleep(3600)
