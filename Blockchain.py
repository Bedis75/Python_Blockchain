import time

import ecdsa
from Block import Block


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, time.ctime(), "Genesis Block", [], "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.transactions = new_block.transactions.copy()
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
    def verify_transaction(self, transaction):
        message = transaction.sender_public_key + transaction.recipient_address.encode() + str(transaction.amount).encode() + transaction.timestamp.encode()
        try:
            vk = ecdsa.VerifyingKey.from_string(transaction.sender_public_key[1:], curve=ecdsa.SECP256k1)  # skip 0x04
            return vk.verify(transaction.signature, message)
        except Exception as e:
            print(f"Verification error: {e}")
            return False

    def add_transaction(self, transaction):
        if self.verify_transaction(transaction):
            self.pending_transactions.append(transaction)
            if len(self.pending_transactions) >= 5:
                self.mine_pending_transactions()
        else:
            print("❌ Invalid transaction signature")

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