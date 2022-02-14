from web3 import Web3
import time
import eth_event
import json
import database_utils

EPOCH_NUMBER = 302400
DFK_START_BLOCK = 16350367

def get_filter_id(web3, from_block, to_block, address, topic):
    filt = web3.eth.filter({
        'fromBlock': from_block,
        'toBlock': to_block - 1,
        'address': Web3.toChecksumAddress(address),
        'topics': topic
    })
    return filt.filter_id, filt

def log_to_dict(topic_map, log):
    result = dict()
    event = eth_event.decode_log(log, topic_map)
    result['blockNumber'] = log['blockNumber']
    result['transactionHash'] = log['transactionHash'].hex()
    result['eventName'] = event['name']
    for o in event['data']:
        result[o['name']] = str(o['value'])
    return result

def get_table_updated_block(tb_name: str):
    tb_name = tb_name.lower()
    if tb_name not in database_utils.TABLES_NAMES:
        return None
    
    db = database_utils.connect_db(database_utils.DATABASE_FILE)
    result = database_utils.select_table(
        database_utils.TABLE_TRACK_TABLE_NAME, 
        where=f"tableName='{tb_name}'", db=db
    )
    if len(result) == 0:
        return None
    else:
        return result[0][1]

class LogCrawler:
    def __init__(self, address, topic0, abi_path, 
                prepare_func, map_funcs, start_block_func):
        self.address = address
        self.topic = topic0

        abi = json.load(open(abi_path))
        self.topic_map = eth_event.get_topic_map(abi)

        self.prepare_func = prepare_func
        self.map_funcs = map_funcs
        self.start_block_func = start_block_func
    
    def filter_id(self, web3, from_block, to_block):
        return get_filter_id(web3, from_block, to_block,
                    self.address, [self.topic])
    
    def prepare(self, args):
        self.prepare_func(args)

    def action(self, web3, from_block, to_block, args):
        filt_id, _ = self.filter_id(web3, from_block, to_block)
        logs = web3.eth.get_filter_logs(filt_id)
        record = map(lambda x : log_to_dict(self.topic_map, x), logs)
        for r in record:
            for f in self.map_funcs:
                f(r, args)
    
    def get_start_block(self):
        return self.start_block_func()

def create_hero_auction_success_table(args):
    db = args['db']
    database_utils.execute_query(db, 
        database_utils.create_hero_auction_success_table_sql
    )

def create_table_track_table(args):
    db = args['db']
    database_utils.execute_query(db, 
        database_utils.create_table_track_table_sql
    )

auction_success_crawler = LogCrawler(
    "0x13a65b9f8039e2c032bc022171dc05b30c3f2892",
    "0xe40da2ed231723b222a7ba7da994c3afc3f83a51da76262083e38841e2da0982",
    "abi/SaleAuction.json",
    create_hero_auction_success_table,
    [database_utils.insert_auction_success_record],
    (lambda : get_table_updated_block(
        database_utils.HERO_AUCTION_SUCCESS_TABLE_NAME
    ))
)

dfk_important_log_crawlers = {
    "Auction Success": (
        auction_success_crawler, 
        database_utils.HERO_AUCTION_SUCCESS_TABLE_NAME, 
        None
    )
}

to_update_table_names = [
    database_utils.HERO_AUCTION_SUCCESS_TABLE_NAME
]

def update_table_track(name, db, num):
    database_utils.insert_or_update_table_track(
        db, name, num
    )

def special_log_crawling(crawler, name, tb_name,
    start_block = None, step = 10000, diff = EPOCH_NUMBER):
    web3 = Web3(Web3.HTTPProvider("https://api.harmony.one"))

    db = database_utils.connect_db(database_utils.DATABASE_FILE)
    args = {}
    args['db'] = db
    create_table_track_table(args)

    if db:
        crawler.prepare(args)
        
        start_block = DFK_START_BLOCK if start_block is None else start_block
        end_block = web3.eth.get_block_number()

        end_epoch = (end_block - start_block) // diff + 1

        for count, epcoh_start in enumerate(range(start_block, end_block, diff)):
            start_time = time.time()
            for i in range(epcoh_start, epcoh_start + diff, step):
                crawler.action(web3, i, i + step, args)

                progress = (i - epcoh_start + step) / diff * 100
                print(min(progress, 100), end = '\r')
            till = min(epcoh_start + diff - 1, end_block)

            update_table_track(tb_name, db, till)
            print(f"({name}) Epoch ({count+1}/{end_epoch}): finished with " +
                    str(time.time() - start_time) + " seconds")

        db.close()
    else:
        print("DB errror")


def update_tables(crawlers):
    # Can change to concurrent approach
    for name in crawlers:
        (c, tb_name, start) = crawlers[name]
        start = c.get_start_block() if start is None else start
        special_log_crawling(c, name, tb_name, start_block=start)

def init_db():
    db = database_utils.connect_db(database_utils.DATABASE_FILE)

    if db is None:
        return

    args = {}
    args['db'] = db
    create_table_track_table(args)
    db.close()


def main():
    init_db()
    update_tables(dfk_important_log_crawlers)

if __name__ == '__main__':
    main()


