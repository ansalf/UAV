import pandas as pd
import numpy as np
import math

def euclidean_distance(point1, point2):
    # Menghitung jarak Euclidean antara dua titik
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def dijkstra_all(start, graph):
    open_list = set(graph.keys())
    
    g_score = {node: float('inf') for node in open_list}
    g_score[start] = 0
    
    came_from = {}
    
    while open_list:
        current_node = min(open_list, key=lambda node: g_score[node])
        open_list.remove(current_node)
        
        for neighbor in graph[current_node]:
            tentative_g_score = g_score[current_node] + euclidean_distance(current_node, neighbor)
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
    
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

# Gunakan algoritma Dijkstra untuk mencari jalur terpendek ke semua titik
came_from, g_score = dijkstra_all(start_point, graph)

# Hitung total jarak yang ditempuh untuk memadamkan semua titik
total_distance_traveled = sum(g_score.values())

# print("Total distance needed to travel to extinguish all points:", total_distance_traveled, "units")

# Cetak jalur yang dilalui dan jaraknya untuk setiap titik
for node in graph.keys():
    if node != start_point:
        print(f"Path to point {node}:")
        print_path_to_node(node, came_from, g_score)
        print()
