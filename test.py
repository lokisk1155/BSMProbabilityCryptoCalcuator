import requests
import math
from datetime import datetime

urlCoinMarketCap = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': '725e2334-04e4-49f9-9940-d63b33a9cb8d'   }
params = {'start': '1', 'limit': '100', 'convert': 'USD'}
json = requests.get(urlCoinMarketCap, params=params, headers=headers).json()

dayOfYear = datetime.now().timetuple().tm_yday 
dateOfExp = 197 # test variable
calenderDaysRemaining =  dateOfExp % dayOfYear
strike = 1200
USER_CLICK = 'ETH'  # test variable
cryptoCurrencies = json['data']

for specificCoin in cryptoCurrencies:
    if specificCoin['symbol'] == USER_CLICK:
        price = (specificCoin['quote']['USD']['price'])
        volatilityOneDay = (specificCoin['quote']['USD']['percent_change_24h'])

percentAnnualVolatility = volatilityOneDay * math.sqrt(365)
annualVolatility = percentAnnualVolatility/100
vt = annualVolatility * math.sqrt(calenderDaysRemaining)
lnpq = math.log(strike / price)
d1 = lnpq / vt
        
y = math.floor(1/(1+.2316419 * (abs(d1))*100000))/100000
z = math.floor(.3989423*math.exp(-((d1*d1)/2))*100000)/100000
y5 = 1.330274*math.pow(y,5)
y4 = 1.821256*math.pow(y,4)
y3 = 1.781478*math.pow(y,3)
y2 = .356538*math.pow(y,2)
y1 = .3193815*y
x = 1-z*(y5-y4+y3-y2+y1)
x = math.floor(x*100000)/100000
if (d1 < 0):
    x = 1 - x
pabove = math.floor(x*1000)/10; 
pbelow = math.floor((1-x)*1000)/10

print(pabove)
print(pbelow)