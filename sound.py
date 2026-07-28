import pygame


class Sound:

    def __init__(self, path: str) -> None:
        self.path = path
        self.sound = pygame.mixer.Sound(self.path)

    def play_sound(self) -> None:
        pygame.mixer.Sound.play(self.sound)

    def stop_sound(self) -> None:
        pygame.mixer.Sound.stop(self.sound)

    def pause_sound(self) -> None:
        pygame.mixer.Sound.pause(self.sound)

    def resume_sound(self) -> None:
        pygame.mixer.Sound.unpause(self.sound)
