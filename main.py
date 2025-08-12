import time
from Blockchain import Blockchain
from Transaction import Transaction
from Account import Account


# Create accounts
alice = Account()
bob = Account()

# Alice creates & signs transaction
timestamp = time.ctime()
message = alice.public_key + bob.address.encode() + str(50).encode() + timestamp.encode()
signature = alice.sign(message)

tx = Transaction(
    sender_public_key=alice.public_key,
    recipient_address=bob.address,
    amount=50,
    signature=signature,
    timestamp=timestamp
)


# Add to blockchain
my_coin = Blockchain()
for i in range(5):
    timestamp = time.ctime()
    message = alice.public_key + bob.address.encode() + str(50 + i).encode() + timestamp.encode()
    signature = alice.sign(message)
    tx = Transaction(
        sender_public_key=alice.public_key,
        recipient_address=bob.address,
        amount=50 + i,
        signature=signature,
        timestamp=timestamp
    )
    print(f"Adding transaction {i+1}...")
    my_coin.add_transaction(tx)

print("All 5 transactions added. Mining and block addition should be visible above.")