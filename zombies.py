# zombies.py

import pygame
import random
from config import *

class Zombie:
    def __init__(self, screen):
        self.screen = screen
        self.size = 30
        self.x = SCREEN_WIDTH
        self.y = random.randint(0, SCREEN_HEIGHT - self.size)
        self.speed = random.randint(1, 3)
        # направление по Y: -1 (вверх), 0 (прямо), 1 (вниз)
        self.direction = random.choice([-1, 0, 1])

    def move(self):
        # движение влево
        self.x -= self.speed

        # с некоторым шансом меняем вертикальное направление
        if random.random() < 0.05:
            self.direction = random.choice([-1, 0, 1])

        if self.direction == -1:
            self.y -= self.speed
        elif self.direction == 1:
            self.y += self.speed

        # не выходим за пределы экрана
        self.y = max(0, min(SCREEN_HEIGHT - self.size, self.y))

    def draw(self):
        # теперь первым аргументом передаём surface
        pygame.draw.rect(self.screen, GREEN, (self.x, self.y, self.size, self.size))

    def is_off_screen(self):
        return self.x + self.size < 0


# глобальный список и таймер спауна (для внешнего кода)
zombies = []
zombie_spawn_timer = 0