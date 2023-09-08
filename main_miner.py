import random

from Blockchain import Blockchain
from Block import Block
import Utils

import threading
import socket
import time
import json

config = json.loads(open('config.json').read())

is_mining = False
mining = False
current_id = -1
already_mined = []
last_input = ''
signed_in = False
username = '-'

def mine_pool(data):
    global mining
    global current_id
    global username

    block = Block(data['index'], data['await_to_mine'], username, data['reward'], data['prev'], data['timestamp'], random.randint(0, 10**12))
    while not block.is_hash_valid() and mining:
        block.mine()
        if current_id != data['index']:
            mining = False
    if mining:
        return block.nonce
    else:
        return None

def mine(server_socket, data):
    global mining
    global last_input
    global username

    Utils.warning(f'\nMining block {data["index"]}...')
    print(last_input, end='')
    nonce = mine_pool(data)
    if nonce == None:
        Utils.error(f'\nBlock already mined!')
        print(last_input, end='')
        return
    Utils.success(f'\nMined block #{data["index"]} with nonce: {nonce}!')
    print(last_input, end='')
    block = Block(data['index'], data['await_to_mine'], username, data['reward'], data['prev'], data['timestamp'], nonce)
    return_json = {
        'origin': 'miner',
        'type': 'return_mine',
        'data': block.json()
    }
    server_socket.sendto(json.dumps(return_json).encode('utf-8'), (config['ip-address'], 6000))
    mining = False

def show_options(options):
    print("Options:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option.capitalize()}")
    print('q. Cancel current')
    print('h. Show this menu')

def start_mining(server_socket):
    global is_mining
    global mining
    global current_id
    global already_mined
    global last_input

    is_mining = True
    while is_mining:
        try:
            message_json = {
                'origin': 'miner',
                'type': 'request_to_mine'
            }
            server_socket.sendto(json.dumps(message_json).encode('utf-8'), (config['ip-address'], 6000))
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
                    Utils.success(f'\nBlock confirmed successfully!')
                else:
                    Utils.error(f'Block already mined!')
                print(last_input, end='')

            time.sleep(0.1)
        except socket.timeout:
            continue

def sign_in(server_socket, username, password):
    message_json = {
        'origin': 'miner',
        'type': 'sign-in',
        'data': {
            'username': username,
            'password': password
        }
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), (config['ip-address'], config['blockchain-port']))
    message, address = server_socket.recvfrom(1024)
    message = json.loads(message.decode('utf-8'))
    return message['data']

def main():
    global is_mining
    global mining
    global current_id
    global already_mined
    global last_input
    global signed_in
    global username

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.settimeout(1.0)

    port_offset = 1
    while True:
        try:
            port = config['blockchain-port'] + port_offset
            if port >= 9999:
                Utils.error('Could not find port!')
                return
            server_socket.bind((config['ip-address'], port))
            break
        except:
            port_offset += 1

    random.seed(port)

    message_json = {
        'origin': 'miner',
        'type': 'connection'
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), (config['ip-address'], 6000))
    Utils.connect(f'Connected as Miner #{port}!')

    options = ['sign-in', 'start mining', 'stop mining', 'balance']
    show_options(options)
    while True:
        quit_loop = False
        while True:
            try:
                last_input = f'Enter your choice (1-{len(options)}): '
                choice = input(last_input)
                if choice == 'h' or 1 <= int(choice) <= len(options):
                    if choice == 'h':
                        command = 'h'
                        break
                    command = options[int(choice) - 1]
                    break
                else:
                    Utils.error("Invalid choice. Please enter a valid number.")
            except ValueError:
                Utils.error("Invalid input. Please enter a number.")

        if command == 'h':
            show_options(options)

        if command == 'sign-in':
            last_input = 'Username: '
            username = input(last_input)
            if username == 'q':
                username = '-'
                continue
            last_input = 'Password: '
            password = input(last_input)
            if password == 'q':
                continue
            success = sign_in(server_socket, username, password)
            if success:
                signed_in = True
                Utils.success('Successfully signed in!')
            else:
                Utils.error('Invalid username or password!')

        if command == 'start mining':
            if not signed_in:
                Utils.warning('Rewards will not be awarded if not signed in.')
            if not is_mining:
                Utils.success('Started mining!')
                mining_thread = threading.Thread(target=start_mining, args=(server_socket,))
                mining_thread.daemon = True
                mining_thread.start()
            else:
                Utils.error('Already mining!')

        if command == 'stop mining':
            if is_mining:
                Utils.success('Stopped mining!')
                is_mining = False
            else:
                Utils.error('Currently not mining!')


if __name__ == "__main__":
    main()