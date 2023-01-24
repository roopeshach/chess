

class Square:
    """A square on a chess board.

    Attributes:
        row (int): The row of the square.
        col (int): The column of the square.
        piece (Piece): The piece on the square.
    """

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __repr__(self):
        return f"Square({self.row}, {self.col}, {self.piece})"
    
    def __str__(self):
        return f"Square({self.row}, {self.col}, {self.piece})"
    
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Square):
            return self.row == other.row and self.col == other.col
        else:
            return False
        
    def has_piece(self):
        return self.piece != None
    
    def get_piece(self):
        return self.piece
  