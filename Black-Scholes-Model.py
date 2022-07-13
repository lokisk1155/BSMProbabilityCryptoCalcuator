import math
import requests
import pandas as pd
import numpy as np
import time
#Manual imputs
strike = 1200 
days_till_expiration = 4 
ticker = 'ETH' 
query_string = f'https://query1.finance.yahoo.com/v7/finance/download/ETH-USD?period1=1649635200&period2=1657497600&interval=1d&events=history&includeAdjustedClose=true'
#coin market cap api connection / formatting
url_coin_market_cap = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': '725e2334-04e4-49f9-9940-d63b33a9cb8d'}
params = {'start': '2', 'limit': '2', 'convert': 'USD'}
json = requests.get(url_coin_market_cap, params=params, headers=headers).json()
crypto_currencies = json['data']

#Get yahoo historical data 
def get_updated_yahoo_variance():
    #turn query_string into pandas dataframe
    historial_data_eth = pd.read_csv(query_string)
    #making new col with data points equal to the mean - adj close (all days)
    variance_values = historial_data_eth['Variance'] = (historial_data_eth['Adj Close'].mean()) - historial_data_eth['Adj Close'] 
    #return value we are going to append values into
    function_variance_array = []
    for index_of_variance, individual_variances in np.ndenumerate(variance_values):
        # each value will be turned into its absolute value, then squared 
        sqrt_abs_of_individual_variances = math.sqrt(abs(individual_variances))
        function_variance_array.append(sqrt_abs_of_individual_variances)
    return function_variance_array
#Calculate standard deviation with updated yahoo data
def update_standard_deviation():       
    #Calls yahoo fetch to calculate updated variance in the form of an array
    variance_array = get_updated_yahoo_variance()
    #Elementry code
    running_count_of_variances = 0
    running_sum_of_all_variances = 0
    #For loop to total variances together , also tracks total variances looped over to allow for alterations
    for stripped_individual_variances in variance_array:
        running_count_of_variances += 1
        running_sum_of_all_variances += stripped_individual_variances
    #Get standard deviation by finding the square root of total variance sum divided by variance count
    standard_deviation_from_variance = math.sqrt(running_sum_of_all_variances / running_count_of_variances)  
    return standard_deviation_from_variance
#Prority variables for Black Scholes model
stddev = update_standard_deviation()
annualized_volaility = (stddev * math.sqrt(365)) / 100
time = days_till_expiration / 365 
#Black Scholes model
def coin_market_cap_crypto_calc(imput): 
#Pull current price from coin market cap's api
    for specific_coin in crypto_currencies:
        if specific_coin['symbol'] == ticker:
            price = (specific_coin['quote']['USD']['price']) 
    vt=annualized_volaility*math.sqrt(time)
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
    if imput == 1: return pabove
    if imput == 0: return pbelow
# envoke yes or no on crypto calculator 
def option_yes():
    return coin_market_cap_crypto_calc(1)
def option_no():
    return coin_market_cap_crypto_calc(0)
#print(update_priority_variables())
print(option_yes())
print(option_no())

