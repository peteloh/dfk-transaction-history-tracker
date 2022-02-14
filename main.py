# Web 3 Setup
from logging import StreamHandler
import hero_auction_tracker
from networksetup import web3
from contract_address import serendale_unit_tokens, serendale_contracts
import datetime
from pycoingecko import CoinGeckoAPI 
from bs4 import BeautifulSoup

from networksetup import chain_url, current_chain
from pyhmy import account
from decoderV2 import decode_reciept, summarise_transaction
import pandas as pd
import streamlit as st
from coin_history_lib import get_coin_price, get_coin_latest_time
import time
import traceback

DFK_START_DATE = datetime.datetime.strptime('2021-08-23', '%Y-%m-%d')

# 0x900554698f30c589389fb4d860Dfa932f1d87039 wallet 1 ~ 1000  txn
# 0xC2cfCDa0cd983C5E920E053F0985708c5e420f2F wallet 2 ~ 2000 txn
# 0x9950b438c5947C5cA7cDC225292f56B50a5c77B0 walplet 3 ~ 10 txn but full of weird ones
# 0xC4b35C78e83b598cF8E60F87E380731457Eb824F wallet 4 ~ 50 txn

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

def datetime_unix_trim_time(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    result = datetime.datetime(dt.year, dt.month, dt.day)
    return datetime.datetime.timestamp(result)

def get_price_USD(token, timestamp):
    # unixtime =  int(datetime.datetime(int(timestamp[6:10]), int(timestamp[3:5]),int(timestamp[0:2])).timestamp())
    unixtime = datetime_unix_trim_time(timestamp)
    if unixtime < 1635724800:
        unixtime += 3600
    else:
        unixtime = unixtime

    item_gold_prices = item_gold_prices_function()

    if token == "JEWEL":
        if unixtime >= 1629676800 and unixtime <= get_coin_latest_time('JEWEL'):
            token_price = float((get_coin_price("JEWEL",unixtime))[1])
        else:
            token_price = 0
   

    elif token == "xJEWEL":
        if unixtime <= get_coin_latest_time('xJEWEL') and unixtime >= 1631232000: 
            token_price = float((get_coin_price("xJEWEL",unixtime))[1])
        else:   
            token_price = 0

    elif token =="DFKTEARS":
        if unixtime >= 1633046400 and unixtime <= get_coin_latest_time('DFKTEARS'):
            token_price = float((get_coin_price("DFKTEARS",unixtime))[1])
        else:
            token_price = 0    

    elif token == "DFKGOLD":
        if unixtime <= get_coin_latest_time('DFKGOLD') and unixtime >= 1638403200:
            token_price = float((get_coin_price("DFKGOLD",unixtime))[1])
        else:  
            token_price = 0

    elif token == "Shvas rune":
        if unixtime <= get_coin_latest_time('DFKSHVAS') and unixtime >= 1638144000:
            token_price = float((get_coin_price("DFKSHVAS",unixtime))[1])
        else:
            token_price = 0

    elif token in item_gold_prices.keys():
        if unixtime <= get_coin_latest_time('DFKGOLD') and unixtime >= 1638403200:
            token_price = float((get_coin_price("DFKGOLD",unixtime))[1]) * item_gold_prices[token]
        else:
            token_price = 0

    elif token == "WONE":
        if unixtime <= get_coin_latest_time('wone') and unixtime >= 1631232000:
            token_price = float((get_coin_price("wone",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1USDC":
        if unixtime <= get_coin_latest_time('wusdc') and unixtime >= 1635206400:
            token_price = float((get_coin_price("wusdc",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "BUSD" or token == "bscBUSD":  ##to be changed
        if unixtime <= get_coin_latest_time('busd') and unixtime >= 1629676800:
            token_price = float((get_coin_price("busd",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "UST":
        if unixtime <= get_coin_latest_time('ust') and unixtime >= 1629676800:
            token_price = float((get_coin_price("ust",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1MATIC":
        if unixtime <= get_coin_latest_time('matic') and unixtime >= 1629676800:
            token_price = float((get_coin_price("matic",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1ETH":
        if unixtime <= get_coin_latest_time('eth') and unixtime >= 1629676800:
            token_price = float((get_coin_price("eth",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1DAI":
        if unixtime <= get_coin_latest_time('dai') and unixtime >= 1629676800:
            token_price = float((get_coin_price("dai",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "AVAX":
        if unixtime <= get_coin_latest_time('AVAX') and unixtime >= 1629676800:
            token_price = float((get_coin_price("AVAX",unixtime))[1])
        else:
            token_price = 0

    elif token == "LUNA":
        if unixtime <= get_coin_latest_time('luna') and unixtime >= 1629676800:
            token_price = float((get_coin_price("luna",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1USDT":
        if unixtime <= get_coin_latest_time('usdt') and unixtime >= 1629676800:
            token_price = float((get_coin_price("usdt",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1BTC":
        if unixtime <= get_coin_latest_time('wbtc') and unixtime >= 1629676800:
            token_price = float((get_coin_price("wbtc",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "LINK":
        if unixtime <= get_coin_latest_time('link') and unixtime >= 1629676800:
            token_price = float((get_coin_price("link",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "1SUPERBID":
        if unixtime <= get_coin_latest_time('superbid') and unixtime >= 1629676800:
            token_price = float((get_coin_price("superbid",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "BNB":
        if unixtime <= get_coin_latest_time('bnb') and unixtime >= 1629676800:
            token_price = float((get_coin_price("bnb",unixtime))[1])
        else:
            token_price = 0
    
    elif token == "MIS":
        if unixtime <= get_coin_latest_time('mis') and unixtime >= 1634774400:
            token_price = float((get_coin_price("mis",unixtime))[1])
        else:
            token_price = 0   

    else:
        token_price = 0
    return token_price 

def get_timestamp2(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    # print(block_number)
    timestamp_unix = web3.eth.get_block(block_number).timestamp
    # timestamp = datetime.datetime.utcfromtimestamp(timestamp_unix).strftime("%d-%m-%Y %H:%M:%S")
    #print(timestamp)
    return timestamp_unix

def generate_transaction_history_harmony(wallet_address):
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

def generate_transaction_history(wallet_address):
    if current_chain == "harmony":
        wallet_transactions = generate_transaction_history_harmony(wallet_address)
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

def get_labelled_transaction(wallet_transactions, wallet_address, pg_bar):
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
        pg_bar.progress(count / total_txs)
        count += 1

    print("Got labelled_transaction!")
    return labelled_transactions

class RecordBuilder:
    def __init__(self, timestamp, description, hero_id='-',
                        token_name='-', token_amount='-', token_price='-',  token_value ='-', auction_id='-', crystal_id='-', txhash='-'):
        self.timestamp = timestamp
        self.description = description
        self.hero_id = hero_id
        self.token_name = token_name
        self.token_amount = token_amount
        self.token_price = token_price
        self.token_value = token_value
        self.auction_id = auction_id
        self.crystal_id = crystal_id
        self.txhash = txhash
    
    @staticmethod
    def from_tx(tx):
        print(tx)
        return RecordBuilder(
            tx['timestamp'],
            tx['description']
        )
    
    def to_list(self):
        return [
            self.timestamp, 
            self.description, 
            self.hero_id,
            self.token_name, 
            self.token_amount,
            self.token_price,
            self.token_value,
            self.auction_id,
            self.crystal_id,
            self.txhash
        ]

def get_transaction(wallet_address, pg_bar):
    df = pd.DataFrame(
        columns=[
            'Timestamp', 
            'Event Description', 
            'Hero ID', 
            'Token Name', 
            'Token Amount', 
            'Token Price ($)',
            'Token Value ($)',
            'Auction ID',
            'Crystal ID',
            'Transaction Hash'
        ]
    )
    print(address)
    
    labelled_transactions = None
    try:
        wallet_transactions = generate_transaction_history(wallet_address)
        wallet_filter_transactions = wallet_transactions

        labelled_transactions = \
            get_labelled_transaction(wallet_filter_transactions, wallet_address, pg_bar) + \
            hero_auction_tracker.get_hero_auctions_with_winner(wallet_address)

    except Exception as e:
        print("Generate Error")
        traceback.print_exc()
        return df

    row = 0

    for tx in labelled_transactions:
        print(tx["description"])
        
        if tx["description"] == "Start Quest":
            builder = RecordBuilder.from_tx(tx)
            builder.hero_id = tx["hero_id"]
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1

        elif tx["description"] == "Auction Created (Hero Sale)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Auction Created (Hero Sale)"
            builder.hero_id = tx["hero_id"]
            builder.auction_id = tx['auction_id']
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1  

        elif tx["description"] == "Auction Successful (Hero Sale)":
            builder = RecordBuilder.from_tx(tx)
            builder.description =  "Auction Successful (Hero Sale)"
            builder.hero_id = tx["hero_id"]
            builder.auction_id = tx['auction_id']
            builder.token_name = tx["token_name"]
            amount = tx["token_amount"]
            builder.token_amount = float(amount)
            timestamp = tx["timestamp"]
            builder.token_price = get_price_USD("JEWEL",timestamp)
            builder.token_value = float(builder.token_price) * float(builder.token_amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1
        
        elif tx['description'] == 'Auction Success (Database)':
            builder = RecordBuilder.from_tx(tx)
            builder.description =  "Auction Successful (Hero Bought)"
            builder.hero_id = tx["tokenId"]
            builder.auction_id = tx['auctionId']
            builder.token_name = "JEWEL"
            amount = tx["totalPrice"]
            builder.token_amount = float(amount)
            timestamp = tx["timestamp"]
            builder.token_price = get_price_USD("JEWEL", timestamp)
            builder.token_value = float(builder.token_price) * float(builder.token_amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1

        elif tx["description"] == "Auction Cancelled (Hero Sale)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Auction Cancelled (Hero Sale)"
            builder.hero_id = tx["hero_id"]
            builder.auction_id = tx['auction_id']
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1     

        elif tx["description"] == "Auction Created (Hero Hire)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Auction Created (Hero Hire)"
            builder.hero_id = tx["hero_id"]
            builder.auction_id = tx['auction_id']
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1    

        elif tx["description"] == "Auction Successful (Hero Hire)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Auction Successful (Hero Hire)"
            builder.hero_id = tx["hero_id"]
            builder.auction_id = tx['auction_id']
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1        

        elif tx["description"] == "Auction Cancelled (Hero Hire)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Auction Cancelled (Hero Hire)"
            builder.hero_id = tx["hero_id"]
            builder.auction_id = tx['auction_id']
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1            
        
        elif tx["description"] == "Complete Quest":
            #transactions without logs do not have token trasnfers
            builder = RecordBuilder.from_tx(tx)
            builder.hero_id = tx["hero_id"]
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount) 
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1

        elif tx["description"] == "Jewels Claim":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Jewels Claim"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                # token rewarded milli (x10^3)
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1  

        elif tx["description"] == "Hero Mint":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Hero Mint"
            builder.crystal_id = tx["crystal_id"]
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1          

        elif tx["description"] == "Crystal Summoned":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Crystal Summoned"
            builder.crystal_id = tx["crystal_id"]
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1  

        elif tx["description"] == "Meditation Completed":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Meditation Completed"
            builder.hero_id = tx["hero_id"]
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1            
        
        elif tx["description"] == "Liquidity Providing (Get Seeds)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Liquidity Providing (Get Seeds)"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount) 
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                # token rewarded milli (x10^3)
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "WONE":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("WONE",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "UST":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("UST",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1MATIC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1MATIC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1ETH":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1ETH",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "bscBUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("bscBUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1DAI":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1DAI",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "AVAX":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("AVAX",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LUNA":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LUNA",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDT":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDT",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1WBTC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1WBTC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LINK":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LINK",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1SUPERBID":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1SUPERBID",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BNB":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BNB",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "MIS":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("MIS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1      
        
        elif tx["description"] == "Liquidity Removal (Split Seeds)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Liquidity Removal (Split Seeds)"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                # token rewarded milli (x10^3)
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "WONE":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("WONE",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "UST":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("UST",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1MATIC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1MATIC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1ETH":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1ETH",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "bscBUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("bscBUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1DAI":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1DAI",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "AVAX":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("AVAX",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LUNA":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LUNA",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDT":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDT",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1WBTC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1WBTC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LINK":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LINK",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1SUPERBID":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1SUPERBID",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BNB":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BNB",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "MIS":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("MIS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1    

        elif tx["description"] == "Normal Transfer":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Normal Transfer"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                # token rewarded milli (x10^3)
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "WONE":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("WONE",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "UST":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("UST",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1MATIC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1MATIC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1ETH":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1ETH",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "bscBUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("bscBUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1DAI":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1DAI",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "AVAX":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("AVAX",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LUNA":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LUNA",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDT":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDT",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1WBTC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1WBTC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LINK":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LINK",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1SUPERBID":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1SUPERBID",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BNB":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BNB",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "MIS":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("MIS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1 

        elif tx["description"] == "DEX Token Swapping":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "DEX Token Swapping"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                # token rewarded milli (x10^3)
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "WONE":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("WONE",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "UST":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("UST",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1MATIC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1MATIC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1ETH":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1ETH",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "bscBUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("bscBUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1DAI":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1DAI",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "AVAX":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("AVAX",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LUNA":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LUNA",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDT":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDT",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1WBTC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1WBTC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LINK":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LINK",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1SUPERBID":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1SUPERBID",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BNB":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BNB",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "MIS":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("MIS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount) 
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1 

        elif tx["description"] == "LP Token Deposit (Plant Seeds)":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "LP Token Deposit (Plant Seeds)"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "WONE":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("WONE",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "UST":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("UST",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1MATIC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1MATIC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1ETH":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1ETH",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "bscBUSD":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("bscBUSD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1DAI":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1DAI",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "AVAX":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("AVAX",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LUNA":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LUNA",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1USDT":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1USDT",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1WBTC":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1WBTC",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "LINK":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("LINK",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "1SUPERBID":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("1SUPERBID",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "BNB":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("BNB",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "MIS":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("MIS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1

        elif tx["description"] == "Banking":
            builder = RecordBuilder.from_tx(tx)
            builder.description = "Banking"
            token = tx["token_name"]
            if token == "":
                continue
            builder.token_name = token
            amount = tx["token_amount"]
            item_gold_prices = item_gold_prices_function()
            if token == "Jewels":
                # token rewarded in wei
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("JEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKTEARS":
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKTEARS",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "DFKGOLD":
                # token rewarded milli (x10^3)
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("DFKGOLD",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "Shvas rune":
                # token rewarded milli (x10^3)
                builder.token_amount = amount
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("Shvas rune",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token == "xJewels":
                builder.token_amount = float(amount)
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD("xJEWEL",timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            elif token in item_gold_prices.keys():  
                builder.token_amount = amount   
                timestamp = tx["timestamp"]
                builder.token_price = get_price_USD(builder.token_name,timestamp)
                builder.token_value = float(builder.token_price) * float(builder.token_amount)
            else:
                builder.token_amount = float(amount)
            builder.txhash = tx["tx_hash"]
            df.loc[row] = builder.to_list()
            row += 1
    
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

    # df.to_csv(f'./histories/{wallet_address}.csv')
    return df

def combine_date_and_time(date, time):
    result = datetime.datetime(
        date.year, date.month, date.day,
        time.hour, time.minute, time.second
    )
    return result

def time_filter_df(df, start, end):
    df = df[(df['Timestamp'] >= start) & (df['Timestamp'] < end)]

    return df

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

if __name__ == '__main__': 
    
    st.markdown("<h1 style='text-align: center;'>Transaction History Generator</h1>", unsafe_allow_html=True)
    st.image("./images/grass.png")

    layout = st.sidebar.columns([4, 9])

    with layout[0]: 
        st.header(" ")
 
    with layout[-1]: 
        st.image("./images/jewel_icon.png")

    st.sidebar.title('Read Me')
    st.sidebar.header('How to Use')
    st.sidebar.markdown('1. Input wallet address in Ethereum Style \
                       \n2. Select start and end time \
                       \n3. Press **_Find_** \
                       \n4. Once finish, view and download as .csv')

    st.sidebar.header('Tips')
    with st.sidebar.expander("Token Amount"):
        st.write("""
            Positive token amount indicates inflow into the wallet.
            Negative represents outflow from the wallet.
        """)

    with st.sidebar.expander("Token Name"):
        st.write("""
            If any token name is not recorded in our database, the contract address is shown instead.
            The token address and wallet transaction hash can be looked up on https://explorer.harmony.one/. 
        """)

    with st.sidebar.expander("Hero ID"):
        st.write("""
            Hero ID is linked to every transaction log that involves that hero.
            Even if hero has gone to do quest as a group, each quest reward is linked to a specific hero!
            Hero ID can also be present with Jewel outflow or inflow, this shows hero bought and sold respectively.
        """)

    with st.sidebar.expander("Crystal ID"):
        st.write("""
            Jewels and Gaia's Tears are used to SummonCrystal. 
            However, Heroes are only minted when we OpenCrystal. 
            Therefore, Crystal ID can be used to link the cost of hero in the transaction log.
        """)

    st.sidebar.header('Known Limitations')
    with st.sidebar.expander("Transaction History"):
        st.write("""
            We are currently using Harmony API to query a transaction history list for an account. However, not all transactions are displayed. 
            The missing ones we found after vigourous checking are: Hero Sold and Hired (when someone buys or rents your listed Hero), Normal transfers **in** to the account.
            It seems like Harmony API does not record the transaction not initiated by the wallet address. A workaround we attempted for Hero Sold and Hire was
            to record the Auction ID for all AuctionCreated and see whether or not it matches the database of stored AuctionSuccessful found from GraphQL. 
            However, it turns out Harmony API somehow misses _some_ AuctionCreated and AuctionCancelled making our tracking method ineffective.
        """)

    with st.sidebar.expander("Prices"):
        st.write("""
            We have found that prices queries from GraphQL for xJewels, DFKGOLD, and DFKSHAVS has a 2 days sync delay. If price is not available, both price and value
            for that transaction will not be shown. Price are also not shown for token not listed on our database of known contracts. https://dexscreener.com/ has no API to call
            but the price is very updated for almost all altcoins.
        """)

    address = st.text_input('Wallet Address (0x..)')

    start_date = st.date_input('Start Date', value=DFK_START_DATE)
    start_time = st.time_input('Time Start (Start Date)', value=datetime.time(0, 0))

    end_date = st.date_input('End Date', value=datetime.date.today())
    end_time = st.time_input('Time End (End Date)', value=datetime.datetime.now())

    if st.button('Find'):
        start = combine_date_and_time(start_date, start_time)
        end = combine_date_and_time(end_date, end_time)

        pg_bar_holder = st.empty()
        pg_bar = pg_bar_holder.progress(0)

        df = get_transaction(address, pg_bar)
        # df.drop(['Auction ID'], axis=1, inplace=True)
        pg_bar_holder.empty()

        st.dataframe(df.astype(str))
        csv = convert_df(df)

        filename = "Transaction-History-"+str(address)+"-"+str(start_date)+"-"+str(end_date) +".csv"
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=filename,
            mime='text/csv',
        )

    st.image("./images/garden_image.png")

