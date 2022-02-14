# other py files
from contract_address import serendale_contracts
from decoder import decode_reciept, summarise_transaction
from networksetup import web3

def get_labelled_transaction(wallet_transactions):
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
                    labelled_transactions += summarise_transaction(receipt_decoded, tx_hash)
                    break
                elif key == receipt.logs[0]["address"]:
                    # only find block and timestamp when it is DFK contract
                    receipt_decoded = decode_reciept(receipt)
                    labelled_transactions += summarise_transaction(receipt_decoded, tx_hash)
        print(f"Prcoesseed {count} / {total_txs} transactions", end="\r")
        count += 1

    print("Got labelled_transaction!")
    return labelled_transactions

