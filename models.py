from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from piece import Piece


ColorName = Literal["white", "black"]
MovePlayer = Literal["user", "ml"]
ChallengeResult = Literal["completed", "missed"]
MoveNotation = Annotated[str, Field(pattern=r"^[a-h][1-8][a-h][1-8]$")]


class UserProfile(BaseModel):
    id: int
    username: str


class MoveRecord(BaseModel):
    player: MovePlayer
    piece: str
    notation: MoveNotation
    captured: bool = False


class GameRecord(BaseModel):
    result: str
    moves: list[MoveRecord]
    created_at: str


class ChallengeAttempt(BaseModel):
    title: str
    result: ChallengeResult
    move: MoveNotation
    created_at: str


class PieceSpec(BaseModel):
    model_config = ConfigDict(frozen=True)

    row: int = Field(ge=0, le=7)
    col: int = Field(ge=0, le=7)
    piece_cls: type[Piece]
    color: ColorName

    def create_piece(self) -> Piece:
        return self.piece_cls(self.color)


class Challenge(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    objective: str
    pieces: tuple[PieceSpec, ...]
    target_moves: tuple[MoveNotation, ...]

    def apply(self, board) -> None:
        for _, _, square in board.iter_squares():
            square.piece = None

        for spec in self.pieces:
            board.squares[spec.row][spec.col].piece = spec.create_piece()

        board.last_move = None

    def completed_by(self, move) -> bool:
        return move.notation() in self.target_moves
