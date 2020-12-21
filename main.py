def main(api_key,api_secret,cryptoCurrency,minCLP,startTime):
    from cryptomarket.exchange.client import Client
    from marketAnalysis import marketAnalysis
    from writeReport import writeReport
    from recording import recording
    from sell import sell
    from buy import buy
    import time

    # Start counting the program execution time
    reportTime=startTime

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
        print("Analyzing")
        doBuy,doSell,CRY_mean,CRY_stDev=marketAnalysis(client,cryptoCurrency)

        # Minimum amount of CryptoCurrency needed to trade
        minCRY=minCLP/float(client.get_ticker(market=cryptoCurrency+'CLP')[0]["last_price"])

        # Buy, Sell, Exit, Wait
        if CLP_available>=minCLP and doBuy:
            #Buy CryptoCurrency
            print("Buying")
            orderPlaced=buy(client,cryptoCurrency,minCLP)

            # Record of Executed Orders
            print("Recording")
            recording(client,cryptoCurrency,orderPlaced)

        elif CRY_available>=minCRY and doSell:
            #Sell CryptoCurrency
            print("Selling")
            orderPlaced=sell(client,cryptoCurrency,minCRY)

            # Record of Executed Orders
            print("Recording")
            recording(client,cryptoCurrency,orderPlaced)

        elif CLP_available<minCLP and CRY_available<minCRY:
            #Exit Program
            print("Exiting")
            raise SyntaxError('MUHAHA THIS IS AN ERROR')
            return None

        else: #doBuy & doSell
            #Wait for a while
            print("Waiting")
            time.sleep(3600/2)

        # Once a week
        if time.time()-reportTime>(3600*6):
            print("Reporting")
            writeReport(client,cryptoCurrency,startTime)
            reportTime=time.time()
