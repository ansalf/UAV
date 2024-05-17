import pandas as pd
import numpy as np
import math
from heapq import heappop, heappush

def euclidean_distance(point1, point2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def line_of_sight(p1, p2, graph):
    # Check if there's a clear line of sight between two points
    # Implementing Bresenham's line algorithm
    x0, y0 = p1
    x1, y1 = p2
    dx = x1 - x0
    dy = y1 - y0
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        err = dx / 2.0
        while x0 != x1:
            if (x0, y0) in graph and graph[(x0, y0)] == 1:
                return False
            err -= dy
            if err < 0:
                y0 += sy
                err += dx
            x0 += sx
    else:
        err = dy / 2.0
        while y0 != y1:
            if (x0, y0) in graph and graph[(x0, y0)] == 1:
                return False
            err -= dx
            if err < 0:
                x0 += sx
                err += dy
            y0 += sy
    return True

def theta_star(start, goal, graph):
    open_list = []
    closed_list = set()
    came_from = {}
    
    g_score = {start: 0}
    f_score = {start: euclidean_distance(start, goal)}
    
    heappush(open_list, (f_score[start], start))  # (f-score, node)
    
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
            return path, total_distance
        
        closed_list.add(current_node)
        
        for neighbor in graph[current_node]:
            if neighbor in closed_list:
                continue
            
            if line_of_sight(current_node, neighbor, graph):
                tentative_g_score = g_score[current_node] + euclidean_distance(current_node, neighbor)
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_node
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                    heappush(open_list, (f_score[neighbor], neighbor))
    
    return None, None  # If no path found

# Load dataset
df = pd.read_csv('fire_archive_M6_96619_5data.csv')

# Create a dictionary to represent the graph
graph = {(row['latitude'], row['longitude']): 0 for index, row in df.iterrows()}

# Set obstacles in the graph (you might need to adjust this based on your data)
# For example, if there's a fire at a certain location, mark it as an obstacle
# For simplicity, let's mark some random points as obstacles
# Let's say if the latitude is greater than 20.0, we consider it as an obstacle
for index, row in df.iterrows():
    if row['latitude'] > 20.0:
        graph[(row['latitude'], row['longitude'])] = 1

# Define start and goal points
start_point = (0.0, 0.0)
end_point = (df.iloc[0]['latitude'], df.iloc[0]['longitude'])

# Find the shortest path using Theta* algorithm
path, total_distance_traveled = theta_star(start_point, end_point, graph)

if path:
    print("Shortest Path found using Theta*:")
    print(path)
    print("Total distance traveled:", total_distance_traveled)
else:
    print("No path found using Theta* algorithm.")
