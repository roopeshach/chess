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
            game.show_moves(screen)
            
            game.show_pieces(screen)

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
                        print("has piece")
                        piece = board.squares[clicked_row][clicked_col].piece
                        board.calc_moves(piece, clicked_row, clicked_col)
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                        #show methods
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)


                #mouse motion / drag
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        #show methods
                        game.show_background(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)

                #mouse button up / drop / leave
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
                            print("valid move")
                            board.move(dragger.piece, move)
                            
                            #show methods
                            game.show_background(screen)
                            game.show_pieces(screen)

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
                    pass

                #key up
                elif event.type == pygame.KEYUP:
                    pass

            

            

            # pygame.display.flip()

            pygame.display.update()


main = Main()
main.mainloop()

# Path: main.py