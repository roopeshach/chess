import math
import os


class Piece:
    """
    A class to represent a chess piece.

    Attributes:
        name (str): The name of the piece.
        color (str): The color of the piece.
        value (int): The value of the piece.
        moves (list): A list of valid moves for the piece.
        texture (str): The texture of the piece.
        texture_rect (pygame.Rect): The rectangle of the texture.


    
    """
    
    def __init__(
        self,
        name: str,
        color: str,
        value: float,
        texture: str | None = None,
        texture_rect=None,
    ) -> None:
        self.name = name
        self.color = color
        value_sign = 1 if color == "white" else -1
        self.value = value_sign * value

        #store all possible valid moves for the piece
        self.moves = []
        self.moved = False
        # overlay texture image on top of the piece 
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect



    def set_texture(self, size: int = 80) -> None:
        # render pieces images respectively
        self.texture = os.path.join(f"assets/images/{size}px/{self.color}_{self.name}_{size}.png")
        # print(self.texture)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    def __str__(self) -> str:
        return f"{self.color} {self.name}"

    def get_moves(self) -> None:
        pass
    
    def add_move(self, move) -> None:
        self.moves.append(move)

    def clear_moves(self) -> None:
        self.moves = []

class Pawn(Piece):
    """
    A class to represent a pawn.

    Attributes:
        dir (int): The direction the pawn can move in.


    """ 
    def __init__(self, color: str) -> None:
        self.dir = -1 if color == "white" else 1
        self.en_passant = False
        super().__init__("pawn", color, 1)
    
    def get_moves(self) -> None:
        pass

class Rook(Piece):
    """ 
    A class to represent a rook.

    Attributes:
        has_moved (bool): Whether the rook has moved or not.

    """


    def __init__(self, color: str) -> None:
        super().__init__("rook", color, 5)
    
    def get_moves(self) -> None:
        pass

    def has_moved(self) -> None:
        pass


class Knight(Piece):

    """
    A class to represent a knight.

    """
    def __init__(self, color: str) -> None:
        super().__init__("knight", color, 3)
    
    def get_moves(self) -> None:
        pass
        

class Bishop(Piece):
    """A class to represent a bishop."""
    def __init__(self, color: str) -> None:
            super().__init__("bishop", color, 3.001)
        
    def get_moves(self) -> None:
        pass
    

class Queen(Piece):

    """A class to represent a queen."""
    def __init__(self, color: str) -> None:
        super().__init__("queen", color, 9)
    
    def get_moves(self) -> None:
        pass

class King(Piece):
    """A class to represent a king."""
    def __init__(self, color: str) -> None:
        self.left_rook = None
        self.right_rook = None
        super().__init__("king", color, math.inf)
    
    def get_moves(self) -> None:
        pass
