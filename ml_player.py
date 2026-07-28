import copy
import math

from board import Board
from move import Move
from piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from storage import GameStorage


PIECE_VALUES = {
    Pawn: 100,
    Knight: 320,
    Bishop: 330,
    Rook: 500,
    Queen: 900,
    King: 20000,
}

CENTER_SQUARES = {(3, 3), (3, 4), (4, 3), (4, 4)}
EXTENDED_CENTER = {
    (2, 2), (2, 3), (2, 4), (2, 5),
    (3, 2), (3, 5),
    (4, 2), (4, 5),
    (5, 2), (5, 3), (5, 4), (5, 5),
}


class LearningPlayer:
    def __init__(
        self,
        storage: GameStorage,
        user_id: int | None = None,
        color: str = "black",
        depth: int = 3,
    ) -> None:
        self.storage = storage
        self.user_id = user_id
        self.color = color
        self.opponent_color = "white" if color == "black" else "black"
        self.depth = depth
        self.learned_replies = self.storage.learned_replies(user_id)
        self._root_reply_weights: dict[str, int] = {}

    def choose_move(self, board: Board, last_user_move: Move | None = None) -> tuple[Piece | None, Move | None]:
        moves = self._legal_moves(board, self.color)
        if not moves:
            return None, None

        self._root_reply_weights = self._reply_weights(last_user_move)
        ordered_moves = self._ordered_moves(moves)
        best_piece, best_move = ordered_moves[0]
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf

        for piece, move in ordered_moves:
            next_board = self._simulate_move(board, move)
            score = self._minimax(
                next_board,
                depth=self.depth - 1,
                alpha=alpha,
                beta=beta,
                maximizing=False,
            )
            score += self._learned_bonus(move)

            if score > best_score:
                best_score = score
                best_piece, best_move = piece, move

            alpha = max(alpha, best_score)

        return best_piece, best_move

    def _minimax(
        self,
        board: Board,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> float:
        if depth == 0:
            return self._evaluate(board)

        color = self.color if maximizing else self.opponent_color
        moves = self._legal_moves(board, color)
        if not moves:
            return self._terminal_score(board, color)

        if maximizing:
            value = -math.inf
            for _, move in self._ordered_moves(moves):
                value = max(
                    value,
                    self._minimax(
                        self._simulate_move(board, move),
                        depth=depth - 1,
                        alpha=alpha,
                        beta=beta,
                        maximizing=False,
                    ),
                )
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value

        value = math.inf
        for _, move in self._ordered_moves(moves):
            value = min(
                value,
                self._minimax(
                    self._simulate_move(board, move),
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                    maximizing=True,
                ),
            )
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

    def _legal_moves(self, board: Board, color: str) -> list[tuple[Piece, Move]]:
        moves: list[tuple[Piece, Move]] = []
        for row, col, piece in board.iter_pieces():
            if piece.color != color:
                continue

            piece.clear_moves()
            board.calc_moves(piece, row, col, bool=True)
            for move in piece.moves:
                moves.append((piece, move))

        return moves

    def _ordered_moves(self, moves: list[tuple[Piece, Move]]) -> list[tuple[Piece, Move]]:
        return sorted(
            moves,
            key=lambda item: (
                self._move_order_score(item[0], item[1]),
                item[1].notation(),
            ),
            reverse=True,
        )

    def _move_order_score(self, piece: Piece, move: Move) -> float:
        captured = move.final.piece
        capture_score = 0
        if captured:
            capture_score = PIECE_VALUES.get(type(captured), 0) - PIECE_VALUES.get(type(piece), 0) / 20

        promotion_score = 800 if isinstance(piece, Pawn) and move.final.row in (0, 7) else 0
        center_score = self._square_activity(piece, move.final.row, move.final.col)
        learned_score = self._learned_bonus(move)
        return capture_score + promotion_score + center_score + learned_score

    def _simulate_move(self, board: Board, move: Move) -> Board:
        next_board = copy.deepcopy(board)
        piece = next_board.squares[move.initial.row][move.initial.col].piece
        next_move = Move(
            next_board.squares[move.initial.row][move.initial.col],
            next_board.squares[move.final.row][move.final.col],
        )
        next_board.move(piece, next_move)
        return next_board

    def _evaluate(self, board: Board) -> float:
        score = 0.0
        for row, col, piece in board.iter_pieces():
            value = PIECE_VALUES.get(type(piece), 0)
            value += self._square_activity(piece, row, col)
            value += self._pawn_structure(board, piece, row, col)

            if piece.color == self.color:
                score += value
            else:
                score -= value

        score += self._mobility_score(board)
        return score

    def _square_activity(self, piece: Piece, row: int, col: int) -> float:
        if isinstance(piece, King):
            return 0

        score = 0.0
        if (row, col) in CENTER_SQUARES:
            score += 25
        elif (row, col) in EXTENDED_CENTER:
            score += 12

        advancement = (6 - row) if piece.color == "white" else (row - 1)
        if isinstance(piece, Pawn):
            score += advancement * 8
        elif isinstance(piece, (Knight, Bishop)):
            score += max(0, advancement) * 3

        return score

    def _pawn_structure(self, board: Board, piece: Piece, row: int, col: int) -> float:
        if not isinstance(piece, Pawn):
            return 0

        score = 0.0
        direction = -1 if piece.color == "white" else 1
        for guard_col in (col - 1, col + 1):
            guard_row = row - direction
            if not (0 <= guard_row < 8 and 0 <= guard_col < 8):
                continue
            guard = board.squares[guard_row][guard_col].piece
            if isinstance(guard, Pawn) and guard.color == piece.color:
                score += 10
        return score

    def _mobility_score(self, board: Board) -> float:
        own_moves = self._pseudo_mobility(board, self.color)
        opponent_moves = self._pseudo_mobility(board, self.opponent_color)
        return (own_moves - opponent_moves) * 2

    def _pseudo_mobility(self, board: Board, color: str) -> int:
        total = 0
        for row, col, piece in board.iter_pieces():
            if piece.color != color:
                continue

            piece.clear_moves()
            board.calc_moves(piece, row, col, bool=False)
            total += len(piece.moves)
        return total

    def _terminal_score(self, board: Board, color_to_move: str) -> float:
        if not self._king_exists(board, self.color):
            return -100000
        if not self._king_exists(board, self.opponent_color):
            return 100000

        return -50000 if color_to_move == self.color else 50000

    def _king_exists(self, board: Board, color: str) -> bool:
        return any(isinstance(piece, King) and piece.color == color for _, _, piece in board.iter_pieces())

    def _reply_weights(self, last_user_move: Move | None) -> dict[str, int]:
        if not last_user_move:
            return {}

        return self.learned_replies.get(last_user_move.notation(), {})

    def _learned_bonus(self, move: Move) -> float:
        count = self._root_reply_weights.get(move.notation(), 0)
        return min(count * 15, 75)
