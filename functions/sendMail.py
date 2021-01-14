def sendMail(emailAddress):
    import sensitive.credentials as credential
    from email.message import EmailMessage
    import smtplib

    email_BOT=credential.email_tradingBot
    pass_BOT=credential.pass_tradingBot

    msg=EmailMessage()
    msg['Subject']='Transaction Report - CryptoMKT'
    msg['From']=email_BOT
    msg['To']=emailAddress
    msg.set_content('This email was sent automatically, please do not reply\nReport is attached.')

    with open('./reports/report.pdf','rb') as file:
        file_data=file.read()
        file_name=file.name

    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL("smtp.yandex.com",465) as smtp:
        smtp.login(email_BOT,pass_BOT)
        smtp.send_message(msg)
