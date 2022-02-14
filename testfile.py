# Web 3 Setup
import hero_auction_tracker
from networksetup import web3
from contract_address import serendale_unit_tokens, serendale_contracts
import datetime
import json
import requests
from pycoingecko import CoinGeckoAPI 
from bs4 import BeautifulSoup 
#################################################################################################
from networksetup import chain_url, current_chain
from decoder import item_gold_prices_function
from pyhmy import account
from decoderV2 import decode_reciept, summarise_transaction

def get_jewel_usd_price():
    cg = CoinGeckoAPI()
    start = datetime.datetime.strptime("2-12-2021", "%d-%m-%Y")  #8-10-2021 first dau
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
    if unixstart > 1639785600:
        cg = CoinGeckoAPI()
        start = datetime.datetime.strptime(period_start, "%d-%m-%Y")  #8-10-2021 first dau
        end = datetime.datetime.today()
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        x = list(range(len(date_generated)))
        dfktears_jewel = list(range(len(date_generated)))
        count = -1
        for date in date_generated[:-1]:
            count +=1
            x[count] = str(date.strftime("%d-%m-%Y"))
            dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=x[count]))['market_data']['current_price']['eur']
        dfktears_jewel[len(date_generated)-1] = cg.get_price(ids='gaias-tears', vs_currencies='usd')["gaias-tears"]["usd"]

    elif unixstart == 1639785600:
        cg = CoinGeckoAPI()
        start = datetime.datetime.strptime(period_start, "%d-%m-%Y")  #8-10-2021 first dau
        end = datetime.datetime.today()
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        x = list(range(len(date_generated)))
        dfktears_jewel = list(range(len(date_generated)))
        dfktears_jewel[0] = 0.22827 #18/12/2021 no price history
        count = 0
        for date in date_generated[1:(len(date_generated)-1)]:
            count +=1
            x[count] = str(date.strftime("%d-%m-%Y"))
            dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=x[count]))['market_data']['current_price']['eur'] 
        dfktears_jewel[len(date_generated)-1] = cg.get_price(ids='gaias-tears', vs_currencies='usd')["gaias-tears"]["usd"]

    elif unixstart < 1639785600:
        cg = CoinGeckoAPI()
        start = datetime.datetime.strptime(period_start, "%d-%m-%Y")  #8-10-2021 first dau
        end = datetime.datetime.today()
        bugdate = datetime.datetime.strptime("18-12-2021", "%d-%m-%Y")
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days+1)]
        x = list(range(len(date_generated)))
        dfktears_jewel = list(range(len(date_generated)))
        count = -1
        for date in date_generated[0:((bugdate-start).days)]:
            count +=1
            x[count] = str(date.strftime("%d-%m-%Y"))
            dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=x[count]))['market_data']['current_price']['eur']  
        dfktears_jewel[((bugdate-start).days)] = 0.22827 #18/12/2021 no price history
        count = (bugdate-start).days
        for date in date_generated[((bugdate-start).days+1):(len(date_generated)-1)]:
            count +=1
            x[count] = str(date.strftime("%d-%m-%Y"))
            compile
            dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=date.strftime(x[count])))['market_data']['current_price']['eur'] 
        dfktears_jewel[len(date_generated)-1] = cg.get_price(ids='gaias-tears', vs_currencies='usd')["gaias-tears"]["usd"]
    return dfktears_jewel

def get_coin_graphql(coin, date):
  url = 'https://graph2.defikingdoms.com/subgraphs/name/defikingdoms/dex'

  headers={ 'Accept': 'application/json', 
            "Content-Type" : "application/json",
  }

  query = """query {
    tokens(where: {symbol:"%s"}) {
      tokenDayData(where:{date_gte:%s}){  
        date
        priceUSD
      }
    }
  }""" % (coin, date)

  x =(json.loads(requests.post(url, json={"query":query}, headers=headers).text))
  x = float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD'])
  #print(float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD']))
  return x 
  
print(get_coin_graphql('xJEWEL',1633995370))
  

def get_graphql_usd_price_date(coin,date):
    if coin == "xJEWEL":
        count = int((date - 1631232000)/86400)
        x = float(xjewel_usd[count]["priceUSD"])
    if coin ==  "DFKGOLD":
        count = int((date - 1638403200)/86400)
        x = float(dfkgold_usd[count]["priceUSD"])  
    if coin ==  "DFKSHVAS":
        count = int((date - 1638057600)/86400)
        x = float(dfkshvas_usd[count]["priceUSD"])  
    return x



def get_jewel_usd_price_date(date):
    present = datetime.datetime.strptime(date, "%d-%m-%Y")
    start = datetime.datetime.strptime(period_start, "%d-%m-%Y")
    count = (present-start).days
    jewel_usd_date = jewel_usd_today[count]
    return jewel_usd_date  

def get_dfktears_jewel_price_date(date): ##maybe wrong
    present = datetime.datetime.strptime(date, "%d-%m-%Y")
    start = datetime.datetime.strptime(period_start, "%d-%m-%Y")
    count = (present-start).days 
    dfktears_jewel_date = dfktears_jewel_today[count]
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

def get_price_USD(token, timestamp):
    unixtime =  int(datetime.datetime(int(timestamp[6:10]), int(timestamp[3:5]),int(timestamp[0:2])).timestamp())
    item_gold_prices = item_gold_prices_function()

    if token == "JEWEL":
        jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
        token_price = jewel_usd

    elif token == "x":
        if unixtime <= 1639958400: 
            token_price = get_graphql_usd_price_date("xJEWEL",unixtime)
        else:   
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10])) 
            xjewel_jewel = get_crpyto_price("xjewel_wone") /get_crpyto_price("jewel_wone")
            token_price = xjewel_jewel * jewel_usd

    elif token =="DFKTEARS":
        dfktears_usd = float(get_dfktears_jewel_price_date(timestamp[:10]))
        token_price = dfktears_usd

    elif token == "DFKGOLD":
        if unixtime <= 1639958400:
            token_price =  get_graphql_usd_price_date("DFKGOLD",unixtime)
        else:  
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
            token_price = get_crpyto_price("dfkgold_jewel") * jewel_usd

    elif token == "Shvas rune":
        if unixtime <= 1639958400:
            token_price =  get_graphql_usd_price_date("DFKSHVAS",unixtime)
        else:
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
            token_price = (get_crpyto_price("dfkshvas_jewel")) * jewel_usd

    elif token in item_gold_prices.keys():
        if unixtime <= 1639958400:
            token_price =  get_graphql_usd_price_date("DFKGOLD",unixtime) * item_gold_prices[token]
        else:
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]))
            token_price = (get_crpyto_price("dfkgold_jewel")) * item_gold_prices[token] * jewel_usd

    else:
        token_price = "n/a"
    return token_price    

def get_timestamp2(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)
    timestamp_unix = web3.eth.get_block(block_number).timestamp
    timestamp = datetime.datetime.utcfromtimestamp(timestamp_unix).strftime("%d-%m-%Y %H:%M:%S")
    #print(timestamp)
    return timestamp

def generate_transaction_history_harmony():
    print("Getting Harmony trasnaction history3..")
    # if tx_list == tx_list2 when page size increase means we have already reached all transaction for this wallet
    # everything in DFK involves HRC20 as it only involves jewel (HRC20) and other items (HRC20 too)

    transactions = 1000
    tx_list = account.get_transaction_history(
        wallet_address,
        page=0,
        page_size=transactions,
        include_full_tx=False,
        endpoint=chain_url[current_chain],
    )
    tx_list2 = account.get_transaction_history(
        wallet_address,
        page=0,
        page_size=transactions + 1000,
        include_full_tx=False,
        endpoint=chain_url[current_chain],
    )

    while tx_list != tx_list2:
        transactions += 1000
        tx_list = account.get_transaction_history(
            wallet_address,
            page=0,
            page_size=transactions,
            include_full_tx=False,
            endpoint=chain_url[current_chain],
        )
        tx_list2 = account.get_transaction_history(
            wallet_address,
            page=0,
            page_size=transactions + 1000,
            include_full_tx=False,
            endpoint=chain_url[current_chain],
        )

    # print(tx_list)
    print("Got Harmony Transaction History")
    print("Total Harmony transaction for on wallet = " + str(len(tx_list)))
    
    return tx_list

def filter_tx_list():
    pass

def generate_transaction_history():
    if current_chain == "harmony":
        wallet_transactions = generate_transaction_history_harmony()
    elif current_chain == "avalanche":
        print("Currently Not Supported")
    elif current_chain == "fantom":
        print("Currently Not Supported")
    else:
        print("Please input a valid chain")

    return wallet_transactions

def time_filter(period_start, period_end,wallet_transactions):
    print("filter start")
    unixtimestart = int(datetime.datetime(int(period_start[6:10]), int(period_start[3:5]),int(period_start[0:2])).timestamp())
    unixtimeend = int(datetime.datetime(int(period_end[6:10]), int(period_end[3:5]),int(period_end[0:2])).timestamp())
    timestamp = list(range(len(wallet_transactions)))
    unixtimestamp = list(range(len(wallet_transactions)))
    wallet_filter_transactions_dummy = list(range(len(wallet_transactions)))
    count = -1
    for i in range(len(wallet_transactions)):
        timestamp[i] = get_timestamp2(wallet_transactions[i])   
        unixtimestamp[i] =  int(datetime.datetime(int((timestamp[i])[6:10]), int((timestamp[i])[3:5]),int((timestamp[i])[0:2])).timestamp())
        if unixtimestamp[i] >= unixtimestart and unixtimestamp[i] <= unixtimeend:
            count += 1
            wallet_filter_transactions_dummy[count] = wallet_transactions[i]
    wallet_filter_transactions = list(range(count))
    for i in range(count):
        wallet_filter_transactions[i] = wallet_filter_transactions_dummy[i]
    print("filter end")    
    return wallet_filter_transactions

def get_labelled_transaction(wallet_transactions):
    print("getting labelled_transaction...")
    labelled_transactions = []

    total_txs = len(wallet_transactions)
    count = 1
    for tx_hash in wallet_transactions:
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        # print(receipt)
        if receipt.logs != []:
            for key in serendale_contracts.keys():
                if key == receipt["from"] or key == receipt["to"]:
                    # only find block and timestamp when it is DFK contract
                    receipt_decoded = decode_reciept(receipt)
                    labelled_transactions += summarise_transaction(receipt_decoded, tx_hash, wallet_address)
                    break
                elif key == receipt.logs[0]["address"]:
                    # only find block and timestamp when it is DFK contract
                    receipt_decoded = decode_reciept(receipt)
                    labelled_transactions += summarise_transaction(receipt_decoded, tx_hash, wallet_address)
        print(f"Prcoesseed {count} / {total_txs} transactions", end="\r")
        count += 1

    print("Got labelled_transaction!")
    return labelled_transactions



################################################################################################

############################################# MAIN ##############################################

# period_start = "16-12-2021"
# period_end = "02-01-2022"
# unixstart =  int(datetime.datetime(int(period_start[6:10]), int(period_start[3:5]),int(period_start[0:2])).timestamp())

# jewel_usd_today = get_jewel_usd_price() 
# dfktears_jewel_today = get_dfktears_jewel_price()
# if unixstart <= 1639958400: #20-12-2021
#     xjewel_usd = get_coin_graphql("xJEWEL", unixstart)
#     dfkgold_usd = get_coin_graphql("DFKGOLD",unixstart)
#     dfkshvas_usd = get_coin_graphql("DFKSHVAS",unixstart)

# # print("Please input wallet address here")
# wallet_address = "0xC4b35C78e83b598cF8E60F87E380731457Eb824F"

# import pandas as pd
# df = pd.DataFrame(
#     columns=[
#         'Timestamp', 
#         'Event Description', 
#         'Hero ID', 
#         'Token Name', 
#         'Token Amount', 
#         'Token Price',
#         'Token Value',
#         'Auction ID',
#         'Crystal ID'
#     ]
# )

# class RecordBuilder:
#     def __init__(self, timestamp, description, hero_id='-',
#                         token_name='-', token_amount='-', token_price='-',  token_value ='-', auction_id='-', crystal_id='-'):
#         self.timestamp = timestamp
#         self.description = description
#         self.hero_id = hero_id
#         self.token_name = token_name
#         self.token_amount = token_amount
#         self.token_price = token_price
#         self.token_value = token_value
#         self.auction_id = auction_id
#         self.crystal_id = crystal_id
    
#     @staticmethod
#     def from_tx(tx):
#         print(tx)
#         return RecordBuilder(
#             tx['timestamp'],
#             tx['description']
#         )
    
#     def to_list(self):
#         return [
#             self.timestamp, 
#             self.description, 
#             self.hero_id,
#             self.token_name, 
#             self.token_amount,
#             self.token_price,
#             self.token_value,
#             self.auction_id,
#             self.crystal_id,
#         ]

# row = 0
# for tx in labelled_transactions:
#     print(tx["description"])
    

#     if tx["description"] == "Start Quest":
#         builder = RecordBuilder.from_tx(tx)
#         builder.hero_id = tx["hero_id"]
#         df.loc[row] = builder.to_list()
#         row += 1

#     elif tx["description"] == "Auction Created (Hero Sale)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Auction Created (Hero Sale)"
#         builder.hero_id = tx["hero_id"]
#         builder.auction_id = tx['auction_id']
#         df.loc[row] = builder.to_list()
#         row += 1  

#     elif tx["description"] == "Auction Successful (Hero Sale)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description =  "Auction Successful (Hero Sale)"
#         builder.hero_id = tx["hero_id"]
#         builder.auction_id = tx['auction_id']
#         builder.token_name = tx["token_name"]
#         amount = tx["token_amount"]
#         builder.token_amount = web3.fromWei(amount,'ether')
#         timestamp = tx["timestamp"]
#         builder.token_price = get_price_USD("JEWEL",timestamp)
#         builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         df.loc[row] = builder.to_list()
#         row += 1     

#     elif tx["description"] == "Auction Cancelled (Hero Sale)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Auction Cancelled (Hero Sale)"
#         builder.hero_id = tx["hero_id"]
#         builder.auction_id = tx['auction_id']
#         df.loc[row] = builder.to_list()
#         row += 1     

#     elif tx["description"] == "Auction Created (Hero Hire)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Auction Created (Hero Hire)"
#         builder.hero_id = tx["hero_id"]
#         builder.auction_id = tx['auction_id']
#         df.loc[row] = builder.to_list()
#         row += 1    

#     elif tx["description"] == "Auction Successful (Hero Hire)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Auction Successful (Hero Hire)"
#         builder.hero_id = tx["hero_id"]
#         builder.auction_id = tx['auction_id']
#         df.loc[row] = builder.to_list()
#         row += 1        

#     elif tx["description"] == "Auction Cancelled (Hero Hire)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Auction Cancelled (Hero Hire)"
#         builder.hero_id = tx["hero_id"]
#         builder.auction_id = tx['auction_id']
#         df.loc[row] = builder.to_list()
#         row += 1            
    
#     elif tx["description"] == "Complete Quest":
#         #transactions without logs do not have token trasnfers
#         builder = RecordBuilder.from_tx(tx)
#         builder.hero_id = tx["hero_id"]
#         builder.token_name = token = tx["token_name"]
#         amount = tx["token_amount"]
#         item_gold_prices = item_gold_prices_function()
#         if token == "Jewels":
#             # token rewarded in wei
#             builder.token_amount = web3.fromWei(amount,'ether')
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("JEWEL",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         elif token == "DFKTEARS":
#             builder.token_amount = amount
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("DFKTEARS",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         elif token == "DFKGOLD":
#             # token rewarded milli (x10^3)
#             builder.token_amount = amount / 1000
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("DFKGOLD",timestamp)
#             if builder.token_price != "n/a":
#                 builder.token_value = float(builder.token_price) * float(builder.token_amount)
#             else:
#                 builder.token_value = "n/a"
#         elif token in item_gold_prices.keys():  
#             builder.token_amount = amount   
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD(builder.token_name,timestamp)
#             if builder.token_price != "n/a":
#                 builder.token_value = float(builder.token_price) * float(builder.token_amount)
#             else:
#                 builder.token_value = "n/a"
#         df.loc[row] = builder.to_list()
#         row += 1

#     elif tx["description"] == "Jewels Claim":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Jewels Claim"
#         builder.token_name = tx["token_name"]
#         amount = tx["token_amount"]
#         builder.token_amount = amount = web3.fromWei(amount,'ether')
#         timestamp = tx["timestamp"]
#         builder.token_price = get_price_USD("JEWEL",timestamp)
#         builder.token_value = builder.token_price * amount
#         df.loc[row] = builder.to_list()
#         row += 1  

#     elif tx["description"] == "Hero Mint":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Hero Mint"
#         builder.crystal_id = tx["crystal_id"]
#         df.loc[row] = builder.to_list()
#         row += 1          

#     elif tx["description"] == "Crystal Summoned":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Crystal Summoned"
#         builder.crystal_id = tx["crystal_id"]
#         df.loc[row] = builder.to_list()
#         row += 1  

#     elif tx["description"] == "Meditation Completed":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Meditation Completed"
#         builder.hero_id = tx["hero_id"]
#         df.loc[row] = builder.to_list()
#         row += 1            
    
#     elif tx["description"] == "Liquidity Providing (Get Seeds)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Liquidity Providing (Get Seeds)"
#         amount = tx["token_amount"]
#         builder.token_name = tx["token_name"]
#         if builder.token_name == "Jewels":
#             builder.token_amount = amount / 10e+18
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("JEWEL",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         else:
#             builder.token_amount = amount / 10e+18  
#         df.loc[row] = builder.to_list()
#         row += 1      

#     elif tx["description"] == "Normal Transfer":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Normal Transfer"
#         amount = tx["token_amount"]
#         if amount != "":
#             builder.token_name = tx["token_name"]
#             builder.token_amount = amount / 10e+18
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("JEWEL",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         df.loc[row] = builder.to_list()
#         row += 1    

#     elif tx["description"] == "DEX Token Swapping":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "DEX Token Swapping"
#         amount = tx["token_amount"]
#         builder.token_name = tx["token_name"]
#         if builder.token_name == "Jewels":
#             builder.token_amount = amount / 10e+18
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("JEWEL",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         else:
#             builder.token_amount = amount / 10e+18
#         df.loc[row] = builder.to_list()
#         row += 1  

#     elif tx["description"] == "LP Token Deposit (Plant Seeds)":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "LP Token Deposit (Plant Seeds)"
#         amount = tx["token_amount"]
#         builder.token_name = tx["token_name"]
#         if builder.token_name == "Jewels":
#             builder.token_amount = amount / 10e+18
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("JEWEL",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         else:
#             builder.token_amount = amount / 10e+18
#         df.loc[row] = builder.to_list()
#         row += 1

#     elif tx["description"] == "Banking":
#         builder = RecordBuilder.from_tx(tx)
#         builder.description = "Banking"
#         amount = tx["token_amount"]
#         builder.token_name = tx["token_name"]
#         if builder.token_name == "Jewels":
#             builder.token_amount = amount / 10e+18
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("JEWEL",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         elif builder.token_name == "xJewels":
#             builder.token_amount = amount / 10e+18
#             timestamp = tx["timestamp"]
#             builder.token_price = get_price_USD("x",timestamp)
#             builder.token_value = float(builder.token_price) * float(builder.token_amount)
#         else:
#             builder.token_amount = amount / 10e+18
#         df.loc[row] = builder.to_list()
#         row += 1                        

# print(df)
# df.to_csv('Transaction_History_Test.csv')

