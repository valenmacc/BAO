import Common.Piece as Piece

#This class represents a particular piece in a defined position in the board.
class Gene:
    def __init__(self, piece: Piece, place: bool):
        self.piece = piece
        self.place = place