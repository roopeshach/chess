from const import *
from square import Square

class Board:
    """A chess board.

    Attributes:
        squares (list): A list of lists of squares.
    """


    def __init__(self):
        self.squares = []

    def _create(self):
        """Create the board."""
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0 ] for col in range(COLS)]
        # print(self.squares)

        self._create()

    
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
                print(self.squares[row][col])


    def _add_pieces(self, color):
        """Add pieces to the board. 
        Args:
            color (str): The color of the pieces to add.
        """
        pass



b = Board()
b._create()