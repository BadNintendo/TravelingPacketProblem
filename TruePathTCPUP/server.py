import math
import socket
import select
import json
from ratelimit import limits, sleep_and_retry
import time

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
processed_requests = {}

# Define the rate limit (500 requests per minute)
REQUEST_LIMIT = 500
TIME_PERIOD = 60 # 60 seconds
CACHE_SIZE_LIMIT = 2000  # Define cache size limit


# Memoized dictionary to store distances for efficiency
memoized_distances = {}

# Higher-order function to memoize distances
def memoize_distance(func):
    def wrapper(city1, city2):
        key = frozenset((city1['name'], city2['name']))
        if key not in memoized_distances:
            memoized_distances[key] = func(city1, city2)
        return memoized_distances[key]
    return wrapper

@memoize_distance
def calculate_distance(city1, city2):
    return math.hypot(city1['x'] - city2['x'], city1['y'] - city2['y'])

# Function to calculate total distance of the path
def total_distance(path):
    return sum(calculate_distance(path[i], path[(i + 1) % len(path)]) for i in range(len(path)))

# Morton order function
def morton_order(city):
    def interleave_bits(x, y):
        def spread_bits(v):
            return (v | (v << 8)) & 0x00FF00FF | ((v | (v << 4)) & 0x0F0F0F0F) | ((v | (v << 2)) & 0x33333333) | ((v | (v << 1)) & 0x55555555)
        return spread_bits(x) | (spread_bits(y) << 1)
    x = int(city['x'] * 10000)  # Scale to avoid float precision issues
    y = int(city['y'] * 10000)
    return interleave_bits(x, y)

def solve_tsp(cities):
    # Precompute and store distances between all pairs of cities in a matrix
    num_cities = len(cities)
    distance_matrix = [[0] * num_cities for _ in range(num_cities)]
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                distance_matrix[i][j] = calculate_distance(cities[i], cities[j])

    # Sort cities based on Morton order
    cities_sorted = sorted(cities, key=morton_order)
    city_indices = {city['name']: idx for idx, city in enumerate(cities_sorted)}

    # Measure time for the optimization process
    start_time = time.time()

    # Initialize the path with the first city and mark it as visited
    path = [cities_sorted[0]]
    visited = set()
    visited.add(cities_sorted[0]['name'])
    current_city = cities_sorted[0]
    current_index = city_indices[current_city['name']]

    # Build the path by selecting the nearest unvisited city
    while len(visited) < num_cities:
        closest_city = None
        closest_dist = float('inf')
        for city in cities_sorted:
            if city['name'] not in visited:
                city_index = city_indices[city['name']]
                dist = distance_matrix[current_index][city_index]
                if dist < closest_dist:
                    closest_dist = dist
                    closest_city = city
                    closest_city_index = city_index

        if closest_city is None:
            break

        path.append(closest_city)
        visited.add(closest_city['name'])
        current_city = closest_city
        current_index = closest_city_index

    # Ensure path returns to start to form a complete tour
    path.append(path[0])

    # 2-opt optimization to improve the path
    def calculate_total_distance(path):
        return sum(distance_matrix[city_indices[path[i]['name']]][city_indices[path[(i + 1) % num_cities]['name']]] for i in range(num_cities))

    def two_opt_swap(path, i, k):
        new_path = path[:i] + path[i:k+1][::-1] + path[k+1:]
        return new_path

    best_distance = calculate_total_distance(path)
    improved = True

    while improved:
        improved = False
        for i in range(1, num_cities - 1):
            for k in range(i + 1, num_cities):
                new_path = two_opt_swap(path, i, k)
                new_distance = calculate_total_distance(new_path)
                if new_distance < best_distance:
                    path = new_path
                    best_distance = new_distance
                    improved = True

    total_dist = best_distance
    end_time = time.time()
    total_time = round((end_time - start_time) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

    # Construct optimized array with coordinates
    optimized_array = [{'name': city['name'], 'x': city['x'], 'y': city['y']} for city in path]

    result = {
        'optimized_path': [city['name'] for city in path],
        'optimized_distance': total_dist,
        'optimization_time': total_time,
        'optimized_array': optimized_array
    }
    return result

# Rate limiting decorator
@sleep_and_retry
@limits(calls=REQUEST_LIMIT, period=TIME_PERIOD)
def process_request(data):
    try:
        request_data = json.loads(data.decode('utf-8'))
        cities = request_data['data']
        received_hash = request_data['hash']

        # Check if the hash already exists in the processed_requests
        if received_hash in processed_requests:
            return processed_requests[received_hash]

        # Calculate the hash of the cities data
        calculated_hash = qprx.custom_hash(json.dumps(cities).encode('utf-8').decode('utf-8'))

        # Verify the hash
        if received_hash != calculated_hash:
            return {"error": "Hash verification failed"}

        # Process the data
        result = solve_tsp(cities)
        processed_requests[received_hash] = result

        # Check cache size and clear if necessary
        if len(processed_requests) > CACHE_SIZE_LIMIT:
            processed_requests.pop(next(iter(processed_requests)))

        return result
    except Exception as e:
        return {"error": str(e)}


# Server setup
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind(('127.0.0.1', 3000))
tcp_socket.listen(5)

udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind(('127.0.0.1', 3000))

print('Server is listening on 127.0.0.1:3000...')

sockets_list = [tcp_socket, udp_socket]

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])

    for notified_socket in read_sockets:
        if notified_socket == tcp_socket:
            connection, client_address = tcp_socket.accept()
            try:
                data = connection.recv(4096)
                if data:
                    result = process_request(data)
                    response = json.dumps(result).encode('utf-8')
                    connection.sendall(response)
            except Exception as e:
                print(f"TCP error: {e}")
            finally:
                connection.close()
        elif notified_socket == udp_socket:
            try:
                data, address = udp_socket.recvfrom(4096)
                if data:
                    result = process_request(data)
                    response = json.dumps(result).encode('utf-8')
                    udp_socket.sendto(response, address)
            except Exception as e:
                print(f"UDP error: {e}")