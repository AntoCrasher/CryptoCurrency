# CryptoCurrency (Sal)

This is a blockchain simulation for my computer science project<br>

Main interactions:<br>
![image](./images/main_interactions.png)
Blockchain:<br>
![image](./images/block_0.png)
![image](./images/block_1.png)
![image](./images/block_2.png)
![image](./images/block_3.png)
Users:<br>
![image](./images/users.png)
Ledger:<br>
![image](./images/ledger.png)
Structure:<br>
![image](./images/structure.png)

# How to use?

Run `main_blockchain.py`. This will create and mine the genesis block (root block).<br>
Run `main_user.py`. This will allow you to interact with the blockchain as a user.<br>
User Commands:<br>
• `(1) Create wallet` : Create a wallet by entering username and password.<br>
• `(2) Sign-in` : Sign-in to a wallet by entering username and password.<br>
• `(3) Send` : Send sals by entering recipient and amount (Requires wallet).<br>
• `(4) Balance` : Get current balance (Requires wallet).<br>
• `q` : Cancel current action.<br>
• `h` : Show commands menu.<br>
Run `main_miner.py`. This will allow blocks to be mined.<br>
Miner Commands:<br>
• `(1) Sign-in` : Sign-in to a wallet by entering username and password.<br>
• `(2) Start mining` : Starts mining blocks (Wallet is optional).<br>
• `(3) Stop mining` : Stops mining blocks.<br>
• `(4) Balance` : Get current balance (Requires wallet).<br>
• `q` : Cancel current action.<br>
• `h` : Show commands menu.<br>
What miner mines:<br>
• `wallet_creation` : When a wallet is created, it will only be created when a miner mines a block that has the `wallet_creation` type data.<br>
• `transaction` : When sals are sent, they will only be transfered when a miner mines a block that has `transaction` type data.<br>
