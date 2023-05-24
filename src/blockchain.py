import os
from config import BLOCKCHAIN_PATH
from src.block import block
import json


class blockchain:

    def __init__(self) -> None:
        
        print("[BLOCKCHAIN]: Start")

        _number_of_blocks = self.read_last_id()

        print("[BLOCKCHAIN]: Start complete")

    def read_last_id(self):

        print("[BLOCKCHAIN]: Start read last id")

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
                            return data.get("id", 0)
            print("[BLOCKCHAIN-FOLDER]: No block_file found")
            raise FileNotFoundError
        except FileNotFoundError:
            print("[BLOCKCHAIN-FILE]: Start create genesis_block")
            file_path = os.path.join(BLOCKCHAIN_PATH, "block_0.json")
            with open(file_path, "w") as file:
                print("[BLOCKCHAIN-CALL]:[BLOCK]")
                genesis_block = block(0, "GENESIS_BLOCK", "")
                genesis_block.calculate_block()

                genesis_block = {
                    "id": genesis_block.id,
                    "hash": genesis_block.hash,
                    "nonce": genesis_block.nonce,
                    "timestamp": genesis_block.timestamp,
                    "payload": genesis_block.payload,
                    "previous_hash": genesis_block.previous_hash
                }

                json.dump(genesis_block, file)
                file.write('\n')
            print("[BLOCKCHAIN-FILE]: End create genesis_block")
            return 0
