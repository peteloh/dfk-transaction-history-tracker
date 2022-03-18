# Defi Kingdoms Trasnaction History Tracker

inputs from user: 
start time:
end time:
wallet address:

DFK_transactions objects:
    list of transactions:
        blocknumber
        description
        list of events:
            ...
            ...
            ...
            ...


csv output:

trasnaction history 
    timestamp:
    labels: 
        quest reward
        ...
        ...
        ...
    Hero ID (if hero related):
    amount (number of token):
    price (in USD):
    value (in USD):

dependency:
- web3
- eth-event
- pypika
- pycoingecko

clone this repo and run locally using: "streamlit run main.py"
