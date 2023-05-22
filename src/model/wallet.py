from config import database_wallet_path
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
        hash_result = self.__create_hash(user)
        
        wallet = {
            "wallet": hash_result,
            "actions": actions,
            "funds": 1
        }
        
        try:
            with open(database_wallet_path, "a") as file:
                json.dump(wallet, file)
                file.write('\n')
        except FileNotFoundError:
            with open(database_wallet_path, "w") as file:
                json.dump(wallet, file)
                file.write('\n')

        return wallet.get("wallet")
    
    def search(self, wallet):

        wallet_data = ""
        error = None

        try: 
            with open(database_wallet_path, "r") as file:
                line = file.readline()
                while line:
                    wallet_data = json.loads(line)
                    if wallet_data['wallet'] == wallet:
                        break
                    line = file.readline()
        except FileNotFoundError:
            error = "[ERROR]: File not found"
            print("[ERROR]: File not found")

        return (error, wallet_data)
    
    def update_funds(self, wallet, value):
        wallet_data = None
        error = None
        found_wallet = False

        try:
            with open(database_wallet_path, 'r+') as file:
                while True:
                    current_position = file.tell()
                    line = file.readline()
                    if not line:
                        break

                    try:
                        wallet_data = json.loads(line.strip())
                    except json.JSONDecodeError:
                        print(f"Invalid JSON format: {line.strip()}")
                        continue

                    if wallet_data['wallet'] == wallet:
                        wallet_data['funds'] += value
                        wallet_data['actions'] = wallet_data['actions'].replace("s", "").strip() if value < 0 else wallet_data['actions']
                        file.seek(current_position)
                        serialized_data = json.dumps(wallet_data)
                        if len(line.strip()) > len(serialized_data):
                            serialized_data += ' ' * (len(line.strip()) - len(serialized_data))
                        #log aqui
                        file.write(serialized_data)
                        break
        except Exception as e:
            error = e
            wallet_data = None
            print("{0}".format(e))

        return (error, wallet_data)