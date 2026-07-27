import random

from piece import Bishop, King, Knight, Pawn, Queen, Rook


PIECE_VALUES = {
    Pawn: 1,
    Knight: 3,
    Bishop: 3,
    Rook: 5,
    Queen: 9,
    King: 0,
}


class LearningPlayer:
    def __init__(self, storage, user_id=None, color="black"):
        self.storage = storage
        self.user_id = user_id
        self.color = color
        self.learned_replies = self.storage.learned_replies(user_id)

    def choose_move(self, board, last_user_move=None):
        moves = self._legal_moves(board)
        if not moves:
            return None, None

        learned = self._learned_move(moves, last_user_move)
        if learned:
            return learned

        return max(moves, key=lambda item: self._score_move(item[1]))

    def _legal_moves(self, board):
        moves = []
        for row, col, piece in board.iter_pieces():
            if piece.color != self.color:
                continue

            piece.clear_moves()
            board.calc_moves(piece, row, col, bool=True)
            for move in piece.moves:
                moves.append((piece, move))

        return moves

    def _learned_move(self, moves, last_user_move):
        if not last_user_move:
            return None

        replies = self.learned_replies.get(last_user_move.notation(), {})
        if not replies:
            return None

        by_notation = {move.notation(): (piece, move) for piece, move in moves}
        known_replies = [
            (notation, count)
            for notation, count in replies.items()
            if notation in by_notation
        ]
        if not known_replies:
            return None

        best_count = max(count for _, count in known_replies)
        best_notations = [
            notation for notation, count in known_replies if count == best_count
        ]
        return by_notation[random.choice(best_notations)]

    def _score_move(self, move):
        captured = move.final.piece
        capture_score = 0
        if captured:
            capture_score = PIECE_VALUES.get(type(captured), 0) * 10

        center_distance = abs(move.final.row - 3.5) + abs(move.final.col - 3.5)
        return capture_score - center_distance
