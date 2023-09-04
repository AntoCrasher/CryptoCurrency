# CryptoCurrency (Sal)

This is a blockchain simulation for my computer science project<br>

Main interactions:<br>
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/6b370428-7959-4255-8233-9fe91ca185f1)
Blockchain:<br>
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/1f0b5143-3d37-44b9-b2c4-69d319016178)
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/1a537bf0-68d2-4e23-8233-ee11c9fcbb32)
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/53e186ab-5436-43c3-b662-4d0cc57336fe)
Users:<br>
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/04a05293-a701-4c5f-8bca-df1676688dec)
Ledger:<br>
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/0a00998b-c0f2-46a1-ab49-2173585ffc60)
Structure:<br>
![image](https://github.com/AntoCrasher/CryptoCurrency/assets/48983909/b7b13dd7-a39e-40cd-9661-28939ec57c8a)

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
What miner mines:<br>
• `wallet_creation` : When a wallet is created, it will only be created when a miner mines a block that has the `wallet_creation` type data.<br>
• `transaction` : When sals are sent, they will only be transfered when a miner mines a block that has `transaction` type data.<br>
