def recording(client,cryptoCurrency,orderPlaced):
    import pandas as pd

    if not orderPlaced:
        pass
    else:
        lastExecuted=client.get_executed_orders(market=cryptoCurrency+'CLP')[0]
        if orderPlaced["id"]==lastExecuted["id"]:
            if lastExecuted["side"]=="sell":
                record=pd.DataFrame([{'Date':lastExecuted["updated_at"],'Side':lastExecuted["side"],'Amount':float(lastExecuted["amount"]["executed"]),'Price':float(lastExecuted["price"]),'Total':float(lastExecuted["fills"][0]["amount"]),'Fees':float(lastExecuted["fee"])}])
            else:   # lastExecuted["side"]=="buy"
                record=pd.DataFrame([{'Date':lastExecuted["updated_at"],'Side':lastExecuted["side"],'Amount':float(lastExecuted["amount"]["executed"]),'Price':float(lastExecuted["price"]),'Total':float(lastExecuted["amount"]["executed"])*float(lastExecuted["price"]),'Fees':float(lastExecuted["fee"])*float(lastExecuted["price"])}])

            record.to_csv('./reports/records.csv',sep=',',header=None,mode='a',index=False)

    return None
