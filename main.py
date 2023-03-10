#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.game = Game()
        
        pygame.display.set_caption("Reev Chess")


    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger


        while self.running:
            #show methods
            game.show_background(screen)
            game.show_last_moves(screen)
            game.show_moves(screen)
            
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                #mouse events
                #mouse button down / click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print(event.pos)
                    dragger.update_mouse(event.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        # print("has piece")
                        piece = board.squares[clicked_row][clicked_col].piece

                        # valid piece color ? /find next player turn
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)

                            #show methods
                            game.show_background(screen)
                            game.show_last_moves(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                            game.show_hover(screen)


                #mouse motion / drag
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show methods
                        game.show_background(screen)
                        game.show_last_moves(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                #mouse button up / drop / leave /release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #check if piece was dropped on a valid square / create possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)

                        #check if move is valid
                        if board.valid_move(dragger.piece, move):
                            # print("valid move")
                            #normal capture
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_enpassant(dragger.piece)


                            game.play_sound(captured)
                            #show methods
                            game.show_background(screen)
                            game.show_last_moves(screen)
                            game.show_pieces(screen)

                            #change player turn
                            game.next_turn()

                        dragger.update_blit(screen)


                    dragger.drop_piece()   
                    # print("dropped piece")



                #quit game
                elif event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                #keyboard events

                #key down
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_t:
                        
                        game.change_theme()
                    if event.key == pygame.K_r:
                        
                        game.reset()
                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                    if event.key == pygame.K_q:
                        self.running = False
                        pygame.quit()
                        sys.exit()
                #key up
                elif event.type == pygame.KEYUP:
                    pass

            pygame.display.update()


main = Main()
main.mainloop()

# Path: main.py