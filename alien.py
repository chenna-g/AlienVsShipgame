import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settins = ai_settings
        self.screen = screen
        self.image = pygame.image.load("/Users/goldenhusband/PycharmProjects/alien_vision/images/alien.bmp")
        self.rect = self.image.get_rect()

        # load image on to screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # place the alien in exact position
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        screen_rect =self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left < 0:
            return True

    def update(self):
        self.x += (self.ai_settins.alien_speed_factor*self.ai_settins.fleet_direction)
        self.rect.x = self.x

