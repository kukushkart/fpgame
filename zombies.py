# zombies.py

import pygame
import random
from config import *

class Zombie:
    # та же верхняя граница, что и у игрока
    VERTICAL_MIN = 458

    def __init__(self, screen):
        self.screen = screen
        self.size = 30
        self.x = SCREEN_WIDTH
        # spawn только между VERTICAL_MIN и SCREEN_HEIGHT–size
        self.y = random.randint(self.VERTICAL_MIN, SCREEN_HEIGHT - self.size)
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

        # не выходим за верхнюю/нижнюю границу
        self.y = max(self.VERTICAL_MIN, min(SCREEN_HEIGHT - self.size, self.y))

    def draw(self):
        pygame.draw.rect(self.screen, GREEN, (self.x, self.y, self.size, self.size))

    def is_off_screen(self):
        return self.x + self.size < 0


zombies = []
zombie_spawn_timer = 0