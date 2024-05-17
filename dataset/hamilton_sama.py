import pandas as pd
import numpy as np

def is_safe(v, graph, path, pos):
    if graph[path[pos - 1]][v] == 0:
        return False
    
    if v in path:
        return False
    
    return True

def hamiltonian_path_util(graph, path, pos):
    if pos == len(graph):
        return True
    
    for v in range(1, len(graph)):
        if is_safe(v, graph, path, pos):
            path[pos] = v
            if hamiltonian_path_util(graph, path, pos + 1):
                return True
            
            path[pos] = -1
    
    return False

def hamiltonian_path(graph):
    path = [-1] * len(graph)
    path[0] = 0
    
    if not hamiltonian_path_util(graph, path, 1):
        print("No Hamiltonian Path found")
        return None
    
    print("Hamiltonian Path found:", path)
    return path

def main():
    # Load dataset
    df = pd.read_csv('fire_archive_M6_96619_5data.csv')
    
    # Create a graph from the dataset
    coords = df[['latitude', 'longitude']].to_numpy()
    n = len(coords)
    graph = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = np.linalg.norm(coords[i] - coords[j])
    
    # Find Hamiltonian Path
    path = hamiltonian_path(graph)
    
    if path is not None:
        for i in range(len(path)):
            print(f"Step {i+1}: {coords[path[i]]}")

if __name__ == "__main__":
    main()
