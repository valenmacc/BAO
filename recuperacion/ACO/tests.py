from ACO import ACO
import tqdm
import random
from Common.fitness import evaluate_fitness
from Common.heuristic import *
from Common.Piece import Piece

def evaluate_variation_alpha_beta(tests: int, runs: int, alpha: float, beta: float, increment: float):
    print(f"doing {runs} runs with alpha={alpha} and beta={beta} with {tests} different seeds.\n")
    defs = []
    a_inc= []
    a_dec= []
    b_inc= []
    b_dec= []
    ab_i = []
    ab_d = []
    tests_bar = tqdm.tqdm(range(tests), desc="Tests")
    for j in tests_bar:
        #print(f"test {i + 1}:\n")
        random.seed(j)
        pieces = Piece.generate_random_pieces(30, 10)
        
        #print("default")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha, beta=beta, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        defs.append(average)
        
        #print(f"increase of {increment} in alpha")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha+increment, beta=beta, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        a_inc.append(average)
        
        #print(f"decrease of {-increment} in alpha")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha-increment, beta=beta, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        a_dec.append(average)
        
        #print(f"increase of {increment} in beta")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha, beta=beta+increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        b_inc.append(average)
        
        #print(f"decrease of {-increment} in beta")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha, beta=beta-increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        b_dec.append(average)
        
        #print(f"increase of {increment} in both")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha+increment, beta=beta+increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        ab_i.append(average)
        
        #print(f"decrease of {increment} in both")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=10, iterations=10, alpha=alpha-increment, beta=beta-increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        #print("average fitness of the solution:",average)
        ab_d.append(average)
    print(f"average over tests of default is:",sum(defs)/len(defs))
    
    print(f"average over tests with alpha {alpha+increment} and beta {beta} is: {sum(a_inc)/len(a_inc)}")
    print(f"average over tests with alpha {alpha-increment} and beta {beta} is: {sum(a_dec)/len(a_dec)}")
    
    print(f"average over tests with alpha {alpha} and beta {beta+increment} is: {sum(b_inc)/len(b_inc)}")
    print(f"average over tests with alpha {alpha} and beta {beta-increment} is: {sum(b_dec)/len(b_dec)}")
    
    print(f"average over tests with alpha {alpha+increment} and beta {beta+increment} is: {sum(ab_i)/len(ab_i)}")
    print(f"average over tests with alpha {alpha-increment} and beta {beta-increment} is: {sum(ab_d)/len(ab_d)}")
    
    
def evaluate_more_ants_or_iterations(tests: int, runs: int, ants: int, iterations: int, heuristic):
    print(f"doing {runs} runs of {iterations} iterations with {ants} ants with {tests} different seeds.\n")
    for j in range(tests):
        print(f"test {j + 1}:\n")
        random.seed(j)
        pieces = Piece.generate_random_pieces(30, 10)
        
        print("default")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=ants, iterations=iterations, alpha=0.6, beta=0.5, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        print("average fitness of the solution:",average)
        
        print("double ants")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=ants*2, iterations=iterations, alpha=0.6, beta=0.5, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        print("average fitness of the solution:",average)

        print("double iterations")
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=ants, iterations=iterations*2, alpha=0.6, beta=0.5, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        print("average fitness of the solution:",average)


def evaluate_heuristics(tests: int, runs: int, ants: int, iterations: int):
    h_1 = []
    h_2 = []
    tests_bar = tqdm.tqdm(range(tests), desc="Tests")
    for i in tests_bar:
        random.seed(i)
        pieces = Piece.generate_random_pieces(30, 10)
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=ants, iterations=iterations, alpha=0.6, beta=0.5, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            h_1.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))

        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol = ACO(n_ants=ants, iterations=iterations, alpha=0.6, beta=0.5, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic2)
            h_2.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))

    average_1 = sum(h_1) / len(h_1) if h_1 else 0
    print("average fitness with heuristic 1:",average_1)
    average_2 = sum(h_2) / len(h_2) if h_2 else 0
    print("average fitness with heuristic 2:",average_2)
evaluate_heuristics(10,10,10,10)
#evaluate_more_ants_or_iterations(tests=3, runs=6, ants=10, iterations=10)
#evaluate_variation_alpha_beta(tests=3, runs= 6, alpha=0.3, beta=0.6, increment=0.2)
