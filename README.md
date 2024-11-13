**Single-Threaded TSP Solver with TCP/UDP Server and Client Communication**

This project implements a single-threaded server-client system to solve the Traveling Salesperson Problem (TSP) using both TCP and UDP communication protocols. The server is designed to handle incoming data from the client, process it to find an optimized path for the TSP, and return the results to the client.

### Features:
- **Single-Threaded Design:** The server handles both TCP and UDP requests in a single thread using the `select` module, ensuring efficient resource utilization and simplicity.
- **TSP Solver:** Utilizes a combination of Morton order sorting, nearest neighbor heuristic, and an in-place 2-opt algorithm to find and optimize a path through a set of cities.
- **TCP and UDP Protocols:** Supports both reliable (TCP) and fast, connectionless (UDP) communication, allowing clients to choose the protocol best suited to their needs.
- **JSON Communication:** Data is serialized and deserialized using JSON, ensuring a structured and easily parseable format for communication between server and client.
- **Performance Logging:** Measures and logs the processing time for both initial and optimized solutions, providing insights into the efficiency of the TSP solver.

### How It Works:
1. **Server Setup:** The server listens for incoming TCP and UDP connections on a specified address and port (`127.0.0.1:3000`). It uses `select.select()` to monitor both TCP and UDP sockets for incoming data.
2. **Client Requests:** The client sends a list of cities, encoded as JSON, to the server via either TCP or UDP. Each city is represented by a dictionary containing its name and coordinates (`x`, `y`).
3. **TSP Solving:**
   - **Distance Calculation:** Uses memoization to efficiently compute and store distances between cities.
   - **Morton Order Sorting:** Sorts cities based on their Morton order to improve the initial path construction.
   - **Nearest Neighbor Heuristic:** Constructs an initial path by repeatedly selecting the closest unvisited city.
   - **2-Opt Optimization:** Improves the initial path by iteratively reversing segments to reduce the total distance.
4. **Response:** The server processes the cities to find an optimized path, measures the time taken for both initial and optimized solutions, and sends the results back to the client.
5. **Client Logging:** The client receives the results, including the initial and optimized paths, distances, and processing times, and logs them to the console for verification.

### Example Use Case:
This project serves as a fun and educational exercise in building networked applications and solving optimization problems. It demonstrates how to combine computational algorithms with network communication, providing a foundation for more advanced distributed computing projects.

```
Sending data using UDP...
UDP Response:
Initial Path: ['City0', 'City1', 'City2', 'City4', 'City7', 'City9', 'City12', 'City14', 'City17', 'City19', 'City22', 'City24', 'City27', 'City29', 'City32', 'City34', 'City37', 'City39', 'City42', 'City44', 'City47', 'City49', 'City48', 'City46', 'City45', 'City43', 'City41', 'City40', 'City38', 'City36', 'City35', 'City33', 'City31', 'City30', 'City28', 'City26', 'City25', 'City23', 'City21', 'City20', 'City18', 'City16', 'City15', 'City13', 'City11', 'City10', 'City8', 'City6', 'City5', 'City3', 'City0']
Optimized Path: ['City0', 'City1', 'City2', 'City4', 'City7', 'City9', 'City12', 'City14', 'City17', 'City19', 'City22', 'City24', 'City27', 'City29', 'City32', 'City34', 'City37', 'City39', 'City42', 'City44', 'City47', 'City49', 'City48', 'City46', 'City45', 'City43', 'City41', 'City40', 'City38', 'City36', 'City35', 'City33', 'City31', 'City30', 'City28', 'City26', 'City25', 'City23', 'City21', 'City20', 'City18', 'City16', 'City15', 'City13', 'City11', 'City10', 'City8', 'City6', 'City5', 'City3', 'City0']
Initial Distance: 1257.0209779547552
Optimized Distance: 1051.0785415861549
Initial Solution Time (ms): 1.0
Optimization Time (ms): 5.23
UDP Processing Time (ms): 7.23
```
