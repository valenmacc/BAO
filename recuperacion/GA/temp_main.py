from Choice import Choice
import random
import inspyred
class RectanglePacking(inspyred.benchmarks.Benchmark): 

    def __init__(self, space):
        super(RectanglePacking, self).__init__(2)
        self.space = space
        self.bounder = inspyred.ec.Bounder([0, 0], [len(space), len(space[0])])
        self.maximize = True  # Queremos maximizar la cantidad de espacio utilizado

    
    #returns a chormosome consisting on num_pieces choices 
    # representing the order and whether the piece is placed or not
    def generator(self, random: random, args):
        num_pieces = args.get('num_pieces')
        pieces = args.get('pieces').clone()
        chromosome = []
        for i in range(num_pieces):
            chromosome.append(Choice(piece=pieces.pop(random.randint(0, len(pieces)-1), random.random()>0.5)))
        return chromosome
    
    def imprimir_espacio(space):
        for row in space:
            print("  ".join(map(str, row)))
        print()
        

    def evaluator(self, candidates, args):
        fitness = []
        for candidate in candidates:
            total_area = 0
            space_copy = copy.deepcopy(self.space)  # Creamos una copia del espacio original para no modificarlo
            for piece in candidate:
                placed = False
                for i in range(len(space_copy) - len(piece[0]) + 1):
                    for j in range(len(space_copy[0]) - len(piece) + 1):
                        if self.is_space_available(space_copy, j, i, len(piece), len(piece[0])):
                            placed = True
                            for x in range(len(piece[0])):
                                for y in range(len(piece)):
                                    space_copy[i + x][j + y] = 1
                            total_area += len(piece) * len(piece[0])
                            break
                    if placed:
                        break
            fitness.append(total_area)
        return fitness

    def is_space_available(self, space, x, y, width, height):
        for i in range(y, y + height):
            for j in range(x, x + width):
                if space[i][j] != 0:
                    return False
        return True
    
def colocar_pieza(space, pieza, x, y):
        temp = copy.deepcopy(space)  # Deep copy the space to avoid modifying the original
        rect_x, rect_y, rect_width, rect_height = pieza 
        if rect_x + rect_width >= len(space) or rect_y + rect_height >= len(space[0]):
            return False  # Return False if the piece goes out of bounds
        for i in range(len(pieza)):
            for j in range(len(pieza[0])):
                # Check bounds
                if space[x+i][y+j] == 1:
                    return False  # Return False if there's an overlap
                temp[x+i][y+j] = 1  # Place the piece in the temporary space
        # Copy the modified temporary space back to the original space
        for i in range(len(space)):
            for j in range(len(space[0])):
                space[i][j] = temp[i][j]
        return True  # Return True if the piece was successfully placed
    
ga = inspyred.ec.GA(random.Random())
def GeneticExecution():
    space = [[0 for column in range(Board_side)] for row in range(Board_side)]

    # Usar la función de envoltura personalizada en lugar de gaussian_mutation directamente
    problem = RectanglePacking(space)  # Definimos un espacio de 10x10
    ga.selector = inspyred.ec.selectors.tournament_selection
    ga.variator = [inspyred.ec.variators.uniform_crossover] #inspyred.ec.variators.gaussian_mutation((0.0,),(1.0,),{'_ec': ga}) no funciona
    ga.replacer = inspyred.ec.replacers.generational_replacement
    ga.terminator = inspyred.ec.terminators.generation_termination

    # Ejecución del algoritmo genético
    final_pop = ga.evolve(generator=problem.generator,
                        evaluator=problem.evaluator,
                        pop_size=10,
                        maximize=problem.maximize,
                        bounder=problem.bounder,
                        max_generations=numberOfIterations)

    # Mejor solución encontrada
    best = max(final_pop)
    return best