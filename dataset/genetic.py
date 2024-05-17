import pandas as pd
import numpy as np
import random

# Load dataset
df = pd.read_csv('fire_archive_M6_96619_5data.csv')

# Define coordinates
coordinates = [(row['latitude'], row['longitude']) for index, row in df.iterrows()]

# Create initial population
def create_individual(coordinates):
    return random.sample(coordinates, len(coordinates))

def calculate_fitness(individual):
    total_distance = 0
    for i in range(len(individual) - 1):
        total_distance += euclidean_distance(individual[i], individual[i + 1])
    return total_distance

def crossover(parent1, parent2):
    # Select a random crossover point
    crossover_point = random.randint(0, len(parent1) - 1)
    
    # Create offspring
    offspring = parent1[:crossover_point]
    remaining = [item for item in parent2 if item not in offspring]
    offspring.extend(remaining)
    
    return offspring

def mutate(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            # Swap two random cities
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def genetic_algorithm(coordinates, population_size, mutation_rate, generations):
    population = [create_individual(coordinates) for _ in range(population_size)]
    
    for generation in range(generations):
        population = sorted(population, key=lambda x: calculate_fitness(x))
        
        # Select top individuals for breeding
        top_individuals = population[:int(0.2 * population_size)]
        
        # Create next generation through crossover and mutation
        next_generation = []
        while len(next_generation) < population_size:
            parent1 = random.choice(top_individuals)
            parent2 = random.choice(top_individuals)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            next_generation.append(child)
        
        population = next_generation
    
    # Find the best individual
    best_individual = min(population, key=lambda x: calculate_fitness(x))
    best_fitness = calculate_fitness(best_individual)
    
    return best_individual, best_fitness

best_path, best_distance = genetic_algorithm(coordinates, population_size=100, mutation_rate=0.01, generations=100)

print("Best path found by genetic algorithm:", best_path)
print("Total distance needed to travel to extinguish all points:", best_distance)
