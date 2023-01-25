import pygame
from const import *

class Dragger:

    """Class to handle dragging pieces.
    Attributes:
        piece (Piece): The piece being dragged.
        dragging (bool): Whether or not a piece is being dragged.
        mouseX (int): The x position of the mouse.
        mouseY (int): The y position of the mouse.
        initial_row (int): The initial row of the piece being dragged.
        initial_col (int): The initial column of the piece being dragged.

        Methods:
            update_mouse(pos): Update the position of the mouse.
            save_initial_pos(pos): Save the initial position of the piece being dragged.

    """


    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouseX  = 0
        self.mouseY  = 0
        self.initial_row = 0
        self.initial_col = 0

    def update_mouse(self, pos):
        """Update the position of the mouse.
        Args:
            pos (tuple): The position of the mouse.
        """

        self.mouseX, self.mouseY = pos # pos is a tuple of (x, y)

    def save_initial(self, pos):
        """Save the initial position of the piece being dragged.
        Args:
            pos (tuple): The initial position of the piece being dragged.
        """

        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self,piece):
        """Set the piece being dragged.

        Args:
            piece (Piece): The piece being dragged.
        """
        self.piece = piece
        self.dragging = True
    
    def drop_piece(self):
        """Drop the piece being dragged.
        """
        self.piece = None
        self.dragging = False

    #blit method
    def update_blit(self, surface):
        """Update the position of the piece being dragged.
        Args:
            surface (pygame.Surface): The surface to draw the piece on.
        """
        #texture 
        self.piece.set_texture(size=120)
        texture = self.piece.texture
        #image 
        image = pygame.image.load(texture)

        #rectangles
        image_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = image.get_rect(center=image_center)

        #blit
        surface.blit(image, self.piece.texture_rect)

    def update(self, surface):
        """Update the position of the piece being dragged.
        Args:
            surface (pygame.Surface): The surface to draw the piece on.
        """
        if self.dragging:
            self.update_blit(surface)

# Path: game.py

    