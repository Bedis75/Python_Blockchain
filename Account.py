import os
import ecdsa
import hashlib

class Account:
    def __init__(self):
        # Generate a private key
        self.private_key = os.urandom(32)
        self.sk = ecdsa.SigningKey.from_string(self.private_key, curve=ecdsa.SECP256k1)

        # Generate public key
        self.vk = self.sk.verifying_key
        self.public_key = b"\x04" + self.vk.to_string()

        # Generate address
        sha256_pk = hashlib.sha256(self.public_key).digest()
        ripemd160 = hashlib.new("ripemd160", sha256_pk).digest()
        self.address = ripemd160.hex()

    def sign(self, message: bytes):
        return self.sk.sign(message)

    def __repr__(self):
        return f"Account(Address={self.address})"