import event_decoder
import json
from contract_address import serendale_contracts, serendale_unit_tokens
from hero_auction_tracker import get_hero_auction_with_auction_id
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


def get_timestamp_from_block_number(block_number):
    return web3.eth.get_block(block_number).timestamp

def get_timestamp(tx_hash):
    block_number = web3.eth.get_transaction_receipt(tx_hash).blockNumber
    timestamp_unix = web3.eth.get_block(block_number).timestamp
    # timestamp = datetime.datetime.utcfromtimestamp(timestamp_unix).strftime("%d-%m-%Y %H:%M:%S")
    return timestamp_unix, block_number


def summarise_transaction(tx_decoded, tx_hash, wallet_address):
    timestamp, blocknumber = get_timestamp(tx_hash)

    summary = []

    relabel = 0
    jewel_transfer = 0
    xjewel_transfer = 0

    for log in tx_decoded:
        transaction = {
        "timestamp": timestamp, 
        "blocknumber": blocknumber, 
        "description": "Normal Transfer", # this will be replaced later for not normal transfer tx
        "hero_id": "",
        "crystal_id": "",
        "token_name": "",
        "token_amount": "",
        "auction_id": "",
        "tx_hash": tx_hash,
         }

        if log != "Decode Error":
            # Things to ignore in Decoded Transaction
            if (
                log["name"] == "QuestStaminaSpent" or
                log["name"] == "QuestXP" or 
                log["name"] == "QuestCompleted" or
                log["name"] == "QuestSkillUp" or
                log["name"] == "Approval" or 
                log["name"] == "StatUp" or
                log["name"] == "LevelUp" or
                log["name"] == "Sync" or 
                log["name"] == "Lock"
            ) : continue

            contract_address = web3.toChecksumAddress(log["address"])
            contract_address
            if log["name"] == "Swap":
                # we need to check for this first because there is infinite pair of LP contracts
                relabel = "DEX Token Swapping"
                continue
            
            if contract_address in serendale_contracts.keys():
                contract_name = serendale_contracts[contract_address]
            else: 
                contract_name = "undefined"
                undefined_contract_name = contract_address

            if contract_name == "xJewels":
                xjewel_transfer = 1
            elif contract_name == "Jewels":
                jewel_transfer = 1

            if log["name"] == "Transfer":
                
                from_address = web3.toChecksumAddress(log["data"][0]["value"])
                to_address = web3.toChecksumAddress(log["data"][1]["value"])

                if to_address == wallet_address:
                    # Token in
                    if contract_name == "Hero":
                        transaction["hero_id"] = log["data"][2]["value"]
                        transaction["token_amount"] = 1
                    else:
                        if contract_name == "undefined": transaction["token_name"] = undefined_contract_name
                        else: transaction["token_name"] = contract_name

                        contract = web3.eth.contract(address= contract_address,abi=abi["ERC20"])
                        # print(contract.all_functions())
                        decimals = contract.functions.decimals().call()
                        transaction["token_amount"] = log["data"][2]["value"] / 10**decimals

                elif from_address == wallet_address:
                    # Token out
                    if contract_name == "Hero":
                        transaction["hero_id"] = log["data"][2]["value"]
                        transaction["token_amount"] = -1
                    else:
                        if contract_name == "undefined": transaction["token_name"] = undefined_contract_name
                        else: transaction["token_name"] = contract_name

                        contract = web3.eth.contract(address= contract_address,abi=abi["ERC20"])
                        # print(contract.all_functions())
                        decimals = contract.functions.decimals().call()
                        transaction["token_amount"] = -log["data"][2]["value"] / 10**decimals
                
                else: continue # no transaction we care about

            elif log["name"] == "QuestStarted":
                transaction["description"] = "Start Quest"
                transaction["hero_id"] = log["data"][2]["value"]
            
            elif log["name"] == "QuestReward":
                rewardItem_address = web3.toChecksumAddress(log["data"][3]["value"])
                if rewardItem_address == "0x0000000000000000000000000000000000000000":
                    continue
                else:
                    relabel = "Complete Quest"
                    transaction["description"] = "Complete Quest"
                    transaction["hero_id"] = log["data"][2]["value"]
                    transaction["token_name"] = serendale_contracts[web3.toChecksumAddress(rewardItem_address)]
                    contract = web3.eth.contract(address= rewardItem_address,abi=abi["ERC20"])
                    # print(contract.all_functions())
                    decimals = contract.functions.decimals().call()
                    transaction["token_amount"] = log["data"][4]["value"] / 10**decimals
            
            elif log["name"] == "AuctionCreated":
                if contract_name == "Auction House":
                    relabel = "Auction Created (Hero Sale)"
                    transaction["description"] = "Auction Created (Hero Sale)"
                    transaction["auction_id"] = log["data"][0]["value"]
                    transaction["hero_id"] = log["data"][2]["value"]

                    #check for auction successful
                    success_auctions = get_hero_auction_with_auction_id(transaction["auction_id"])
                    if success_auctions is not None:
                        print("Some thing need to be added")
                        extraTx = {
                            "timestamp": success_auctions['timestamp'], 
                            "blocknumber": success_auctions['blockNumber'], 
                            "crystal_id": ""
                        }
                        extraTx["description"] = "Auction Successful (Hero Sale)"
                        extraTx["auction_id"] = success_auctions['auctionId']
                        extraTx["hero_id"] = success_auctions['tokenId']
                        extraTx["token_name"] = "Jewels"
                        extraTx["token_amount"] = success_auctions['totalPrice'] / 10e17 *0.965
                        summary += [extraTx]

                elif contract_name == "Hiring Place":
                    relabel = "Auction Created (Hero Hire)"
                    transaction["description"] = "Auction Created (Hero Hire)"
                    transaction["auction_id"] = log["data"][0]["value"]
                    transaction["hero_id"] = log["data"][2]["value"]
            
            elif log["name"] == "AuctionSuccessful":
                if contract_name == "Auction House":
                    relabel = "Auction Successful (Hero Sale)"
                    transaction["description"] = "Auction Successful (Hero Sale)"
                    transaction["auction_id"] = log["data"][0]["value"]
                    transaction["hero_id"] = log["data"][1]["value"]
                    transaction["token_name"] = "Jewels"
                    transaction["token_amount"] = log["data"][2]["value"] / 10e17

                    winner_address = web3.toChecksumAddress(log["data"][3]["value"])

                    if winner_address == wallet_address: transaction["token_amount"]*=-1 # if we are winner, we pay
                    # harmony only detect transaciton initiated by us so no need the below condition as it will never detect
                    # else: transaction["token_amount"] *=0.9625 # we are the one selling, 3.75% on seller.

                if contract_name == "Hiring Place":
                    relabel = "Auction Successful (Hero Hire)"
                    transaction["description"] = "Auction Successful (Hero Sale)"
                    transaction["auction_id"] = log["data"][0]["value"]
                    transaction["hero_id"] = log["data"][1]["value"]
                    transaction["token_name"] = "Jewels"
                    transaction["token_amount"] = log["data"][2]["value"]/ 10e17

                    winner_address = web3.toChecksumAddress(log["data"][3]["value"])
                    if winner_address == wallet_address: transaction["token_amount"]*=-1 # if we are winner, we pay
                    # harmony only detect transaciton initiated by us so no need the below condition as it will never detect
                    # else: transaction["token_amount"] *=0.9625 # we are the one selling, 3.75% on seller.
            
            elif log["name"] == "AuctionCancelled":
                if contract_name == "Auction House":
                    relabel = "Auction Cancelled (Hero Sale)"
                    transaction["description"] = "Auction Cancelled (Hero Sale)"
                    transaction["auction_id"] = log["data"][0]["value"]
                    transaction["hero_id"] = log["data"][1]["value"]
                elif contract_name == "Hiring Place":
                    relabel = "Auction Cancelled (Hero Hire)"
                    transaction["description"] = "Auction Cancelled (Hero Hire)"
                    transaction["auction_id"] = log["data"][0]["value"]
                    transaction["hero_id"] = log["data"][1]["value"]

            elif log["name"] == "SendGovernanceTokenReward":
                # This is unique to garden claim
                relabel = "Jewels Claim"
                transaction["description"] = "Jewels Claim"
                transaction["token_name"] = "Jewels"
                transaction["token_amount"] = (log["data"][2]["value"] - log["data"][3]["value"]) / 10e17 #total - locked
            
            elif log["name"] == "CrystalOpen":
                relabel = "Crystal Open"
                transaction["description"] = "Crystal Open"
                transaction["crystal_id"] = log["data"][1]["value"]

            elif log["name"] == "CrystalSummoned":
                relabel = "Crystal Summoned"
                transaction["description"] = "Crystal Summoned"
                transaction["crystal_id"] = log["data"][0]["value"]

            elif log["name"] == "MeditationCompleted":
                transaction["description"] = "Meditation Completed"
                transaction["hero_id"] = log["data"][2]["value"]
            
            elif log["name"] == "MeditationBegun":
                relabel = "Meditation Begun"
                transaction["description"] = "Meditation Begun"
                transaction["hero_id"] = log["data"][1]["value"]
            
            elif log["name"] == "Mint":
                relabel = "Liquidity Providing (Get Seeds)"
                pair_contract = web3.eth.contract(address=contract_address, abi=abi["UniswapV2Pair"])
                token1_address = web3.toChecksumAddress(pair_contract.functions.token0().call())
                token2_address = web3.toChecksumAddress(pair_contract.functions.token1().call())
                try:
                    pair_name = str(serendale_contracts[token1_address]) + "-" + str(serendale_contracts[token2_address]) + " Pair"
                except:
                    pair_name =  undefined_contract_name
                continue

            elif log["name"] == "Burn":
                relabel = "Liquidity Removal (Split Seeds)"
                pair_contract = web3.eth.contract(address=contract_address, abi=abi["UniswapV2Pair"])
                token1_address = web3.toChecksumAddress(pair_contract.functions.token0().call())
                token2_address = web3.toChecksumAddress(pair_contract.functions.token1().call())
                try:
                    pair_name = str(serendale_contracts[token1_address]) + "-" + str(serendale_contracts[token2_address]) + " Pair"
                except:
                    pair_name = undefined_contract_name
                continue
            
            elif log["name"] == "Deposit":
                relabel = "LP Token Deposit (Plant Seeds)"
                transaction["description"] = "LP Token Deposit (Plant Seeds)"
                continue

            summary += [transaction]
    
    #After For Loop Finishes
    if xjewel_transfer == 1 and jewel_transfer == 1: # there is a swap in jewel and xjewel in 1 transaction
        for transaction in summary: transaction["description"] = "Banking"

    elif relabel != 0:  # Relabelling Needed
        if relabel == "Complete Quest":
            correct_summary = []
            for transaction in summary: 
                if transaction["description"] == "Complete Quest": correct_summary += [transaction]
            return correct_summary

        # HERO SALES
        elif relabel == "Auction Created (Hero Sale)":
            for transaction in summary: 
                if transaction["description"] == "Auction Created (Hero Sale)": return [transaction]
                
        elif relabel == "Auction Cancelled (Hero Sale)":
            for transaction in summary: 
                if transaction["description"] == "Auction Cancelled (Hero Sale)": return [transaction]

        elif relabel == "Auction Successful (Hero Sale)":
            for transaction in summary: 
                print(transaction)
                # if transaction["description"] == "Auction Successful (Hero Sale)": return [transaction]


        # HERO HIRES
        elif relabel == "Auction Created (Hero Hire)":
            for transaction in summary: 
                if transaction["description"] == "Auction Created (Hero Hire)": return [transaction]

        elif relabel == "Auction Cancelled (Hero Hire)":
            for transaction in summary: 
                if transaction["description"] == "Auction Cancelled (Hero Hire)": return [transaction]
        
        elif relabel == "Auction Successful (Hero Hire)":
            for transaction in summary: 
                if transaction["description"] == "Auction Cancelled (Hero Hire)": return [transaction]
        
        # Gardens
        elif relabel == "Jewels Claim":
            for transaction in summary: 
                if transaction["description"] == "Jewels Claim": return [transaction]
        
        elif relabel == "Liquidity Providing (Get Seeds)":
            correct_summary = []
            for transaction in summary: 
                transaction["description"] = "Liquidity Providing (Get Seeds)"
                if transaction["token_name"] == "undefined": transaction["token_name"] = pair_name
        
        elif relabel == "Liquidity Removal (Split Seeds)":
            correct_summary = []
            for transaction in summary: 
                transaction["description"] = "Liquidity Removal (Split Seeds)"
                if transaction["token_name"] == "undefined": transaction["token_name"] = pair_name

        elif relabel == "Crystal Open":
            correct_summary = []
            for transaction in summary: 
                if transaction["description"] == "Normal Transfer": correct_summary += [transaction]    # not actually Normal Transfer but currently labelled so
                elif transaction["description"] == "Crystal Open": crystal_id =  transaction["crystal_id"]
            correct_summary[0]["crystal_id"] = crystal_id
            correct_summary[0]["description"] = "Hero Mint"
            summary = correct_summary
        
        elif relabel == "Crystal Summoned" or relabel == "Meditation Begun":
            correct_summary = []
            tokens = {}
            crystal_id = ""
            hero_id = ""
            for transaction in summary: 
                # print(transaction)
                if transaction["description"] == "Normal Transfer":
                    if transaction["token_name"] in tokens.keys():
                        tokens[transaction["token_name"]] += transaction["token_amount"]
                    else:
                        tokens[transaction["token_name"]] = transaction["token_amount"]

                elif transaction["description"] == "Crystal Summoned": crystal_id =  transaction["crystal_id"]
                elif transaction["description"] == "Meditation Begun": hero_id =  transaction["hero_id"]
            
            for key in tokens.keys():
                correct_summary += [{
                    "timestamp": timestamp, 
                    "blocknumber": blocknumber,
                    "description": relabel,
                    "hero_id": hero_id,
                    "token_name": key,
                    "token_amount": tokens[key],
                    "crystal_id": crystal_id,
                    "tx_hash": tx_hash,
                }]
            summary = correct_summary

        else:
            for transaction in summary: transaction["description"] = relabel

    return summary

def display_transaction(transaction_summary):
    print("displaying transactions...")
    for i in transaction_summary:
        print(i)
    print("Transactions displayed")

# Testing

wallet_1 = web3.toChecksumAddress("0xc2cfcda0cd983c5e920e053f0985708c5e420f2f")
normal_jewel_transfer = "0x8dce68b22eacad3c2ca96dc0ffd1b7a4125cc4bdd21724be5151532bf4202faa"
normal_xjewel_transfer = "0x8bb4aee834128125b105c60055e5c5e9c90e8e59f72ba385d9bc7546e91057c2"
normal_hero_transfer = "0x530e448d6c19fe1769887ee8134905942d15f8b8673fe2def646ba904c65f33b"
foraging_quest_start = "0xcf82380fc079753630efa19c63d51c68cc9f9e784462ae03c9324f79718b7c31"
foraging_quest_complete ="0x16f2058a6692806283bf69d3595b0f42cb9b0fe62c33b8814d4ecf8ef0ab35e1"
bank_deposit = "0xa1e762c5e41527a538078179ed204821f8ff9dac5100680a58e9a970ebbd4eba"
bank_deposit2 = "0xf5adccf44a5974d0837e71f4766566ac2202e2c4ca46863911707b92f1891197"
bank_withdrawal = "0x5315ccce1e049afd3df3cba512535de97784830d758c037a70f6254ba61f6edb"
gardens_claim = "0x48181dc8787020d22c1118379bec9b88f622de9e6123e66b9de9ff3f1692f583"
list_hero_sale = "0x907c3f68e9c6808a178a04e7d8c38084261b2a61f549bb5b22a43f4ca8beb738" 
cancel_hero_sale = "0xb6ade054567bb5864578f4f304de771db7fb43f63ac5fe1b505edcfc809d37cd"
list_hero_hire = "0x702446594026768bd65361457bd765d28fe6da31f4314efa44c3e76b38013b09" 
cancel_hero_hire = "0xb9d5ef9f44709cf7e57c496aadc529be9ae829ac2e40e8fb93ee930da04b0826"
hero_crystal_open ="0x097a480ff7a12f09ecfa28cfdd4d4b44e1b61ac68f396567606773f89ee0565e"
hero_crystal_open2 = "0x2fefa34550e5bcc4fb207de16554e76e55f8f9ea2fea665ce9c47f4bd54042bc"
hero_crystal_summon = "0x7381db9c7a6245e04c21732dd683caf4c68a98d7deabad347499e3766c8e2ea0"
hero_meditation_completed = "0x1c8e242b7d9701d764981dbc89ad5eee45914aafbfd4efb41ea98d176e09982c"
hero_meditation_init = "0x54a4cb66afb0c4e46d879e01e5ec82931561ddec7501855bb429219330fee16d"
tokenswap = "0x45671bef7ab67080bb27eb21bc241b95b1049084e88a38346d1d5027c2b2fb76"
hero_hiring_and_crystal_summon = "0x8bf415cd3dc2ca79df93216c0da24d02d368673d2ac0039e8a1579d6fa7a3ebd"

wallet_2 = web3.toChecksumAddress("0x900554698f30c589389fb4d860dfa932f1d87039")
hero_sold = "0x876e4ea1b61c0fc0f7ff415b2c42242b4ba4f4d1a52e85dcd5b8cab3ed0bff58"
fishing_quest_start = "0x8d28fc904c89907dabfa511963d527799fb5c08ca0e67ac034d50a9deb46a80b"
fishing_quest_finish = "0x58f1152272091b493a40b2e32c558925107cf8e3d5da2e1cd5b6418f7ed36173"
hero_sale_cancelled = "0xecc3865ca89528c922b83c7efcb38a09f163bd97d32add454b12fb73dc227280"
hero_list_for_sale = "0x4872b05916a2e82d4258f71f136995c842eff5494ec20f29b0c173c91adb9292"

wallet_3 = web3.toChecksumAddress("0x9950b438c5947C5cA7cDC225292f56B50a5c77B0")
abnormal_LP_Pair = "0x1b2a14a27c8f6ba835e3499eaa6e056fa33ff1f251500dfa745bffc6fbbce009"
abnormal_LP_Pair2 = "0x26132ebe9543f0262781eaef9fc277a5c82602621b76b2eb40b8b113641f274b"
no_token1_name_LP_pair = "0x7f42acf6ea052b6dcee48def3789f1786ef00d9c7ad2b25de9c1d82b00a6baa1"
remove_abnormal_LP_Pair = "0xb0321cac6019883fdf8a1689c109ec7485f1fcaffd260a81139a49a2dc39d8d6"
swap_jewel_for_questitem = "0xae571d19f439ac5fab846993a9a52c62ac1078b9a3ba2c7fc7736a29c9bc9457"
swap_jewel_for_non_contract_address_item = "0x1971dabaf9d9efeb75d552e836ed7ac77344af8e0f3ce9f9bea528ebc4b674a9"

wallet_4 = web3.toChecksumAddress("0xc4b35c78e83b598cf8e60f87e380731457eb824f")
liquidity_providing = "0xc7711b5783978da2789ff3e3be7b7ec7badf6f30531f59efd368b9303ea03e75"
staking_LP = "0xfc670b2516937e0e0c0565aec2d61b34cb863771f6c8a5a8cfb08c940e58e7d0"
swapping_jewel_to_USDC = "0x1431d8d45d7ac1c0e786bac0775cf6bcf47bd26d8fc9e08a1cb032d4d1cdcf55"

wallet_address = wallet_2
tx_hash = hero_list_for_sale

if __name__ == "__main__":
    from pyhmy import account
    tx_list = account.get_transaction_history(
        wallet_address,
        page=0,
        page_size=10000,
        include_full_tx=False,
        endpoint="https://rpc.s0.t.hmny.io",
    )
    print(tx_list)
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
    tx_decoded = decode_reciept(tx_receipt)
    print(tx_decoded)
    display_logs(tx_decoded)
    transaction_summary = summarise_transaction(tx_decoded, tx_hash, wallet_address)
    print(transaction_summary)
    
