import hashlib
import time

class Transaction:
    def __init__(self, sender_public_key, recipient_address, signature, amount , timestamp=None):
        self.sender_public_key = sender_public_key
        self.recipient_address = recipient_address
        self.signature = signature
        self.amount = amount
        self.timestamp = timestamp or time.ctime()
    def to_dict(self):
        return {
            "sender_public_key": self.sender_public_key,
            "recipient_address": self.recipient_address,
            "signature": self.signature,
            "amount": self.amount,
            "timestamp": self.timestamp
        }

    def calculate_hash(self):
        tx_bytes = self.sender_public_key + self.recipient_address.encode() + str(self.amount).encode() + self.timestamp.encode()
        return hashlib.sha256(tx_bytes).hexdigest()