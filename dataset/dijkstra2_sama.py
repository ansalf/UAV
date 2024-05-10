import pandas as pd
import numpy as np
import math

def euclidean_distance(point1, point2):
    # Menghitung jarak Euclidean antara dua titik
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def dijkstra_sequential(start, graph, nodes):
    open_list = set(graph.keys())
    
    g_score = {node: float('inf') for node in open_list}
    g_score[start] = 0
    
    came_from = {}
    
    current_node = start
    for node in nodes:
        if node == start:
            continue
        tentative_g_score = g_score[current_node] + euclidean_distance(current_node, node)
        if tentative_g_score < g_score[node]:
            came_from[node] = current_node
            g_score[node] = tentative_g_score
        current_node = node
    
    return came_from, g_score

def print_path_to_node(node, came_from, g_score):
    path = []
    while node in came_from:
        path.append(node)
        node = came_from[node]
    path.append(node)
    path.reverse()
    print("Path:", path)
    print("Distance:", g_score[path[-1]])

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

# Titik awal dimulai dari (0.0, 0.0)
start_point = (0.0, 0.0)

# Mendapatkan list node yang akan diekspansi
nodes_to_expand = list(graph.keys())
nodes_to_expand.remove(start_point)

# Gunakan algoritma Dijkstra untuk mencari jalur terpendek ke setiap titik dari (0,0)
came_from, g_score = dijkstra_sequential(start_point, graph, nodes_to_expand)

# Hitung total jarak yang ditempuh untuk memadamkan semua titik
total_distance_traveled = sum(g_score.values())

print("Total distance needed to travel to extinguish all points:", total_distance_traveled, "units")

# Cetak jalur yang dilalui dan jaraknya untuk setiap titik
for node in nodes_to_expand:
    print(f"Path to point {node}:")
    print_path_to_node(node, came_from, g_score)
    print()
