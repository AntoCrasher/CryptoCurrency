import time

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

    transaction_pool_thread = threading.Thread(target=transaction_pool, args=(blockchain, ))
    transaction_pool_thread.daemon = True
    transaction_pool_thread.start()

    while True:
        message, address = server_socket.recvfrom(1024)
        message = json.loads(message.decode('utf-8'))
        if message['type'] == 'connection':
            print(Utils.rgb_color(200, 50, 255) + f'{message["origin"].capitalize()} #{address[1]} connected!' + Utils.reset_color())
            continue
        if message['origin'] == 'user':
            data = message['data']
            blockchain.add_to_transaction_pool(data)
            print(Utils.rgb_color(50, 50, 255) + f'Added to Transaction Pool: {data}' + Utils.reset_color())
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
                    blockchain.publish_block(data[0], data[1])
                else:
                    message_json['data'] = False

                server_socket.sendto(json.dumps(message_json).encode('utf-8'), address)
                blockchain.current_mine_index = -1
            pass

if __name__ == "__main__":
    main()