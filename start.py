import sensitive.credentials as credential
from main import main
import base64
import time

api_key=base64.b64decode(credential.api_key).decode()
api_secret=base64.b64decode(credential.api_secret).decode()

cryptoCurrency='EOS' #'ETH','XLM','BTC','EOS'
initialInvestemnt=600000
minCLP=1000
emailAddress='yourEmail@mail.com'

print("Starting")
startTime=time.time()

while True:
    try:
        main(api_key,api_secret,cryptoCurrency,initialInvestemnt,minCLP,emailAddress,startTime)
    except:
        pass
