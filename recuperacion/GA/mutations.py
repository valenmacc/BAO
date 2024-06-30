import random

def bit_flip_and_swap_mutation(chromosome, flip_prob=0.1, swap_prob=0.1):
    # Bit Flip Mutation
    for gene in chromosome:
        if random.random() < flip_prob:
            gene.place = not gene.place  # Flip the place boolean

    # Swap Mutation
    if random.random() < swap_prob:
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]  # Swap two genes
    return chromosome

def bit_flip_and_scramble_mutation(chromosome, flip_prob=0.1, scramble_prob=0.1):
    # Bit Flip Mutation
    for gene in chromosome:
       if random.random() < flip_prob:
           gene.place = not gene.place  # Flip the place boolean
    # Scramble Mutation
    if random.random() < scramble_prob:
        start_idx = random.randint(0, len(chromosome) - 2)
        end_idx = random.randint(start_idx + 1, len(chromosome))
        scrambled_segment = chromosome[start_idx:end_idx]
        random.shuffle(scrambled_segment)
        chromosome[start_idx:end_idx] = scrambled_segment
    return chromosome   