
# Import required modules
import time
from Blockchain import Blockchain  # Blockchain class manages the chain and mining
from Transaction import Transaction  # Transaction class represents a transaction
from Account import Account  # Account class for public/private key management


# Create two accounts: Alice (sender) and Bob (recipient)
alice = Account()
bob = Account()
Daniel = Account()

chain = Blockchain()


# 1) give Alice some starting coins via a genesis UTXO (minimal approach)
chain.create_genesis_utxo(alice.address, 500)  # now Alice has 500 in a UTXO


# Helper function to build a spend transaction from an Account
def build_payment_tx(chain: Blockchain, sender: Account, recipient_address: str, amount: int):

        # Select UTXOs for the sender
    total = 0  # Total amount selected
    chosen = []  # List of chosen UTXOs
    for key, utxo in chain.utxos.items():
        if utxo['address'] != sender.address:
            continue
        tx_id, out_index = key.split(':')
        out_index = int(out_index)
        chosen.append((tx_id, out_index, utxo['amount']))
        total += utxo['amount']
        if total >= amount:
            break
    if total < amount:
        raise ValueError("Insufficient funds")


        # Build inputs and outputs for the transaction
    inputs = [{'tx_id': tx_id, 'out_index': out_idx} for (tx_id, out_idx, _a) in chosen]
    outputs = [{'address': recipient_address, 'amount': amount}]
    change = total - amount
    if change > 0:
        outputs.append({ 'address': sender.address, 'amount': change })

    tx = Transaction(inputs=inputs, outputs=outputs, sender_public_key=sender.public_key, signature=None, timestamp=time.ctime())
    # sign using sender.sk (ecdsa.SigningKey)
    tx.sign_with(sender.sk)
    return tx


recipients = [bob.address, Daniel.address, bob.address, Daniel.address, bob.address]
amounts = [30, 20, 50, 10, 15]

for i in range(5):
    tx = build_payment_tx(chain, alice, recipients[i], amounts[i])
    print(f"Adding transaction {i+1} sending {amounts[i]} to recipient {i+1}...")
    chain.add_transaction(tx)  # this will append to pending_transactions

# At this point, because pending_transactions >= 5, the block should auto-mine
# No need to manually call chain.mine_pending_transactions()


# Display the UTXOs after mining
print("UTXOs after mining:", chain.utxos)  # Show the updated UTXOs after mining
