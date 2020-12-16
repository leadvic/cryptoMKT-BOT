def sell(client,cryptoCurrency,minCRY):
    import pandas as pd
    import time

    startSelling=time.time()
    i=0

    while True:

        CRY_executedOrders=pd.DataFrame(client.get_executed_orders(market=cryptoCurrency+'CLP',limit=50)["data"])

        CRY_bookBuy=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP',side="buy",limit=30)["data"],dtype=float)
        CRY_bookSell=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP',side="sell",limit=30)["data"],dtype=float)
        bigSellers=CRY_bookSell[CRY_bookSell["amount"]>CRY_bookSell.mean()["amount"]]
        mostExpensiveBuyer=CRY_bookBuy["price"][0]

        CRY_historicalOrders=pd.DataFrame(list((CRY_executedOrders["id"][i],CRY_executedOrders["side"][i],CRY_executedOrders["fills"][i][0]["price"],CRY_executedOrders["fills"][i][0]["amount"],CRY_executedOrders["fills"][i][0]["fee"],CRY_executedOrders["fills"][i][0]["date"]) for i in range (50)),columns=["id","side","price","amount","fee","date"],dtype=float)
        CRY_sortedBuyHistory=CRY_historicalOrders.loc[CRY_historicalOrders["side"]=="buy"].sort_values(by="price", ascending=False)
        worstPurchase=CRY_sortedBuyHistory["price"][CRY_sortedBuyHistory.index[i]]

        firstBigSellerPrice=bigSellers["price"][bigSellers.index[0]]
        lastPrice=firstBigSellerPrice-0.5

        if lastPrice>mostExpensiveBuyer and lastPrice>worstPurchase+50:

            lastOrder=client.create_order(market=cryptoCurrency+'CLP', type="limit", amount=minCRY, price=lastPrice, side="sell")
            print("Selling at:",lastPrice,end="\r")
            time.sleep(5)

            try:
                client.cancel_order(id=lastOrder["id"])
                print("Selling at: ----.-",end="\r")
            except:
                print("")
                return lastOrder
        else:
            print("Not Selling",end="\r")

        if time.time()-startSelling>(60*5):
            print("")
            return None
