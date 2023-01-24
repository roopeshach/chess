import math

class Piece:
    """
    A class to represent a chess piece.

    Attributes:
        name (str): The name of the piece.
        color (str): The color of the piece.
        value (int): The value of the piece.

    
    """
    
    def __init__(self,name, color, value):
        self.name = name
        self.color = color
        
        value_sign = 1 if color == "white" else -1

        self.value = value_sign * value

    def get_moves(self):
        pass


class Pawn(Piece):
    """
    A class to represent a pawn.

    Attributes:
        dir (int): The direction the pawn can move in.


    """
    def __init__(self, color):
        self.dir = -1 if color == "white" else 1
        super().__init__("pawn", color, 1)
    
    def get_moves(self):
        pass

class Rook(Piece):
    """ 
    A class to represent a rook.

    Attributes:
        has_moved (bool): Whether the rook has moved or not.

    """


    def __init__(self, color):
        super().__init__("rook", color, 5)
    
    def get_moves(self):
        pass

    def has_moved(self):
        pass


class Knight(Piece):

    """
    A class to represent a knight.

    """
    def __init__(self, color):
        super().__init__("knight", color, 3)
    
    def get_moves(self):
        pass
        

class Bishop(Piece):
    """A class to represent a bishop."""
    def __init__(self, color):
            super().__init__("bishop", color, 3.001)
        
    def get_moves(self):
        pass
    

class Queen(Piece):

    """A class to represent a queen."""
    def __init__(self, color):
        super().__init__("queen", color, 9)
    
    def get_moves(self):
        pass

class King(Piece):
    """A class to represent a king."""
    def __init__(self, color):
        super().__init__("king", color, math.inf)
    
    def get_moves(self):
        pass


