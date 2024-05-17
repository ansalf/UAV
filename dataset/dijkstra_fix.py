import pandas as pd
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
df = pd.read_csv('datasetedit.csv')

# Inisialisasi graf
graph = {}
for index, row in df.iterrows():
    node = (row['X'], row['Y'])
    neighbors = []
    for idx, r in df.iterrows():
        if (r['X'], r['Y']) != node:
            neighbors.append((r['X'], r['Y']))
    graph[node] = neighbors

# Titik awal dimulai dari baris pertama dalam dataset
start_point = (df.iloc[0]['X'], df.iloc[0]['Y'])

# Mendapatkan list node yang akan diekspansi
nodes_to_expand = list(graph.keys())
nodes_to_expand.remove(start_point)

# Gunakan algoritma Dijkstra untuk mencari jalur terpendek ke setiap titik dari titik awal
came_from, g_score = dijkstra_sequential(start_point, graph, nodes_to_expand)

# Hitung total jarak yang ditempuh untuk memadamkan semua titik
total_distance_traveled = sum(g_score.values())

print("Total distance needed to travel to extinguish all points:", total_distance_traveled, "units")

# Cetak jalur yang dilalui dan jaraknya untuk setiap titik
for node in nodes_to_expand:
    print(f"Path to point {node}:")
    print_path_to_node(node, came_from, g_score)
    print()
