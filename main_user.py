from Blockchain import Blockchain
import Utils

import threading
import socket
import json

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    port = int(input('Port: '))
    server_socket.bind(('192.168.1.36', port))

    message_json = {
        'origin': 'user',
        'type': 'connection'
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', 6000))

    while True:
        message = input("Enter a message: ")

        message_json = {
            'origin': 'user',
            'type': 'communication',
            'data': message
        }

        server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', 6000))


if __name__ == "__main__":
    main()