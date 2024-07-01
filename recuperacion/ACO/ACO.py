import tqdm
from typing import Callable
from Common.fitness import evaluate_fitness
from Pheromone import Pheromone
from Common.Solution import Solution

def ACO(n_ants: int, iterations: int, alpha: float, beta: float, max_pieces: int, pieces: list, x_dim: int, y_dim: int, heuristic: Callable):
    pheromones = Pheromone.initialize_pheromones(max_pieces)
    pheromone_evolution = []
    fitness_evolution =  []
    
    best_fitness = 0
    best_solution = Solution(x_dim=x_dim, y_dim=y_dim,pieces=pieces,max_pieces=max_pieces) #empty solution.
    
    progress_bar = tqdm.tqdm(range(iterations), desc="iterations", leave=False)
    for i in progress_bar:
        Solution_list = []
        
        progress_ants = tqdm.tqdm(range(n_ants), desc="ants", leave=False)
        for _ in progress_ants:
            solution = Solution.construct_solution(pheromones, x_dim, y_dim, pieces, max_pieces, alpha, beta, heuristic)
            Solution_list.append(solution)
            fitness = evaluate_fitness(solution.board, solution.x_dim, solution.y_dim)
            if (fitness > best_fitness):
                best_solution = solution
                best_fitness = fitness
        fitness_evolution.append(best_fitness)
        pheromones = Pheromone.update_pheromones(pheromones, Solution_list, max_pieces, pieces)
        pheromone_evolution += Pheromone.get_placed(pheromones)
        
        i = i + 1 
    progress_bar.close()

    return best_solution, fitness_evolution, pheromone_evolution