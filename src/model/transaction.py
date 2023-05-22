from config import database_transaction_path
from src.model.wallet import wallet
import hashlib
import json
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
        
        (error, sender) = wt.search(sender)
        if error != None:
            return (error, None)

        (error, receiver) = wt.search(receiver)
        if error != None:
            return (error, None)

        if sender['funds'] == 0 or sender['funds'] - value < 0:
            print(f"{sender['wallet']}: Insuficients funds") # ja votou
            error = f"{sender['wallet']}: Insuficients funds"
            return (error, None)

        if sender['actions'] == 'r':
            print(f"{sender['wallet']}: Already voted")
            error = f"{sender['wallet']}: Insuficients funds"
            return (error, None)

        timestamp = str(time.time())
        transaction_hash = self.__create_hash(sender['wallet'], receiver['wallet'], value, timestamp)

        transaction = {
            'transaction': transaction_hash,
            'sender': sender['wallet'],
            'receiver': receiver['wallet'],
            'value': value,
            'timestamp': timestamp
        }

        try:
            with open(database_transaction_path, 'a') as file:
                json.dump(transaction, file)
                file.write('\n')
        except FileNotFoundError:
            with open(database_transaction_path, 'w') as file:
                json.dump(transaction, file)
                file.write('\n')  

        wt.update_funds(sender['wallet'], -value)
        wt.update_funds(receiver['wallet'], value)

        return (error, transaction)

