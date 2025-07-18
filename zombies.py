import pygame
import random
import math
from pygame.math import Vector2
from config import *
class Zombie:
    BASE_SPEED_RANGE = (1, 2)
    SPEED_PER_DAY = 0.5
    BASE_HEALTH = 50
    HEALTH_PER_DAY = 10
    DETECTION_RADIUS = 300
    DAMAGE = 5
    VERTICAL_MIN = 500
    VERTICAL_MAX = SCREEN_HEIGHT - ZOMBIE_SIZE - 50
    def __init__(self, screen, day=1):
        self.screen = screen
        self.day = day
        try:
            self.original_image = pygame.image.load(ZOMBIE_IMAGE_PATH).convert_alpha()
        except Exception as e:
            print(f"Cannot load zombie image: {e}. Using fallback.")
            self.original_image = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(self.original_image, GREEN, (0, 0, ZOMBIE_SIZE, ZOMBIE_SIZE))
        self.size = ZOMBIE_SIZE
        self.image = pygame.transform.smoothscale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(self.VERTICAL_MIN, self.VERTICAL_MAX)
        self.rect.x = SCREEN_WIDTH
        self.pos = Vector2(self.rect.topleft)
        sp_min, sp_max = self.BASE_SPEED_RANGE
        self.speed = random.randint(sp_min, sp_max) + (day - 1) * self.SPEED_PER_DAY
        self.health = self.BASE_HEALTH + (day - 1) * self.HEALTH_PER_DAY
        self.detection_radius = self.DETECTION_RADIUS
        self.damage = self.DAMAGE
        self.direction = random.choice([-1, 0, 1])
        self.alerted = False
        self.attack_timer = 0.0
        self.attack_delay = 1.5
    def move(self, player_pos):
        px, py = player_pos
        to_player = Vector2(px, py) - self.pos
        dist = to_player.length()
        if not self.alerted and dist <= self.detection_radius:
            self.alerted = True
        if self.alerted and dist != 0:
            dir_vec = to_player.normalize()
            self.pos += dir_vec * self.speed
        else:
            self.pos.x -= self.speed
            if random.random() < 0.05:
                self.direction = random.choice([-1, 0, 1])
            self.pos.y += self.direction * self.speed
        self.pos.y = max(self.VERTICAL_MIN,
                         min(self.VERTICAL_MAX, self.pos.y))
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
    def draw(self):
        self.screen.blit(self.image, self.rect)
    def is_off_screen(self):
        return self.rect.right < 0