from web3 import Web3

current_chain = "harmony"

# mainnet urls
chain_url = {
    "harmony": "https://api.harmony.one",
    "avalanche": "https://api.avax.network/",
    "fantom": "https://xapi.fantom.network/",
}

web3 = Web3(Web3.HTTPProvider(chain_url[current_chain]))