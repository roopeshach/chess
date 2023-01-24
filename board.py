from const import *
from square import Square

class Board:

    def __init__(self):
        self.squares = []

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0 ] for col in range(COLS)]
        # print(self.squares)

        self._create()

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
                print(self.squares[row][col])


    def _add_pieces(self, color):
        pass



b = Board()
b._create()