from Block import Block
import Utils

from datetime import datetime
import json
import os

class Blockchain:
    def __init__(self):
        self.config = json.loads(open('config.json').read())
        self.path = self.config['blockchain-path']
        self.initial_balance = 100.0
        self.pool_size = 3
        self.max_block_time = 10.0
        self.transaction_pool = []
        self.await_to_mine = []
        self.current_mine_index = -1
        self.reward = self.config['mining-reward']
        if self.get_last_block() == None:
            Utils.error('Genesis NOT found (mining)')
            genesis = self.create_block([], '-')
            while not genesis.is_hash_valid():
                genesis.mine()
            self.save_block(genesis)
            Utils.success('Mined new Genesis Block!')

    def create_block(self, data, miner):
        last_block = self.get_last_block()
        last_id = -1
        last_hash = '0'*64
        if last_block != None:
            last_id = last_block.id
            last_hash = last_block.hash
        new_block = Block(last_id + 1, data, miner, self.reward, last_hash, datetime.now().isoformat())
        return new_block

    def add_to_transaction_pool(self, data):
        self.transaction_pool.append(data)
        Utils.success(f'Added to Transaction Pool: {data}')

    def add_to_await_to_mine(self):
        self.await_to_mine = self.transaction_pool
        self.current_mine_index = self.get_last_block().id + 1
        self.transaction_pool = []

    def get_await_to_mine(self):
        ret = {
            'index': self.current_mine_index,
            'await_to_mine': self.await_to_mine,
            'reward': self.reward,
            'prev': self.get_last_block().hash,
            'timestamp': datetime.now().isoformat()
        }
        return ret

    def publish_block(self, data):
        block = Block(data['id'], data['data'], data['miner'], data['reward'], data['prev'], data['timestamp'], data['nonce'])
        self.save_block(block)
        self.await_to_mine = []
        Utils.success(f'Mined block {block.id}!')

    def get_last_block(self):
        files = os.listdir(self.path)
        largest_number = None
        for file_name in files:
            try:
                number = int(file_name.split('.')[0])
                if largest_number is None or number > largest_number:
                    largest_number = number
            except ValueError:
                pass
        if largest_number == None:
            return None

        return self.parse_block(f'{self.path}{str(largest_number)}.json')

    def is_block_valid(self, block, prev):
        pass
    def save_block(self, block):
        with open(f'{self.path}{block.id}.json', 'w') as block_file:
            block_file.write(json.dumps(block.json(), indent=4))

    def is_chain_vaid(self, chain):
        return True

    def parse_block(self, path):
        block_data = json.loads(open(path).read())
        block = Block(block_data['id'], block_data['data'], block_data['miner'], block_data['reward'], block_data['prev'], block_data['timestamp'], block_data['nonce'])
        return block

    def __str__(self):
        out = ''
        files = os.listdir(self.path)
        for file_name in files:
            block = self.parse_block(f'{self.path}{file_name}')
            out += str(block) + '\n'
        return out

    def is_chain_valid(self):
        result = True

        files = os.listdir(self.path)
        last_hash = '0' * 64

        final_users = json.loads(open(self.config['users-path']).read())
        final_ledger = json.loads(open(self.config['ledger-path']).read())

        sim_users = []
        sim_ledger = {}
        for file_name in files:
            block_json = json.loads(open(self.path + file_name).read())
            b_id = block_json['id']
            b_data = block_json['data']
            b_miner = block_json['miner']
            b_reward = block_json['reward']
            b_prev = block_json['prev']
            b_timestamp = block_json['timestamp']
            b_nonce = block_json['nonce']
            b_hash = block_json['hash']

            block = Block(b_id, b_data, b_miner, b_reward, b_prev, b_timestamp, b_nonce)
            b_calc_hash = block.get_hash()

            is_hash_mined = b_hash[:5] == '00000'
            is_hash_correct = b_hash == b_calc_hash
            is_prev_correct = b_prev == last_hash
            last_hash = b_calc_hash
            for action in b_data:
                if action['type'] == 'wallet_creation':
                    w_username = action['username']
                    w_password = action['password']
                    w_balance = action['balance']
                    sim_new_user = {
                        "username": w_username,
                        "password": w_password
                    }
                    sim_users.append(sim_new_user)
                    sim_ledger[w_username] = w_balance
                if action['type'] == 'transaction':
                    t_sender = action['sender']
                    t_recipient = action['recipient']
                    t_amount = action['amount']
                    if t_sender in sim_ledger:
                        sim_ledger[t_sender] -= t_amount
                    if t_recipient in sim_ledger:
                        sim_ledger[t_recipient] += t_amount
            if b_miner != '-':
                if b_miner in sim_ledger:
                    sim_ledger[b_miner] += b_reward
            if not (is_hash_mined and is_hash_correct and is_prev_correct):
                result = False
        is_users_correct = sim_users == final_users
        is_ledger_correct = sim_ledger == final_ledger
        if not (is_users_correct and is_ledger_correct):
            result = False
        return result