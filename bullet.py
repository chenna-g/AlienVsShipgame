import sys
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_settings, ship, screen):
        super(Bullet, self).__init__()
        # self.ai_settings = ai_settings
        # self.ship = ship
        self.screen = screen
        # create bullets
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_height, ai_settings.bullet_width)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # making bullet to accept float values
        self.y = float(self.rect.y)
        # making bullet colored
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
