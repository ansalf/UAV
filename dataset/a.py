import pandas as pd
import numpy as np
import math
from heapq import heappop, heappush

def euclidean_distance(point1, point2):
    # Menghitung jarak Euclidean antara dua titik
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def a_star(start, goal, graph):
    open_list = []
    heappush(open_list, (0, start))  # (f-score, node)
    
    g_score = {start: 0}
    f_score = {start: euclidean_distance(start, goal)}
    
    came_from = {}
    
    while open_list:
        current_f, current_node = heappop(open_list)
        
        if current_node == goal:
            # Jika mencapai tujuan, kembalikan jalur
            path = []
            total_distance = g_score[current_node]
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path, total_distance, f_score[goal] - total_distance
        
        for neighbor in graph[current_node]:
            tentative_g_score = g_score[current_node] + euclidean_distance(current_node, neighbor)
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_node
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                heappush(open_list, (f_score[neighbor], neighbor))
    
    return None, None, None  # Jika tidak ada jalur yang ditemukan

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

# Titik awal dan akhir sama dengan titik pertama dalam dataset
start_point = (df.iloc[0]['latitude'], df.iloc[0]['longitude'])
end_point = start_point

# Gunakan algoritma A* untuk mencari jalur terpendek
shortest_paths = []
total_distance_traveled = 0

for i in range(len(df)):
    # Cari jalur dari titik saat ini ke titik berikutnya
    path, distance_traveled, distance_remaining = a_star(start_point, end_point, graph)
    if path:
        shortest_paths.append((path, distance_traveled, distance_remaining))
        total_distance_traveled += distance_traveled
        # Perbarui titik awal untuk pencarian jalur berikutnya
        start_point = end_point
        # Pilih titik berikutnya sebagai titik akhir
        end_point = (df.iloc[i]['latitude'], df.iloc[i]['longitude'])

# Cari jalur terpendek dari titik terakhir kembali ke titik awal
final_path, final_distance_traveled, final_distance_remaining = a_star(end_point, (0.0, 0.0), graph)
if final_path:
    shortest_paths.append((final_path, final_distance_traveled, final_distance_remaining))
    total_distance_traveled += final_distance_traveled

# Tampilkan hasil rute
for i, (path, distance_traveled, distance_remaining) in enumerate(shortest_paths):
    print(f"Jalur {i+1}: {path}")
    print(f"Jarak yang telah ditempuh: {distance_traveled} satuan")
    print(f"Sisa jarak yang harus ditempuh: {distance_remaining} satuan")
