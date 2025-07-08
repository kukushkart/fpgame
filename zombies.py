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
            self.original_image = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, GREEN, (0, 0, ZOMBIE_SIZE, ZOMBIE_SIZE))

        self.size = ZOMBIE_SIZE
        self.image = pygame.transform.smoothscale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()

        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(self.VERTICAL_MIN, SCREEN_HEIGHT - self.size)

        self.speed = random.randint(1, 2)
        self.direction = random.choice([-1, 0, 1])  # -1 вверх, 0 прямо, 1 вниз

        self.health = 50     # <-- добавлено здоровье

    def move(self):
        self.rect.x -= self.speed
        if random.random() < 0.05:
            self.direction = random.choice([-1, 0, 1])
        if self.direction == -1:
            self.rect.y -= self.speed
        elif self.direction == 1:
            self.rect.y += self.speed
        self.rect.y = max(self.VERTICAL_MIN, min(SCREEN_HEIGHT - self.size, self.rect.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0