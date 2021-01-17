def sellEverything(client,cryptoCurrency):
    import pandas as pd
    import time

    while True:

        for currency in client.get_balance()["data"]:
            if currency["wallet"]==cryptoCurrency:
                CRY_available=float(currency["available"])
                break

        CRY_bookBuy=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP', side="buy", limit=50)["data"],dtype=float)
        bigBuyers=CRY_bookBuy[CRY_bookBuy["amount"]>CRY_available]
        mostExpensiveBuyer=bigBuyers.iloc[0,0]

        theLastOrder=client.create_order(market=cryptoCurrency+'CLP', type="limit", amount=CRY_available, price=mostExpensiveBuyer, side="sell")
        time.sleep(10)

        if client.get_order_status(id=str(theLastOrder["id"]))["status"]=='filled':
            return float(client.get_balance()[3]["available"])
        else:
            client.cancel_order(id=theLastOrder["id"])
