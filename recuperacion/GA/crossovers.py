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

#!broken
def pmx_crossover(parent1, parent2):
    assert len(parent1) == len(parent2)
    
    size = len(parent1)
    child1, child2 = [None] * size, [None] * size
    
    # Select two crossover points
    start, end = sorted(random.sample(range(size), 2))
    
    # Copy the subsequence between the crossover points from the parents
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]
    
    # Create a mapping for the crossover section
    mapping1, mapping2 = {}, {}
    for i in range(start, end):
        mapping1[parent2[i]] = parent1[i]
        mapping2[parent1[i]] = parent2[i]
    
    # Fill the remaining positions using the mapping
    def fill_child(child, parent, mapping, start, end):
        for i in range(size):
            if i >= start and i < end:
                continue
            gene = parent[i]
            while gene in mapping:
                gene = mapping[gene]
            child[i] = gene
    
    fill_child(child1, parent2, mapping1, start, end)
    fill_child(child2, parent1, mapping2, start, end)
    
    return child1, child2
