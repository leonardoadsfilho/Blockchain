from config import DIFICCULTY
import time
import hashlib

class block:

    def __init__(self, id, payload, previous_hash) -> None:
        print("[BLOCK]: Create")
        self.id = id
        self.hash = ""
        self.nonce = 0
        self.timestamp = str(time.time())
        self.payload = payload
        self.previous_hash = previous_hash

    def calculate_block(self):
        
        nonce = 0

        print("[BLOCK]: Calculating hash...")
        while(True):

            concatened_data = str(nonce) + self.timestamp + self.payload + self.previous_hash
            hash_object = hashlib.sha256(concatened_data.encode()).hexdigest()
            print(hash_object[:4], DIFICCULTY)
            if hash_object[:4] == DIFICCULTY:
                self.nonce = nonce
                self.hash = hash_object
                break

            nonce = nonce + 1

        print("[BLOCK]: Hash calculate")
        print("[BLOCK]: End create")
            

    