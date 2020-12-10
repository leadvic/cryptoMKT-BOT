def buy(client):
    
    EOS_book_buy=pd.DataFrame(client.get_book(market="EOSCLP", side="buy", limit=50)["data"],dtype=float)
    EOS_book_sell=pd.DataFrame(client.get_book(market="EOSCLP", side="sell", limit=50)["data"],dtype=float)
    bigBuyers=EOS_book_buy[EOS_book_buy["amount"]>EOS_book_buy.mean()["amount"]]
    cheapestSeller=EOS_book_sell["price"][0]


    firstBigBuyerPrice=bigBuyers["price"][bigBuyers.index[0]]
    lastPrice=firstBigBuyerPrice+0.5

    if (lastPrice<cheapestSeller):
        try:
            client.cancel_order(id=lastOrder["id"])
            print("Buying at: ----.-",end="\r")
        except:
            CLP_available=float(client.get_balance()[3]["available"])
        lastOrder=client.create_order(market="EOSCLP", type="limit", amount=str(CLP_available/lastPrice), price=lastPrice, side="buy")
        print("Buying at:",lastPrice,end="\r")

        time.sleep(5)
