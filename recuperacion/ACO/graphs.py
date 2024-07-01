from ACO import ACO
from Common.Piece import Piece
from Common.heuristic import heuristic2
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
    ax.set(title='Pheromones evolution')
    plt.show()

pieces = Piece.generate_random_pieces(30, 20)
phero_evolution = []

sol, fitnes_evolution, temp_phero_evolution = ACO(n_ants=20,iterations=50,alpha=0.6,beta=0.3,max_pieces=30,pieces=pieces,x_dim=40,y_dim=40,heuristic=heuristic2)
phero_evolution.append(temp_phero_evolution)

fitness_Evolution_Graph(fitnes_evolution)
pheromone_Evolution_Graph(phero_evolution)