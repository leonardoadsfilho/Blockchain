from datetime import datetime
from config import DATABASE_WALLET_PATH
import hashlib
import json
import fileinput
import time

class wallet:

    def __init__(self) -> None:
        pass

    def __create_hash(self, user):
        concatened_data = user.get("name") + user.get("last_name") + user.get("birth_date") + user.get("cpf")
        hash_object = hashlib.sha256(concatened_data.encode())
        return hash_object.hexdigest()

    def create(self, user, actions):
        
        print("[WALET]: Creating hash")
        print(f"[WALLET]: Start register")

        hash_result = self.__create_hash(user)
        
        wallet = {
            "wallet": hash_result,
            "actions": actions,
            "funds": 1
        }
        
        try:
            print(f"[WALLET-FILE]: Start append")
            with open(DATABASE_WALLET_PATH, "a") as file:
                json.dump(wallet, file)
                file.write('\n')
            print(f"[WALLET-FILE]: End append")
        except FileNotFoundError:
            
            print(f"[WALLET-FILE]: Start write")
            with open(DATABASE_WALLET_PATH, "w") as file:
                json.dump(wallet, file)
                file.write('\n')
            print(f"[WALLET-FILE]: End write")

        print(f"[WALLET]: End register")

        return wallet.get("wallet")
    
    def search(self, wallet):

        wallet_data = ""
        error = None

        print(f"[WALLET]({datetime.now()}): Search start => {wallet}")

        try: 
            print(f"[WALLET-FILE]: Search start")
            with open(DATABASE_WALLET_PATH, "r") as file:
                line = file.readline()
                while line:
                    wallet_file_data = json.loads(line)
                    if wallet_file_data['wallet'] == wallet:
                        wallet_data = wallet_file_data
                        print("[WALLET]: Found")
                        break
                    line = file.readline()
                print("[WALLET]: Not found")
                
            print(f"[WALLET-FILE]: Search end")                
        except FileNotFoundError:
            error = "[WALLET-FILE-ERROR]: File not found"
            print(error)

        print(f"[WALLET]: Search end => {wallet}")

        return (error, wallet_data)
    
    def update_funds(self, wallet, value):
        wallet_data = None
        error = None

        print(f"[WALLET]: Start update => {wallet}")

        try:
            print("[WALLET-FILE]: Start searching")
            with open(DATABASE_WALLET_PATH, 'r+') as file:
                while True:
                    current_position = file.tell()
                    line = file.readline()
                    if not line:
                        break

                    try:
                        wallet_data = json.loads(line.strip())
                    except json.JSONDecodeError:
                        print(f"[WALLET-FILE-WARNING]: Invalid JSON format {line.strip()}")
                        continue

                    if wallet_data['wallet'] == wallet:
                        print("[WALLET-FILE]: Updating...")
                        wallet_data['funds'] += value
                        wallet_data['actions'] = wallet_data['actions'].replace("s", "").strip() if value < 0 else wallet_data['actions']
                        file.seek(current_position)
                        serialized_data = json.dumps(wallet_data)
                        if len(line.strip()) > len(serialized_data):
                            serialized_data += ' ' * (len(line.strip()) - len(serialized_data))
                        file.write(serialized_data)
                        print("[WALLET-FILE]: Update success")
                        break

            print("[WALLET-FILE]: End processing")
        except Exception as e:
            error = e
            wallet_data = None
            print("[WALLET-ERROR]: {0}".format(e))

        print(f"[WALLET]({datetime.now()}): End update => {wallet}")

        return (error, wallet_data)