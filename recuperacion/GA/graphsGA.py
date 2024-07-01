from GA import Problem
from Common.Piece import Piece
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def fitness_Evolution_Graph(fitnessList):
    plt.title("Fitness evolution")
    plt.xlabel('Executions')
    plt.ylabel('Fitness value')
    plt.plot(fitnessList)
    plt.show()

_, fitEvol = Problem(20, 20, Piece.generate_random_pieces(99, 5), 200, 0.001, 0.7, 0.3).runForGraphs(100)

fitness_Evolution_Graph(fitEvol)