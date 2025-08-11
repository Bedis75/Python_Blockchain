# 🚀 Python Blockchain Project

## 📌 About This Project
This is a minimal blockchain implementation in **Python** demonstrating:
- Block structure & hashing
- Proof of Work (PoW) mining
- Transaction batching
- Blockchain validation

It’s part of my personal **Blockchain Learning Journey**, where I progressively build more complex blockchain-related tools while learning the theory behind them.

---

## 🛠 Features in My Python Blockchain
- **Genesis block** creation at startup
- **Adjustable mining difficulty**
- **Pending transactions** stored until mined (batch size: 5)
- **Hashing** with `SHA-256`
- **Proof of Work** implemented in `proof_of_work.py`
- **Chain validation** to detect tampering

---

## 📂 File Structure
.
├── Block.py # Block structure & mining logic
├── Blockchain.py # Blockchain management
├── Transaction.py # Transaction model
├── proof_of_work.py # Proof of Work mining
├── main.py # Demo usage of the blockchain

yaml
Copier
Modifier

---

## 🚀 How to Run

### 1️⃣ Prerequisites
- Python 3.x installed

### 2️⃣ Run the demo
```bash
python main.py
Example Output
mathematica
Copier
Modifier
Mining block 1...
Block mined: 00000a3e...
Mining block 2...
Block mined: 000001bc...
Blockchain valid? True
Block(2, Mon Aug 11 15:32:10 2025, Block 2, [...], 000001bc...)
