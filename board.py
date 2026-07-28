from const import *
from square import Square
from piece import  Pawn, Rook, Knight, Bishop, Queen, King
from move import Move
import copy

class Board:
    """A chess board.

    Attributes:
        squares (list): A list of lists of squares.
    """


    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0 ] for col in range(COLS)]

        self.last_move = None
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

        # print knights on the board
        back_rank = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_cls in enumerate(back_rank):
            self.squares[row_other][col] = Square(row_other, col, piece_cls(color))
    
    def __str__(self):
        """Return a string representation of the board."""
        return f"Board({self.squares})"
    
    def __repr__(self):
        """Return a string representation of the board."""
        return f"Board({self.squares})"

    def iter_squares(self):
        for row in range(ROWS):
            for col in range(COLS):
                yield row, col, self.squares[row][col]

    def iter_pieces(self):
        for row, col, square in self.iter_squares():
            if square.has_piece():
                yield row, col, square.piece

    
 
    def calc_moves(self, piece, row, col, bool=True):
        '''
        Calculate the possible moves for a piece in specific square
        
        '''

        def create_move(final_row, final_col, final_piece=None):
            if final_piece is None:
                final_piece = self.squares[final_row][final_col].piece
            return Move(
                Square(row, col),
                Square(final_row, final_col, final_piece)
            )

        def add_move_if_legal(move):
            if bool and self.in_check(piece, move):
                return False

            piece.add_move(move)
            return True
 
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
                        add_move_if_legal(create_move(possible_move_row, possible_move_col))

        def pawn_moves():
            #steps 
            steps = 1 if piece.moved else 2
            
            # vertical moves 
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        if not add_move_if_legal(create_move(possible_move_row, col)):
                            break
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
                        add_move_if_legal(create_move(possible_move_row, possible_move_col))

            #en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            if row == r:
                for possible_move_col in (col - 1, col + 1):
                    if not Square.in_range(possible_move_col):
                        continue

                    square = self.squares[row][possible_move_col]
                    if not square.has_enemy_piece(piece.color):
                        continue

                    enemy_piece = square.piece
                    if isinstance(enemy_piece, Pawn) and enemy_piece.en_passant:
                        add_move_if_legal(create_move(fr, possible_move_col, enemy_piece))


        def straightline_moves(increments):
            for increment in increments:
                row_increment, col_increment = increment
                possible_move_row = row + row_increment
                possible_move_col = col + col_increment

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        move = create_move(possible_move_row, possible_move_col)

                        #append new valid move

                        #empty square = continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            add_move_if_legal(move)

                        #has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            add_move_if_legal(move)
                            break

                        #has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                        #incrementing increments
                        possible_move_row, possible_move_col = possible_move_row + row_increment, possible_move_col + col_increment

                    #out of range
                    else: break

        def king_moves():
            """
            Calculate the possible moves for a king in specific square
            
            """

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
                        add_move_if_legal(create_move(possible_move_row, possible_move_col))

            #castling moves
            if not piece.moved:
                #queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            #castling is not possible beacause there are pieces in between
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                #add left rook to king
                                piece.left_rook = left_rook
                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                #creating new move
                                moveR = Move(initial, final)

                                #append new valid move
                                # left_rook.add_move(moveR)

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                # piece.add_move(moveK)

                                #check potential check
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(piece, moveR):
                                       #append new move to rook 
                                        left_rook.add_move(moveR)
                                            #append new move to king
                                        piece.add_move(moveK)
                                else:
                                    #append new move to rook 
                                    left_rook.add_move(moveR)
                                        #append new move to king
                                    piece.add_move(moveK)




                

                #king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            #castling is not possible beacause there are pieces in between
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                #add right rook to king
                                piece.right_rook = right_rook

                                #rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)

                                #creating new move
                                moveR = Move(initial, final)

                                #append new valid move
                                # right_rook.add_move(move)

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                # piece.add_move(move)

                                #check potential check
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(piece, moveR):
                                       #append new move to rook 
                                        right_rook.add_move(moveR)
                                            #append new move to king
                                        piece.add_move(moveK)
                                else:
                                    #append new move to rook 
                                    right_rook.add_move(moveR)
                                        #append new move to king
                                    piece.add_move(moveK)

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


    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        captured_piece = self.squares[final.row][final.col].piece
        enpassant = self.enpassant(piece, move)

        # #console board move update
        self.squares[initial.row][initial.col].piece = None
        #moving piece
        self.squares[final.row][final.col].piece = piece

       

        #pawn promotion
        if isinstance(piece, Pawn):
            #enpassant capture
            diff = final.col - initial.col
            if enpassant:
                #console board move update
                captured_piece = self.squares[initial.row][initial.col + diff].piece
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
            
            # #pawn enpassant
            # if self.enpassant(initial, final):
            #     piece.en_passant = True
            #     # print('pawn moved 2 squares')

            else:
                self.check_promotion(piece, final)

        
        #king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])


        piece.moved = True

        #clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move

        if not testing:
            self.update_enpassant(piece, move)

        return captured_piece

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def pawn_double_step(self, piece, move):
        return isinstance(piece, Pawn) and abs(move.initial.row - move.final.row) == 2

    def enpassant(self, piece, move):
        if not isinstance(piece, Pawn):
            return False

        diagonal_move = move.initial.col != move.final.col
        empty_destination = self.squares[move.final.row][move.final.col].is_empty()
        return diagonal_move and empty_destination

    def set_false_enpassant(self, except_piece=None):
        for _, _, board_piece in self.iter_pieces():
            if isinstance(board_piece, Pawn) and board_piece is not except_piece:
                board_piece.en_passant = False

    def set_true_enpassant(self, piece, move=None):
        move = move or self.last_move
        if not move or not self.pawn_double_step(piece, move):
            return

        piece.en_passant = True

    def update_enpassant(self, piece, move):
        self.set_false_enpassant(except_piece=piece)
        if isinstance(piece, Pawn):
            piece.en_passant = False
        self.set_true_enpassant(piece, move)

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move,testing=True)
        
        for row, col, enemy_piece in temp_board.iter_pieces():
            if enemy_piece.color == piece.color:
                continue

            temp_board.calc_moves(enemy_piece, row, col, bool=False)
            for m in enemy_piece.moves:
                if isinstance(m.final.piece, King):
                    return True
        return False
    


    
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
