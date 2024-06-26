from Gene import Gene
from Common.Solution import Solution
from Common.Piece import Piece
import random
import tqdm
from mutations import *
from crossovers import *
from Common.fitness import evaluate_fitness
class Problem:
    def __init__(self, x_dim: int, y_dim: int, pieces: list,population_size: int, place_probability: float, bit_flip_prob: float, alter_prob: float):
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.pieces = pieces
        self.num_pieces = len(pieces)
        self.population_size = population_size
        self.place_prob = place_probability
        self.bit_flip_prob = bit_flip_prob  
        self.alter_prob = alter_prob
        
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

    def selector(self, candidates: list, fitnesses: list, tournament_size=4) -> list:
        selected_candidates = []
        for _ in range(len(candidates)):
            # Randomly select tournament_size individuals for the tournament
            indices = random.sample(range(len(candidates)), tournament_size)
            tournament_candidates = [candidates[i] for i in indices]
            tournament_fitnesses = [fitnesses[i] for i in indices]
            best_index = tournament_fitnesses.index(max(tournament_fitnesses))
            selected_candidates.append(tournament_candidates[best_index])
        return selected_candidates
    
     
    def recombinator(self, progenitors: list, crossover) -> list:
        offspring = []
        for i in range(0, len(progenitors), 2):
            mom = progenitors[i]
            dad = progenitors[i + 1] if i + 1 < len(progenitors) else progenitors[0]  # Handle odd number of parents
            child1, child2 = crossover(mom, dad)
            offspring.append(child1)
            offspring.append(child2)
        return offspring
    



    def mutator(self, candidates: list, mutation) -> list:
        for chromosome in candidates:
            mutation(chromosome, self.bit_flip_prob, self.alter_prob)
        return candidates
    
    def replacer(self, mu: list, lambda_: list) -> list:
        pool = mu + lambda_
        fitnesses = self.evaluator(pool)
        sorted_indices = sorted(range(len(pool)), key=lambda i: fitnesses[i], reverse=True)
        selected_indices = sorted_indices[:len(mu)]
        new_generation = [pool[i] for i in selected_indices]
        new_fitnesses = [fitnesses[i] for i in selected_indices]
        return new_generation, new_fitnesses
    
    def evaluator(self, candidates):
        fitness = []
        for candidate in candidates:
            fitness.append(evaluate_fitness(self.decoder(candidate).board, self.x_dim, self.y_dim))
        return fitness

    def run(self, max_generations: int):
        population = self.initialization()
        max_fitness = 0
        fitnesses = self.evaluator(population)
        generation_bar = tqdm.tqdm(range(max_generations), desc="generations")
        for _ in generation_bar:
            possible_best_fitness =  max(fitnesses)
            if possible_best_fitness > max_fitness:
                best =  population[fitnesses.index(possible_best_fitness)]
                max_fitness = possible_best_fitness
            if max_fitness == 1.0: break
            progenitors = self.selector(population, fitnesses)
            children = self.recombinator(progenitors, order_crossover)
            children = self.mutator(children, bit_flip_and_scramble_mutation)
            assert(progenitors != children)
            population, fitnesses = self.replacer(progenitors, children)
            
        return self.decoder(best)
    
    def runForGraphs(self, max_generations: int):
        fitnes_evol=[]
        population = self.initialization()
        max_fitness = 0.9
        fitnesses = self.evaluator(population)
        generation_bar = tqdm.tqdm(range(max_generations), desc="generations")
        for _ in generation_bar:
            possible_best_fitness =  max(fitnesses)
            if possible_best_fitness > max_fitness:
                best =  population[fitnesses.index(possible_best_fitness)]
                max_fitness = possible_best_fitness
            fitnes_evol.append(max_fitness)
            if max_fitness == 1.0: break
            progenitors = self.selector(population, fitnesses)
            children = self.recombinator(progenitors, order_crossover)
            children = self.mutator(children, bit_flip_and_scramble_mutation)
            assert(progenitors != children)
            population, fitnesses = self.replacer(progenitors, children)
            
        return self.decoder(best), fitnes_evol
            
            
Problem(24, 24, Piece.generate_random_pieces(99, 6), 200, 0.001, 0.7, 0.3).runForGraphs(100)