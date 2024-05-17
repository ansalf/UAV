import pandas as pd
import math

def euclidean_distance(point1, point2):
    # Menghitung jarak Euclidean antara dua titik
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def bidirectional_search(graph, start_points, goal_points):
    # Inisialisasi titik awal dan titik tujuan
    open_set_start = set(start_points)
    open_set_goal = set(goal_points)
    
    # Inisialisasi kumpulan titik yang sudah diekspansi untuk kedua arah
    expanded_start = set()
    expanded_goal = set()
    
    # Loop sampai kedua arah bertemu
    while open_set_start and open_set_goal:
        # Ekspansi dari titik awal
        current_start = expanded_start.pop() if expanded_start else open_set_start.pop()
        for neighbor in graph.get(current_start, []):  # Periksa apakah titik ada dalam graf
            if neighbor in open_set_start:
                open_set_start.remove(neighbor)
                expanded_start.add(neighbor)
        
        # Ekspansi dari titik tujuan
        current_goal = expanded_goal.pop() if expanded_goal else open_set_goal.pop()
        for neighbor in graph.get(current_goal, []):  # Periksa apakah titik ada dalam graf
            if neighbor in open_set_goal:
                open_set_goal.remove(neighbor)
                expanded_goal.add(neighbor)
        
        # Cek apakah kedua arah bertemu
        intersection = expanded_start.intersection(expanded_goal)
        if intersection:
            intersecting_nodes = intersection
            return intersecting_nodes
    
    # Jika tidak ada titik yang bertemu
    return None

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

# Tambahkan titik awal ke graf dengan koneksi ke semua titik dalam dataset
start_points = [(0.0, 0.0)]
goal_points = list(graph.keys())

# Gunakan algoritma bidirectional search untuk mencari titik yang bertemu
intersecting_nodes = bidirectional_search(graph, start_points, goal_points)

if intersecting_nodes is not None:
    print("Paths exist between start and goal:")
    print("Intersecting nodes:", intersecting_nodes)
else:
    print("Paths do not exist between start and goal.")
