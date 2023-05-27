from datetime import datetime
import hashlib
import os
from config import BLOCKCHAIN_PATH
from src.block import block
from src.transaction import transaction
import json


class blockchain:

    def __init__(self) -> None:
        
        print(f"[BLOCKCHAIN]({datetime.now()}): Start")
        self.last_id, self.previous_hash = self.read_last_id()
        self.transactions = []
        self.transactions_position = 0
        print("[BLOCKCHAIN]: Start complete")
        
    def __register_block(self, block):

        print(f"[BLOCKCHAIN-FILE]({datetime.now()}): Start register a new block")
        file_path = os.path.join(BLOCKCHAIN_PATH, f"block_{block.id}.json")

        with open(file_path, "a") as file:

            register_block = {
                "id": block.id,
                "hash": block.hash,
                "nonce": block.nonce,
                "timestamp": block.timestamp,
                "payload": block.payload,
                "transactions": block.transactions,
                "previous_hash": block.previous_hash
            }

            json.dump(register_block, file)
            file.write('\n')
        print("[BLOCKCHAIN-FILE]: End register a new block")

    def create_block(self, position=-1, amount=0):

        if position <= -1:
            position = self.transactions_position

        if amount <= 0:
            amount = 10

        self.transactions, self.transactions_position = transaction.read(position, amount)

        payload = self.__calculate_markle_tree_root()

        print("[BLOCKCHAIN-CALL]:[BLOCK]")
        new_block = block(self.last_id + 1, payload, self.transactions, self.previous_hash)

        self.previous_hash, self.last_id = new_block.calculate_block()

        self.__register_block(new_block)

        self.transactions.clear()

        return new_block

    def read_last_id(self):

        print(f"[BLOCKCHAIN]({datetime.now()}): Start read last id")

        last_id = -1
        previous_hash = ""

        try:

            print("[BLOCKCHAIN-FOLDER]: Reading search last block_file")
            file_list = os.listdir(BLOCKCHAIN_PATH)
            file_list.sort(reverse=True)
            
            for file_name in file_list:
                if file_name.startswith("block_") and file_name.endswith(".json"):
                    print("[BLOCKCHAIN-FILE]: Start reading id")
                    file_path = os.path.join(BLOCKCHAIN_PATH, file_name)
                    with open(file_path, "r") as file:
                        lines = file.readlines()
                        if lines:
                            last_line = lines[-1]
                            data = json.loads(last_line)
                            print("[BLOCKCHAIN-FILE]: End reading id")
                            last_id = data.get("id", 0)
                            previous_hash = data.get("hash", 0)
                            break
            if last_id == -1:
                print("[BLOCKCHAIN-FOLDER]: No block_file found")
                raise FileNotFoundError
            else:
                print(f"[BLOCKCHAIN-FOLDER]: Block_file found => {last_id}")

        except FileNotFoundError:
            print("[BLOCKCHAIN-FILE]: Start create and register genesis_block")
            file_path = os.path.join(BLOCKCHAIN_PATH, "block_0.json")
            with open(file_path, "w") as file:
                print("[BLOCKCHAIN-CALL]:[BLOCK]")
                last_id = 0
                genesis_block = block(0, "GENESIS_BLOCK", [], "")
                previous_hash, _ = genesis_block.calculate_block()

                genesis_block = {
                    "id": genesis_block.id,
                    "hash": genesis_block.hash,
                    "nonce": genesis_block.nonce,
                    "timestamp": genesis_block.timestamp,
                    "payload": genesis_block.payload,
                    "transactions": [],
                    "previous_hash": genesis_block.previous_hash
                }

                json.dump(genesis_block, file)
                file.write('\n')
            print("[BLOCKCHAIN-FILE]: End create and register genesis_block")
        
        print("[BLOCKCHAIN]: End read last id")

        return (last_id, previous_hash)
    

    def __calculate_markle_tree_root(self):

        print(f"[BLOCKCHAIN]({datetime.now()}): Start create markle tree")

        def calcular_hash(transaction):
            transaction_str = str(transaction)
            return hashlib.sha256(transaction_str.encode()).hexdigest()

        hashes = [calcular_hash(transaction) for transaction in self.transactions]

        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])  

            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined_hash = hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
                new_hashes.append(combined_hash)

            hashes = new_hashes

        print("[BLOCKCHAIN]: End create markle tree")
        print(f"[BLOCKCHAIN]: Return markle tree root => {hashes[0]}")
        return hashes[0]  