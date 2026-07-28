import random

from models import Challenge, PieceSpec
from piece import Bishop, King, Knight, Pawn, Queen, Rook


FILES = "abcdefgh"


def notation(initial: tuple[int, int], final: tuple[int, int]) -> str:
    return f"{FILES[initial[1]]}{8 - initial[0]}{FILES[final[1]]}{8 - final[0]}"


def base_pieces(extra: tuple[PieceSpec, ...]) -> tuple[PieceSpec, ...]:
    occupied = {(spec.row, spec.col) for spec in extra}
    white_king = next(
        pos for pos in ((7, 4), (7, 7), (7, 0), (6, 4)) if pos not in occupied
    )
    black_king = next(
        pos for pos in ((0, 4), (0, 0), (0, 7), (1, 4)) if pos not in occupied
    )
    return (
        PieceSpec(row=white_king[0], col=white_king[1], piece_cls=King, color="white"),
        PieceSpec(row=black_king[0], col=black_king[1], piece_cls=King, color="black"),
        *extra,
    )


def challenge(
    title: str,
    objective: str,
    mover: tuple[int, int, type],
    target: tuple[int, int],
    target_piece: type,
) -> Challenge:
    return Challenge(
        title=title,
        objective=objective,
        pieces=base_pieces(
            (
                PieceSpec(row=mover[0], col=mover[1], piece_cls=mover[2], color="white"),
                PieceSpec(row=target[0], col=target[1], piece_cls=target_piece, color="black"),
            )
        ),
        target_moves=(notation(mover, target),),
    )


def rook_challenges(limit: int = 25) -> list[Challenge]:
    items: list[Challenge] = []
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


def bishop_challenges(limit: int = 25) -> list[Challenge]:
    items: list[Challenge] = []
    used: set[tuple[int, int, int, int]] = set()
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


def knight_challenges(limit: int = 25) -> list[Challenge]:
    items: list[Challenge] = []
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


def queen_challenges(limit: int = 25) -> list[Challenge]:
    items: list[Challenge] = []
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


def promotion_pieces(col: int) -> tuple[PieceSpec, ...]:
    black_king_col = 7 if col == 0 else 0
    return (
        PieceSpec(row=7, col=4, piece_cls=King, color="white"),
        PieceSpec(row=0, col=black_king_col, piece_cls=King, color="black"),
        PieceSpec(row=1, col=col, piece_cls=Pawn, color="white"),
    )


def promotion_challenges(limit: int = 8) -> list[Challenge]:
    items: list[Challenge] = []
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


CHALLENGES: tuple[Challenge, ...] = tuple(
    rook_challenges()
    + bishop_challenges()
    + knight_challenges()
    + queen_challenges()
    + promotion_challenges()
)


def random_challenge() -> Challenge:
    return random.choice(CHALLENGES)
