import json
import sqlite3
from datetime import datetime


class GameStorage:
    def __init__(self, path="chess_history.db"):
        self.path = path
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    result TEXT NOT NULL,
                    moves TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS challenges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    result TEXT NOT NULL,
                    move TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )

    def get_or_create_user(self, username):
        username = username.strip() or "Guest"
        now = datetime.utcnow().isoformat(timespec="seconds")

        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO users (username, created_at) VALUES (?, ?)",
                (username, now),
            )
            row = conn.execute(
                "SELECT id, username FROM users WHERE username = ?",
                (username,),
            ).fetchone()

        return {"id": row[0], "username": row[1]}

    def save_game(self, user_id, result, moves):
        if not moves:
            return

        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO games (user_id, result, moves, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    user_id,
                    result,
                    json.dumps(moves),
                    datetime.utcnow().isoformat(timespec="seconds"),
                ),
            )

    def recent_games(self, user_id, limit=10):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT result, moves, created_at
                FROM games
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()

        return [
            {
                "result": result,
                "moves": json.loads(moves),
                "created_at": created_at,
            }
            for result, moves, created_at in rows
        ]

    def save_challenge(self, user_id, title, result, move):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO challenges (user_id, title, result, move, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    title,
                    result,
                    move,
                    datetime.utcnow().isoformat(timespec="seconds"),
                ),
            )

    def recent_challenges(self, user_id, limit=10):
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT title, result, move, created_at
                FROM challenges
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (user_id, limit),
            ).fetchall()

        return [
            {
                "title": title,
                "result": result,
                "move": move,
                "created_at": created_at,
            }
            for title, result, move, created_at in rows
        ]

    def learned_replies(self, user_id=None):
        with self._connect() as conn:
            if user_id:
                rows = conn.execute(
                    "SELECT moves FROM games WHERE user_id = ?",
                    (user_id,),
                ).fetchall()
            else:
                rows = conn.execute("SELECT moves FROM games").fetchall()

        replies = {}
        for (moves_json,) in rows:
            moves = json.loads(moves_json)
            for index in range(0, len(moves) - 1, 2):
                player_move = moves[index]["notation"]
                ai_reply = moves[index + 1]["notation"]
                replies.setdefault(player_move, {})
                replies[player_move][ai_reply] = replies[player_move].get(ai_reply, 0) + 1

        return replies
