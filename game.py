from const import *
import pygame

class Game:
    """ 
    Game class to handle game logic and state.
        
    """

    def __init__(self):
        pass


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
                    color = WHITE
                else:
                    color = BLACK
                #draw square
                rectangle = (row*SQSIZE, col*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rectangle)
                
                # pygame.draw.rect(surface, color, (row*SQSIZE, col*SQSIZE, SQSIZE, SQSIZE))

    def show_pieces(self, surface):
        pass

    def show(self, surface):
        self.show_background(surface)
        self.show_pieces(surface)

    #update methods to update board and pieces

    def update_background(self):
        pass

    def update_pieces(self):
        pass


