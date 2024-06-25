import Common.Piece as Piece

#This class represents a particular piece in a defined position in the board.
class Choice:
    def __init__(self, piece: Piece, x_pos: int, y_pos: int):
        self.piece = piece
        self.x_pos = x_pos
        self.y_pos = y_pos