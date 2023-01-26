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

        self.squares[5][1] = Square(4, 0, Pawn("black"))
            # self.squares[row_piece][col].piece = Piece(color)

        # print knights on the board
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # self.squares[4][4] = Square(4, 4, Knight("white"))

        # print bishops on the board
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        self.squares[4][4] = Square(4, 4, Bishop("black"))

        # print rooks on the board
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        self.squares[3][3] = Square(43, 3, Rook("black"))

        # print queen on the board
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[2][3] = Square(2, 3, Queen("white"))

        # print king on the board
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        self.squares[3][4] = Square(3, 4, King('black'))
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
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
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
            
            # vertical moves 
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        #creating square for new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        #creating new move
                        move = Move(initial, final)

                        #append new valid move
                        piece.add_move(move)
                    #blocked
                    else: break
                # out of range
                else: break

            #diagonal moves 
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]

            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #creating square for new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #creating new move
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)

        def straightline_moves(increments):
            for increment in increments:
                row_increment, col_increment = increment
                possible_move_row = row + row_increment
                possible_move_col = col + col_increment

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        #create square for possible new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        #create new move
                        move = Move(initial, final)

                        #append new valid move
                        


                        #empty square
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)

                        #has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        #has team piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                        #incrementing increments
                        possible_move_row, possible_move_col = possible_move_row + row_increment, possible_move_col + col_increment

                    #out of range
                    else: break

        def king_moves():
            adjacents = [
                (row - 1, col + 0), # up
                (row - 1, col + 1), # up-right
                (row + 0, col + 1), # right
                (row + 1, col + 1), # down-right
                 (row + 1, col + 0), # down
                (row + 1, col - 1), # down-left
                (row + 0, col - 1), # left
                (row - 1, col - 1), # up-left
            ]

            for possible_move in adjacents:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        #creating square for new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        #creating new move
                        move = Move(initial, final)

                        #append new valid move
                        piece.add_move(move)

            #castling moves
            
            #king side

            #queen side

        if isinstance(piece, Pawn):pawn_moves()
        elif isinstance(piece, Knight): knight_moves()
        elif isinstance(piece, Bishop):straightline_moves([
                (-1, 1), #up-right
                (-1, -1), #up-left
                (1, 1), #down-right
                (1, -1), #down-left      
        ])
        elif isinstance( piece, Rook):straightline_moves([
                (-1, 0), #up
                (0, 1), #right
                (1, 0), #down
                (0, -1), #left
        ])
        
        elif isinstance(piece, Queen): straightline_moves([
                (-1, 1), #up-right
                (-1, -1), #up-left
                (1, 1), #down-right
                (1, -1), #down-left
                 (-1, 0), #up
                (0, 1), #right
                (1, 0), #down
                (0, -1), #left
                
        ])
        elif isinstance(piece, King):king_moves()
        else: raise ValueError("Invalid piece")


b = Board()
b._create()