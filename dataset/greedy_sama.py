import pandas as pd
import numpy as np
import math

def euclidean_distance(point1, point2):
    # Menghitung jarak Euclidean antara dua titik
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def greedy(start, goals, graph):
    current_node = start
    path = [start]
    total_distance = 0
    
    for goal in goals:
        nearest_neighbor = min(graph[current_node], key=lambda neighbor: euclidean_distance(neighbor, goal))
        distance = euclidean_distance(current_node, nearest_neighbor)
        total_distance += distance
        path.append(nearest_neighbor)
        print(f"Step: {current_node} -> {nearest_neighbor} (Distance: {distance})")
        current_node = nearest_neighbor
    
    return path, total_distance

# Load dataset
df = pd.read_csv('fire_archive_M6_96619_5data.csv')

# Inisialisasi graf
graph = {}
for index, row in df.iterrows():
    node = (row['latitude'], row['longitude'])
    neighbors = [(r['latitude'], r['longitude']) for idx, r in df.iterrows() if (r['latitude'], r['longitude']) != node]
    graph[node] = neighbors

# Tambahkan titik awal ke graf dengan koneksi ke titik pertama dalam dataset
graph[(0.0, 0.0)] = [(df.iloc[0]['latitude'], df.iloc[0]['longitude'])]

# Titik awal dimulai dari (0.0, 0.0)
start_point = (0.0, 0.0)

# Tujuan diambil dari setiap titik dalam dataset
goals = [(row['latitude'], row['longitude']) for index, row in df.iterrows()]

# Gunakan algoritma Greedy untuk mencari jalur terpendek
path, total_distance = greedy(start_point, goals, graph)

# Output jalur dan total jarak
print("Greedy Path:")
print(path)
print("Total distance traveled:", total_distance, "units")
