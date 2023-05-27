from src.transaction import transaction
from src.blockchain import blockchain

blc = blockchain()

blc.create_block()
blc.create_block()
blc.create_block()







# from src.transaction import transaction
# from src.wallet import wallet

# tr = transaction()

# sender = "708d09db5f414bf1e41dc43d28fdf4ecc60bee75c66c829004ac27353e9f1f0a"
# receiver = "98b0f00a6a32d9f13fe5fb0ee286615b78e69576d35592eab0b53ca9c38cbaa3"
# value = 10

# tr.create(sender, receiver, value)









# from src.model.user import user
# import tkinter as tk

# # Exemplo de uso da função
# nome = "Cleuto"
# sobrenome = "Fazen do Chaon"
# cpf = "09878665431"
# data_aniversario = "23/03/1997"
# actions = "sr"

# print(user.create(nome, sobrenome, data_aniversario, cpf, actions))
# print(user.read(cpf))

# nome = "Juca"
# sobrenome = "Castelo de Madeira"
# cpf = "12345678912"
# data_aniversario = "19/02/1993"
# actions = "sr"

# print(user.create(nome, sobrenome, data_aniversario, cpf, actions))
# print(user.read(cpf))



