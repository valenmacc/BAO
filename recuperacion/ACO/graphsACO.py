from ACO import ACO
from Common.Piece import Piece
from Common.heuristic import heuristic2,heuristic1
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def fitness_Evolution_Graph(fitnessList):
    plt.title("Fitness evolution")
    plt.xlabel('Executions')
    plt.ylabel('Fitness value')
    plt.plot(fitnessList)
    plt.show()

def pheromone_Evolution_Graph(pheroList):
    ax = sns.heatmap(pheroList, cmap='Blues', xticklabels=100, yticklabels=100)
    ax.set(title='Pheromones evolution', xlabel="Pieces", ylabel="Iterations")
    plt.show()

pieces = Piece.generate_random_pieces(30, 20)
phero_evolution = []
#
sol, fitnes_evolution, temp_phero_evolution = ACO(n_ants=10,iterations=40,alpha=0.3,beta=0.8,max_pieces=30,pieces=pieces,x_dim=40,y_dim=40,heuristic=heuristic1)
print(temp_phero_evolution)
#
#fitness_Evolution_Graph(fitnes_evolution)
pheromone_Evolution_Graph(temp_phero_evolution)