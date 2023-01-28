

class Square:
    """A square on a chess board.

    Attributes:
        row (int): The row of the square.
        col (int): The column of the square.
        piece (Piece): The piece on the square.
    """

    ALPHACOLS = {
        0: "a", 
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h"

    }

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = Square.ALPHACOLS[col]

    def has_piece(self):
        return self.piece != None
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def is_empty(self):
        return not self.has_piece()

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_enemy(self, color):
        return self.is_empty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def get_alpha_col(col):
        ALPHACOLS = {
        0: "a", 
        1: "b",
        2: "c",
        3: "d",
        4: "e",
        5: "f",
        6: "g",
        7: "h"

        }
        return ALPHACOLS[col]


# print(Square.in_range(5, 2, 5, 3))