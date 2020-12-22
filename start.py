import sensitive.credentials as credential
from main import main
import base64
import time

api_key=base64.b64decode(credential.api_key).decode()
api_secret=base64.b64decode(credential.api_secret).decode()

cryptoCurrency='EOS' #'ETH','XLM','BTC','EOS'
minCLP=1000

print("Starting")
startTime=time.time()

while True:
    try:
        main(api_key,api_secret,cryptoCurrency,minCLP,startTime)
    except:
        pass
