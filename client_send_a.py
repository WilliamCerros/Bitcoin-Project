ledger = open("transactions.rtf", "w")

transactions = [100, 200, 300, 400, 500]

for transaction in transactions:
    ledger.write(str(transaction))
