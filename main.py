def main(api_key,api_secret,cryptoCurrency):
    from cryptomarket.exchange.client import Client
    from time import sleep
    from sell import sell
    from buy import buy
    #cryptoCurrency+='CLP'

    # Connection as the client
    client = Client(api_key,api_secret)

    while True:

        # CLP available
        CLP_available=float(client.get_balance()[3]["available"])

        # CryptoCurrency (CRY) available
        for currency in client.get_balance()["data"]:
            if currency["wallet"]==cryptoCurrency:
                CRY_available=float(currency["available"])
                break

        # Market Analysis
        print("analising")
        buy=1
        sell=0



        # Buy, Sell, Pass, Exit
        if CLP_available>=1000 and buy==1:
            #Buy CryptoCurrency
            print("Buying")
            buy(client)

        elif CRY_available>=1 and sell==1:
            #Sell CryptoCurrency
            print("Selling")
            sell(client)

        elif CLP_available<1000 and CRY_available<1:
            #Exit Program
            print("Exiting")
            raise SyntaxError('MUHAHA THIS IS A ERROR')
            return None

        else: #buy==0 & sell==0
            #Wait for a while
            print("Waiting")
            sleep(3600)
