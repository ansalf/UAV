import pandas as pd
import math

def euclidean_distance(point1, point2):
    # Calculate the Euclidean distance between two points
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def bidirectional_search(start, goal, graph):
    forward_open_list = [(0, start)]  # (cost, node)
    backward_open_list = [(0, goal)]  # (cost, node)
    forward_g_score = {start: 0}
    backward_g_score = {goal: 0}
    common_node = None
    min_cost = float('inf')

    while forward_open_list and backward_open_list:
        forward_cost, forward_node = forward_open_list.pop(0)
        backward_cost, backward_node = backward_open_list.pop(0)

        if forward_node in backward_g_score:
            # Found common node, calculate total cost
            cost = forward_g_score[forward_node] + backward_g_score[forward_node]
            if cost < min_cost:
                min_cost = cost
                common_node = forward_node

        if common_node:
            break

        for neighbor in graph[forward_node]:
            tentative_g_score = forward_g_score[forward_node] + euclidean_distance(forward_node, neighbor)
            if neighbor not in forward_g_score or tentative_g_score < forward_g_score[neighbor]:
                forward_g_score[neighbor] = tentative_g_score
                forward_open_list.append((tentative_g_score, neighbor))
                forward_open_list.sort(key=lambda x: x[0])

        for neighbor in graph[backward_node]:
            tentative_g_score = backward_g_score[backward_node] + euclidean_distance(backward_node, neighbor)
            if neighbor not in backward_g_score or tentative_g_score < backward_g_score[neighbor]:
                backward_g_score[neighbor] = tentative_g_score
                backward_open_list.append((tentative_g_score, neighbor))
                backward_open_list.sort(key=lambda x: x[0])

        # Update forward open list with proper cost
        for i, (cost, node) in enumerate(forward_open_list):
            forward_open_list[i] = (forward_g_score[node], node)
        forward_open_list.sort()

        # Update backward open list with proper cost
        for i, (cost, node) in enumerate(backward_open_list):
            backward_open_list[i] = (backward_g_score[node], node)
        backward_open_list.sort()

    if common_node:
        return min_cost, common_node
    else:
        return None, None

# Load dataset
df = pd.read_csv('fire_archive_M6_96619_5data.csv')

# Initialize the graph
graph = {}
for index, row in df.iterrows():
    node = (row['latitude'], row['longitude'])
    neighbors = []
    for idx, r in df.iterrows():
        if (r['latitude'], r['longitude']) != node:
            neighbors.append((r['latitude'], r['longitude']))
    graph[node] = neighbors

# Add the starting point to the graph with a connection to the first point in the dataset
graph[(0.0, 0.0)] = [(df.iloc[0]['latitude'], df.iloc[0]['longitude'])]

# The starting and ending points
start_point = (0.0, 0.0)
end_point = (df.iloc[0]['latitude'], df.iloc[0]['longitude'])

# Use bidirectional search to find the shortest path
total_distance_traveled, common_node = bidirectional_search(start_point, end_point, graph)

if common_node:
    print("Common node found:", common_node)
    print("Total distance traveled:", total_distance_traveled)
else:
    print("No common node found, path does not exist.")
