def mine_block(self, difficulty):
    nonce = 0
    while True:
        self.nonce = nonce
        self.hash = self.calculate_hash()
        if self.hash[:difficulty] == "0" * difficulty:
            print(f"Block mined: {self.hash}")
            return self
        nonce += 1
