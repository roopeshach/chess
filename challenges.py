import random
from dataclasses import dataclass

from piece import Bishop, King, Knight, Pawn, Queen, Rook


@dataclass
class Challenge:
    title: str
    objective: str
    pieces: tuple
    target_moves: tuple

    def apply(self, board):
        for _, _, square in board.iter_squares():
            square.piece = None

        for row, col, piece in self.pieces:
            board.squares[row][col].piece = piece

        board.last_move = None

    def completed_by(self, move):
        return move.notation() in self.target_moves


CHALLENGES = (
    Challenge(
        title="Win the Queen",
        objective="Find the rook move that wins the queen.",
        pieces=(
            (7, 4, King("white")),
            (0, 4, King("black")),
            (7, 0, Rook("white")),
            (0, 0, Queen("black")),
        ),
        target_moves=("a1a8",),
    ),
    Challenge(
        title="Knight Fork",
        objective="Use the knight to fork the king and queen.",
        pieces=(
            (7, 4, King("white")),
            (0, 6, King("black")),
            (3, 3, Knight("white")),
            (1, 5, Queen("black")),
        ),
        target_moves=("d5f6",),
    ),
    Challenge(
        title="Promotion",
        objective="Promote the pawn.",
        pieces=(
            (7, 4, King("white")),
            (0, 4, King("black")),
            (1, 0, Pawn("white")),
        ),
        target_moves=("a7a8",),
    ),
    Challenge(
        title="Long Diagonal",
        objective="Capture the rook on the long diagonal.",
        pieces=(
            (7, 6, King("white")),
            (0, 6, King("black")),
            (7, 0, Bishop("white")),
            (0, 7, Rook("black")),
        ),
        target_moves=("a1h8",),
    ),
)


def random_challenge():
    return random.choice(CHALLENGES)
