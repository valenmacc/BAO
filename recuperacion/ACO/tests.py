from ACO import ACO
import tqdm
import random
from Common.fitness import evaluate_fitness
from Common.heuristic import *
from Common.Piece import Piece
#import graphs

#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt

def evaluate_variation_alpha_beta(tests: int, runs: int, alpha: float, beta: float, increment: float):
    print(f"doing {runs} runs with alpha={alpha} and beta={beta} with {tests} different seeds.\n")
    defs = []
    a_inc= []
    a_dec= []
    b_inc= []
    b_dec= []
    ab_i = []
    ab_d = []

    #sns.set_style('darkgrid')

    best_fitness_graph = []

    tests_bar = tqdm.tqdm(range(tests), desc="Tests")
    for j in tests_bar:
        random.seed(j)
        pieces = Piece.generate_random_pieces(30, 10)
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha, beta=beta, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        defs.append(average)
        
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha+increment, beta=beta, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        a_inc.append(average)
        
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha-increment, beta=beta, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        a_dec.append(average)
        
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha, beta=beta+increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        b_inc.append(average)
        
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha, beta=beta-increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        b_dec.append(average)
        
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha+increment, beta=beta+increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        ab_i.append(average)
        
        fitnesses = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=10, iterations=50, alpha=alpha-increment, beta=beta-increment, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        ab_d.append(average)

    print(f"average over tests of default is:",sum(defs)/len(defs))
    
    print(f"average over tests with alpha {alpha+increment} and beta {beta} is: {sum(a_inc)/len(a_inc)}")
    print(f"average over tests with alpha {alpha-increment} and beta {beta} is: {sum(a_dec)/len(a_dec)}")
    
    print(f"average over tests with alpha {alpha} and beta {beta+increment} is: {sum(b_inc)/len(b_inc)}")
    print(f"average over tests with alpha {alpha} and beta {beta-increment} is: {sum(b_dec)/len(b_dec)}")
    
    print(f"average over tests with alpha {alpha+increment} and beta {beta+increment} is: {sum(ab_i)/len(ab_i)}")
    print(f"average over tests with alpha {alpha-increment} and beta {beta-increment} is: {sum(ab_d)/len(ab_d)}")
    
    return
    
def evaluate_more_ants_or_iterations(tests: int, runs: int, ants: int, iterations: int, heuristic):
    print(f"doing {runs} runs of {iterations} iterations with {ants} ants with {tests} different seeds.\n")
    tests_bar = tqdm.tqdm(range(tests), desc="Tests")
    defs = []
    dants = []
    diter = []
    for j in tests_bar:
        random.seed(j)
        pieces = Piece.generate_random_pieces(30, 10)
        
        fitnesses = []
        phero_history = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, sol_phero, _ = ACO(n_ants=ants, iterations=iterations, alpha=0.3, beta=0.8, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
            phero_history.append(sol_phero)
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        defs.append(average)
        
        fitnesses = []
        phero_history = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, sol_phero, _ = ACO(n_ants=ants*2, iterations=iterations, alpha=0.3, beta=0.8, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
            phero_history.append(sol_phero)
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        dants.append(average)

        fitnesses = []
        phero_history = []
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, sol_phero, _ = ACO(n_ants=ants, iterations=iterations*2, alpha=0.3, beta=0.8, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic)
            fitnesses.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))
            phero_history.append(sol_phero)
        average = sum(fitnesses) / len(fitnesses) if fitnesses else 0
        diter.append(average)
    print(f"average over tests of default is:",sum(defs)/len(defs))
    print(f"average over tests with double ants is: {sum(dants)/len(dants)}")
    print(f"average over tests with double iterations is: {sum(diter)/len(diter)}")
    
def evaluate_heuristics(tests: int, runs: int, ants: int, iterations: int):
    h_1 = []
    h_2 = []


    tests_bar = tqdm.tqdm(range(tests), desc="Tests")
    for i in tests_bar:
        random.seed(i)
        pieces = Piece.generate_random_pieces(30, 10)
        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=ants, iterations=iterations, alpha=0.3, beta=0.8, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic1)
            h_1.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))


        for _ in tqdm.tqdm(range(runs), desc="runs",leave=False):
            sol, _, _ = ACO(n_ants=ants, iterations=iterations, alpha=0.3, beta=0.8, max_pieces=30, pieces=pieces, x_dim=20, y_dim=20, heuristic=heuristic2)
            h_2.append(evaluate_fitness(sol.board, sol.x_dim, sol.y_dim))

    average_1 = sum(h_1) / len(h_1) if h_1 else 0
    print("average fitness with heuristic 1:",average_1)
    average_2 = sum(h_2) / len(h_2) if h_2 else 0
    print("average fitness with heuristic 2:",average_2)


#evaluate_variation_alpha_beta(tests=4, runs= 5, alpha=0.25, beta=0.75, increment=0.05)
#evaluate_heuristics(tests=4,runs=5,ants=10,iterations=50)
evaluate_more_ants_or_iterations(tests=4, runs=5, ants=10, iterations=20, heuristic=heuristic1)