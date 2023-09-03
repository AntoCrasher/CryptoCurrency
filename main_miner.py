import random

from Blockchain import Blockchain
from Block import Block
import Utils

import threading
import socket
import time
import json

mining = False
current_id = -1
already_mined = []

def mine_pool(id, data, prev, timestamp):
    global mining
    global current_id

    block = Block(id, data, prev, timestamp, random.randint(0, 10**12))
    while not block.is_hash_valid() and mining:
        block.mine()
        if current_id != id:
            mining = False
    if mining:
        return block.nonce
    else:
        return None

def mine(server_socket, data):
    global mining

    print(Utils.rgb_color(255, 150, 50) + f'Mining block {data["index"]}...' + Utils.reset_color())
    nonce = mine_pool(data['index'], data['await_to_mine'], data['prev'], data['timestamp'])
    if nonce == None:
        print(Utils.rgb_color(255, 50, 50) + f'Block already mined!' + Utils.reset_color())
        return
    print(Utils.rgb_color(50, 255, 50) + f'Mined block {data["index"]} with nonce: {nonce}!' + Utils.reset_color())
    return_json = {
        'origin': 'miner',
        'type': 'return_mine',
        'data': [data['timestamp'], nonce]
    }
    server_socket.sendto(json.dumps(return_json).encode('utf-8'), ('192.168.1.36', 6000))
    mining = False

def main():
    global mining
    global current_id
    global already_mined

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.settimeout(1.0)

    port = int(input('Port: '))
    server_socket.bind(('192.168.1.36', port))
    random.seed(port)

    message_json = {
        'origin': 'miner',
        'type': 'connection'
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', 6000))

    while True:
        try:
            message_json = {
                'origin': 'miner',
                'type': 'request_to_mine'
            }
            server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', 6000))
            message, address = server_socket.recvfrom(1024)
            message = json.loads(message.decode('utf-8'))
            data = message['data']
            if message['type'] == 'to_be_mined':
                current_id = data['index']
                if len(data['await_to_mine']) > 0:
                    if not mining and not current_id in already_mined:
                        mining = True
                        already_mined.append(current_id)
                        transaction_pool_thread = threading.Thread(target=mine, args=(server_socket, data,))
                        transaction_pool_thread.daemon = True
                        transaction_pool_thread.start()
            if message['type'] == 'update_id':
                current_id = data
            if message['type'] == 'confirmation':
                if message['data']:
                    print(Utils.rgb_color(50, 255, 50) + f'Block confirmed successfully!' + Utils.reset_color())
                else:
                    print(Utils.rgb_color(255, 50, 50) + f'Block already mined!' + Utils.reset_color())

            time.sleep(0.1)
        except socket.timeout:
            continue


if __name__ == "__main__":
    main()