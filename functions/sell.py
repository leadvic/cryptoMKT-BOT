def sell(client,cryptoCurrency,minCRY):
    from data import infoCRY
    import pandas as pd
    import time

    startSelling=time.time()

    while True:

        CRY_bookBuy=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP',side="buy",limit=30)["data"],dtype=float)
        CRY_bookSell=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP',side="sell",limit=30)["data"],dtype=float)
        bigSellers=CRY_bookSell[CRY_bookSell["amount"]>CRY_bookSell.mean()["amount"]]
        mostExpensiveBuyer=CRY_bookBuy["price"][0]

        firstBigSellerPrice=bigSellers["price"][bigSellers.index[0]]
        lastPrice=firstBigSellerPrice-infoCRY.minStepCRY[cryptoCurrency]

        if lastPrice>mostExpensiveBuyer:

            lastOrder=client.create_order(market=cryptoCurrency+'CLP', type="limit", amount=minCRY, price=lastPrice, side="sell")
            print("Selling at:",lastPrice,end="\r")
            time.sleep(8)

            if float(client.get_order_status(id=lastOrder["id"])["amount"]["executed"])==0:
                client.cancel_order(id=lastOrder["id"])
                print("Selling at: ----.-",end="\r")
            else:
                try:
                    client.cancel_order(id=lastOrder["id"])
                except:
                    pass
                finally:
                    print("")
                    return lastOrder

        if time.time()-startSelling>(60*5):
            print("")
            return None
