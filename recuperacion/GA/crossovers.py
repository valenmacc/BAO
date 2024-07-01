import random
def order_crossover(parent1, parent2):
    assert len(parent1) == len(parent2)
    
    size = len(parent1)
    child1, child2 = [None] * size, [None] * size
    
    # Select two crossover points
    start, end = sorted(random.sample(range(size), 2))
    
    # Copy the subsequence between the crossover points from the first parent
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]
    
    # Fill the remaining positions with the genes from the second parent in order
    fill_pos1, fill_pos2 = end, end
    for i in range(size):
        index = (i + end) % size
        if parent2[index] not in child1:
            child1[fill_pos1 % size] = parent2[index]
            fill_pos1 += 1
        if parent1[index] not in child2:
            child2[fill_pos2 % size] = parent1[index]
            fill_pos2 += 1
            
    return child1, child2
