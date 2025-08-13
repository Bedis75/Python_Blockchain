# Transaction.py
import hashlib
import time
import ecdsa

class Transaction:
    """
    UTXO-style transaction:
    - inputs: list of {'tx_id': str, 'out_index': int}
    - outputs: list of {'address': str, 'amount': int}
    - sender_public_key: bytes (uncompressed) or None for coinbase/genesis
    - signature: bytes or None
    """

    def __init__(self, inputs=None, outputs=None, sender_public_key=None, signature=None, timestamp=None):
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.sender_public_key = sender_public_key  # bytes or None
        self.signature = signature
        self.timestamp = timestamp or time.ctime()
        # tx_id computed from core data (excludes signature) so it's stable
        self.tx_id = self.calculate_tx_id()

    def _serialize_core(self) -> bytes:
        ins = ''.join([f"{i['tx_id']}:{i['out_index']}" for i in self.inputs])
        outs = ''.join([f"{o['address']}:{o['amount']}" for o in self.outputs])
        pk_hex = self.sender_public_key.hex() if self.sender_public_key else ''
        s = f"{ins}|{outs}|{pk_hex}|{self.timestamp}"
        return s.encode()

    def calculate_tx_id(self) -> str:
        return hashlib.sha256(self._serialize_core()).hexdigest()

    def signing_message(self) -> bytes:
        # We'll sign the tx_id bytes (32 bytes) — consistent and small
        return bytes.fromhex(self.calculate_tx_id())

    def sign_with(self, signing_key: ecdsa.SigningKey):
        if self.sender_public_key is None:
            return
        # signing_key is an ecdsa.SigningKey (your Account.sk)
        self.signature = signing_key.sign(self.signing_message())

    def verify_signature(self) -> bool:
        if self.sender_public_key is None:
            # coinbase/genesis: no signature needed
            return True
        if not self.signature:
            return False
        try:
            vk = ecdsa.VerifyingKey.from_string(self.sender_public_key[1:], curve=ecdsa.SECP256k1)
            return vk.verify(self.signature, self.signing_message())
        except Exception:
            return False

    def total_output(self) -> int:
        return sum(o['amount'] for o in self.outputs)

    def __repr__(self):
        return f"TX(id={self.tx_id[:10]}..., in={len(self.inputs)}, out={len(self.outputs)})"
