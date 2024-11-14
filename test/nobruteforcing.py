import math
import time

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

def total_distance(path):
    return sum(calculate_distance(path[i], path[(i + 1) % len(path)]) for i in range(len(path)))

def morton_order(city):
    def interleave_bits(x, y):
        def spread_bits(v):
            return (v | (v << 8)) & 0x00FF00FF | ((v | (v << 4)) & 0x0F0F0F0F) | ((v | (v << 2)) & 0x33333333) | ((v | (v << 1)) & 0x55555555)
        return spread_bits(x) | (spread_bits(y) << 1)
    x = int(city['x'] * 10000)  # Scale to avoid float precision issues
    y = int(city['y'] * 10000)
    return interleave_bits(x, y)

def solve_tsp(cities):
    """
    Solve the Traveling Salesperson Problem (TSP) using the 2-opt optimization method.
    
    :param cities: List of city dictionaries to be visited.
    :return: Dictionary containing the optimized path, distance, time, and coordinates.
    """
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

# Run the function and print results
result = solve_tsp(cities)
if 'error' in result:
    print(f"Error: {result['error']}")
else:
    print("Optimized Path:", result['optimized_path'])
    print("Optimized Distance:", result['optimized_distance'])
    print("Optimization Time (ms):", result['optimization_time'])
    print("Optimized Array:", result['optimized_array'])
