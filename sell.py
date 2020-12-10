def sell(client):
    
    EOS_executed_orders=pd.DataFrame(client.get_executed_orders(market="EOSCLP",limit=50)["data"])

    EOS_book_buy=pd.DataFrame(client.get_book(market="EOSCLP", side="buy", limit=30)["data"],dtype=float)
    EOS_book_sell=pd.DataFrame(client.get_book(market="EOSCLP", side="sell", limit=30)["data"],dtype=float)
    bigSellers=EOS_book_sell[EOS_book_buy["amount"]>EOS_book_sell.mean()["amount"]]
    mostExpensiveBuyer=EOS_book_buy["price"][0]

    EOS_historical_orders=pd.DataFrame(list((EOS_executed_orders["id"][i],EOS_executed_orders["side"][i],EOS_executed_orders["fills"][i][0]["price"],EOS_executed_orders["fills"][i][0]["amount"],EOS_executed_orders["fills"][i][0]["fee"],EOS_executed_orders["fills"][i][0]["date"]) for i in range (50)),columns=["id","side","price","amount","fee","date"],dtype=float)
    EOS_sorted_buy_history=EOS_historical_orders.loc[EOS_historical_orders["side"]=="buy"].sort_values(by="price", ascending=False)
    worstPurchase=EOS_sorted_buy_history["price"][EOS_sorted_buy_history.index[i]]

    firstBigSellerPrice=bigSellers["price"][bigSellers.index[0]]
    lastPrice=firstBigSellerPrice-0.5

    if lastPrice>mostExpensiveBuyer and lastPrice>worstPurchase+50:
        try:
            client.cancel_order(id=lastOrder["id"])
            print("Selling at: ----.-",end="\r")
        except:
            EOS_available=float(client.get_balance()[11]["available"])

        lastOrder=client.create_order(market="EOSCLP", type="limit", amount=1, price=lastPrice, side="sell")
        print("Selling at:",lastPrice,end="\r")

        time.sleep(6)
    else:
        print("Not Selling",end="\r")
