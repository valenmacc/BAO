from Gene import Gene
from Common.Solution import Solution
from Common.Piece import Piece
import random
from Common.fitness import evaluate_fitness
class Problem:
    def __init__(self, x_dim: int, y_dim: int, pieces: list,population_size: int, place_probability: float):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.pieces = pieces
        self.num_pieces = len(pieces)
        self.population_size = population_size
        self.place_prob = place_probability
        
    def generator(self):
        chromosome = []
        order = [i for i in range(self.num_pieces)] #list of piece indexes
        for _ in range(self.num_pieces):
            #get random index and use that piece
            index = random.choice(order)
            index = order.pop(order.index(index))
            chromosome.append(Gene(piece=self.pieces[index], place=random.random()<=self.place_prob))

        #All unused pieces are pushed to the back to reduce the number of equivalent chromosomes.
        for i in range(len(chromosome)):
            if not chromosome[i].place:
                chromosome.append(chromosome.pop(i))
        return chromosome    

    def initialization(self):
        population = []
        for _ in range(self.population_size):
            population.append(self.generator())

        return population
        
    def decoder(self, chromosme: list) -> Solution:
        solution = Solution(x_dim=self.x_dim, y_dim=self.y_dim, pieces=self.pieces, max_pieces=self.num_pieces)
        i = 0
        for gene in chromosme:
            assert(self.pieces.__contains__(gene.piece))
            if gene.place:
                position = solution.get_Choice(gene.piece)
                if position.x_pos != -1: #valid
                    solution.place_Choice(position, i)
                    i += 1
        return solution

    def selector(self, candidates: list, fitnesses: list) -> list:
        return []
    
    def recombinator(self, progenitors: list) -> list:
        return []
    
    def mutator(self, candidates: list) -> list:
        return []
    
    def replacer(self, mu: list, lamda: list) -> list:
        return []
    
    def evaluator(self, candidates):
        fitness = []
        for candidate in candidates:
            fitness.append(evaluate_fitness(self.decoder(candidate).board, self.x_dim, self.y_dim))
        return fitness

    def run(self, max_generations: int):
        population = self.initialization()
        best = None
        for _ in range(max_generations):
            fitnesses = self.evaluator(population)
            best = population[fitnesses.index(max(fitnesses))]
            progenitors = self.selector(population, fitnesses)
            children = self.recombinator(progenitors)
            children = self.mutator(children)
            population = self.replacer(progenitors, children)
        return best
            
            
Problem(10, 10, Piece.generate_random_pieces(20, 5), 5, 0.5).run(3)  