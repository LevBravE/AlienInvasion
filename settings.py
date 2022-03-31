class Settings:
    """Класс для хранения всех настроек игры"""

    def __init__(self):
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Настройки корабля
        self.ship_speed = 5

        # Параметры снаряда
        self.bullet_speed = 3
        self.bullet_wight = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3
