import event_decoder
import json
from contract_address import serendale_contracts
from networksetup import web3
# external lib
import datetime
import time
from bs4 import BeautifulSoup 
from pycoingecko import CoinGeckoAPI 
import requests



event_contracts = {
    "0x9014B937069918bd319f80e8B3BB4A2cf6FAA5F7": "UniswapV2Factory",
    "0x24ad62502d1C652Cc7684081169D04896aC20f30": "UniswapV2Router02",
    "0xA9cE83507D872C5e1273E745aBcfDa849DAA654F": "Bank",
    "0x3685Ec75Ea531424Bbe67dB11e07013ABeB95f1e": "Banker ",
    "0xDB30643c71aC9e2122cA0341ED77d09D5f99F924": "MasterGardener ",
    "0xa678d193fEcC677e137a00FEFb43a9ccffA53210": "Airdrop",
    "0xabD4741948374b1f5DD5Dd7599AC1f85A34cAcDD": "Profiles",
    "0x5F753dcDf9b1AD9AabC1346614D1f4746fd6Ce5C": "Hero",
    "0x13a65b9f8039e2c032bc022171dc05b30c3f2892": "Auction House",
    "0x0594d86b2923076a2316eaea4e1ca286daa142c1": "Meditation Circle",
    "0xe4154B6E5D240507F9699C730a496790A722DF19": "Gardening Quest"
}
# abi = open("abi/ERC20.json").read()   # get dict from json -> gives error
abi= {
    "JEWEL": json.load(open("abi/JEWEL.json")),
    "ERC20": json.load(open("abi/ERC20.json")),
    "ERC721": json.load(open("abi/ERC721.json")),
    "HeroSale": json.load(open("abi/HeroSale.json")),
    "HeroSummoningUpgradeable": json.load(open("abi/HeroSummoningUpgradeable.json")),
    "MasterGardener": json.load(open("abi/MasterGardener.json")),
    "MeditationCircle": json.load(open("abi/MeditationCircle.json")),
    "QuestCoreV2": json.load(open("abi/QuestCoreV2.json")),
    "SaleAuction": json.load(open("abi/SaleAuction.json")),
    "UniswapV2Factory": json.load(open("abi/UniswapV2Factory.json")),
    "UniswapV2Pair": json.load(open("abi/UniswapV2Pair.json")),
}

def item_gold_prices_function():
    item_gold_prices = {
    "Silverfin": 100,
    "Goldvein": 100,
    "Swift-Thistle": 75,
    "Shimmerskin": 60,
    "Sailfish": 50,
    "Redgill": 15,
    "Redleaf": 15,
    "Ambertaffy": 12.5,
    "Milkweed" : 12.5,
    "Darkweed": 10,
    "Spiderfruit": 10,
    "Ironscale": 5,
    "Lanterneye": 5,
    "Blue Stem": 5,
    "Rockroot": 5,
    "Ragweed": 2.5,
    "Bloater": 2.5,
    }
    return item_gold_prices


period_start = "16-12-2021"
period_end = "1-1-2021"
unixstart =  int(datetime.datetime(int(period_start[6:10]), int(period_start[3:5]),int(period_start[0:2])).timestamp())

def get_jewel_usd_price():
    cg = CoinGeckoAPI()
    start = datetime.datetime.strptime(period_start, "%d-%m-%Y")  #8-10-2021 first dau
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
  x = x['data']['tokens'][0]['tokenDayData'][:]
  #print(float(x['data']['tokens'][0]['tokenDayData'][0]['priceUSD']))
  return x 
  
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



def get_jewel_usd_price_date(date, jewel_usd_today):
    present = datetime.datetime.strptime(date, "%d-%m-%Y")
    start = datetime.datetime.strptime(period_start, "%d-%m-%Y")
    count = (present-start).days
    jewel_usd_date = jewel_usd_today[count]
    return jewel_usd_date  

def get_dfktears_jewel_price_date(date, dfktears_jewel_today): ##maybe wrong
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

def timestamp_from_blocknumber(blocknumber):
    timestamp_unix = web3.eth.get_block(blocknumber).timestamp
    timestamp = datetime.datetime.utcfromtimestamp(timestamp_unix).strftime("%d-%m-%Y %H:%M:%S")
    return timestamp

def get_timestamp(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)
    timestamp_unix = web3.eth.get_block(block_number).timestamp
    timestamp = datetime.datetime.utcfromtimestamp(timestamp_unix).strftime("%d-%m-%Y %H:%M:%S")
    #print(timestamp)
    return timestamp, block_number

def get_price_USD(token, timestamp, jewel_usd_today, dfktears_jewel_today):
    unixtime =  int(datetime.datetime(int(timestamp[6:10]), int(timestamp[3:5]),int(timestamp[0:2])).timestamp())
    item_gold_prices = item_gold_prices_function()

    if token == "JEWEL":
        jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]),jewel_usd_today)
        token_price = jewel_usd

    elif token == "x":
        if unixtime <= 1639958400: 
            token_price = get_graphql_usd_price_date("xJEWEL",unixtime)
        else:   
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]),jewel_usd_today) 
            xjewel_jewel = get_crpyto_price("xjewel_wone") /get_crpyto_price("jewel_wone")
            token_price = xjewel_jewel * jewel_usd

    elif token =="DFKTEARS":
        dfktears_usd = float(get_dfktears_jewel_price_date(timestamp[:10]),dfktears_jewel_today)
        token_price = dfktears_usd

    elif token == "DFKGOLD":
        if unixtime <= 1639958400:
            token_price =  get_graphql_usd_price_date("DFKGOLD",unixtime)
        else:  
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]),jewel_usd_today)  
            token_price = get_crpyto_price("dfkgold_jewel") * jewel_usd

    elif token == "Shvas rune":
        if unixtime <= 1639958400:
            token_price =  get_graphql_usd_price_date("DFKSHVAS",unixtime)
        else:
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]),jewel_usd_today)
            token_price = (get_crpyto_price("dfkshvas_jewel")) * jewel_usd

    elif token in item_gold_prices.keys():
        if unixtime <= 1639958400:
            token_price =  get_graphql_usd_price_date("DFKGOLD",unixtime) * item_gold_prices[token]
        else:
            jewel_usd = float(get_jewel_usd_price_date(timestamp[:10]),jewel_usd_today)
            token_price = (get_crpyto_price("dfkgold_jewel")) * item_gold_prices[token] * jewel_usd

    else:
        token_price = "n/a"
    return token_price

def decode_reciept(tx_receipt):
    logs = []
    for log in tx_receipt.logs:
        for key in abi.keys():
            topic_map = event_decoder.get_topic_map(abi[key])
            try:
                logs += [event_decoder.decode_log(log, topic_map)]
                break
            except:
                logs += ["Decode Error"]
    # print(logs)
    return logs

def display_logs(tx_decoded):
    for item in tx_decoded:
        # print(item)
        # print("\n")
        if item == "Decode Error":
            print("Decode Error")
            print("\n")
        else:
            for key in item.keys():
                if item[key] == "None":
                    break
                elif isinstance(item[key], list):
                    print(str(key) + " : ")
                    for stuff in item[key]:
                        if isinstance(stuff, dict):
                            event_string = "    "
                            for key in stuff.keys():
                                if key == "decoded":
                                    pass
                                else:
                                    event_string += str(stuff[key])
                                    event_string += " "
                            print(event_string)
                        else: print(stuff)

                else: print(str(key) + " : " + str(item[key]))
            print("\n")

def summarise_transaction(tx_decoded, tx_hash):
    print("decoding transaction...")
    timestamp, blocknumber = get_timestamp(tx_hash)
    transaction = {"timestamp": timestamp, "blocknumber": blocknumber, "description": "Normal Transfer"}
    events = []
    for log in tx_decoded:
        if log == "Decode Error":    
            #ignore
            continue
        else:
            if log["name"] == "Transfer":
                # store the event type and token
                
                token_name = serendale_contracts[log["address"]]
                data = {
                    "event": "Transfer",
                    "token": token_name
                }
                # log["data"] has a dict stored in list with 1 item
                for i in range(len(log["data"])):
                    for key in log["data"][i].keys():

                        # the 3 conditions below are applicable for all ERC20 transfers

                        if log["data"][i][key] == "from":
                            data["from"] = log["data"][i]["value"]  #save the 'to' address
                        elif log["data"][i][key] == "to":
                            data["to"] = log["data"][i]["value"]  #save the 'to' address
                        elif log["data"][i][key] == "value":

                            # data["priceUSD"] = get_price_USD(token_name, timestamp) # we want to do this outside now

                            if token_name == "Jewels":
                                data["amount"] = float(log["data"][i]["value"]) / 1000000000000000000 #convert to ether from wei
                            elif token_name == "xJewels":
                                data["amount"] = float(log["data"][i]["value"]) / 1000000000000000000 #convert to ether from wei
                                transaction["description"] = "Banking"
                            else:
                                data["amount"] = float(log["data"][i]["value"]) # other quest item rewards are in 'ether' unit already

                            # we want to do this outside now
                            # if data["priceUSD"] != "n/a":
                            #     data["valueUSD"] = data["priceUSD"] * data["amount"]
                            # else:
                            #     data["valueUSD"] = "n/a"

                        # the condition below is for hero related transaction

                        elif log["data"][i][key] == "tokenId":
                            data["heroId"] = log["data"][i]["value"]
                events += [data]
            
            # CrystalSummoned gives all the costs associated to summoning but does not show heroId
            # CrystalOpen has no cost but gives heroId
            # CrystalSummoned and CrystalOpen are linked by CrystalIdcontinue

            elif log["name"] == "CrystalOpen":
                transaction["description"] = "Crystal Open" 
                data = {
                    "event": "CrystalOpen",
                }
                for i in range(len(log["data"])):
                    for key in log["data"][i].keys():

                        if log["data"][i][key] == "crystalId":
                            data["crystalId"] = log["data"][i]["value"] 
                        elif log["data"][i][key] == "heroId":
                            data["heroId"] = log["data"][i]["value"] 
                events += [data]

            elif log["name"] == "CrystalSummoned":
                transaction["description"] = "Crystal Summon" 
                data = {
                    "event": "CrystalSummoned",
                }
                for i in range(len(log["data"])):
                    for key in log["data"][i].keys():

                        if log["data"][i][key] == "crystalId":
                            data["crystalId"] = log["data"][i]["value"] 

                events += [data]

            elif log["name"] == "MeditationBegun":
                transaction["description"] = "Hero Level Up" 
                data = {
                    "event": "MeditationBegun",
                }
                for i in range(len(log["data"])):
                    for key in log["data"][i].keys():

                        if log["data"][i][key] == "heroId":
                            data["heroId"] = log["data"][i]["value"] 

                events += [data]

            # Getting unique log that only occurs in different possible transaction on DFK

            # DEX Swapping
            elif log["name"] == "Swap": 
                transaction["description"] = "Token Swapping" 

            # Provide Liquidity Pair
            elif log["name"] == "Mint": 
                transaction["description"] = "Mint LP Tokens" 

            # Staking LP into the garden
            elif log["name"] == "Deposit": 
                transaction["description"] = "Staking LP Tokens"         

            # Unstaking LP from the garden
            elif log["name"] == "Withdraw": 
                transaction["description"] = "Staking LP Tokens"      

            # Completing Quests
            elif log["name"] == "QuestCompleted": 
                transaction["description"] = "Quest Completed"

            elif log["name"] == "QuestReward": 
                transaction["description"] = "Quest Reward"

            # Claiming Jewels from Garden
            elif log["name"] == "SendGovernanceTokenReward":
                transaction["description"] = "Harvest Jewels" 

            # Sucessfully Sold Hero in Auction House
            elif log["name"] == "AuctionSuccessful": 
                transaction["description"] = "Auction Successful"

            # EVENTS WITH NO TRANSFERS ARE SHOWN BELOW
            # Cancel Hero Listing
            elif log["name"] == "AuctionCancelled":
                transaction["description"] = "Auction Cancelled"
                # technically no token transfer between users, just return empty dict
                return {
                    "timestamp": timestamp, 
                    "blocknumber": blocknumber,
                    "description": "Auction Cancelled", 
                    "auctionId": log["data"][0]["value"],
                    "heroId": log["data"][2]["value"]
                }
            
            # Listing Hero into Auction House for Sale
            elif log["name"] == "AuctionCreated":
                transaction["description"] = "Auction Created"
                # technically no token transfer between users, just return empty dict
                return {
                    "timestamp": timestamp, 
                    "blocknumber": blocknumber,
                    "description": "Auction Created", 
                    "auctionId": log["data"][0]["value"],
                    "heroId": log["data"][2]["value"]
                }
            
            # Starting Quest
            elif log["name"] == "QuestStarted":
                transaction["description"] = "Quest Started"
                # technically no token transfer between users, just return empty dict
                return {
                    "timestamp": timestamp, 
                    "blocknumber": blocknumber,
                    "description": "Quest Started", 
                    "heroId": log["data"][2]["value"]
                }

    if events == []:
        print("transaction decoded!")
        return {"description": "Unidentified by ABI, no significance for P/L calculation"}
    else: 
        transaction["logs"] = events
    print("transaction decoded!")
    return transaction

def display_transaction(transaction_summary):
    print("displaying transactions...")
    for i in transaction_summary:
        if isinstance(i, list):
            for log in transaction_summary[i]:
                print(log)
        else:
            print(str(i) + " : " + str(transaction_summary[i]))
    print("\n")
    print("Transactions displayed")

# Testing
if __name__ == '__main__':
    normal_transfer = "0x8dce68b22eacad3c2ca96dc0ffd1b7a4125cc4bdd21724be5151532bf4202faa"
    hero_sold = "0x876e4ea1b61c0fc0f7ff415b2c42242b4ba4f4d1a52e85dcd5b8cab3ed0bff58"

    fishing_quest_start = "0x8d28fc904c89907dabfa511963d527799fb5c08ca0e67ac034d50a9deb46a80b"
    fishing_quest_finish = "0x58f1152272091b493a40b2e32c558925107cf8e3d5da2e1cd5b6418f7ed36173"
    foraging_quest_start_3man = "0xcf82380fc079753630efa19c63d51c68cc9f9e784462ae03c9324f79718b7c31"

    bank_deposit = "0xa1e762c5e41527a538078179ed204821f8ff9dac5100680a58e9a970ebbd4eba"
    bank_withdrawal = "0x5315ccce1e049afd3df3cba512535de97784830d758c037a70f6254ba61f6edb"

    gardens_claim = "0x48181dc8787020d22c1118379bec9b88f622de9e6123e66b9de9ff3f1692f583"

    list_hero_sale = "0x907c3f68e9c6808a178a04e7d8c38084261b2a61f549bb5b22a43f4ca8beb738" 
    cancel_hero_sale = "0xb6ade054567bb5864578f4f304de771db7fb43f63ac5fe1b505edcfc809d37cd"
    list_hero_hire = "0x702446594026768bd65361457bd765d28fe6da31f4314efa44c3e76b38013b09" # hero hire and sale is v similar
    cancel_hero_hire = "0xb9d5ef9f44709cf7e57c496aadc529be9ae829ac2e40e8fb93ee930da04b0826"

    hero_crystal_open ="0x097a480ff7a12f09ecfa28cfdd4d4b44e1b61ac68f396567606773f89ee0565e"
    hero_crystal_summon = "0x7381db9c7a6245e04c21732dd683caf4c68a98d7deabad347499e3766c8e2ea0"

    hero_meditation_completed = "0x1c8e242b7d9701d764981dbc89ad5eee45914aafbfd4efb41ea98d176e09982c"
    hero_meditation_init = "0x54a4cb66afb0c4e46d879e01e5ec82931561ddec7501855bb429219330fee16d"

    tokenswap = "0x45671bef7ab67080bb27eb21bc241b95b1049084e88a38346d1d5027c2b2fb76"
    liquidity_providing = "0xc7711b5783978da2789ff3e3be7b7ec7badf6f30531f59efd368b9303ea03e75"
    staking_LP = "0xfc670b2516937e0e0c0565aec2d61b34cb863771f6c8a5a8cfb08c940e58e7d0"

    tx_hash = fishing_quest_finish
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
    tx_decoded = decode_reciept(tx_receipt)
    print(tx_decoded)
    transaction_summary = summarise_transaction(tx_decoded, tx_hash)

    display_transaction(transaction_summary)
    display_logs(tx_decoded)
