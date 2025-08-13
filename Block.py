import hashlib
from proof_of_work import mine_block as mine_block_func
class Block:
    def __init__(self, index, timestamp, data, transactions, previous_hash=""):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.transactions = transactions
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # include tx ids for stability
        tx_ids_concat = ''.join([tx.tx_id for tx in self.transactions])
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{self.nonce}{tx_ids_concat}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        return mine_block_func(self, difficulty)

    def __repr__(self):
        return f"Block({self.index}, {self.timestamp}, {self.data}, {self.transactions}, {self.hash})"

