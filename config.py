import os

BLOCKCHAIN_PATH = os.path.realpath("./database/blockchain")
DIFICCULTY = "0000"

DATABASE_USER_PATH = os.path.realpath("./database/users/users.json")
DATABASE_WALLET_PATH = os.path.realpath("./database/wallets/wallets.json")
DATABASE_TRANSACTION_PATH = os.path.realpath("./database/transactions/transactions.json")

LOG_USER_PATH = os.path.realpath("./logs/users.txt")
LOG_WALLET_PATH = os.path.realpath("./logs/wallets.txt")
LOG_TRANSACTION_PATH = os.path.realpath("./logs/transactions.txt")
LOG_BLOCKCHAIN_PATH = os.path.realpath("./logs/blockchain.txt")