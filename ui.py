import pygame


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text

    def draw(self, surface, font, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)
        bg = (40, 46, 54) if hovered else (28, 33, 40)
        border = (83, 92, 104) if hovered else (57, 64, 74)
        pygame.draw.rect(surface, bg, self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, width=2, border_radius=6)

        label = font.render(self.text, True, (245, 246, 250))
        surface.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class TextInput:
    def __init__(self, rect, placeholder=""):
        self.rect = pygame.Rect(rect)
        self.placeholder = placeholder
        self.value = ""
        self.active = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            return False

        if event.type != pygame.KEYDOWN or not self.active:
            return False

        if event.key == pygame.K_RETURN:
            return True
        if event.key == pygame.K_BACKSPACE:
            self.value = self.value[:-1]
        elif event.unicode and event.unicode.isprintable() and len(self.value) < 20:
            self.value += event.unicode

        return False

    def draw(self, surface, font):
        border = (82, 160, 255) if self.active else (80, 86, 96)
        pygame.draw.rect(surface, (22, 26, 32), self.rect, border_radius=6)
        pygame.draw.rect(surface, border, self.rect, width=2, border_radius=6)

        text = self.value or self.placeholder
        color = (245, 246, 250) if self.value else (135, 142, 153)
        label = font.render(text, True, color)
        surface.blit(label, (self.rect.x + 14, self.rect.y + 13))


def draw_text(surface, text, font, pos, color=(245, 246, 250)):
    label = font.render(text, True, color)
    surface.blit(label, pos)
