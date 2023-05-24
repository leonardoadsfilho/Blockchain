from config import DATABASE_TRANSACTION_PATH
from src.wallet import wallet
import hashlib
import json
from datetime import datetime
import time

class transaction:

    def __init__(self) -> None:
        pass

    def __create_hash(self, sender, receiver, value, timestamp):
        concatened_data = sender + receiver + str(value) + timestamp
        hash_object = hashlib.sha256(concatened_data.encode())
        return hash_object.hexdigest()

    def create(self, sender, receiver, value):
        
        wt = wallet()
        error = None
        
        print(f"[TRANSACTION]({datetime.now()}): Start create")

        print("[TRANSACTION-CALL]:[WALLET]")
        (error, sender) = wt.search(sender)
        if error != None or sender == "":
            return (error, None)

        if sender['funds'] == 0 or sender['funds'] - value < 0:
            error = f"[TRANSACITON]: Insuficients funds => {sender['wallet']}:"
            print(error)
            return (error, None)
        
        if sender['actions'] == 'r':
            error = f"[TRANSACTION]: Already voted => {sender['wallet']}"
            print(error)            
            return (error, None)
        
        if sender['actions'] == '':
            error = f"[TRANSACTION]: Can't vote => {sender['wallet']}"
            print(error)            
            return (error, None)

        print("[TRANSACTION-CALL]:[WALLET]")
        (error, receiver) = wt.search(receiver)
        if error != None or receiver == "":
            return (error, None)

        if receiver['actions'] == '' or receiver['actions'] == 's':
            error = f"[TRANSACTION]: Can't receive a vote => {sender['wallet']}"
            print(error)            
            return (error, None)

        timestamp = str(time.time())
        print("[TRANSACTION]: Creating hash")
        transaction_hash = self.__create_hash(sender['wallet'], receiver['wallet'], value, timestamp)

        transaction = {
            'transaction': transaction_hash,
            'sender': sender['wallet'],
            'receiver': receiver['wallet'],
            'value': value,
            'timestamp': timestamp
        }

        print("[TRANSACTION-FILE]: Start register")
        try:

            print("[TRANSACTION-FILE]: Start append")
            with open(DATABASE_TRANSACTION_PATH, 'a') as file:
                json.dump(transaction, file)
                file.write('\n')
            print("[TRANSACTION-FILE]: End append")
        except FileNotFoundError:

            print("[TRANSACTION-FILE]: Start write")
            with open(DATABASE_TRANSACTION_PATH, 'w') as file:
                json.dump(transaction, file)
                file.write('\n')  
            print("[TRANSACTION-FILE]: End write")
            
        print("[TRANSACTION-FILE]: End register")

        print("[TRANSACTION-CALL]:[WALLET]")
        wt.update_funds(sender['wallet'], -value)
        
        print("[TRANSACTION-CALL]:[WALLET]")
        wt.update_funds(receiver['wallet'], value)

        print(f"[TRANSACTION]({datetime.now()}): End create")

        return (error, transaction)

