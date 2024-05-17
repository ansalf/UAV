import pandas as pd
import numpy as np
import random
import math

# Load dataset
df = pd.read_csv('fire_archive_M6_96619_5data.csv')

# Inisialisasi graf
graph = {}
for index, row in df.iterrows():
    node = (row['latitude'], row['longitude'])
    neighbors = []
    for idx, r in df.iterrows():
        if (r['latitude'], r['longitude']) != node:
            neighbors.append((r['latitude'], r['longitude']))
    graph[node] = neighbors

# Tambahkan titik awal ke graf dengan koneksi ke titik pertama dalam dataset
graph[(0.0, 0.0)] = [(df.iloc[0]['latitude'], df.iloc[0]['longitude'])]

# Parameter ACO
num_ants = 10
alpha = 1.0  # Bobot jejak feromon
beta = 2.0   # Bobot jarak
evaporation_rate = 0.5  # Tingkat penguapan feromon
initial_pheromone = 1.0  # Konsentrasi awal feromon
num_iterations = 100

# Inisialisasi jejak feromon
pheromone = {}
for node in graph.keys():
    pheromone[node] = {}
    for neighbor in graph[node]:
        pheromone[node][neighbor] = initial_pheromone

# Fungsi untuk memilih node berikutnya berdasarkan jejak feromon dan jarak
def select_next_node(current_node, allowed_nodes):
    probabilities = []
    total = 0.0
    for node in allowed_nodes:
        pheromone_level = pheromone[current_node][node]
        distance = euclidean_distance(current_node, node)
        probabilities.append((node, pheromone_level ** alpha * (1.0 / distance) ** beta))
        total += probabilities[-1][1]
    probabilities = [(node, p / total) for node, p in probabilities]
    selected_node = np.random.choice([node for node, _ in probabilities], p=[p for _, p in probabilities])
    return selected_node

# Fungsi untuk menghitung jarak Euclidean antara dua titik
def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Algoritma ACO
best_path = None
best_distance = float('inf')
for iteration in range(num_iterations):
    for ant in range(num_ants):
        current_node = (0.0, 0.0)  # Memulai dari titik awal
        unvisited_nodes = list(graph.keys())
        unvisited_nodes.remove(current_node)
        path = [current_node]
        while unvisited_nodes:
            next_node = select_next_node(current_node, unvisited_nodes)
            path.append(next_node)
            unvisited_nodes.remove(next_node)
            current_node = next_node
        distance = sum(euclidean_distance(path[i], path[i+1]) for i in range(len(path) - 1))
        if distance < best_distance:
            best_distance = distance
            best_path = path
    # Penguapan feromon
    for node in graph.keys():
        for neighbor in graph[node]:
            pheromone[node][neighbor] *= (1.0 - evaporation_rate)
    # Peningkatan jejak feromon
    for i in range(len(best_path) - 1):
        pheromone[best_path[i]][best_path[i+1]] += (1.0 / best_distance)

# Output hasil terbaik
print("Best path found:", best_path)
print("Best distance found:", best_distance)
