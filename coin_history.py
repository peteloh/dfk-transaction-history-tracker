import coin_history_lib

IMPORTANT_COINS = {
    'JEWEL': [
        (lambda s,e : coin_history_lib.get_coin_graphql('JEWEL', s, e)),
        coin_history_lib.get_jewel_usd_price
    ],
    'DFKTEARS': [
        (lambda s,e : coin_history_lib.get_coin_graphql('DFKTEARS', s, e)),
        coin_history_lib.get_dfktears_jewel_price
    ],
    'xJEWEL': [
        (lambda s,e : coin_history_lib.get_coin_graphql('xJEWEL', s, e))
    ],
    'DFKGOLD': [
        (lambda s,e : coin_history_lib.get_coin_graphql('DFKGOLD', s, e))
    ],
    'DFKSHVAS': [
        (lambda s,e : coin_history_lib.get_coin_graphql('DFKSHVAS', s, e))
    ],
    'wbtc': [
        (lambda s,e : coin_history_lib.get_wbtc_usd_price(s, e)),
    ],
    'wone': [
        (lambda s,e : coin_history_lib.get_wone_usd_price(s, e)),
    ],
    'wusdc': [
        (lambda s,e : coin_history_lib.get_wusdc_usd_price(s, e)),
    ],
    'busd': [
        (lambda s,e : coin_history_lib.get_busd_usd_price(s, e)),
    ],
    'ust': [
        (lambda s,e : coin_history_lib.get_ust_usd_price(s, e)),
    ],
    'matic': [
        (lambda s,e : coin_history_lib.get_matic_usd_price(s, e)),
    ],
    'eth': [
        (lambda s,e : coin_history_lib.get_eth_usd_price(s, e)),
    ],
    'dai': [
        (lambda s,e : coin_history_lib.get_dai_usd_price(s, e)),
    ],
    'AVAX': [
        (lambda s,e : coin_history_lib.get_AVAX_usd_price(s, e)),
    ],
    'luna': [
        (lambda s,e : coin_history_lib.get_luna_usd_price(s, e)),
    ],
    'usdt': [
        (lambda s,e : coin_history_lib.get_usdt_usd_price(s, e)),
    ],
    'link': [
        (lambda s,e : coin_history_lib.get_link_usd_price(s, e)),
    ],
    'superbid': [
        (lambda s,e : coin_history_lib.get_superbid_usd_price(s, e)),
    ],
    'bnb': [
        (lambda s,e : coin_history_lib.get_bnb_usd_price(s, e)),
    ],
    'mis': [
        (lambda s,e : coin_history_lib.get_mis_usd_price(s, e)),
    ],
}

if __name__ == '__main__':
    for c in IMPORTANT_COINS:
        src_func = IMPORTANT_COINS[c]
        for f in src_func:
            coin_history_lib.coin_price_crawling(c, f)