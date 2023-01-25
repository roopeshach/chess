#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
import sys
from const import *
from game import Game


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
        board = game.board
        dragger = self.game.dragger


        while self.running:
            game.show_background(screen)
            game.show_pieces(screen)
            # self.clock.tick(60)
            for event in pygame.event.get():

                #mouse events

                #mouse button down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # print(event.pos)
                    dragger.update_mouse(event.pos)

                    clicked_row = event.pos[0] // SQSIZE
                    clicked_col = event.pos[1] // SQSIZE

                    # print(clicked_row, clicked_col)
                    print(dragger.mouseY, clicked_row)
                    print(dragger.mouseX, clicked_col)

                    if board.squares[clicked_row][clicked_col].has_piece():
                        print("has piece")
                        piece = board.squares[clicked_row][clicked_col].piece
                        dragger.save_initial(event.pos)
                        dragger.drag_piece(piece)

                        print(dragger.initial_row, dragger.initial_col)
                        print(dragger.mouseX, dragger.mouseY)


                #mouse button up
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass

                #mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_blit(event.pos)



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