import os

blockchain_path = os.path.realpath("./database/blockchain")

database_user_path = os.path.realpath("./database/users/users.json")
database_wallet_path = os.path.realpath("./database/wallets/wallets.json")
database_transaction_path = os.path.realpath("./database/transactions/transactions.json")

log_user_path = os.path.realpath("./logs/users.txt")
log_wallet_path = os.path.realpath("./logs/wallets.txt")
log_transaction_path = os.path.realpath("./logs/transactions.txt")
log_blockchain_path = os.path.realpath("./logs/blockchain.txt")