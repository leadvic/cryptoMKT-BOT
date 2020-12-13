def buy(client,cryptoCurrency):
    import pandas as pd
    import time

    CRY_bookBuy=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP', side="buy", limit=50)["data"],dtype=float)
    CRY_bookSell=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP', side="sell", limit=50)["data"],dtype=float)
    bigBuyers=CRY_bookBuy[CRY_bookBuy["amount"]>CRY_bookBuy.mean()["amount"]]
    cheapestSeller=CRY_bookSell["price"][0]


    firstBigBuyerPrice=bigBuyers["price"][bigBuyers.index[0]]
    lastPrice=firstBigBuyerPrice+0.5

    if (lastPrice<cheapestSeller):
        try:
            client.cancel_order(id=lastOrder["id"])
            print("Buying at: ----.-",end="\r")
        except:
            CLP_available=float(client.get_balance()[3]["available"])
        lastOrder=client.create_order(market=cryptoCurrency+'CLP', type="limit", amount=str(CLP_available/lastPrice), price=lastPrice, side="buy")
        print("Buying at:",lastPrice,end="\r")

        time.sleep(5)

    return None
