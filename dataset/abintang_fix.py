import pandas as pd
import numpy as np
import math
from heapq import heappop, heappush

def euclidean_distance(point1, point2):
    # Calculate the Euclidean distance between two points
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
            # If reached the goal, return the path
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
    
    return None, None, None  # If no path found

# Load dataset
df = pd.read_csv('datasetedit.csv')

# Initialize the graph
graph = {}
for index, row in df.iterrows():
    node = (row['X'], row['Y'])
    neighbors = []
    for idx, r in df.iterrows():
        if (r['X'], r['Y']) != node:
            neighbors.append((r['X'], r['Y']))
    graph[node] = neighbors

# The starting and ending points
start_point = (df.iloc[0]['X'], df.iloc[0]['Y'])
end_point = (df.iloc[-1]['X'], df.iloc[-1]['Y'])

# Use the A* algorithm to find the shortest path
total_distance_traveled = 0
current_point = start_point
for i in range(len(df) - 1):
    next_point = (df.iloc[i]['X'], df.iloc[i]['Y'])
    next_next_point = (df.iloc[i+1]['X'], df.iloc[i+1]['Y'])
    distance = euclidean_distance(current_point, next_point)
    total_distance_traveled += distance
    print(f"\nDistance {i+1}: {current_point} to {next_point} = {distance} units")
    print(f"Total current distance: {total_distance_traveled} units")
    print(f"Distance to be traveled: {euclidean_distance(next_point, next_next_point)} units")
    current_point = next_point

print("\nTotal distance traveled:", total_distance_traveled, "units")
