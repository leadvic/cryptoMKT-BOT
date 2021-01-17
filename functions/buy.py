def buy(client,cryptoCurrency,minCLP):
    from data import infoCRY
    import pandas as pd
    import time

    startBuying=time.time()

    while True:

        CRY_bookBuy=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP', side="buy", limit=50)["data"],dtype=float)
        CRY_bookSell=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP', side="sell", limit=50)["data"],dtype=float)
        bigBuyers=CRY_bookBuy[CRY_bookBuy["amount"]>CRY_bookBuy.mean()["amount"]]
        cheapestSeller=CRY_bookSell["price"][0]

        firstBigBuyerPrice=bigBuyers["price"][bigBuyers.index[0]]
        lastPrice=firstBigBuyerPrice+infoCRY.minStepCRY[cryptoCurrency]

        if lastPrice<cheapestSeller:

            lastOrder=client.create_order(market=cryptoCurrency+'CLP', type="limit", amount=str(minCLP/lastPrice), price=lastPrice, side="buy")
            print("Buying at:",lastPrice,end="\r")
            time.sleep(8)

            try:
                client.cancel_order(id=lastOrder["id"])
                print("Buying at: ----.-",end="\r")
            except:
                print("")
                return lastOrder

        if time.time()-startBuying>(60*5):
            print("")
            return None
