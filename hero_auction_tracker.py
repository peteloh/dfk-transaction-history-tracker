import database_utils
from networksetup import web3

def get_timestamp_from_block_number(block_number):
    return web3.eth.get_block(block_number).timestamp

def tuple_to_auction_dict(obj, from_id=False):
    result = dict()
    result["description"]   = "Auction Success (Database)"
    result["timestamp"]     = get_timestamp_from_block_number(obj[1])
    result["from_id"]       = from_id
    result["auctionId"]     = obj[0]
    result["blockNumber"]   = obj[1]
    result["tokenId"]       = obj[2]
    result["totalPrice"]    = int(obj[3])
    result["txHash"]        = obj[4]
    result["winner"]        = obj[5]

    return result

def get_hero_auction_with_auction_id(id):    
    db = database_utils.connect_db(database_utils.DATABASE_FILE)
    cur = db.cursor()
    sql = f"""select * from {database_utils.HERO_AUCTION_SUCCESS_TABLE_NAME} 
                where auctionId={id}"""
    result = cur.execute(sql)
    result = list(map(lambda x : tuple_to_auction_dict(x, True), result))
    if len(result) == 0:
        return None
    else:
        return result[0]

def get_hero_auctions_with_winner(address):
    db = database_utils.connect_db(database_utils.DATABASE_FILE)
    cur = db.cursor()
    sql = f"""select * from {database_utils.HERO_AUCTION_SUCCESS_TABLE_NAME} 
                where winner='{address}'"""
    result = cur.execute(sql)
    return list(map(tuple_to_auction_dict, result))

# pp = pprint.PrettyPrinter(indent=2)

# print("By address")
# pp.pprint(get_hero_auctions_with_winner("0x0dfc7152f83fafcc909bf3f1a26f5efbe324b195"))

# print("By Id")
# pp.pprint(get_hero_auction_with_auction_id(362623))
# pp.pprint(get_hero_auction_with_auction_id(362624))
