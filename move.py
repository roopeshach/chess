

class Move:

    def __init__(self, initial , final):
        """A move from initial square to final square.
        Args:
            initial (Square): The initial square.
            final (Square): The final square.
            
        """
        self.initial = initial
        self.final = final
        
    def __str__(self):
        """
        Returns:
            str: A string representation of the move.

        e.g. (0, 0) -> (1, 1)
        """
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'
        return s

    def notation(self):
        return f"{self.initial.alphacol}{8 - self.initial.row}{self.final.alphacol}{8 - self.final.row}"

    def __eq__(self, other):
        """Overrides the default implementation"""

        if not isinstance(other, Move):
            return False
        return self.initial == other.initial and self.final == other.final
