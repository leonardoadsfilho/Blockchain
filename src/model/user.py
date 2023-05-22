from src.model.wallet import wallet
from config import database_user_path
import json
import time

# create_user() => (ERROR, WALLET)

class user:

    def __init__(self) -> None:
        pass

    def create(name, last_name, birth_date, cpf, actions):
        user = {
            "name": name,
            "last_name": last_name,
            "birth_date": birth_date,
            "cpf": cpf,
            "register_time": str(time.time())
        }

        exist_cpf = False

        try: 
            with open(database_user_path, "r") as file:
                line = file.readline()
                while line:
                    exist_user = json.loads(line)
                    if exist_user["cpf"] == cpf:
                        exist_cpf = True
                        break
                    line = file.readline()

            if not exist_cpf:
                with open(database_user_path, "a") as file:
                    json.dump(user, file)
                    file.write('\n')
            else:
                return ("User already exists", None)
        except FileNotFoundError:
            with open(database_user_path, "w") as file:
                json.dump(user, file)
                file.write('\n')                
            
        return (None, wallet().create(user, actions))
    
    def read(cpf):
        exist_user = ""
        
        try: 
            with open(database_user_path, "r") as file:
                line = file.readline()
                while line:
                    exist_user = json.loads(line)
                    if exist_user["cpf"] == cpf:
                        break
                    line = file.readline()
                
        except FileNotFoundError:
            exist_user = "[ERROR]: File not found"
            print(f"[ERROR]: File not found")

        return exist_user
        