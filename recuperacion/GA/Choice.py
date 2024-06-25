import Common.Piece as Piece

#This class represents a particular piece in a defined position in the board.
class Choice:
    def __init__(self, piece: Piece, place: bool):
        self.place = piece
        self.place = place