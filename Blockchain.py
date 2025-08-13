# Blockchain.py
import time
import hashlib
import ecdsa
from Block import Block
from Transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []
        # utxos: "tx_id:out_index" -> { 'address': str, 'amount': int }
        self.utxos = {}

    def create_genesis_block(self):
        return Block(0, time.ctime(), "Genesis Block", [], "0")

    def create_genesis_utxo(self, address: str, amount: int):
        """Create a one-off genesis UTXO so an address has spendable coins (minimal approach)."""
        genesis_txid = hashlib.sha256(f"genesis:{address}:{amount}:{time.time()}".encode()).hexdigest()
        key = f"{genesis_txid}:0"
        self.utxos[key] = {'address': address, 'amount': amount}
        print(f"Created genesis UTXO {key} -> {amount} to {address}")

    def get_latest_block(self):
        return self.chain[-1]

    def index_block_utxos(self, block: Block):
        # Remove spent UTXOs (inputs) and add new outputs
        for tx in block.transactions:
            # consume inputs
            for inp in tx.inputs:
                key = f"{inp['tx_id']}:{inp['out_index']}"
                if key in self.utxos:
                    del self.utxos[key]
            # add outputs
            for idx, out in enumerate(tx.outputs):
                key = f"{tx.tx_id}:{idx}"
                self.utxos[key] = { 'address': out['address'], 'amount': out['amount'] }

    def verify_transaction(self, tx: Transaction) -> bool:
        # coinbase/genesis-like (no sender_public_key): allow only if no inputs and outputs positive
        if tx.sender_public_key is None:
            if len(tx.inputs) != 0 or tx.total_output() <= 0:
                return False
            return True

        # 1) signature must be valid
        if not tx.verify_signature():
            return False

        # 2) inputs must exist in utxos and belong to sender
        sha256_pk = hashlib.sha256(tx.sender_public_key).digest()
        sender_addr = hashlib.new("ripemd160", sha256_pk).hexdigest()

        input_sum = 0
        for i in tx.inputs:
            key = f"{i['tx_id']}:{i['out_index']}"
            utxo = self.utxos.get(key)
            if not utxo or utxo['address'] != sender_addr:
                return False
            input_sum += utxo['amount']

        # 3) amounts valid
        if input_sum <= 0:
            return False
        if any(o['amount'] <= 0 for o in tx.outputs):
            return False
        if tx.total_output() > input_sum:
            return False

        return True

    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.transactions = new_block.transactions.copy()
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        # update UTXO set (consume inputs & add outputs)
        self.index_block_utxos(new_block)

    def add_transaction(self, tx: Transaction):
        if self.verify_transaction(tx):
            self.pending_transactions.append(tx)
        else:
            print("❌ Invalid transaction")
        if len(self.pending_transactions) >= 5:
            self.mine_pending_transactions()

    def mine_pending_transactions(self):
        print(f"Mining block {len(self.chain)}...")
        block = Block(len(self.chain), time.ctime(), f"Block {len(self.chain)}", self.pending_transactions.copy())
        self.add_block(block)
        self.pending_transactions = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True
