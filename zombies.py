# zombies.py

import pygame
import random
from config import *

class Zombie:
    VERTICAL_MIN = 458  # как у игрока

    def __init__(self, screen):
        self.screen = screen

        # пытаемся загрузить ваш спрайт
        try:
            self.original_image = pygame.image.load(ZOMBIE_IMAGE_PATH).convert_alpha()
        except Exception as e:
            print(f"Cannot load zombie image: {e}. Using fallback.")
            # если не удалось загрузить — простой прямоугольник
            self.original_image = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, GREEN, (0, 0, ZOMBIE_SIZE, ZOMBIE_SIZE))

        # теперь размер берём из константы
        self.size = ZOMBIE_SIZE
        self.image = pygame.transform.smoothscale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()

        # спавн в правом краю, в тех же вертикальных пределах
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(self.VERTICAL_MIN, SCREEN_HEIGHT - self.size)

        # скорость и направление по Y
        self.speed = random.randint(1, 3)
        self.direction = random.choice([-1, 0, 1])  # -1 вверх, 0 прямо, 1 вниз

    def move(self):
        # движение влево
        self.rect.x -= self.speed

        # шанс сменить вертикальное направление
        if random.random() < 0.05:
            self.direction = random.choice([-1, 0, 1])

        if self.direction == -1:
            self.rect.y -= self.speed
        elif self.direction == 1:
            self.rect.y += self.speed

        # не выходить за пределы сверху/снизу
        self.rect.y = max(self.VERTICAL_MIN, min(SCREEN_HEIGHT - self.size, self.rect.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0


# глобальные данные, если используете их в GameWindow
zombies = []
zombie_spawn_timer = 0