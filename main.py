#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
from typing import Literal

import pygame

from challenges import random_challenge
from const import HEIGHT, SQSIZE, WIDTH
from game import Game
from ml_player import LearningPlayer
from move import Move
from models import Challenge, UserProfile
from square import Square
from storage import GameStorage
from ui import Button, TextInput, draw_text


LOGIN = "login"
MENU = "menu"
PLAY = "play"
HISTORY = "history"
CHALLENGE = "challenge"
AppState = Literal["login", "menu", "play", "history", "challenge"]


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Reev Chess")

        self.running = True
        self.state: AppState = LOGIN
        self.storage = GameStorage()
        self.user: UserProfile | None = None
        self.game = Game()
        self.learning_player = LearningPlayer(self.storage)
        self.game_saved = False
        self.challenge: Challenge | None = None
        self.challenge_result: str = ""
        self.challenge_finished: bool = False

        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.heading_font = pygame.font.SysFont("monospace", 30, bold=True)
        self.font = pygame.font.SysFont("monospace", 20)
        self.small_font = pygame.font.SysFont("monospace", 16)

        self.username_input = TextInput((210, 355, 380, 52), "Username")
        self.login_button = Button((300, 430, 200, 52), "Login")
        self.play_button = Button((270, 280, 260, 52), "Play vs ML")
        self.challenge_button = Button((270, 350, 260, 52), "Challenges")
        self.history_button = Button((270, 420, 260, 52), "Last Games")
        self.logout_button = Button((270, 490, 260, 52), "Logout")
        self.back_button = Button((32, 720, 150, 44), "Back")
        self.new_game_button = Button((610, 18, 160, 38), "New Game")
        self.next_challenge_button = Button((590, 18, 180, 38), "Next")

    def mainloop(self) -> None:
        while self.running:
            self.render()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif self.state == LOGIN:
                    self.handle_login_event(event)
                elif self.state == MENU:
                    self.handle_menu_event(event)
                elif self.state == PLAY:
                    self.handle_play_event(event)
                elif self.state == HISTORY:
                    self.handle_history_event(event)
                elif self.state == CHALLENGE:
                    self.handle_challenge_event(event)

            pygame.display.update()

    def render(self) -> None:
        if self.state == LOGIN:
            self.render_login()
        elif self.state == MENU:
            self.render_menu()
        elif self.state == PLAY:
            self.render_play()
        elif self.state == HISTORY:
            self.render_history()
        elif self.state == CHALLENGE:
            self.render_challenge()

    def render_panel_background(self) -> None:
        self.screen.fill((15, 18, 24))
        pygame.draw.rect(self.screen, (26, 31, 38), (0, 0, WIDTH, 90))
        pygame.draw.line(self.screen, (62, 70, 82), (0, 90), (WIDTH, 90), 2)

    def render_login(self) -> None:
        self.render_panel_background()
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.screen, "Reev Chess", self.title_font, (245, 150))
        draw_text(self.screen, "Player Profile", self.heading_font, (275, 245), (186, 194, 205))
        self.username_input.draw(self.screen, self.font)
        self.login_button.draw(self.screen, self.font, mouse_pos)

    def render_menu(self) -> None:
        self.render_panel_background()
        mouse_pos = pygame.mouse.get_pos()
        username = self.user.username if self.user else "Guest"
        draw_text(self.screen, "Home", self.title_font, (335, 145))
        draw_text(self.screen, f"Signed in as {username}", self.font, (285, 230), (186, 194, 205))
        self.play_button.draw(self.screen, self.font, mouse_pos)
        self.challenge_button.draw(self.screen, self.font, mouse_pos)
        self.history_button.draw(self.screen, self.font, mouse_pos)
        self.logout_button.draw(self.screen, self.font, mouse_pos)

    def render_play(self) -> None:
        self.game.render(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        self.new_game_button.draw(self.screen, self.small_font, mouse_pos)
        status = f"{self.user.username} vs ML - {self.game.next_player.title()} to move"
        draw_text(self.screen, status, self.small_font, (18, 18), (20, 24, 30))

        if self.game.dragger.dragging:
            self.game.dragger.update_blit(self.screen)

    def render_history(self) -> None:
        self.render_panel_background()
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.screen, "Last Games", self.title_font, (255, 110))

        games = self.storage.recent_games(self.user.id, limit=8)
        if not games:
            draw_text(self.screen, "No saved games yet.", self.font, (280, 250), (186, 194, 205))
        else:
            y = 205
            for index, game in enumerate(games, start=1):
                moves = " ".join(move.notation for move in game.moves[:12])
                if len(game.moves) > 12:
                    moves += " ..."
                draw_text(
                    self.screen,
                    f"{index}. {game.created_at} - {game.result}",
                    self.font,
                    (70, y),
                )
                draw_text(self.screen, moves, self.small_font, (90, y + 28), (186, 194, 205))
                y += 72

        challenges = self.storage.recent_challenges(self.user.id, limit=4)
        if challenges:
            draw_text(self.screen, "Challenges", self.heading_font, (70, 575))
            y = 620
            for challenge in challenges:
                text = f"{challenge.created_at} - {challenge.title} - {challenge.result} ({challenge.move})"
                draw_text(self.screen, text, self.small_font, (90, y), (186, 194, 205))
                y += 28

        self.back_button.draw(self.screen, self.font, mouse_pos)

    def render_challenge(self) -> None:
        self.game.render(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        self.next_challenge_button.draw(self.screen, self.small_font, mouse_pos)
        self.back_button.draw(self.screen, self.small_font, mouse_pos)

        title = self.challenge.title if self.challenge else "Challenge"
        objective = self.challenge.objective if self.challenge else ""
        draw_text(self.screen, title, self.small_font, (18, 16), (20, 24, 30))
        draw_text(self.screen, objective, self.small_font, (18, 42), (20, 24, 30))
        if self.challenge_result:
            draw_text(self.screen, self.challenge_result, self.small_font, (18, 68), (20, 24, 30))

        if self.game.dragger.dragging:
            self.game.dragger.update_blit(self.screen)

    def handle_login_event(self, event: pygame.event.Event) -> None:
        submitted = self.username_input.handle_event(event)
        if submitted or self.login_button.clicked(event):
            self.user = self.storage.get_or_create_user(self.username_input.value)
            self.state = MENU

    def handle_menu_event(self, event: pygame.event.Event) -> None:
        if self.play_button.clicked(event):
            self.start_new_game()
        elif self.challenge_button.clicked(event):
            self.start_challenge()
        elif self.history_button.clicked(event):
            self.state = HISTORY
        elif self.logout_button.clicked(event):
            self.finish_current_game("left menu")
            self.user = None
            self.username_input.value = ""
            self.state = LOGIN

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.start_new_game()

    def handle_history_event(self, event: pygame.event.Event) -> None:
        if self.back_button.clicked(event):
            self.state = MENU
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.state = MENU

    def handle_play_event(self, event: pygame.event.Event) -> None:
        game = self.game
        board = game.board
        dragger = game.dragger

        if self.new_game_button.clicked(event):
            self.finish_current_game("new game")
            self.start_new_game()
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                game.change_theme()
            elif event.key == pygame.K_r:
                self.finish_current_game("reset")
                self.start_new_game()
            elif event.key == pygame.K_ESCAPE:
                self.finish_current_game("left game")
                self.state = MENU
            elif event.key == pygame.K_q:
                self.quit()
            return

        if game.next_player != "white":
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            dragger.update_mouse(event.pos)
            row, col = self.board_position(event.pos)
            if row is None:
                return

            square = board.squares[row][col]
            if square.has_piece() and square.piece.color == game.next_player:
                piece = square.piece
                piece.clear_moves()
                board.calc_moves(piece, row, col, bool=True)
                dragger.save_initial(event.pos)
                dragger.drag_piece(piece)

        elif event.type == pygame.MOUSEMOTION:
            row, col = self.board_position(event.pos)
            if row is not None:
                game.set_hover(row, col)

            if dragger.dragging:
                dragger.update_mouse(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if not dragger.dragging:
                return

            dragger.update_mouse(event.pos)
            row, col = self.board_position(event.pos)
            if row is not None:
                move = Move(
                    Square(dragger.initial_row, dragger.initial_col),
                    Square(row, col),
                )
                if board.valid_move(dragger.piece, move):
                    game.apply_move(dragger.piece, move, "user")
                    dragger.drop_piece()
                    self.play_learning_move(move)
                    return

            dragger.drop_piece()

    def handle_challenge_event(self, event: pygame.event.Event) -> None:
        game = self.game
        board = game.board
        dragger = game.dragger

        if self.next_challenge_button.clicked(event):
            self.start_challenge()
            return
        if self.back_button.clicked(event):
            self.state = MENU
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state = MENU
            elif event.key == pygame.K_r:
                self.start_challenge()
            elif event.key == pygame.K_t:
                game.change_theme()
            elif event.key == pygame.K_q:
                self.quit()
            return

        if self.challenge_finished or game.next_player != "white":
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            dragger.update_mouse(event.pos)
            row, col = self.board_position(event.pos)
            if row is None:
                return

            square = board.squares[row][col]
            if square.has_piece() and square.piece.color == "white":
                piece = square.piece
                piece.clear_moves()
                board.calc_moves(piece, row, col, bool=True)
                dragger.save_initial(event.pos)
                dragger.drag_piece(piece)

        elif event.type == pygame.MOUSEMOTION:
            row, col = self.board_position(event.pos)
            if row is not None:
                game.set_hover(row, col)
            if dragger.dragging:
                dragger.update_mouse(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if not dragger.dragging:
                return

            dragger.update_mouse(event.pos)
            row, col = self.board_position(event.pos)
            if row is not None:
                move = Move(
                    Square(dragger.initial_row, dragger.initial_col),
                    Square(row, col),
                )
                if board.valid_move(dragger.piece, move):
                    game.apply_move(dragger.piece, move, "user")
                    self.finish_challenge(move)
                    dragger.drop_piece()
                    return

            dragger.drop_piece()

    def play_learning_move(self, last_user_move: Move) -> None:
        if self.game.next_player != "black":
            return

        piece, move = self.learning_player.choose_move(self.game.board, last_user_move)
        if not piece or not move:
            self.finish_current_game("user wins")
            self.state = MENU
            return

        self.game.apply_move(piece, move, "ml")

    def board_position(self, pos: tuple[int, int]) -> tuple[int | None, int | None]:
        col = pos[0] // SQSIZE
        row = pos[1] // SQSIZE
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None, None

    def start_new_game(self) -> None:
        self.game = Game()
        self.learning_player = LearningPlayer(self.storage, self.user.id)
        self.game_saved = False
        self.state = PLAY

    def start_challenge(self) -> None:
        self.game = Game()
        self.challenge = random_challenge()
        self.challenge.apply(self.game.board)
        self.challenge_result = ""
        self.challenge_finished = False
        self.state = CHALLENGE

    def finish_challenge(self, move: Move) -> None:
        success = self.challenge.completed_by(move)
        result = "completed" if success else "missed"
        self.challenge_result = "Correct. Press Next for another." if success else "Missed. Press R to retry or Next."
        self.challenge_finished = True
        self.storage.save_challenge(
            self.user.id,
            self.challenge.title,
            result,
            move.notation(),
        )

    def finish_current_game(self, result: str) -> None:
        if self.user and not self.game_saved and self.game.move_history:
            self.storage.save_game(self.user.id, result, self.game.move_history)
            self.game_saved = True

    def quit(self) -> None:
        self.finish_current_game("quit")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Main().mainloop()
