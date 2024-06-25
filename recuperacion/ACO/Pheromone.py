from typing import Callable
from Common.Choice import Choice
from Common.fitness import evaluate_fitness

#This class represents the pheromones.
class Pheromone:
    def __init__(self, max_pieces: int):
        self.placed = 1.0                       #represents the binary choice of usign or not a piece.
        self.placeOrder = [1.0] * max_pieces    #represents the best order in which to pick the pieces.
    
    def initialize_pheromones(max_pieces: int):
        Pheromones = [Pheromone(max_pieces) for i in range(max_pieces)]
        return Pheromones
    
    def calculate_probabilities(Candidates: list, Pheromones: list, order: int, alpha: float, beta: float, x_dim: int, y_dim: int, board: list,heuristic: Callable[[Choice], float]):
        dividend = []
        sum = 0
        for i in range(0, len(Candidates)):
            dividend.append(pow((Pheromones[i].placed * Pheromones[i].placeOrder[order]), alpha) * pow(heuristic(Candidates[i], x_dim, y_dim, board),beta))
            sum += dividend[i]

        #avoid dividing by zero.
        if sum == 0:
            sum = 0.000001
        for j in dividend:
            j = j/sum
        return dividend
    
    def clamp(value):
        if value > 0:
            return min(value, 1)
        else: 
            return max (value, 0)
    
    def clampOf100(value):
        if value > 100:
            return min(value, 100)
        else: 
            return max (value, 0)
    

    
    def update_pheromones(Pheromones, Solution_list, max_pieces: int, pieces: list):
        New_Pheromones = Pheromones

        #Pheromones affected by evaporation
        for j in New_Pheromones:
            j.placed = Pheromone.clampOf100((1 - 0.8) * j.placed)
            for i in range(len(j.placeOrder)):
                j.placeOrder[i] = Pheromone.clampOf100((1 - 0.3) * j.placeOrder[i])

        #Pheromones affected by pheromone amount
        #Fittnes of solution multiply by 0.7
        for tempSol in Solution_list:
            tempFit = Pheromone.clampOf100(evaluate_fitness(tempSol.board, tempSol.x_dim, tempSol.y_dim) * 0.3)
            for tempPieza in range(max_pieces):
                if(tempSol.does_use_piece(pieces[tempPieza])):
                    New_Pheromones[tempPieza].placed = Pheromone.clampOf100(New_Pheromones[tempPieza].placed + tempFit)
                    tempPosition = tempSol.get_piece_order(pieces[tempPieza])
                    New_Pheromones[tempPieza].placeOrder[tempPosition] = Pheromone.clampOf100(New_Pheromones[tempPieza].placed + tempFit)
                else:
                    New_Pheromones[tempPieza].placed = Pheromone.clampOf100(New_Pheromones[tempPieza].placed - (tempFit * 0.6))

        return New_Pheromones