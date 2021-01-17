def withdrawItAll(client,amountCLP):

    client.get_account()["bank_accounts"][0]["id"]
    client.notify_withdrawal(bank_account=str(client.get_account()["bank_accounts"][0]["id"]), amount=str(amountCLP))
    return None
