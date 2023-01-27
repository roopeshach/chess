import pygame

class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(self.path)



    def play_sound(self):
        pygame.mixer.Sound.play(self.sound)

    def stop_sound(self):
        pygame.mixer.Sound.stop(self.sound)

    def pause_sound(self):
        pygame.mixer.Sound.pause(self.sound)

    def resume_sound(self):
        pygame.mixer.Sound.unpause(self.sound)

        