def main(api_key,api_secret,cryptoCurrency,minCLP):
    from cryptomarket.exchange.client import Client
    from marketAnalysis import marketAnalysis
    from writeReport import writeReport
    from recording import recording
    from sell import sell
    from buy import buy
    import time

    # Start counting the program execution time
    startTime=time.time()
    reportTime=startTime

    # An empty list for the record of executed orders
    records=[{'Date':'2020-01-01','Side':'sell','Amount':1,'Price':1000,'Total':1000,'Fees':0.1},{'Date':'2020-01-01','Side':'buy','Amount':1,'Price':1000,'Total':1000,'Fees':0.1}]

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

        # Buy, Sell, Exit, Wait
        if CLP_available>=minCLP and doBuy:
            #Buy CryptoCurrency
            print("Buying")
            orderPlaced=buy(client,cryptoCurrency,minCLP)

            if not orderPlaced:
                pass
            else:
                # Record of Executed Orders
                print("Recording")
                records=recording(client,cryptoCurrency,records,orderPlaced)

        elif CRY_available>=minCRY and doSell:
            #Sell CryptoCurrency
            print("Selling")
            orderPlaced=sell(client,cryptoCurrency,minCRY)

            if not orderPlaced:
                pass
            else:
                # Record of Executed Orders
                print("Recording")
                records=recording(client,cryptoCurrency,records,orderPlaced)

        elif CLP_available<minCLP and CRY_available<minCRY:
            #Exit Program
            print("Exiting")
            raise SyntaxError('MUHAHA THIS IS AN ERROR')
            return None

        else: #doBuy & doSell
            #Wait for a while
            print("Waiting")
            time.sleep(3600)

        # Once a week
        if time.time()-reportTime>604800:
            print("Reporting")
            writeReport(client,cryptoCurrency,startTime,records)
            reportTime=time.time()
