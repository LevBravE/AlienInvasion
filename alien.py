from pygame.sprite import Sprite

import pygame as pg


class Alien(Sprite):
    """Класс, представляющий одного прешельца"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        self.image = pg.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый пришелиц появляется в левом верхнем углу экрана
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
