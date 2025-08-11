


from Block import Block
from Blockchain import Blockchain
from Transaction import Transaction

my_coin = Blockchain()

for i in range(25):
	sender = f"User{i}"
	recipient = f"User{i+1}"
	amount = (i+1) * 10
	my_coin.add_transaction(Transaction(sender, recipient, amount))


print("Blockchain valid?", my_coin.is_chain_valid())


if len(my_coin.chain) > 2:
	print(repr(my_coin.chain[2]))

