import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keyup_events(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_keydown_events(event, ai_settings, ship, screen, bullets):  # bullets
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, ship, screen)

    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(bullets, ai_settings, ship, screen):
    # fire bullet if limit is not reached
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, ship, screen)
        bullets.add(new_bullet)


def check_events(ai_settings, ship, screen, bullets, stats, play_button, aliens, sb):  # bullets
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, ship, screen, bullets)  # bullets

        elif event.type == pygame.KEYUP:
            check_keyup_events(ship, event)


def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset the game stting
        ai_settings.initialize_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        # if play_button.rect.collidepoint(mouse_x, mouse_y):
        # reset the game statitics
        stats.reset_stats()
        stats.game_active = True
        # reset scoreboard and images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        # create the new fleet and center the ship
        # create_fleet(ai_settings, screen, ship, aliens)
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def screen_update(ship, screen, ai_settings, bullets, aliens, play_button, stats, sb):  # bullets
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    # alien.blitme()
    # aliens.draw(screen)
    sb.show_score()
    for alien in aliens.sprites():
        alien.blitme()

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullet(aliens, bullets, ai_settings, screen, ship, stats, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, stats, sb)


def check_bullet_alien_collision(bullets, aliens, ai_settings, screen, ship, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # destroy exisiting bullets , increase speed and create mew fleet
        bullets.empty()
        ai_settings.increase_speed()
        # increase level
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)


def get_number_alien_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(ai_settings, screen)
    number_alien_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_row = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)

    for row_number in range(number_row):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, alien_height, ship_height):
    available_space_y = (ai_settings.screen_width - (3 * alien_height) - ship_height)
    number_row = int(available_space_y / (3 * alien_height))
    return number_row


def update_aliens(ship, aliens, ai_settings, stats, screen, bullets, sb):
    check_fleet_edges(aliens, ai_settings)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, aliens, ship, ai_settings, screen, bullets,sb)
    check_aliens_bottom(screen, aliens, stats, ai_settings, bullets, ship,sb)


def check_fleet_edges(aliens, ai_settings):
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(stats, aliens, ship, ai_settings, screen, bullets, sb):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        #update scoreboard
        sb.prep_ships()
        # empty list of aliens and bullets
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(screen, aliens, stats, ai_settings, bullets, ship,sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(stats, aliens, ship, ai_settings, screen, bullets,sb)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
