import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, screen, ai_settings):
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings=ai_settings

        # load the ship image
        self.image=pygame.image.load('/Users/goldenhusband/PycharmProjects/alien_vision/images/ship.bmp')
        # get the rectangle values of screen and image
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()
        # make the image and screen centers equal to place ship in middle
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right= False
        self.moving_left= False
        self.center=float(self.rect.centerx)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # update image rect coordinates
        self.rect.centerx = self.center

    def center_ship(self):
        self.center =self.screen_rect.centerx
