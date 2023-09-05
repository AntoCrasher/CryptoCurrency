import hashlib

def error(message):
    print(C_ERROR + message + C_RESET)

def success(message):
    print(C_SUCCESS + message + C_RESET)

def warning(message):
    print(C_WARNING + message + C_RESET)

def connect(message):
    print(C_CONNECT + message + C_RESET)

def connection(message):
    print(C_CONNECTION + message + C_RESET)

def info(message):
    print(C_INFO + message + C_RESET)

def currency(amount):
    return C_CURRENCY + str(amount) + ' sal(s)' + C_RESET

def rgb_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def sha256(input_string):
    input_bytes = str(input_string).encode('utf-8')
    hash_hex = hashlib.sha256(input_bytes).hexdigest()
    return hash_hex

C_WARNING = rgb_color(255, 150, 50)
C_SUCCESS = rgb_color(50, 255, 50)
C_ERROR = rgb_color(255, 50, 50)
C_CONNECT = rgb_color(0, 200, 255)
C_CONNECTION = rgb_color(200, 50, 255)
C_INFO = rgb_color(50, 50, 255)
C_CURRENCY = rgb_color(50, 50, 255)
C_RESET = f'\033[0m'