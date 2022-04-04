import pygame as pg


class Button:

    def __init__(self, ai_game, msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Размеры и свойства кнопки
        self.wight, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (250, 250, 250)
        self.font = pg.font.SysFont(None, 48)

        # Построение объекта rect кнопки и выравнивание по центру
        self.rect = pg.Rect(0, 0, self.wight, self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
