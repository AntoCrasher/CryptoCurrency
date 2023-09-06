import json

import Utils


class UserManager:
    def __init__(self):
        self.config = json.loads(open('config.json').read())
        self.users_path = self.config['users-path']
        self.ledger_path = self.config['ledger-path']

    def username_exist(self, username):
        users = json.loads(open(self.users_path).read())
        for user in users:
            if user['username'] == username:
                return True
        return False

    def create_wallet(self, username, password, balance):
        users = json.loads(open(self.users_path).read())
        ledger = json.loads(open(self.ledger_path).read())
        users.append({
            'username': username,
            'password': password
        })
        ledger[username] = balance
        try:
            with open(self.users_path, 'w') as users_file:
                users_file.write(json.dumps(users, indent=4))
        except:
            return False
        try:
            with open(self.ledger_path, 'w') as ledger_file:
                ledger_file.write(json.dumps(ledger, indent=4))
        except:
            return False
        return True

    def sign_in(self, username, password):
        hashed_password = Utils.sha256(password)
        users = json.loads(open(self.users_path).read())
        for user in users:
            if user['username'] == username and user['password'] == hashed_password:
                return True
        return False

    def send(self, sender, recipient, amount):
        ledger = json.loads(open(self.ledger_path).read())
        ledger[sender] -= amount
        ledger[recipient] += amount
        try:
            with open(self.ledger_path, 'w') as ledger_file:
                ledger_file.write(json.dumps(ledger, indent=4))
        except:
            return False
        return True

    def change_sals(self, username, amount):
        ledger = json.loads(open(self.ledger_path).read())
        ledger[username] += amount
        try:
            with open(self.ledger_path, 'w') as ledger_file:
                ledger_file.write(json.dumps(ledger, indent=4))
        except:
            return False
        return True

    def get_balance(self, username):
        ledger = json.loads(open(self.ledger_path).read())
        return ledger[username]