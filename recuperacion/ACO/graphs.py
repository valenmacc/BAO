from ACO import ACO
from Common import Solution
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
    ax.set(title='Pheromones evolution' ,xlabel='Piece \n More blue indicates more probabilities for that piece to be picked', ylabel='Executions')
    plt.show()