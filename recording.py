def recording(client,cryptoCurrency,records,orderPlaced):

    lastExecuted=client.get_executed_orders(market=cryptoCurrency+'CLP')[0]

    if lastOrder["id"]==lastExecuted["id"]:
        if lastExecuted["side"]=="sell"
            records.insert(0,{'Date':lastExecuted["updated_at"],'Side':lastExecuted["side"],'Amount':float(lastExecuted["amount"]["executed"]),'Price':float(lastExecuted["price"]),'Total':float(lastExecuted["fills"][0]["amount"]),'Fees':float(lastExecuted["fee"])})
        else:   # lastExecuted["side"]=="buy"
            records.insert(0,{'Date':lastExecuted["updated_at"],'Side':lastExecuted["side"],'Amount':float(lastExecuted["amount"]["executed"]),'Price':float(lastExecuted["price"]),'Total':float(lastExecuted["amount"]["executed"])*float(lastExecuted["price"]),'Fees':float(lastExecuted["fee"])*float(lastExecuted["price"])})
    return records
