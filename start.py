import sensitive.credentials as credential
from functions.main import main
import base64
import time

api_key=base64.b64decode(credential.api_key).decode()
api_secret=base64.b64decode(credential.api_secret).decode()

cryptoCurrency='EOS'                #It's possible to choose 'ETH','XLM','BTC','EOS'
initialInvestemnt=100000            #How much money was initially invested
profitExpected=0.3                  #Once the profit (%) is achived, the bot will sell everything
emailAddress='yourEmail@mail.com'   #Write your email address to receive reports

print("Starting")
startTime=time.time()

while True:
    try:
        main(api_key,api_secret,cryptoCurrency,initialInvestemnt,profitExpected,emailAddress,startTime)
    except:
        pass
