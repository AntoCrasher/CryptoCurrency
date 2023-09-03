import hashlib

def error(message):
    print(rgb_color(255, 50, 50) + message + reset_color())

def success(message):
    print(rgb_color(50, 255, 50) + message + reset_color())

def rgb_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def reset_color():
    return f'\033[0m'

def sha256(input_string):
    input_bytes = str(input_string).encode('utf-8')
    hash_hex = hashlib.sha256(input_bytes).hexdigest()
    return hash_hex