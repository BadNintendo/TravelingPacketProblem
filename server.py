import socket
import select
import math
import time
import json

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
    """Find and optimize a path using Morton order, nearest neighbor heuristic, and in-place 2-opt algorithm."""

    # Precompute and store distances between all pairs of cities
    distances = {frozenset((city1['name'], city2['name'])): calculate_distance(city1, city2)
                 for city1 in cities for city2 in cities if city1 != city2}

    # Sort cities based on Morton order
    cities_sorted = sorted(cities, key=morton_order)

    # Measure time for initial solution using nearest neighbor heuristic
    start_initial = time.time()
    
    # Nearest neighbor heuristic and path initialization
    unvisited = set(city['name'] for city in cities_sorted)
    path = [cities_sorted[0]]
    current_city = cities_sorted[0]

    while unvisited:
        unvisited.discard(current_city['name'])
        closest = min((city for city in cities_sorted if city['name'] in unvisited), 
                      key=lambda city: calculate_distance(current_city, city), 
                      default=None)
        if closest is None:
            break

        path.append(closest)
        current_city = closest

    # Ensure path returns to start to form a complete tour
    path.append(path[0])
    initial_distance = total_distance(path)
    end_initial = time.time()
    initial_time = round((end_initial - start_initial) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

    # Measure time for optimizing the path using in-place 2-opt
    start_optimized = time.time()
    
    # In-place 2-opt optimization
    improved = True

    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                if (
                    calculate_distance(path[i - 1], path[i]) + calculate_distance(path[j], path[(j + 1) % len(path)])
                    > calculate_distance(path[i - 1], path[j]) + calculate_distance(path[i], path[(j + 1) % len(path)])
                ):
                    path[i:j + 1] = reversed(path[i:j + 1])
                    improved = True

    optimized_distance = total_distance(path)
    end_optimized = time.time()
    optimized_time = round((end_optimized - start_optimized) * 1000, 2)  # Convert to milliseconds and round to 2 decimal places

    result = {
        'initial_path': [city['name'] for city in path],
        'optimized_path': [city['name'] for city in path],
        'initial_distance': initial_distance,
        'optimized_distance': optimized_distance,
        'initial_time': initial_time,
        'optimized_time': optimized_time
    }
    return result

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
                    cities = json.loads(data.decode('utf-8'))
                    result = solve_tsp(cities)
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
                    cities = json.loads(data.decode('utf-8'))
                    result = solve_tsp(cities)
                    response = json.dumps(result).encode('utf-8')
                    udp_socket.sendto(response, address)
            except Exception as e:
                print(f"UDP error: {e}")
