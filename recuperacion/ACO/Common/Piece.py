import random

#this class represents a rectangle that may be placed on the board.
class Piece:
    def __init__(self, x_dim: int, y_dim: int):
        self.x_dim = x_dim
        self.y_dim = y_dim

    def generate_random_pieces(cardinality, max_size) -> list:
        pieces = []
        for i in range(cardinality):
            pieces.append(Piece(random.randint(1, max_size),random.randint(1, max_size)))
        return pieces