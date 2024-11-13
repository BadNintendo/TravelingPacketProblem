import socket
import json
import time

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

def tcp_client():
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect(('127.0.0.1', 3000))
        
        start_time = time.time()
        tcp_socket.sendall(cities_data)
        
        data = tcp_socket.recv(4096)
        end_time = time.time()
        processing_time = round((end_time - start_time) * 1000, 2)
        
        response = json.loads(data.decode('utf-8'))
        print("TCP Response:")
        print(f"Initial Path: {response['initial_path']}")
        print(f"Optimized Path: {response['optimized_path']}")
        print(f"Initial Distance: {response['initial_distance']}")
        print(f"Optimized Distance: {response['optimized_distance']}")
        print(f"Initial Solution Time (ms): {response['initial_time']}")
        print(f"Optimization Time (ms): {response['optimized_time']}")
        print(f"TCP Processing Time (ms): {processing_time}")
    except Exception as e:
        print(f"TCP error: {e}")
    finally:
        tcp_socket.close()

def udp_client():
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('127.0.0.1', 3000)
        
        start_time = time.time()
        udp_socket.sendto(cities_data, server_address)
        
        data, _ = udp_socket.recvfrom(4096)
        end_time = time.time()
        processing_time = round((end_time - start_time) * 1000, 2)
        
        response = json.loads(data.decode('utf-8'))
        print("UDP Response:")
        print(f"Initial Path: {response['initial_path']}")
        print(f"Optimized Path: {response['optimized_path']}")
        print(f"Initial Distance: {response['initial_distance']}")
        print(f"Optimized Distance: {response['optimized_distance']}")
        print(f"Initial Solution Time (ms): {response['initial_time']}")
        print(f"Optimization Time (ms): {response['optimized_time']}")
        print(f"UDP Processing Time (ms): {processing_time}")
    except Exception as e:
        print(f"UDP error: {e}")
    finally:
        udp_socket.close()

# Sequentially handle both TCP and UDP
print("Sending data using TCP...")
tcp_client()
print("\nSending data using UDP...")
udp_client()