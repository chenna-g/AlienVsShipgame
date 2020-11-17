import sys
import pygame

from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(screen, ai_settings)
    pygame.display.set_caption("alien vision")
    play_button=Button(screen,ai_settings, "play")
    stats = GameStats(ai_settings)
    sb=ScoreBoard(screen,ai_settings, stats)
    bullets = Group()
    # alien=Alien(ai_settings, screen)
    aliens = Group()

    gf.create_fleet(ai_settings, screen, aliens, ship)

    while True:
        gf.check_events(ai_settings, ship, screen, bullets, stats, play_button, aliens,sb)  # bullets
        if stats.game_active:
            ship.update()
            # bullets.update()
            gf.update_bullet(aliens, bullets, ai_settings, screen, ship, stats, sb)
            gf.update_aliens(ship, aliens, ai_settings, stats, screen, bullets, sb)
        gf.screen_update(ship, screen, ai_settings, bullets, aliens, play_button, stats,sb)  # bullets


run_game()
