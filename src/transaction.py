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
    
    
    def read(position=0, amount=10):

        print(f"[TRANSACTION]({datetime.now()}): Start read")
        try:
            print("[TRANSACTION-FILE]: Start Read")

            amount_readed = 0

            with open(DATABASE_TRANSACTION_PATH, "r") as file:
                file.seek(position)  

                transactions = []
                for _ in range(amount):
                    try:
                        linha = file.readline() 
                        if linha:
                            transaction = json.loads(linha)
                            transactions.append(transaction['transaction'])
                        else:
                            print("[TRANSACTION-FILE]: EOF")
                            break  # Interrompe a leitura caso encontre o final do arquivo

                        if amount_readed == amount:
                            break  # Interrompe a leitura se já atingiu a quantidade desejada
                    except json.JSONDecodeError:
                        print("[TRANSACTION-FILE-ERROR]: Conversion to JSON")
                        continue

                    amount_readed = amount_readed + 1

                last_position = file.tell()  # Obtém a posição do ponteiro de leitura atual

            print(f"[TRANSACTION-FILE]: amount readed => {amount_readed}")
            print("[TRANSACTION-FILE]: End read")
            print("[TRANSACTION]: End read")

            return transactions, last_position

        except IOError:
            print("[TRANSACTION-FILE-ERROR]: Can't open")
            print("[TRANSACTION]: End read")
            return None

    def create(self, sender, receiver, value=1):
        
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