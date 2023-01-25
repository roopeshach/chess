from const import *
from square import Square
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from move import Move

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
        """Add pieces to the board.     image = pygame.image.load(piece.texture)
                        image_center  = col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2
                        piece.texture_rect = image.get_rect(center=image_center)    
                        surface.blit(image, piece.texture_rect)
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

        # self.squares[4][4] = Square(4, 4, Knight("white"))

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


    def calc_moves(self, piece, row, col):
        '''
        Calculate the possible moves for a piece in specific square
        
        '''
 
        def knight_moves():

            possible_moves = [
                (row-2, col + 1),
                (row -1 , col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        #creating square for new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col) #piece = piece

                        #creating new move
                        move = Move(initial, final)

                        #append new valid move    
                        piece.add_move(move)

        def pawn_moves():
            #steps 
            steps = 1 if piece.moved else 2
            
            # vertical moves / eating pieces moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for move_row in range(start, end, piece.dir):
                pass




        if isinstance(piece, Pawn):pawn_moves()
        elif isinstance( piece, Rook):pass
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop):pass
        elif isinstance(piece, Queen): pass
        elif isinstance(piece, King):pass
        else: raise ValueError("Invalid piece")


b = Board()
b._create()