from Gene import Gene
from Common.Piece import Piece
import random
import inspyred
from Common.Solution import Solution
from Common.fitness import evaluate_fitness
class RectanglePacking(inspyred.benchmarks.Benchmark): 

    def __init__(self, space, pieces=None):
        super(RectanglePacking, self).__init__(2)
        self.space = space
        self.bounder = inspyred.ec.Bounder([0, 0], [len(space), len(space[0])])
        self.maximize = True  # Queremos maximizar la cantidad de espacio utilizado

    #modified
    #returns a chormosome consisting on num_pieces genes 
    # representing the order and whether the piece is placed or not
    def generator(self, random: random, args):
        num_pieces = args.get('num_pieces')
        pieces = args.get('pieces')
        place_prob = args.get('place_prob')
        chromosome = []
        order = [i for i in range(num_pieces)] #list of piece indexes
        for _ in range(num_pieces):
            #get random index and use that piece
            index = random.choice(order)
            index = order.pop(order.index(index))
            chromosome.append(Gene(piece=pieces[index], place=random.random()<=place_prob))
        return chromosome       

    def custom_crossover(random, candidates, args):
        #the crossover should preserve the decision of picking a piece if its the same in both parents
        # the rest is just a "normal" permutation crossover.
        offspring = []
        # Assuming two parents for each crossover
            #!!this isn't it
        for i in range(0, len(candidates), 2):
            mom = candidates[i]
            dad = candidates[i+1]

            # Example crossover logic: single-point crossover
            crossover_point = random.randint(1, len(mom) - 1)

            child1 = mom[:crossover_point] + dad[crossover_point:]
            child2 = dad[:crossover_point] + mom[crossover_point:]

            offspring.append(child1)
            offspring.append(child2)
        return offspring

    #modified
    def solution_from_chromosome(chromosme: list, x_dim: int, y_dim: int, pieces: list, max_pieces: int):
        solution = Solution(x_dim=x_dim, y_dim=y_dim, pieces=pieces, max_pieces=max_pieces)
        i = 0
        for choice in chromosme:
            if choice.place:
                position = solution.get_Choice(choice.piece)
                if position.x_pos != -1: #valid
                    solution.place_Choice(position, i)
                    i += 1
        return solution
    
    #modified
    def evaluator(self, candidates, args):
        x_dim = args.get('x_dim')
        y_dim = args.get('y_dim')
        pieces = args.get('pieces')
        max_pieces = args.get('num_pieces')
        fitness = []
        for candidate in candidates:
            fitness.append(evaluate_fitness(RectanglePacking.solution_from_chromosome(candidate, x_dim, y_dim, pieces, max_pieces).board, x_dim, y_dim))
        return fitness
    
ga = inspyred.ec.GA(random.Random())
def GeneticExecution(pieces: list, x_dim: int, y_dim: int):
    space = [[0 for column in range(10)] for row in range(10)]

    # Usar la función de envoltura personalizada en lugar de gaussian_mutation directamente
    problem = RectanglePacking(space)  # Definimos un espacio de 10x10
    ga.selector = inspyred.ec.selectors.tournament_selection
    ga.variator = [RectanglePacking.custom_crossover]
    ga.replacer = inspyred.ec.replacers.generational_replacement
    ga.terminator = inspyred.ec.terminators.generation_termination

    # Ejecución del algoritmo genético
    final_pop = ga.evolve(generator=problem.generator,
                        evaluator=problem.evaluator,
                        pop_size=10,
                        maximize=problem.maximize,
                        num_elites= 2,
                        bounder=problem.bounder,
                        max_generations=10,
                        num_pieces=len(pieces),
                        pieces=pieces,
                        x_dim=x_dim,
                        y_dim=y_dim,
                        place_prob= 0.5)

    # Mejor solución encontrada
    best = max(final_pop)
    return best
num_pieces = 10
max_size = 5
pieces = Piece.generate_random_pieces(num_pieces, max_size)
solGen = GeneticExecution(pieces=pieces, x_dim=10, y_dim=10)
print('Best Solution: {0}:'.format(str(solGen.candidate)))
print("Fitness",solGen.fitness)

ga.selector = inspyred.ec.selectors.uniform_selection
solGen = GeneticExecution()
print('Best Solution: {0}:'.format(str(solGen.candidate)))
print("Fitness",solGen.fitness)