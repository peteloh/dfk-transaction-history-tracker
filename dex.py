# getting uniswap gardencontracts
from web3 import Web3
from main import chain_url, current_chain
web3 = Web3(Web3.HTTPProvider(chain_url[current_chain]))

import json

gardens_token = {
    "0x72Cb10C6bfA5624dD07Ef608027E366bd690048F": "Jewels",
    "0xcf664087a5bb0237a0bad6742852ec6c8d69a27a": "WONE",
    "0x985458e523db3d53125813ed68c274899e9dfab4": "1USDC",
    "0xe176ebe47d621b984a73036b9da5d834411ef734": "BUSD",
    "0x224e64ec1bdce3870a6a6c777edd450454068fec": "UST",
    "0x301259f392b551ca8c592c9f676fcd2f9a0a84c5": "1MATIC",
    "0x6983D1E6DEf3690C4d616b13597A09e6193EA013": "1ETH",
    "0x0ab43550a6915f9f67d0c454c2e90385e6497eaa": "bscBUSD",
    "0xef977d2f931c1978db5f6747666fa1eacb0d0339": "1DAI",
    "0xb12c13e66ade1f72f71834f2fc5082db8c091358": "AVAX",
    "0x95ce547d730519a90def30d647f37d9e5359b6ae": "LUNA",
    "0x3c2b8be99c50593081eaa2a724f0b8285f5aba8f": "1USDT",
    "0x3095c7557bcb296ccc6e363de01b760ba031f2d9": "1WBTC",
    "0x218532a12a389a4a92fc0c5fb22901d1c19198aa": "LINK",
    "0x17fdedda058d43ff1615cdb72a40ce8704c2479a": "1SUPERBID",
    # LP-Tokens
    "0xeb579ddcd49a7beb3f205c9ff6006bb6390f138f": "JEWEL-ONE Pair",
    "0x68a73f563ba14d51f070A6ddD073177FB794190A": "ONE-1SUPERBID Pair",
    "0xEaB84868f6c8569E14263a5326ECd62F5328a70f": "JEWEL-1ETH Pair",
    "0xE01502Db14929b7733e7112E173C3bCF566F996E": "JEWEL-BUSD Pair",
    "0x751606585fcaa73bf92cf823b7b6d8a0398a1c99": "JEWEL-MIS Pair",
    "0xe7d0116dd1dbbba2efbad58f097d1ffbbedc4923": "JEWEL-bscBNB Pair",
    "0xa1221a5bbea699f507cc00bdedea05b5d2e32eba": "JEWEL-1USDC Pair",
    "0xb91a0dfa0178500fedc526f26a89803c387772e8": "JEWEL-UST Pair",
    "0x7f89b5f33138c89fad4092a7c079973c95362d53": "JEWEL-FTM Pair",
    "0x093956649d43f23fe4e7144fb1c3ad01586ccf1e": "JEWEL-AVAX Pair",
    "0x3e81154912e5e2cc9b10ad123bf14aeb93ae5318": "JEWEL-WMATIC Pair",
    "0x0acce15d05b4ba4dbedfd7afd51ea4fa1592f75e": "JEWEL-1WBTC Pair",
    "0xb6e9754b90b338ccb2a74fa31de48ad89f65ec5e": "JEWEL-LUNA Pair",
    "0x95f2409a44a9b989f8c5601037c513890e90cd06": "JEWEL-1SUPERBID Pair",
    "0x3733062773b24f9bafa1e8f2e5a352976f008a95": "JEWEL-XYA Pair",
    "0x3a0c4d87bde442150779d63c1c695d003184df52": "ONE-BUSD Pair",
    "0x66c17f5381d7821385974783be34c9b31f75eb78": "ONE-1USDC Pair",
    "0x864fcd9a42a5f6e0f76bc309ee26c8fab473fc3e": "ONE-1ETH Pair",
    "0x997f00485b238c83f7e58c2ea1866dfd79f04a4b": "1WBTC-1ETH Pair",
}

contract_address = web3.toChecksumAddress("0x9014B937069918bd319f80e8B3BB4A2cf6FAA5F7")
abi = json.load(open("abi/UniswapV2Factory.json"))
dex_contract = web3.eth.contract(address=contract_address, abi=abi)

print(dex_contract.all_functions())

token1_address = web3.toChecksumAddress("0x72Cb10C6bfA5624dD07Ef608027E366bd690048F")
token2_address = web3.toChecksumAddress("0xe176ebe47d621b984a73036b9da5d834411ef734")
pair_contract = dex_contract.functions.getPair(token1_address, token2_address).call()
print(pair_contract)