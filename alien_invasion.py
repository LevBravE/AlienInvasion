from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship
from time import sleep

import pygame as pg
import sys


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""

    def __init__(self):
        pg.init()
        self.settings = Settings()

        self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pg.display.set_caption('Alien Invasion')

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pg.sprite.Group()
        self.aliens = pg.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, 'Play')

    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pg.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек
            self.settings.initialize_dynamic_settings()

            # Сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_scope()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрываем
            pg.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pg.K_q:
            sys.exit()
        elif event.key == pg.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        if event.key == pg.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pg.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновлении позиции снарядов и удаление старых снарядов"""
        self.bullets.update()

        # Удаление снарядов вышедших за экран
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Проверка попаданий в пришельцев
        # При обнаружении попадания удалить снаряд и пришельца
        collisions = pg.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_scope()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Создание флота вторжения"""
        alien = Alien(self)
        alien_wight, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 + alien_wight)
        number_aliens_x = available_space_x // (2 * alien_wight)

        # Определим кол-во рядов помещающихся на экране
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создаем пришельца и размещаем его в ряду"""
        alien = Alien(self)
        alien_wight, alien_height = alien.rect.size
        alien.x = alien_wight + 2 * alien_wight * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Отпускает весь флот и меняет направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец-корабль"
        if pg.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверка добрались ли пришельцы до нижнего края экрана
        self._check_alians_bottom()

    def _ship_hit(self):
        """Обработка столкновения коробля с пришельцем"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.stats.game_active = False
            pg.mouse.set_visible(True)

    def _check_alians_bottom(self):
        """Проверяет добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pg.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
