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
        
        
        pygame.display.set_caption("Reev Chess")


    def mainloop(self):
        
        while self.running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            self.screen.fill(WHITE)

            pygame.display.flip()

            pygame.display.update()


main = Main()
main.mainloop()

# Path: main.py