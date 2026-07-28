

class Square:
    """A square on a chess board.

    Attributes:
        row (int): The row of the square.
        col (int): The column of the square.
        piece (Piece): The piece on the square.
    """

    ALPHACOLS = ("a", "b", "c", "d", "e", "f", "g", "h")

    def __init__(self, row: int, col: int, piece=None) -> None:
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = Square.ALPHACOLS[col]

    def has_piece(self) -> bool:
        return self.piece is not None
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Square):
            return False
        return self.row == other.row and self.col == other.col
    
    def is_empty(self) -> bool:
        return not self.has_piece()

    def has_team_piece(self, color: str) -> bool:
        return self.has_piece() and self.piece.color == color
    
    def has_enemy_piece(self, color: str) -> bool:
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_enemy(self, color: str) -> bool:
        return self.is_empty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args: int) -> bool:
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def get_alpha_col(col: int) -> str:
        return Square.ALPHACOLS[col]


# print(Square.in_range(5, 2, 5, 3))
