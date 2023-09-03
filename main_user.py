import time

from Blockchain import Blockchain
import Utils

import threading
import socket
import json

blockchain_port = 6000
last_input = ''

username_exists_value = False
username_exists_returned = False

sign_in_value = False
sign_in_returned = False

get_balance_value = False
get_balance_returned = False

def create_wallet(server_socket, username, password):
    message_json = {
        'origin': 'user',
        'type': 'create_wallet',
        'data': {
            'username': username,
            'password': password
        }
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', blockchain_port))

def username_exist(server_socket, username):
    global username_exists_value
    global username_exists_returned

    message_json = {
        'origin': 'user',
        'type': 'username_exist',
        'data': username
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', blockchain_port))
    while not username_exists_returned:
        time.sleep(0.1)
    username_exists_returned = False
    return username_exists_value

def sign_in(server_socket, username, password):
    global sign_in_value
    global sign_in_returned

    message_json = {
        'origin': 'user',
        'type': 'sign-in',
        'data': {
            'username': username,
            'password': password
        }
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', blockchain_port))
    while not sign_in_returned:
        time.sleep(0.1)
    sign_in_returned = False
    return sign_in_value

def get_balance(server_socket, username):
    global get_balance_value
    global get_balance_returned

    message_json = {
        'origin': 'user',
        'type': 'get_balance',
        'data': username
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', blockchain_port))
    while not get_balance_returned:
        time.sleep(0.1)
    get_balance_returned = False
    return get_balance_value

def confirmations(server_socket):
    global last_input

    global username_exists_value
    global username_exists_returned

    global sign_in_value
    global sign_in_returned

    global get_balance_value
    global get_balance_returned

    while True:
        message, address = server_socket.recvfrom(1024)
        message = json.loads(message.decode('utf-8'))
        if message['type'] == 'confirmation':
            print()
            if message['process'] == 'wallet_creation':
                success = message['data']
                if success:
                    Utils.success('Successfully created wallet!')
                else:
                    Utils.error('Error occurred when creating wallet!')
            if message['process'] == 'transaction':
                success = message['data']
                if success:
                    Utils.success(f'Successfully sent {message["recipient"]} {Utils.rgb_color(50, 50, 255)}{message["amount"]} sal(s){Utils.rgb_color(50, 255, 50)}!')
                else:
                    Utils.error('Transaction could not be completed!')
            if message['process'] == 'payment':
                success = message['data']
                if success:
                    Utils.success(f'You received {Utils.rgb_color(50, 50, 255)}{message["amount"]} sal(s){Utils.rgb_color(50, 255, 50)} from {message["sender"]}!')
            print(last_input, end='')
        if message['type'] == 'username_exist':
            username_exists_value = message['data']
            username_exists_returned = True
        if message['type'] == 'sign-in':
            sign_in_value = message['data']
            sign_in_returned = True
        if message['type'] == 'get_balance':
            get_balance_value = message['data']
            get_balance_returned = True

def show_options(options):
    print("Options:")
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option.capitalize()}")
    print('q. Cancel current')
    print('h. Show this menu')

def main():
    global last_input
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    port = int(input('Port: '))
    server_socket.bind(('192.168.1.36', port))

    signed_in = False
    username = ''

    message_json = {
        'origin': 'user',
        'type': 'connection'
    }
    server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', blockchain_port))

    confirmations_thread = threading.Thread(target=confirmations, args=(server_socket,))
    confirmations_thread.daemon = True
    confirmations_thread.start()

    options = ['create wallet', 'sign-in', 'send', 'balance']
    show_options(options)
    while True:
        quit_loop = False
        while True:
            try:
                last_input = f'Enter your choice (1-{len(options)}): '
                choice = int(input(last_input))
                if 1 <= choice <= len(options):
                    command = options[choice - 1]
                    break
                else:
                    Utils.error("Invalid choice. Please enter a valid number.")
            except ValueError:
                Utils.error("Invalid input. Please enter a number.")
        if command == 'h':
            show_options(options)
        if command == 'create wallet':
            while True:
                last_input = 'Username: '
                username = input('Username: ')
                if username == 'q':
                    quit_loop = True
                    break
                if len(username) >= 3:
                    username_exists = username_exist(server_socket, username)
                    if username_exists:
                        Utils.error('Username already taken! (Try logging in)')
                        continue
                    break
                else:
                    Utils.error('Username must have at least 3 characters.')
            if quit_loop:
                continue

            while True:
                last_input = 'Password: '
                password = input(last_input)
                if password == 'q':
                    quit_loop = True
                    break
                if len(password) < 5:
                    Utils.error('Password must have at least 5 characters.')
                elif not any(char.isdigit() for char in password):
                    Utils.error('Password must contain at least one digit.')
                elif not any(char.isalpha() for char in password):
                    Utils.error('Password must contain at least one letter.')
                else:
                    break
            if quit_loop:
                continue
            create_wallet(server_socket, username, password)

        if command == 'sign-in':
            last_input = 'Username: '
            username = input(last_input)
            if username == 'q':
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

        if command == 'send':
            if signed_in:
                while True:
                    last_input = 'Who is the recipient: '
                    recipient = input(last_input)
                    if recipient == 'q':
                        quit_loop = True
                        break
                    username_exists = username_exist(server_socket, username)
                    if not username_exists:
                        Utils.error('Recipient does not exist!')
                    else:
                        break
                if quit_loop:
                    continue
                while True:
                    try:
                        last_input = 'Amount: '
                        amount = input(last_input)
                        if amount == 'q':
                            quit_loop = True
                            break
                        amount = float(amount)
                        balance = get_balance(server_socket, username)
                        if amount <= 0:
                            Utils.error('Amount must be greater than 0.')
                        elif balance < amount:
                            Utils.error('Insufficient balance. Enter a valid amount.')
                        else:
                            break
                    except ValueError:
                        Utils.error('Invalid input. Please enter a valid number.')
                if quit_loop:
                    continue

                print(Utils.rgb_color(255, 150, 50) + f'Are you sure you want to send {recipient}' + Utils.rgb_color(50, 50, 255) + f' {amount} sal(s)' + Utils.rgb_color(255, 150, 50) + '?' + Utils.reset_color())

                user_input = input('y | (n): ').strip().lower()
                if user_input != 'y':
                    Utils.error('Cancelled.')
                    continue

                print(Utils.rgb_color(255, 150, 50) + 'Processing...' + Utils.reset_color())

                message_json = {
                    'origin': 'user',
                    'type': 'blockchain',
                    'data': {
                        'type': 'transaction',
                        'sender': username,
                        'recipient': recipient,
                        'amount': amount
                    }
                }
                server_socket.sendto(json.dumps(message_json).encode('utf-8'), ('192.168.1.36', blockchain_port))
            else:
                Utils.error('Please sign-in to a wallet.')

        if command == 'balance':
            if signed_in:
                print(Utils.rgb_color(50, 50, 255) + f'You have {round(get_balance(server_socket, username), 2)} sal(s).' + Utils.reset_color())
            else:
                Utils.error('Please sign-in to a wallet.')


if __name__ == "__main__":
    main()