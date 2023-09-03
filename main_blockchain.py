import time

from UserManager import UserManager
from Blockchain import Blockchain
import Utils

import threading
import socket
import json

def transaction_pool(blockchain):
    time_without_transaction = 0.0
    last_length = 0
    while True:
        time.sleep(1.0)
        current_length = len(blockchain.transaction_pool)
        if current_length == last_length:
            time_without_transaction += 1.0
        else:
            time_without_transaction = 0
        if (current_length >= blockchain.pool_size or time_without_transaction >= blockchain.max_block_time) and len(blockchain.await_to_mine) == 0:
            blockchain.add_to_await_to_mine()
            if len(blockchain.await_to_mine) > 0:

                print(Utils.rgb_color(255, 150, 50) + f'Await to Mine: {blockchain.await_to_mine}' + Utils.reset_color())
        last_length = current_length
    pass

def main():
    blockchain_port = 6000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('192.168.1.36', blockchain_port))  # Replace '0.0.0.0' with your local IP address

    print(Utils.rgb_color(0, 200, 255) + 'Started blockchain!' + Utils.reset_color())

    blockchain = Blockchain()
    user_manager = UserManager()

    wallets_adresses = {}

    transaction_pool_thread = threading.Thread(target=transaction_pool, args=(blockchain, ))
    transaction_pool_thread.daemon = True
    transaction_pool_thread.start()

    while True:
        message, address = server_socket.recvfrom(1024)
        message = json.loads(message.decode('utf-8'))
        if message['type'] == 'connection':
            print(Utils.rgb_color(200, 50, 255) + f'{message["origin"].capitalize()} #{address[1]} connected!' + Utils.reset_color())
            continue

        if message['type'] == 'username_exist':
            username = message['data']
            exists = user_manager.username_exist(username)
            message_json = {
                'origin': 'blockchain',
                'type': 'username_exist',
                'data': exists,
            }
            server_socket.sendto(json.dumps(message_json).encode('utf-8'), address)
            continue

        if message['type'] == 'create_wallet':
            username = message['data']['username']
            password = message['data']['password']
            data = {
                'type': 'wallet_creation',
                'username': username,
                'password': Utils.sha256(password),
                'balance': blockchain.initial_balance
            }
            wallets_adresses[username] = address
            blockchain.add_to_transaction_pool(data)
            continue

        if message['type'] == 'sign-in':
            username = message['data']['username']
            password = message['data']['password']
            success = user_manager.sign_in(username, password)
            message_json = {
                'origin': 'blockchain',
                'type': 'sign-in',
                'data': success,
            }
            wallets_adresses[username] = address
            server_socket.sendto(json.dumps(message_json).encode('utf-8'), address)
            continue

        if message['type'] == 'get_balance':
            username = message['data']
            balance = user_manager.get_balance(username)
            message_json = {
                'origin': 'blockchain',
                'type': 'get_balance',
                'data': balance,
            }
            server_socket.sendto(json.dumps(message_json).encode('utf-8'), address)
            continue

        if message['origin'] == 'user':
            data = message['data']
            blockchain.add_to_transaction_pool(data)

        if message['origin'] == 'miner':
            if message['type'] == 'request_to_mine':
                message_json = {}
                if blockchain.current_mine_index >= 0:
                    message_json = {
                        'origin': 'blockchain',
                        'type': 'to_be_mined',
                        'data': blockchain.get_await_to_mine(),
                    }
                else:
                    message_json = {
                        'origin': 'blockchain',
                        'type': 'update_id',
                        'data': blockchain.current_mine_index,
                    }
                server_socket.sendto(json.dumps(message_json).encode('utf-8'), address)

            if message['type'] == 'return_mine':
                message_json = {
                    'origin': 'blockchain',
                    'type': 'confirmation',
                }
                if blockchain.current_mine_index >= 0:
                    message_json['data'] = True
                    data = message['data']
                    for action in blockchain.await_to_mine:
                        if action['type'] == 'transaction':
                            sender = action['sender']
                            recipient = action['recipient']
                            amount = action['amount']
                            success = user_manager.send(sender, recipient, amount)
                            message_json_sender = {
                                'origin': 'blockchain',
                                'type': 'confirmation',
                                'process': 'transaction',
                                'recipient': recipient,
                                'amount': amount,
                                'data': success,
                            }
                            message_json_recipient = {
                                'origin': 'blockchain',
                                'type': 'confirmation',
                                'process': 'payment',
                                'sender': username,
                                'amount': amount,
                                'data': success,
                            }
                            if username in wallets_adresses:
                                server_socket.sendto(json.dumps(message_json_sender).encode('utf-8'), wallets_adresses[username])
                            if recipient in wallets_adresses:
                                server_socket.sendto(json.dumps(message_json_recipient).encode('utf-8'), wallets_adresses[recipient])
                        if action['type'] == 'wallet_creation':
                            username = action['username']
                            password = action['password']
                            balance = action['balance']
                            success = user_manager.create_wallet(username, password, balance)
                            message_json = {
                                'origin': 'blockchain',
                                'type': 'confirmation',
                                'process': 'wallet_creation',
                                'data': success,
                            }
                            if username in wallets_adresses:
                                server_socket.sendto(json.dumps(message_json).encode('utf-8'), wallets_adresses[username])
                    blockchain.publish_block(data[0], data[1])
                else:
                    message_json['data'] = False

                server_socket.sendto(json.dumps(message_json).encode('utf-8'), address)
                blockchain.current_mine_index = -1
            pass

if __name__ == "__main__":
    main()