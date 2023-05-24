from datetime import datetime
from src.wallet import wallet
from config import DATABASE_USER_PATH
import json
import time

# create_user() => (ERROR, WALLET)

class user:

    def __init__(self) -> None:
        pass

    def create(name, last_name, birth_date, cpf, actions):

        print(f"[USER]({datetime.now()}): Start create")

        user = {
            "name": name,
            "last_name": last_name,
            "birth_date": birth_date,
            "cpf": cpf,
            "register_time": str(time.time())
        }

        exist_cpf = False
        user_wallet = ""
        error = None

        print(f"[USER-FILE]: Start register")

        try: 
            print(f"[USER-FILE]: Start search")
            
            with open(DATABASE_USER_PATH, "r") as file:
                line = file.readline()
                while line:
                    exist_user = json.loads(line)
                    if exist_user["cpf"] == cpf:
                        exist_cpf = True
                        print(f"[USER-FILE]: User already exists => {cpf}")
                        break
                    line = file.readline()

            print(f"[USER-FILE]: End search")

            print(f"[USER-FILE]: Start append")
            if not exist_cpf:
                with open(DATABASE_USER_PATH, "a") as file:
                    json.dump(user, file)
                    file.write('\n')
            print(f"[USER-FILE]: End append")         
        except FileNotFoundError:

            print(f"[USER-FILE]: Start write")
            with open(DATABASE_USER_PATH, "w") as file:
                json.dump(user, file)
                file.write('\n')              
            print(f"[USER-FILE]: End write")  
            
        print(f"[USER-FILE]: End register")         
        
        if(not exist_cpf):
            print(f"[USER-CALL][WALLET]")
            user_wallet = wallet().create(user, actions)

        print(f"[USER]({datetime.now()}): End create")

        return (None, user_wallet)
    
    def read(cpf):
        exist_user = ""
        
        try: 
            with open(DATABASE_USER_PATH, "r") as file:
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
        