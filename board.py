from const import *
from square import Square
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    """A chess board.

    Attributes:
        squares (list): A list of lists of squares.
    """


    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0 ] for col in range(COLS)]

        self._create()
        self._add_pieces("white")
        self._add_pieces("black")


    def _create(self):
        """Create the board."""
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
                # print(self.squares[row][col])


    def _add_pieces(self, color):
        """Add pieces to the board. 
        Args:
            color (str): The color of the pieces to add.
        """
        #black  must start from top 2 rows and white from bottom 2 rows
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)

        #print pawns on the board
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

            # self.squares[row_piece][col].piece = Piece(color)

        # print knights on the board
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # print bishops on the board
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # print rooks on the board
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # print queen on the board
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # print king on the board
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    # def __str__(self):
    #     """Return a string representation of the board."""
    #     return f"Board({self.squares})"
    
    # def __repr__(self):
    #     """Return a string representation of the board."""
    #     return f"Board({self.squares})"





b = Board()
b._create()