import pygame
import colors


class Text:
    def __init__(self, text, x=0, y=0, font_size=18, text_color=colors.WHITE, surface_color=colors.BLACK):
        # create the display surface object
        # of specific dimension..e(X, Y).
        font = pygame.font.Font('freesansbold.ttf', font_size)
        self.text = font.render(text, True, text_color, surface_color)
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)

    def draw(self, surface):
        surface.blit(self.text, self.textRect)
