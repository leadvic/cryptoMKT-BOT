def main(api_key,api_secret,cryptoCurrency,initialInvestemnt,profitExpected,emailAddress,startTime):
    from cryptomarket.exchange.client import Client
    from functions.marketAnalysis import marketAnalysis
    from functions.sellEverything import sellEverything
    from functions.profitReached import profitReached
    from functions.withdrawItAll import withdrawItAll
    from functions.writeReport import writeReport
    from functions.recording import recording
    from functions.sendMail import sendMail
    from functions.sell import sell
    from functions.buy import buy
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
        doBuy,doSell,minCLP,minCRY=marketAnalysis(client,cryptoCurrency,initialInvestemnt,CLP_available,CRY_available)

        # Buy, Sell or Wait
        if CLP_available>=minCLP and doBuy:
            #Buy CryptoCurrency
            print("Buying")
            orderPlaced=buy(client,cryptoCurrency,minCLP)

        elif CRY_available>=minCRY and doSell:
            #Sell CryptoCurrency
            print("Selling")
            orderPlaced=sell(client,cryptoCurrency,minCRY)

        else:
            # Wait for a while
            print("Waiting")
            time.sleep(3600/2)
            orderPlaced=None

        # Record of Executed Orders
        print("Recording")
        recording(client,cryptoCurrency,orderPlaced)

        # End the program if the expected benefits were obtained
        if profitReached(client,cryptoCurrency,initialInvestemnt,profitExpected,CLP_available,CRY_available):
            print("The expected benefits were obtained")
            amountCLP=sellEverything(client,cryptoCurrency)
            print("Withdrawing all the money")
            withdrawItAll(client,amountCLP)
            print("Ending Program")
            return None

        # If the expected benefits were not obtained, a report is sent daily
        elif time.time()-reportTime>(3600*24):
            print("Reporting")
            writeReport(client,cryptoCurrency,initialInvestemnt,startTime)
            print("Sending Report")
            sendMail(emailAddress)
            reportTime=time.time()
