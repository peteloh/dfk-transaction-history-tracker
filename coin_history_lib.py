import datetime
from hero_auction_crawler import init_db, update_table_track
from database_utils import execute_query, select_table
import database_utils
from pypika import Query, Table
import json
import requests
import time
from pycoingecko import CoinGeckoAPI
import datetime

COIN_START_TIME = 1629673200
WEEK_DIFF = 604800
GRAPHQL_STEP_LIMIT = WEEK_DIFF * 5
YEAR_DIFF = 31556926

def get_coin_table_name(coin):
    return coin + "_price_usd"

def create_coin_table(db, coin):
    table_name = get_coin_table_name(coin)
    sql =  f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        time     INTEGER PRIMARY KEY,
        priceUSD REAL
    );
    """
    return execute_query(db, sql)

def insert_coin_table(db, coin, time, price):
    query = Query.into(get_coin_table_name(coin))\
        .columns(
            'time',
            'priceUSD'
        )\
        .insert(time, price)
    sql = query.get_sql()
    return execute_query(db, sql)

def get_coin_price(coin, time, db=None):
    r = select_table(
        get_coin_table_name(coin),
        where=f"time={time}",
        db=db
    )

    if len(r) != 0:
        return r[0]
    else:
        return None

def get_coin_latest_time(coin, print_error = False):
    db = database_utils.connect_db(database_utils.DATABASE_FILE)
    if db is None:
        return None

    tb_name = get_coin_table_name(coin)
    sql = f"select max(time) from {tb_name};"
    cur = db.cursor()
    
    result = None
    try:
        result = cur.execute(sql)
        result = list(result)

        if len(result) > 0:
            result = result[0][0]

    except Exception as e:
        if print_error:
            print(e)
    
    if db is not None:
        db.close()

    return result


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


def coin_price_crawling(coin, source_func, start_time = None, 
                        step = GRAPHQL_STEP_LIMIT, diff = YEAR_DIFF):
    db = database_utils.connect_db(database_utils.DATABASE_FILE)

    if db:
        r = create_coin_table(db, coin)
        if not r:
            print("Error")
            return
        
        if start_time is None:
            start_time = get_coin_latest_time(coin)
        
        if start_time is None:
            start_time = COIN_START_TIME

        end_time = int(time.time())
        end_epoch = (end_time - start_time) // diff + 1
        print(f"Crawling price from {start_time} to {end_time}")

        for count, epcoh_start in enumerate(range(start_time, end_time, diff)):
            measure_start = time.time()
            for i in range(epcoh_start, min(epcoh_start + diff, end_time), step):
                till = min(i + step, end_time)
                result = source_func(i, till)
                time.sleep(60)

                for t, p in result:
                    insert_coin_table(db, coin, t, p)

                progress = (i - epcoh_start + step) / diff * 100
                print(min(progress, 100), end = '\r')

            print(f"({coin}) Epoch ({count+1}/{end_epoch}): finished with " +
                    str(time.time() - measure_start) + " seconds")

        db.close()
    else:
        print("DB errror")

def get_jewel_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    jewel_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='defi-kingdoms', date=x[count])

        if 'market_data' in result:
            jewel_usd[count] = result['market_data']['current_price']['usd']

    return zip(date_generated, jewel_usd)

def get_dfktears_jewel_price(period_start, period_end):  ##maybe wrong
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    dfktears_jewel = list(range(len(date_generated)))
    count = -1
    for date in date_generated[:-1]:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date_generated[count]).strftime('%d-%m-%Y'))
        dfktears_jewel[count] = (cg.get_coin_history_by_id(id='gaias-tears', date=x[count]))['market_data']['current_price']['eur']
    dfktears_jewel[len(date_generated)-1] = cg.get_price(ids='gaias-tears', vs_currencies='usd')["gaias-tears"]["usd"]

    return zip(date_generated, dfktears_jewel)

def get_xjewel_usd_price(period_start, period_end):
    date = [1640044800, 1640131200, 1640217600, 1640304000, 1640390400, 1640476800, 1640563200, 1640649600, 1640736000, 1640822400, 1640908800, 1640995200, 1641081600, 1641168000]
    price = [21.5839, 22.8925, 23.5467, 23.4278, 23.4872, 24.1415, 23.9631, 21.7029, 21.1081, 20.7513, 21.5245, 24.9147, 30.7435, 31.2788]
    return zip(date, price)

def get_dfkshvas_usd_price(period_start, period_end):
    date = [1640044800, 1640131200, 1640217600, 1640304000, 1640390400, 1640476800, 1640563200, 1640649600, 1640736000, 1640822400, 1640908800, 1640995200, 1641081600, 1641168000]
    price = [34.669, 32.7839, 34.1978, 26.893, 27.8356, 27.893, 23.5941, 26.6574, 23.5941, 22.8872, 19.5883, 27.1287, 24.4188, 24.6642]
    return zip(date, price)

def get_dfkgold_usd_price(period_start, period_end):
    date = [1640044800, 1640131200, 1640217600, 1640304000, 1640390400, 1640476800, 1640563200, 1640649600, 1640736000, 1640822400, 1640908800, 1640995200, 1641081600, 1641168000]
    price = [0.02152, 0.02482, 0.0237, 0.02058, 0.01826, 0.01683, 0.01588, 0.0176, 0.01442, 0.0135, 0.01691, 0.01637, 0.01978, 0.01877]
    return zip(date, price)

def get_wbtc_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    wbtc_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='wrapped-bitcoin', date=x[count])

        if 'market_data' in result:
            wbtc_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, wbtc_usd)

def get_wone_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    wone_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='wrapped-one', date=x[count])

        if 'market_data' in result:
            wone_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, wone_usd)

def get_wusdc_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    wusdc_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='wrapped-usdc', date=x[count])

        if 'market_data' in result:
            wusdc_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, wusdc_usd)

def get_wusdc_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    wusdc_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='wrapped-usdc', date=x[count])

        if 'market_data' in result:
            wusdc_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, wusdc_usd)

def get_busd_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    busd_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='binance-usd', date=x[count])

        if 'market_data' in result:
            busd_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, busd_usd)
    
def get_ust_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    ust_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='terrausd', date=x[count])

        if 'market_data' in result:
            ust_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, ust_usd)

def get_matic_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    matic_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='matic-network', date=x[count])

        if 'market_data' in result:
            matic_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, matic_usd)

def get_eth_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    eth_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='ethereum', date=x[count])

        if 'market_data' in result:
            eth_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, eth_usd)

def get_dai_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    dai_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='dai', date=x[count])

        if 'market_data' in result:
            dai_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, dai_usd)

def get_AVAX_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    AVAX_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='avalanche-2', date=x[count])

        if 'market_data' in result:
            AVAX_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, AVAX_usd)

def get_luna_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    luna_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='terra-luna', date=x[count])

        if 'market_data' in result:
            luna_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, luna_usd)

def get_usdt_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    usdt_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='tether', date=x[count])

        if 'market_data' in result:
            usdt_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, usdt_usd)

def get_link_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    link_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='chainlink', date=x[count])

        if 'market_data' in result:
            link_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, link_usd)

def get_superbid_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    superbid_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='superbid', date=x[count])

        if 'market_data' in result:
            superbid_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, superbid_usd)


def get_bnb_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    bnb_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='binancecoin', date=x[count])

        if 'market_data' in result:
            bnb_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, bnb_usd)

def get_mis_usd_price(period_start, period_end):
    cg = CoinGeckoAPI()
    date_generated = [ i for i in range(period_start, period_end, 86400)]
    x = list(range(len(date_generated)))
    mis_usd = list(range(len(date_generated)))
    count = -1
    for date in date_generated:
        count +=1
        x[count] = str(datetime.datetime.fromtimestamp(date).strftime('%d-%m-%Y'))
        result = cg.get_coin_history_by_id(id='artemis', date=x[count])

        if 'market_data' in result:
            mis_usd[count] = result['market_data']['current_price']['usd']
    return zip(date_generated, mis_usd)

