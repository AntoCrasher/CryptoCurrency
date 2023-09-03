from Blockchain import Blockchain
import Utils



# class Wallet:
#     def __init__(self):
#         self.private_key = self.generate_private_key()
#         self.public_key = self.generate_public_key(self.private_key)
#
#     def generate_private_key(self):
#         return ''.join(random.choice(string.hexdigits) for _ in range(64))
#     def generate_public_key(self, private_key):
#         private_key_bytes = bytes.fromhex(private_key)
#         public_key_bytes = sha256(private_key_bytes)
#         return public_key_bytes
#
#     def sign_transaction(self, recipient, amount):
#         message = f"Recipient: {recipient}, Amount: {amount}"
#         signature = sha256(message.encode() + bytes.fromhex(self.private_key))
#         return message, signature
#     def verify_transaction(self, message, signature, sender_public_key):
#         reconstructed_signature = sha256(message.encode() + bytes.fromhex(sender_public_key))
#         return signature == reconstructed_signature
# class Ledger:
#     def __init__(self):
#         self.path = './ledger.json'
#         self.ledger = self.load()
#
#     def add_public_user(self, public_key):
#         self.ledger[public_key] = 0.0
#     def load(self):
#         return json.loads(open(self.path).read())
#
#     def save(self):
#         with open(self.path, 'w') as ledger_file:
#             ledger_file.write(json.dumps(self.ledger, indent=4))
#
#     def __str__(self):
#         return json.dumps(self.ledger, indent=4)

if __name__ == '__main__':
    blockchain = Blockchain()
    print(blockchain)
    # for block inin blockchain.chain:
    #     print(block)
    # user1 = '580e2dfe57c73d92ffb7bd027df2cc1e4f53dc538f206871d722a76cd313d1cb'
    # user2 = 'cde3e745dbf7d9a5d645b3fa7fda18fa0bf9f4b8e1be3b4e6e5920e62d771f72'
    #
    # ledger = Ledger()
    #
    # print(ledger)
    # ledger.save()

# wallet = Wallet()
# print(wallet.private_key)
# print(wallet.public_key)