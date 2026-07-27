#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pygame

from const import HEIGHT, SQSIZE, WIDTH
from game import Game
from ml_player import LearningPlayer
from move import Move
from square import Square
from storage import GameStorage
from ui import Button, TextInput, draw_text


LOGIN = "login"
MENU = "menu"
PLAY = "play"
HISTORY = "history"


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Reev Chess")

        self.running = True
        self.state = LOGIN
        self.storage = GameStorage()
        self.user = None
        self.game = Game()
        self.learning_player = LearningPlayer(self.storage)
        self.game_saved = False

        self.title_font = pygame.font.SysFont("monospace", 48, bold=True)
        self.heading_font = pygame.font.SysFont("monospace", 30, bold=True)
        self.font = pygame.font.SysFont("monospace", 20)
        self.small_font = pygame.font.SysFont("monospace", 16)

        self.username_input = TextInput((210, 355, 380, 52), "Username")
        self.login_button = Button((300, 430, 200, 52), "Login")
        self.play_button = Button((270, 310, 260, 56), "Play vs ML")
        self.history_button = Button((270, 385, 260, 56), "Last Games")
        self.logout_button = Button((270, 460, 260, 56), "Logout")
        self.back_button = Button((32, 720, 150, 44), "Back")
        self.new_game_button = Button((610, 18, 160, 38), "New Game")

    def mainloop(self):
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

            pygame.display.update()

    def render(self):
        if self.state == LOGIN:
            self.render_login()
        elif self.state == MENU:
            self.render_menu()
        elif self.state == PLAY:
            self.render_play()
        elif self.state == HISTORY:
            self.render_history()

    def render_panel_background(self):
        self.screen.fill((15, 18, 24))
        pygame.draw.rect(self.screen, (26, 31, 38), (0, 0, WIDTH, 90))
        pygame.draw.line(self.screen, (62, 70, 82), (0, 90), (WIDTH, 90), 2)

    def render_login(self):
        self.render_panel_background()
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.screen, "Reev Chess", self.title_font, (245, 150))
        draw_text(self.screen, "Player Profile", self.heading_font, (275, 245), (186, 194, 205))
        self.username_input.draw(self.screen, self.font)
        self.login_button.draw(self.screen, self.font, mouse_pos)

    def render_menu(self):
        self.render_panel_background()
        mouse_pos = pygame.mouse.get_pos()
        username = self.user["username"] if self.user else "Guest"
        draw_text(self.screen, "Home", self.title_font, (335, 145))
        draw_text(self.screen, f"Signed in as {username}", self.font, (285, 230), (186, 194, 205))
        self.play_button.draw(self.screen, self.font, mouse_pos)
        self.history_button.draw(self.screen, self.font, mouse_pos)
        self.logout_button.draw(self.screen, self.font, mouse_pos)

    def render_play(self):
        self.game.render(self.screen)
        mouse_pos = pygame.mouse.get_pos()
        self.new_game_button.draw(self.screen, self.small_font, mouse_pos)
        status = f"{self.user['username']} vs ML - {self.game.next_player.title()} to move"
        draw_text(self.screen, status, self.small_font, (18, 18), (20, 24, 30))

        if self.game.dragger.dragging:
            self.game.dragger.update_blit(self.screen)

    def render_history(self):
        self.render_panel_background()
        mouse_pos = pygame.mouse.get_pos()
        draw_text(self.screen, "Last Games", self.title_font, (255, 110))

        games = self.storage.recent_games(self.user["id"], limit=8)
        if not games:
            draw_text(self.screen, "No saved games yet.", self.font, (280, 250), (186, 194, 205))
        else:
            y = 205
            for index, game in enumerate(games, start=1):
                moves = " ".join(move["notation"] for move in game["moves"][:12])
                if len(game["moves"]) > 12:
                    moves += " ..."
                draw_text(
                    self.screen,
                    f"{index}. {game['created_at']} - {game['result']}",
                    self.font,
                    (70, y),
                )
                draw_text(self.screen, moves, self.small_font, (90, y + 28), (186, 194, 205))
                y += 72

        self.back_button.draw(self.screen, self.font, mouse_pos)

    def handle_login_event(self, event):
        submitted = self.username_input.handle_event(event)
        if submitted or self.login_button.clicked(event):
            self.user = self.storage.get_or_create_user(self.username_input.value)
            self.state = MENU

    def handle_menu_event(self, event):
        if self.play_button.clicked(event):
            self.start_new_game()
        elif self.history_button.clicked(event):
            self.state = HISTORY
        elif self.logout_button.clicked(event):
            self.finish_current_game("left menu")
            self.user = None
            self.username_input.value = ""
            self.state = LOGIN

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.start_new_game()

    def handle_history_event(self, event):
        if self.back_button.clicked(event):
            self.state = MENU
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            self.state = MENU

    def handle_play_event(self, event):
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

    def play_learning_move(self, last_user_move):
        if self.game.next_player != "black":
            return

        piece, move = self.learning_player.choose_move(self.game.board, last_user_move)
        if not piece or not move:
            self.finish_current_game("user wins")
            self.state = MENU
            return

        self.game.apply_move(piece, move, "ml")

    def board_position(self, pos):
        col = pos[0] // SQSIZE
        row = pos[1] // SQSIZE
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None, None

    def start_new_game(self):
        self.game = Game()
        self.learning_player = LearningPlayer(self.storage, self.user["id"])
        self.game_saved = False
        self.state = PLAY

    def finish_current_game(self, result):
        if self.user and not self.game_saved and self.game.move_history:
            self.storage.save_game(self.user["id"], result, self.game.move_history)
            self.game_saved = True

    def quit(self):
        self.finish_current_game("quit")
        self.running = False
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Main().mainloop()
