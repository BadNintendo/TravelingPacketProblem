import socket
import json
import time
import networkx as nx

class QPRx2025:
    def __init__(self, seed=0):
        self.seed = seed % 1000000
        self.entropy = self.mix_entropy(int(time.time() * 1000))
        self.CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        self.LCG_PARAMS = {
            'a': 1664525,
            'c': 1013904223,
            'm': 4294967296
        }

    def mix_entropy(self, value):
        return value ^ (value >> 32) ^ (value >> 16) ^ (value >> 8) ^ value

    def lcg(self, a=None, c=None, m=None):
        if a is None: a = self.LCG_PARAMS['a']
        if c is None: c = self.LCG_PARAMS['c']
        if m is None: m = self.LCG_PARAMS['m']
        self.seed = (a * self.seed + c + self.entropy) % m
        self.entropy = self.mix_entropy(self.seed + int(time.time() * 1000))
        return self.seed

    def mersenne_twister(self):
        MT = [0] * 624
        index = 0

        def initialize(seed):
            MT[0] = seed
            for i in range(1, 624):
                MT[i] = (0x6c078965 * (MT[i - 1] ^ (MT[i - 1] >> 30)) + i) & 0xffffffff

        def generate_numbers():
            for i in range(624):
                y = (MT[i] & 0x80000000) + (MT[(i + 1) % 624] & 0x7fffffff)
                MT[i] = MT[(i + 397) % 624] ^ (y >> 1)
                if y % 2 != 0:
                    MT[i] ^= 0x9908b0df

        def extract_number():
            nonlocal index
            if index == 0:
                generate_numbers()
            y = MT[index]
            y ^= y >> 11
            y ^= (y << 7) & 0x9d2c5680
            y ^= (y << 15) & 0xefc60000
            y ^= y >> 18
            index = (index + 1) % 624
            return y

        initialize(self.seed)
        return extract_number()

    def quantum_polls_relay(self, max_val):
        if not isinstance(max_val, int) or max_val <= 0:
            raise ValueError('Invalid max value for QuantumPollsRelay')
        lcg_value = self.lcg()
        mt_value = self.mersenne_twister()
        return ((lcg_value + mt_value) % 1000000) % max_val

    def generate_characters(self, length):
        if not isinstance(length, int) or length <= 0:
            raise ValueError('Invalid length for generateCharacters')
        return ''.join(self.CHARACTERS[self.quantum_polls_relay(len(self.CHARACTERS))] for _ in range(length))

    def the_options(self, options):
        if not isinstance(options, list) or len(options) == 0:
            raise ValueError('No options provided')
        return options[self.quantum_polls_relay(len(options))]

    def the_rewarded(self, participants):
        if not isinstance(participants, list) or len(participants) == 0:
            raise ValueError('No participants provided')
        return participants[self.quantum_polls_relay(len(participants))]

    def generate_uuid(self):
        bytes_array = [self.mersenne_twister() + self.quantum_polls_relay(256) & 0xff for _ in range(16)]
        bytes_array[6] = (bytes_array[6] & 0x0f) | 0x40
        bytes_array[8] = (bytes_array[8] & 0x3f) | 0x80
        uuid = ''.join(f'{b:02x}' for b in bytes_array)
        return f'{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}'

    def custom_hash(self, input, salt='', hash_val=False):
        def hashing(input, salt):
            combined = f'{input}{salt}'
            hashed = 0x811c9dc5
            for char in combined:
                hashed ^= ord(char)
                hashed = (hashed * 0x01000193) & 0xffffffff
            return f'{hashed:08x}'

        def verify_hash(input, salt, hashed):
            return hashing(input, salt) == hashed

        if isinstance(hash_val, str):
            return verify_hash(input, salt, hash_val)
        return hashing(input, salt)

    def xor_cipher(self, input, key):
        return ''.join(chr(ord(input[i]) ^ ord(key[i % len(key)])) for i in range(len(input)))

# Initialize QPRx2025
qprx = QPRx2025(seed=12345)

# Define the cities data
cities = [
    {'name': 'City0', 'x': 0, 'y': 0},
    {'name': 'City1', 'x': 10, 'y': 10},
    {'name': 'City2', 'x': 20, 'y': 20},
    {'name': 'City3', 'x': 30, 'y': 5},
    {'name': 'City4', 'x': 40, 'y': 15},
    {'name': 'City5', 'x': 50, 'y': 0},
    {'name': 'City6', 'x': 60, 'y': 10},
    {'name': 'City7', 'x': 70, 'y': 20},
    {'name': 'City8', 'x': 80, 'y': 5},
    {'name': 'City9', 'x': 90, 'y': 15},
    {'name': 'City10', 'x': 100, 'y': 0},
    {'name': 'City11', 'x': 110, 'y': 10},
    {'name': 'City12', 'x': 120, 'y': 20},
    {'name': 'City13', 'x': 130, 'y': 5},
    {'name': 'City14', 'x': 140, 'y': 15},
    {'name': 'City15', 'x': 150, 'y': 0},
    {'name': 'City16', 'x': 160, 'y': 10},
    {'name': 'City17', 'x': 170, 'y': 20},
    {'name': 'City18', 'x': 180, 'y': 5},
    {'name': 'City19', 'x': 190, 'y': 15},
    {'name': 'City20', 'x': 200, 'y': 0},
    {'name': 'City21', 'x': 210, 'y': 10},
    {'name': 'City22', 'x': 220, 'y': 20},
    {'name': 'City23', 'x': 230, 'y': 5},
    {'name': 'City24', 'x': 240, 'y': 15},
    {'name': 'City25', 'x': 250, 'y': 0},
    {'name': 'City26', 'x': 260, 'y': 10},
    {'name': 'City27', 'x': 270, 'y': 20},
    {'name': 'City28', 'x': 280, 'y': 5},
    {'name': 'City29', 'x': 290, 'y': 15},
    {'name': 'City30', 'x': 300, 'y': 0},
    {'name': 'City31', 'x': 310, 'y': 10},
    {'name': 'City32', 'x': 320, 'y': 20},
    {'name': 'City33', 'x': 330, 'y': 5},
    {'name': 'City34', 'x': 340, 'y': 15},
    {'name': 'City35', 'x': 350, 'y': 0},
    {'name': 'City36', 'x': 360, 'y': 10},
    {'name': 'City37', 'x': 370, 'y': 20},
    {'name': 'City38', 'x': 380, 'y': 5},
    {'name': 'City39', 'x': 390, 'y': 15},
    {'name': 'City40', 'x': 400, 'y': 0},
    {'name': 'City41', 'x': 410, 'y': 10},
    {'name': 'City42', 'x': 420, 'y': 20},
    {'name': 'City43', 'x': 430, 'y': 5},
    {'name': 'City44', 'x': 440, 'y': 15},
    {'name': 'City45', 'x': 450, 'y': 0},
    {'name': 'City46', 'x': 460, 'y': 10},
    {'name': 'City47', 'x': 470, 'y': 20},
    {'name': 'City48', 'x': 480, 'y': 5},
    {'name': 'City49', 'x': 490, 'y': 15}
]

# JSON encode the cities data
cities_data = json.dumps(cities).encode('utf-8')

# JSON encode the cities data and calculate the hash
hash_value = qprx.custom_hash(cities_data.decode('utf-8'))
request_data = json.dumps({'data': cities, 'hash': hash_value}).encode('utf-8')

def client(protocol='TCP'):
    try:
        if protocol == 'TCP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('127.0.0.1', 3000))
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server_address = ('127.0.0.1', 3000)
        
        start_time = time.time()
        
        if protocol == 'TCP':
            sock.sendall(request_data)
            data = sock.recv(4096)
        else:
            sock.sendto(request_data, server_address)
            data, _ = sock.recvfrom(4096)
        
        end_time = time.time()
        processing_time = round((end_time - start_time) * 1000, 2)
        
        response = json.loads(data.decode('utf-8'))
        print(f"{protocol} Response Time (ms): {processing_time}")
        print("Optimized Path:", response['optimized_path'])
        print("Optimized Distance:", response['optimized_distance'])
        print("Optimized Array:", response['optimized_array'])
        
    except Exception as e:
        print(f"{protocol} error: {e}")
    finally:
        sock.close()

# Handle both TCP and UDP
print("Sending data using TCP...")
client(protocol='TCP')
print("\nSending data using UDP...")
client(protocol='UDP')
