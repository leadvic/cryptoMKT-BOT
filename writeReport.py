def writeReport(client,cryptoCurrency,startTime,records):
    from weasyprint import HTML
    from datetime import datetime
    import pandas as pd
    import time

    # How many CRY are in the balance
    for currency in client.get_balance()["data"]:
        if currency["wallet"]==cryptoCurrency:
            CRY_available=float(currency["balance"])
            break

    # How much time has it been running
    seconds=time.time()-startTime
    days=int(seconds//(24*3600))
    seconds%=(24*3600)
    hours=int(seconds//3600)
    seconds%=3600
    minutes=int(seconds//60)
    seconds%=60

    # Today's date
    today=datetime.now().strftime("%A, %d %B %Y")

    records=pd.DataFrame(records)

    # Record Summary
    onlyCRY=int(CRY_available*float(client.get_ticker(market=cryptoCurrency+'CLP')[0]["last_price"]))
    onlySales=int(sum(records.loc[records["Side"]=="sell"]["Total"]))
    onlyPurchases=int(sum(records.loc[records["Side"]=="buy"]["Total"]))
    onlyProfit=onlyCRY+onlySales-onlyPurchases

    html="""
    <html>
    <head></head>
    <h1 style="text-align: center;">{} Investment Report</h1>
    <p style="text-align: justify;">This report is automatically generated by the Trading Bot using the CryptoMKT API. The following information has been generated after a running time of {} Days, {} Hours, {} Minutes, {} Seconds.</p>
    <p style="text-align: justify;">All the information presented here is dated {}. Therefore, it may be out of date by the time it is read.</p>
    <h2>Trading Summary</h2>
    <table style="width: 80%; border-collapse: collapse; margin-left: auto; margin-right: auto;" border="1" cellpadding="10">
    <tbody>
    <tr>
    <td style="width: 50%;">{} assessed in CLP</td>
    <td style="width: 50%;">{}*</td>
    </tr>
    <tr>
    <td style="width: 50%;">Money earned from Sales</td>
    <td style="width: 50%;">{}</td>
    </tr>
    <tr>
    <td style="width: 50%;">Money spent on Purchases</td>
    <td style="width: 50%;">{}</td>
    </tr>
    <tr>
    <td style="width: 50%;">Relative Profit Estimate</td>
    <td style="width: 50%;">{}**</td>
    </tr>
    </tbody>
    </table>
    <p><em>*Its value may vary over time, so this is not a static value.</em></p>
    <p><em>**These are not actual earnings but a profit relative to the value of the {} today.</em></p>
    <h2>Trade Detail</h2>
    """.format(cryptoCurrency, str(days),str(hours),str(minutes),str(int(seconds)),today,cryptoCurrency,
    str(onlyCRY),str(onlySales),str(onlyPurchases),str(onlyProfit),cryptoCurrency)

    html+=records.to_html()

    # Write the HTML file
    f=open('./reports/report.html','w')
    f.write(html)
    f.close()

    # Write the report in PDF
    HTML.write_pdf(HTML('./reports/report.html'),'./reports/report.pdf')
    #HTML.write_pdf(HTML(html),'./reports/report.pdf')
