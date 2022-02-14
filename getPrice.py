import datetime
from bs4 import BeautifulSoup 
from pycoingecko import CoinGeckoAPI 
import requests
import json

def get_jewel_usd_price():
    cg = CoinGeckoAPI()
    start = datetime.datetime.strptime("09-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
    end = datetime.datetime.today()
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

    x = list(range(len(date_generated)))
    jewel_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated[:-1]:
        count +=1
        x[count] = str(date.strftime("%d-%m-%Y"))
        jewel_usd[count] = (cg.get_coin_history_by_id(id='defi-kingdoms', date=date.strftime(x[count])))['market_data']['current_price']['usd']
    jewel_usd[len(date_generated)-1] = cg.get_price(ids='defi-kingdoms', vs_currencies='usd')["defi-kingdoms"]["usd"]
    return jewel_usd

def get_dfktears_jewel_price():  ##maybe wrong
    cg = CoinGeckoAPI()
    start = datetime.datetime.strptime("09-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
    end = datetime.datetime.today()
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]

    x = list(range(len(date_generated)))
    dfktears_jewel = list(range(len(date_generated)))
    count = -1
    for date in date_generated[0:9]:
        count +=1
        x[count] = str(date.strftime("%d-%m-%Y"))
        dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=date.strftime(x[count])))['market_data']['current_price']['eur'] 
    dfktears_jewel[9] = 0.22827 #18/12/2021 no price history
    count = 9
    for date in date_generated[10:len(date_generated)-1]:
        count +=1
        x[count] = str(date.strftime("%d-%m-%Y"))
        dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=date.strftime(x[count])))['market_data']['current_price']['eur']
    dfktears_jewel[len(date_generated)-1] = cg.get_price(ids='gaias-tears', vs_currencies='usd')["gaias-tears"]["usd"]
    return dfktears_jewel

#dfktears_jewel = get_dfktears_jewel_price()
#jewel_usd = get_jewel_usd_price()

def get_jewel_usd_price_date(date):
    start =  start = datetime.datetime.strptime(date, "%d-%m-%Y")
    end = datetime.datetime.today()
    count = len(jewel_usd) - (end-start).days - 1
    jewel_usd_date = jewel_usd[count]

    return jewel_usd_date  

def get_dfktears_jewel_price_date(date): ##maybe wrong
    start =  start = datetime.datetime.strptime(date, "%d-%m-%Y")
    end = datetime.datetime.today()
    count = len(dfktears_jewel) - (end-start).days - 1
    dfktears_jewel_date = dfktears_jewel[count]

    return dfktears_jewel_date

def get_crpyto_price(x):  
    if x == 'dfkshvas_jewel':
        url = 'https://geckoterminal.com/one/pools/0xb270556714136049b27485f1aa8089b10f6f7f57'  #dfkshave/jewel
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])

    if x == 'dfkgold_jewel':
        url = 'https://geckoterminal.com/one/pools/0x321eafb0aed358966a90513290de99763946a54b'  #dfkgold/jewel
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])
    
    if x == 'jewel_wone':
        url = 'https://geckoterminal.com/one/pools/0xeb579ddcd49a7beb3f205c9ff6006bb6390f138f' #jewel/wone
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])
    
    if x == 'xjewel_wone':
        url = 'https://geckoterminal.com/one/pools/0xfdab6b23053e22b74f21ed42834d7048491f8f32' #xjewel/wone
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])

    if x =='dfktears_jewel':
        url = 'https://geckoterminal.com/one/pools/0xc79245ba0248abe8a385d588c0a9d3db261b453c?utm_source=coingecko&utm_medium=referral&utm_campaign=livechart' #dfktears/jewel
        HTML = requests.get(url)
        soup = BeautifulSoup(HTML.text, 'html.parser')
        price = soup.find('div', attrs={'class':'my-3'}).find('span', attrs={'data-price-target':'price'}).text
        price = float(price[2:len(price)])
    
    return price

# def get_coin_graphql(coin, date):
#   url = 'https://graph4.defikingdoms.com/subgraphs/name/defikingdoms/dex'

#   headers={ 'Accept': 'application/json', 
#             "Content-Type" : "application/json",
#   }

#   query = """query {
#     tokens(where: {symbol:"%s"}) {
#       tokenDayData(where:{date_gte:%s}){  
#         date
#         priceUSD
#       }
#     }
#   }""" % (coin, date)

#   x =(json.loads(requests.post(url, json={"query":query}, headers=headers).text))
#   x = x['data']['tokens'][0]['tokenDayData'][:]
#   #print(float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD']))
#   return x  


def get_DFKGOLD_graphql():
  url = 'https://graph2.defikingdoms.com/subgraphs/name/defikingdoms/dex'

  headers={ 'Accept': 'application/json', 
            "Content-Type" : "application/json",
  }

  query = """query {
    tokens(where: {symbol:"DFKGOLD"}) {
      tokenDayData{  
        date
        priceUSD
      }
    }
  }"""

  x =(json.loads(requests.post(url, json={"query":query}, headers=headers).text))
  x = x['data']['tokens'][0]['tokenDayData'][:]
  #print(float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD']))
  return x     

def get_DFKSHVAS_graphql():
  url = 'https://graph2.defikingdoms.com/subgraphs/name/defikingdoms/dex'

  headers={ 'Accept': 'application/json', 
            "Content-Type" : "application/json",
  }

  query = """query {
    tokens(where: {symbol:"DFKSHVAS"}) {
      tokenDayData{  
        date
        priceUSD
      }
    }
  }"""

  x =(json.loads(requests.post(url, json={"query":query}, headers=headers).text))
  x = x['data']['tokens'][0]['tokenDayData'][:]
  #print(float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD']))
  return x    

# def get_graphql_usd_price_date(coin,date):
#     if coin == "xJEWEL":
#         count = int((date - 1631232000)/86400)
#         x = float(xjewel_usd[count]["priceUSD"])
#     if coin ==  "DFKGOLD":
#         count = int((date - 1638403200)/86400)
#         x = float(dfkgold_usd[count]["priceUSD"])  
#     if coin ==  "DFKSHVAS":
#         count = int((date - 1638057600)/86400)
#         x = float(dfkshvas_usd[count]["priceUSD"])  
#     return x    


def get_coin_graphql(coin, date_start, date_end, trial=5):
    url = 'https://graph4.defikingdoms.com/subgraphs/name/defikingdoms/dex'

    headers={ 'Accept': 'application/json', 
            "Content-Type" : "application/json",
    }

    query = """query {
    tokens(where: {symbol:"%s"}) {
        tokenDayData(where:{date_gte:%s, date_lt:%s}){  
        date
        priceUSD
        }
    }
    }""" % (coin, date_start, date_end)
    
    response = None
    for i in range(trial):
        try:
            response = requests.post(url, json={"query":query}, headers=headers)
        except Exception as e:
            print("Response Error")
            if i < (trial - 1):
                print("Retrying")

    if response is None:
        return []

    x =(json.loads(response.text))
    result = x['data']['tokens'][0]['tokenDayData']
    result = list(map((lambda x: (int(x['date']), float(x['priceUSD']))), result))

    return result


print(get_coin_graphql('JEWEL',	1640390400, 1641995200))