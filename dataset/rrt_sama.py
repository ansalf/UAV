import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

def euclidean_distance(point1, point2):
    return math.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

def get_random_node(goal_sample_rate, x_range, y_range, goal_node):
    if np.random.rand() > goal_sample_rate:
        return Node(np.random.uniform(x_range[0], x_range[1]), np.random.uniform(y_range[0], y_range[1]))
    return goal_node

def get_nearest_node(tree, random_node):
    distances = [euclidean_distance((node.x, node.y), (random_node.x, random_node.y)) for node in tree]
    nearest_index = distances.index(min(distances))
    return tree[nearest_index]

def steer(from_node, to_node, extend_length=float('inf')):
    new_node = Node(from_node.x, from_node.y)
    distance = euclidean_distance((from_node.x, from_node.y), (to_node.x, to_node.y))
    
    if distance <= extend_length:
        new_node.x = to_node.x
        new_node.y = to_node.y
    else:
        theta = np.arctan2(to_node.y - from_node.y, to_node.x - from_node.x)
        new_node.x += extend_length * np.cos(theta)
        new_node.y += extend_length * np.sin(theta)
    
    new_node.parent = from_node
    return new_node

def is_collision_free(node, obstacle_list):
    for (ox, oy, radius) in obstacle_list:
        if euclidean_distance((node.x, node.y), (ox, oy)) <= radius:
            return False
    return True

def generate_final_path(goal_node):
    path = []
    node = goal_node
    while node is not None:
        path.append([node.x, node.y])
        node = node.parent
    return path

def rrt(start, goal, obstacle_list, x_range, y_range, max_iter=500, goal_sample_rate=0.1, extend_length=1.0):
    start_node = Node(start[0], start[1])
    goal_node = Node(goal[0], goal[1])
    tree = [start_node]

    for _ in range(max_iter):
        random_node = get_random_node(goal_sample_rate, x_range, y_range, goal_node)
        nearest_node = get_nearest_node(tree, random_node)
        new_node = steer(nearest_node, random_node, extend_length)
        
        if is_collision_free(new_node, obstacle_list):
            tree.append(new_node)
            
            if euclidean_distance((new_node.x, new_node.y), (goal_node.x, goal_node.y)) <= extend_length:
                final_node = steer(new_node, goal_node, extend_length)
                if is_collision_free(final_node, obstacle_list):
                    return generate_final_path(final_node)

    return None

def main():
    # Load dataset
    df = pd.read_csv('fire_archive_M6_96619_5data.csv')

    # Define search space boundaries
    x_range = (df['latitude'].min(), df['latitude'].max())
    y_range = (df['longitude'].min(), df['longitude'].max())

    # Define obstacles (assuming none in this example)
    obstacle_list = []

    # Start and goal locations (starting from origin to the first point)
    start = (0.0, 0.0)
    goal = (df.iloc[0]['latitude'], df.iloc[0]['longitude'])

    path = rrt(start, goal, obstacle_list, x_range, y_range)

    if path is None:
        print("No path found!")
    else:
        print("Path found!")
        path = np.array(path)
        plt.plot(path[:,0], path[:,1], '-r')
        plt.plot(start[0], start[1], 'go')
        plt.plot(goal[0], goal[1], 'bo')
        
        for (ox, oy, radius) in obstacle_list:
            circle = plt.Circle((ox, oy), radius, color='gray')
            plt.gca().add_patch(circle)
        
        plt.xlim(x_range)
        plt.ylim(y_range)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()
