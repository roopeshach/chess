from const import *
import pygame
from board import Board
from PIL import Image
from drag import Dragger

class Game:
    """ 
    Game class to handle game logic and state.
        
    """

    def __init__(self):
        self.next_player = 'white'
        self.hovered_square = None
        self.board = Board()
        self.dragger = Dragger()

    #show methods  to draw board and pieces

    def show_background(self, surface):
        """Draw the background of the board.
        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        
        for row in range(ROWS):
            for col in range(COLS):
                #alternate board colors
                if (row + col) % 2 == 0:
                    color = DARK_BLUE
                else:
                    color = LIGHT_BLUE
                #draw square
                rectangle = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rectangle)
                

    def show_pieces(self, surface):
        """Draw the pieces on the board.
        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        
        for row in range(ROWS):
            for col in range(COLS):
                #check if square has a piece
                if self.board.squares[row][col].has_piece():
                    #get piece
                    piece = self.board.squares[row][col].piece

                    #all pieces except dragged piece
                    if piece is not self.dragger.piece: 
                        #draw piece
                        piece.set_texture(size=80)
                        image = pygame.image.load(piece.texture)
                        image_center  = col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2
                        piece.texture_rect = image.get_rect(center=image_center)    
                        surface.blit(image, piece.texture_rect)
        

    def show(self, surface):
        self.show_background(surface)
        self.show_pieces(surface)

    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece

            #loop through all valid moves
            for move in piece.moves:
                #color of move
                color = LIGHT_GREEN if (move.final.row + move.final.col) % 2 == 0 else DARK_GREEN
                rect = (move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE, SQSIZE)

                #draw move / blit
                pygame.draw.rect(surface, color, rect)
    
    def next_turn(self):
        """Change the current player."""
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        print(self.next_player)

        
    def show_last_moves(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial , final]:
                 #color of move
                color = (228, 245, 154) if (pos.row + pos.col) % 2 == 0 else (236, 247, 186)
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)

                #draw move / blit
                pygame.draw.rect(surface, color, rect)

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def show_hover(self, surface):
        if self.hovered_square:
            color = (180, 180, 180)
            rect = (self.hovered_square.col*SQSIZE, self.hovered_square.row*SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=2)