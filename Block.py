import Utils

from datetime import datetime
import json

class Block:
    def __init__(self, id, data, prev, timestamp, nonce=1):
        self.id = id
        self.nonce = nonce
        self.data = data
        self.timestamp = timestamp
        self.prev = prev
        self.hash = self.get_hash()

    def is_hash_valid(self):
        return self.hash[:5] == "00000"

    def mine(self):
        self.nonce += 1
        self.hash = self.get_hash()

    def get_hash(self):
        json_block = {
            'id': self.id,
            'nonce': self.nonce,
            'data': self.data,
            'timestamp': self.timestamp,
            'prev': self.prev
        }
        return Utils.sha256(json.dumps(json_block))

    def json(self):
        ret = {
            'id': self.id,
            'nonce': self.nonce,
            'data': self.data,
            'timestamp': self.timestamp,
            'prev': self.prev,
            'hash': self.hash
        }
        return ret

    def __str__(self):
        return json.dumps(self.json(), indent=4)