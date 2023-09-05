from Block import Block
import Utils

from datetime import datetime
import json
import os

class Blockchain:
    def __init__(self):
        self.path = "./sals_cryptocurrency/blockchain/"
        self.initial_balance = 100.0
        self.pool_size = 3
        self.max_block_time = 10.0
        self.transaction_pool = []
        self.await_to_mine = []
        self.current_mine_index = -1
        self.reward = 5.0
        if self.get_last_block() == None:
            Utils.error('Genesis NOT found (mining)')
            genesis = self.create_block([], 'bc')
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
        new_block = Block(last_id + 1, data, miner, 0.0, last_hash, datetime.now().isoformat())
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
