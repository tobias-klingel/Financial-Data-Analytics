import requests
import pandas as pd
import matplotlib.pyplot as plt

######################################################################################################
#Generic parameters for inrinio

api_key='xxxx---Use your own API Key----xxxx'

stock_quote='AAPL'
indicator='$indicator$'
hist_data_url=f'https://api-v2.intrinio.com/companies/{stock_quote}/historical_data/{indicator}?api_key={api_key}&frequency=yearly&start_date=01-01-2013'
data_point_url=f'https://api-v2.intrinio.com/companies/{stock_quote}/data_point/{indicator}/number?api_key={api_key}'

######################################################################################################
#Functions

#Get all listed companies in intrinio
def getAllListedCompanies():
    companies_url = 'https://api-v2.intrinio.com/companies?api_key=OmNmMzljNDdhM2MwNjg3MTkwYzc4ODFmYjEzYzdhYjkz'
    companies = (requests.get(companies_url).json())
    return companies

#Get all the ticker symbols of a companies e.g. AAPL for Apple
def getAllListedCompanyTicker():
    companies = getAllListedCompanies()
    companyTicker = []
    for comp in companies['companies']:
        companyTicker.append(comp['ticker'])
    return companyTicker

##############

#Generic function to get data from a indicator
def create_hist_df(indicator_str):
    url=hist_data_url.replace(indicator,indicator_str)
    req=requests.get(url)
    data=req.json()
    if len(data['historical_data'])>0:
        panda_df=pd.DataFrame(data['historical_data'])
        #Inverse Dates
        panda_df=panda_df.iloc[::-1]
        #Cut months and days, only year stays as date
        panda_df['date'] =panda_df['date'].str[0:4]
        return panda_df
    else:
        print("Error receiving historical data")
        return False

#Get data from intrinio without changes
def getHistoricalDataViaIndicator(indicator_str):
    url = hist_data_url.replace(indicator, indicator_str)
    req = requests.get(url)
    dataJSON = req.json()
    return dataJSON


def getDataPoint(indicator_str):
    url = data_point_url.replace(indicator, indicator_str)
    req = requests.get(url)
    dataJSON = req.json()
    return dataJSON

#################
#Output functions
#################

#Print plot of JSON (dataJSON)
def showPlotHistorical(dataJSON):
    df = pd.DataFrame(dataJSON['historical_data'])
    dividend_df = df.iloc[::-1]
    dividend_df.head()
    dividend_df.plot(x='date', y='value', title='Dividend per Share')
    plt.show()

#Print in console X(number of results printed) of results
def printXheadOfDataframeOfHistorical(dataJSON,numberX):
    df = pd.DataFrame(dataJSON['historical_data'])
    df = df.iloc[::-1]
    print(df.head(numberX))


######################################################################################################
######################################################################################################
#Strong and Consistent Return on Equity (net income/shareholder's equity)
roe_df = create_hist_df('roe')
print("###Return on Equity###")
print(roe_df.head().to_string())
print("#######################################")

ax=roe_df.plot(kind='line',x='date',y='value')
ax.set(xlabel='year',ylabel='Percentage',title='Return on Equity')
plt.savefig('roe.png')
plt.show()
