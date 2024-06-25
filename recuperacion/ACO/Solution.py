from  Common.Piece import Piece
from  Common.Choice import Choice
from Pheromone import Pheromone
import random
from typing import Callable
import numpy as np

#This class represents a complete
class Solution:
    def __init__(self, x_dim: int, y_dim: int, pieces: list, max_pieces: int):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.pieces = pieces
        #the repeated reference approach to initialization
        #provides a speedup of >300 (99.67% inprovement) over iteration for very large boards (tested with 3000x3000 board)
        self.board = [[False] * x_dim for _ in range(y_dim)]
        self.used_pieces = [False] * max_pieces
        self.pieces_order = [-1] * max_pieces
        self.pieces_pos = [[[-1,-1]]* 2 for i in range(max_pieces)]


    #! this is broken.
    def __get_candidates(self) -> list:
        Candidates = []
        for candidate in self.pieces:
            if not self.does_use_piece(candidate):
                choice = self.get_Choice(candidate)
                if choice.x_pos != -1:
                    Candidates.append(choice)       
        return Candidates
    
    def get_Choice (self, piece: Piece) -> Choice:
        for x in range(self.x_dim):  # Recorre todas las posiciones del espacio
            for y in range(self.y_dim):
                posible = Choice(piece, x, y)
                if self.does_Choice_fit(posible):
                    return Choice(piece, x, y)
        return Choice(piece, -1, -1)

    
    
    
    #todo seed all random values.
    
    
    
    
    
    def __random_choice(Candidates, Probabilities):
        for i in range(len(Candidates)):
            if random.random() < Probabilities[i]: #good option for experimenting an using other choosing algos
                return Candidates[i]
        return Candidates[random.randint(0, len(Candidates)-1)] #program keep hanging while selectign a candidate.
            
    
    def construct_solution(Pheromones: list, x_dim: int, y_dim: int, pieces: list, max_pieces: int, alpha: float, beta: float, heuristic: Callable[[Choice], float]):
        solution = Solution(x_dim, y_dim, pieces, max_pieces)
        Candidates = solution.__get_candidates() #candidates are always valid
        order = 0
        while (len(Candidates) > 0):
            Probabilities = Pheromone.calculate_probabilities(Candidates, Pheromones, order, alpha, beta, x_dim, y_dim, solution.board, heuristic)
            choice = Solution.__random_choice(Candidates, Probabilities)
            solution.place_Choice(choice, order)
            Candidates = solution.__get_candidates()
            order = order + 1
        return solution

    def does_Choice_fit(self, choice: Choice) -> bool:
        if choice.piece.x_dim + choice.x_pos > self.x_dim:
            return False
        if choice.piece.y_dim + choice.y_pos > self.y_dim:
            return False
        for i in range(choice.piece.x_dim):
            for j in range(choice.piece.y_dim):
                if self.board[choice.x_pos + i][choice.y_pos + j]:
                    return False
        return True
    

                
    def place_Choice(self, choice: Choice, order: int):
        for y in range(choice.piece.y_dim):
            for x in range(choice.piece.x_dim):
                x_pos = choice.x_pos + x
                y_pos = choice.y_pos + y
                self.board[x_pos][y_pos] = True
                
        self.used_pieces[self.pieces.index(choice.piece)] = True
        self.pieces_order[self.pieces.index(choice.piece)] = order
        self.pieces_pos[self.pieces.index(choice.piece)] = [[choice.x_pos,choice.y_pos],[choice.x_pos + choice.piece.x_dim-1,choice.y_pos + choice.piece.y_dim-1]]

    def does_use_piece(self, piece: Piece):
        return self.used_pieces[self.pieces.index(piece)]
    
    def get_piece_order(self, piece: Piece):
        return self.pieces_order[self.pieces.index(piece)]
    
    def piece_in_pos(self, x, y):
        i = 0
        for piece in self.pieces_pos:
            if x>= piece[0][0] and x <= piece[1][0]:
                if y>= piece[0][1] and y <= piece[1][1]:
                    return i
            i = i + 1
        return -1
    
    def printSol (self):
        board = np.array([[0]*self.x_dim] * self.y_dim)
        
        
        print('\n\n')
        print("pieces:")
        for y in range (self.y_dim):
            #print('|', end='')  
            for x in range (self.x_dim):
                piece = self.piece_in_pos(x, y)
                if  piece != -1:
                    board[y][x] = piece + 1 #print(' ',"{:03d}".format(self.piece_in_pos(j, i)), end='')
                else:
                    board[y][x] = 0
                    #print("  ·  ", end= '')
            #print('|')    

        i = 0
        print(board)
        print('\n\n')
        
        for piece in self.pieces:
            print("piece ",i + 1, ' (',piece.x_dim, ', ',piece.y_dim, ')', sep='')
            i = i + 1