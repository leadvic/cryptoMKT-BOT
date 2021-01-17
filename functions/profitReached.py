def profitReached(client,cryptoCurrency,initialInvestemnt,profitExpected,CLP_available,CRY_available):
    import pandas as pd

    CRY_bookBuy=pd.DataFrame(client.get_book(market=cryptoCurrency+'CLP', side="buy", limit=50)["data"],dtype=float)
    bigBuyers=CRY_bookBuy[CRY_bookBuy["amount"]>CRY_available]
    mostExpensiveBuyer=bigBuyers.iloc[0,0]

    if CLP_available+CRY_available*mostExpensiveBuyer>=initialInvestemnt*(1+profitExpected):
        return True
    else:
        return False
