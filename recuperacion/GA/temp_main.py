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
        self.bounder = inspyred.ec.Bounder
        self.maximize = True  # Queremos maximizar la cantidad de espacio utilizado

    #modified
    #returns a chormosome consisting on num_pieces genes 
    # representing the order and whether the piece is placed or not
   

    def custom_crossover(random, candidates, args):
        print("+")
        return candidates
        #the crossover should preserve the decision of picking a piece if its the same in both parents
        # the rest is just a "normal" permutation crossover.
        pieces = args.get('pieces')
        num_pieces = args.get('num_pieces')
        selected = [False for i in range(num_pieces)]
        
        offspring = []
        # Assuming two parents for each crossover
            #!!this isn't it
        for i in range(0, len(candidates), 2):
            mom = candidates[i]
            dad = candidates[i+1]
            index = 0
            child1 = []
            child2 = []
            #select if the first piece should come from the mom or the dad.
            if random.random() <= alsfdhksdf:
                piece_index = pieces.index(mom[index].piece)
                if not selected[piece_index]:
                    selected[piece_index] = True
                    child1.append(Gene(mom[index].piece), True)
                    #child2.append(Gene(dad[index].piece), True)
                else:
                    print()
            else:
                if selected[pieces.index(dad[index].piece)]:
                    print()
                else:
                    print()

            offspring.append(child1)
            offspring.append(child2)
        return offspring

        
#
    #modified

    
ga = inspyred.ec.GA(random.Random())
def GeneticExecution(pieces: list, x_dim: int, y_dim: int):

    # Usar la función de envoltura personalizada en lugar de gaussian_mutation directamente
    problem = RectanglePacking(space)  # Definimos un espacio de 10x10
    ga.selector = inspyred.ec.selectors.tournament_selection
    ga.variator = [RectanglePacking.custom_crossover]
    ga.replacer = inspyred.ec.replacers.generational_replacement
    ga.terminator = inspyred.ec.terminators.generation_termination

    # Ejecución del algoritmo genético
    final_pop = ga.evolve(generator=problem.generator,
                        evaluator=problem.evaluator,
                        pop_size=4,
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
num_pieces = 1
max_size = 5
pieces = Piece.generate_random_pieces(num_pieces, max_size)
solGen = GeneticExecution(pieces=pieces, x_dim=10, y_dim=10)
print('Best Solution: {0}:'.format(str(solGen.candidate)))
print("Fitness",solGen.fitness)

ga.selector = inspyred.ec.selectors.uniform_selection
solGen = GeneticExecution()
print('Best Solution: {0}:'.format(str(solGen.candidate)))
print("Fitness",solGen.fitness)