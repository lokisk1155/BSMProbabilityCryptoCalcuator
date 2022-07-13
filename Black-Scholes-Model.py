import math
from statistics import variance
import requests
import pandas as pd
import numpy as np
import time 
start = time.time()
url_coin_market_cap = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
# !UPDATE QUERY! -daily for eth- 
query_string = f'https://query1.finance.yahoo.com/v7/finance/download/ETH-USD?period1=1649635200&period2=1657497600&interval=1d&events=history&includeAdjustedClose=true' 
headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': '725e2334-04e4-49f9-9940-d63b33a9cb8d'   }
params = {'start': '1', 'limit': '100', 'convert': 'USD'}
json = requests.get(url_coin_market_cap, params=params, headers=headers).json()
interval = '1d' 
date_of_exp = 197 # !UPDATE! To Expiration Date (scrappy bot here)
strike = 1200 # !UPDATE! To Crypto Strike Price (scrappy bot here)
days_till_expiration = 4 # !FIX THIS SHIT!
coin_selector = 'ETH'  # !UPDATE! To Crypto Ticker Wanted
crypto_currencies = json['data']
historial_data_eth = pd.read_csv(query_string)

def update_standard_deviation():       
    variance_values = historial_data_eth['Variance'] = (historial_data_eth['Adj Close'].mean()) - historial_data_eth['Adj Close'] 
    variance_array = []

    for index_of_variance, individual_variances in np.ndenumerate(variance_values):
        sqrt_abs_of_individual_variances = math.sqrt(abs(individual_variances))
        variance_array.append(sqrt_abs_of_individual_variances)
   
    running_total_of_variances = 0
    running_sum_of_all_variances = 0
    for stripped_individual_variances in variance_array:
        running_total_of_variances += 1
        running_sum_of_all_variances  += stripped_individual_variances
        running_sum_of_all_variances, stripped_individual_variances
        standard_deviation_from_variance = math.sqrt(running_sum_of_all_variances / running_total_of_variances) 
    return standard_deviation_from_variance

updated_stddev = update_standard_deviation()
annualized_volitility_from_standard_deviation = updated_stddev * math.sqrt(365)
time_to_maturity = days_till_expiration / 365
annualized_volaility = annualized_volitility_from_standard_deviation / 100

def update_annualized_volitility_once_per_day():
    return annualized_volaility


def coin_market_cap_crypto_calc():
    for specific_coin in crypto_currencies:
        if specific_coin['symbol'] == coin_selector:
            price = (specific_coin['quote']['USD']['price']) 
    vt=annualized_volaility*math.sqrt(time_to_maturity)
    lnpq=math.log(strike/price)
    d1= lnpq / vt
    y=math.floor(1/(1+.2316419* abs(d1))*100000)/100000
    z=math.floor(.3989423*math.exp(-((d1*d1)/2))*100000)/100000
    y5=1.330274*math.pow(y,5)
    y4=1.821256*math.pow(y,4)
    y3=1.781478*math.pow(y,3)
    y2=.356538*math.pow(y,2)
    y1=.3193815*y
    x=1-z*(y5-y4+y3-y2+y1)
    x=math.floor(x*100000)/100000
    if (d1<0):
       x=1-x
    pabove=math.floor(x*1000)/10
    pbelow=math.floor((1-x)*1000)/10
    return pabove, pbelow 

print(coin_market_cap_crypto_calc())
#print(update_annualized_volitility_once_per_day())

end = time.time()
total_time = end - start
print("\n"+ str(total_time))