import random
from dataclasses import dataclass

from piece import Bishop, King, Knight, Pawn, Queen, Rook


FILES = "abcdefgh"


@dataclass(frozen=True)
class PieceSpec:
    row: int
    col: int
    piece_cls: type
    color: str

    def create_piece(self):
        return self.piece_cls(self.color)


@dataclass(frozen=True)
class Challenge:
    title: str
    objective: str
    pieces: tuple
    target_moves: tuple

    def apply(self, board):
        for _, _, square in board.iter_squares():
            square.piece = None

        for spec in self.pieces:
            board.squares[spec.row][spec.col].piece = spec.create_piece()

        board.last_move = None

    def completed_by(self, move):
        return move.notation() in self.target_moves


def notation(initial, final):
    return f"{FILES[initial[1]]}{8 - initial[0]}{FILES[final[1]]}{8 - final[0]}"


def base_pieces(extra):
    occupied = {(spec.row, spec.col) for spec in extra}
    white_king = next(
        pos for pos in ((7, 4), (7, 7), (7, 0), (6, 4)) if pos not in occupied
    )
    black_king = next(
        pos for pos in ((0, 4), (0, 0), (0, 7), (1, 4)) if pos not in occupied
    )
    return (
        PieceSpec(white_king[0], white_king[1], King, "white"),
        PieceSpec(black_king[0], black_king[1], King, "black"),
        *extra,
    )


def challenge(title, objective, mover, target, target_piece):
    return Challenge(
        title=title,
        objective=objective,
        pieces=base_pieces(
            (
                PieceSpec(mover[0], mover[1], mover[2], "white"),
                PieceSpec(target[0], target[1], target_piece, "black"),
            )
        ),
        target_moves=(notation(mover, target),),
    )


def rook_challenges(limit=25):
    items = []
    lanes = ((0, 7), (7, 0), (1, 6), (6, 1), (2, 5))
    for row in range(1, 6):
        for source_col, target_col in lanes:
            items.append(
                challenge(
                    f"Rook Raid {len(items) + 1}",
                    "Capture the loose queen with the rook.",
                    (row, source_col, Rook),
                    (row, target_col),
                    Queen,
                )
            )
            if len(items) == limit:
                return items
    return items


def bishop_challenges(limit=25):
    items = []
    used = set()
    for source_row in range(2, 8):
        for source_col in range(0, 8):
            for row_step, col_step in ((-1, 1), (-1, -1)):
                target_row = source_row + row_step * 3
                target_col = source_col + col_step * 3
                if not (0 <= target_row < 8 and 0 <= target_col < 8):
                    continue
                if (source_row, source_col) == (7, 4):
                    continue
                key = (source_row, source_col, target_row, target_col)
                if key in used:
                    continue
                used.add(key)
                items.append(
                    challenge(
                        f"Bishop Line {len(items) + 1}",
                        "Use the bishop to win the rook on the diagonal.",
                        (source_row, source_col, Bishop),
                        (target_row, target_col),
                        Rook,
                    )
                )
                if len(items) == limit:
                    return items
    return items


def knight_challenges(limit=25):
    items = []
    offsets = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
    for source_row in range(2, 7):
        for source_col in range(1, 7):
            if (source_row, source_col) == (7, 4):
                continue
            for row_offset, col_offset in offsets:
                target_row = source_row + row_offset
                target_col = source_col + col_offset
                if not (0 <= target_row < 8 and 0 <= target_col < 8):
                    continue
                items.append(
                    challenge(
                        f"Knight Strike {len(items) + 1}",
                        "Jump with the knight to capture the queen.",
                        (source_row, source_col, Knight),
                        (target_row, target_col),
                        Queen,
                    )
                )
                if len(items) == limit:
                    return items
    return items


def queen_challenges(limit=25):
    items = []
    lines = (
        ((6, 0), (1, 5)),
        ((6, 7), (1, 2)),
        ((5, 0), (5, 7)),
        ((5, 7), (5, 0)),
        ((4, 1), (1, 4)),
        ((4, 6), (1, 3)),
        ((3, 0), (0, 3)),
        ((3, 7), (0, 4)),
        ((2, 0), (2, 7)),
        ((2, 7), (2, 0)),
    )
    index = 0
    while len(items) < limit:
        source, target = lines[index % len(lines)]
        items.append(
            challenge(
                f"Queen Tactic {len(items) + 1}",
                "Use the queen to capture the undefended rook.",
                (source[0], source[1], Queen),
                target,
                Rook,
            )
        )
        index += 1
    return items


def promotion_pieces(col):
    black_king_col = 7 if col == 0 else 0
    return (
        PieceSpec(7, 4, King, "white"),
        PieceSpec(0, black_king_col, King, "black"),
        PieceSpec(1, col, Pawn, "white"),
    )


def promotion_challenges(limit=8):
    items = []
    for col in range(8):
        items.append(
            Challenge(
                title=f"Promotion Push {len(items) + 1}",
                objective="Promote the pawn.",
                pieces=promotion_pieces(col),
                target_moves=(notation((1, col), (0, col)),),
            )
        )
        if len(items) == limit:
            return items
    return items


CHALLENGES = tuple(
    rook_challenges()
    + bishop_challenges()
    + knight_challenges()
    + queen_challenges()
    + promotion_challenges()
)


def random_challenge():
    return random.choice(CHALLENGES)
