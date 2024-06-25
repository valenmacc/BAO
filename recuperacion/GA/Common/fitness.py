#The fitness function subtracts the number of holes from the number of cells and normalizes the result.
def evaluate_fitness(sol, x_dim, y_dim) -> float: 
    holes = sum(not cell for row in sol for cell in row)
    size = x_dim * y_dim
    fitness = size - holes
    fitness /= size
    return fitness