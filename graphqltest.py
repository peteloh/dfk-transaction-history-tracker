

from typing import Text
import requests
import json
import pandas as pd

# url = 'https://graph2.defikingdoms.com/subgraphs/name/defikingdoms/dex'

# headers={ 'Accept': 'application/json', 
#           "Content-Type" : "application/json",
# }

# query = """query {
#   tokens(where: {symbol:"DFKGOLD"}) {
#     tokenDayData(where:{date: 1639612800}){  
#       priceUSD
#     }
#   }
# }"""

# x =json.loads(requests.post(url, json={"query":query}, headers=headers).text)
# print(float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD']))


def get_dfkgold_graphql():
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


dfkgold_usd = get_dfkgold_graphql()

def get_price_crpyto_date(coin,date):
  if coin == "DFKGOLD":
    count = int((date - 1638403200)/86400)
    x = float(dfkgold_usd[count]["priceUSD"])
  return x

dfkgold_usd_day =get_price_crpyto_date("DFKGOLD", 1639612800)
print(dfkgold_usd_day)


def get_xJEWEL_graphql():
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

xjewel_usd = get_xJEWEL_graphql()
print(xjewel_usd)



