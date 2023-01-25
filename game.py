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
                
                # pygame.draw.rect(surface, color, (row*SQSIZE, col*SQSIZE, SQSIZE, SQSIZE))

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

    #update methods to update board and pieces

    def update_background(self):
        pass

    def update_pieces(self):
        pass


