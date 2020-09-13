import pygame
import colors


class Button:

    def __init__(self, text, x=0, y=0, width=100, height=50, font_size=20, normal_color=colors.BLUE, hovered_color=colors.LIGHT_BLUE, command=None):

        self.text = text
        self.command = command

        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill(normal_color)

        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill(hovered_color)

        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.Font('freesansbold.ttf', font_size)

        text_image = font.render(text, True, colors.WHITE)
        text_rect = text_image.get_rect(center=self.rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)

        # you can't use it before `blit`
        self.rect.topleft = (x, y)

        self.hovered = False
        # self.clicked = False

    def update(self):

        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, surface):

        surface.blit(self.image, self.rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                return True
        return False
