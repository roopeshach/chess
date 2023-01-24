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
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game()
        
        pygame.display.set_caption("Reev Chess")


    def mainloop(self):
        
        while self.running:
            self.game.show_background(self.screen)
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            

            pygame.display.flip()

            pygame.display.update()


main = Main()
main.mainloop()

# Path: main.py