from main import main
import sensitive.credentials
import base64

api_key=base64.b64decode(sensitive.credentials.api_key).decode()
api_secret=base64.b64decode(sensitive.credentials.api_secret).decode()

cryptoCurrency='EOS' #'ETH','XLM','BTC','EOS'
minCLP=1000

print("Starting")
main(api_key,api_secret,cryptoCurrency,minCLP)
