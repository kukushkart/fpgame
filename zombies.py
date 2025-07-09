# zombies.py

import pygame
import random
import math
from pygame.math import Vector2
from config import *


class Zombie:
    VERTICAL_MIN = 500  # как у игрока
    DETECTION_RADIUS = 300  # радиус «обнаружения» (пикс.)

    def __init__(self, screen, day=1):
        self.screen = screen
        self.day = day

        # пытаемся загрузить спрайт зомби
        try:
            self.original_image = pygame.image.load(ZOMBIE_IMAGE_PATH).convert_alpha()
        except Exception as e:
            print(f"Cannot load zombie image: {e}. Using fallback.")
            self.original_image = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, GREEN, (0, 0, ZOMBIE_SIZE, ZOMBIE_SIZE))

        self.size = ZOMBIE_SIZE
        self.image = pygame.transform.smoothscale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()

        # старт за правой границей экрана
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(self.VERTICAL_MIN, SCREEN_HEIGHT - self.size)

        # переводим позицию в float
        self.pos = Vector2(self.rect.topleft)

        # скорость и направление для хаоса
        self.speed = random.randint(1, 2) + (self.day - 1) * 0.5  # Увеличиваем скорость
        self.health = 50 + (self.day - 1) * 10  # Увеличиваем здоровье
        self.direction = random.choice([-1, 0, 1])
        self.alerted = False

        # Таймер атаки для каждого зомби
        self.attack_timer = 0.0  # Таймер между атаками
        self.attack_delay = 1.5  # Задержка между атаками в секундах
        self.damage = 5  # Урон, наносимый зомби

    def move(self, player_pos):
        px, py = player_pos
        # вектор от зомби к игроку
        to_player = Vector2(px, py) - self.pos
        dist = to_player.length()

        # если ещё не был в состоянии chase и игрок в зоне — переключаемся
        if not self.alerted and dist <= self.DETECTION_RADIUS:
            self.alerted = True

        if self.alerted:
            # преследуем по вектору, масштабируя на full speed
            if dist != 0:
                direction = to_player.normalize()
                self.pos += direction * self.speed
        else:
            # хаотичное движение влево с вертикальным дрейфом
            self.pos.x -= self.speed
            if random.random() < 0.05:
                self.direction = random.choice([-1, 0, 1])
            self.pos.y += self.direction * self.speed

        # ограничения по Y
        self.pos.y = max(self.VERTICAL_MIN, min(SCREEN_HEIGHT - self.size, self.pos.y))

        # обновляем rect
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def is_off_screen(self):
        return self.rect.right < 0