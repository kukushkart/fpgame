# animated_zombie.py

import pygame
import random
from pygame.math import Vector2
from config import ZOMBIE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from zombies import Zombie

class AnimatedZombie(Zombie):
    FRAMES = []
    FRAME_TIME = 0.15

    def __init__(self, screen, day=1):
        super().__init__(screen, day)
        self.frames = []
        for path in self.FRAMES:
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception as e:
                print(f"Не удалось загрузить {path}: {e}")
                img = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(img, (255,0,255), img.get_rect())
            img = pygame.transform.smoothscale(img, (self.size, self.size))
            self.frames.append(img)


        self.current_frame = 0
        self.timer = 0.0
        # первая картинка
        if self.frames:
            self.image = self.frames[0]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def animate(self, dt):
        if not self.frames:
            return
        self.timer += dt
        if self.timer >= self.FRAME_TIME:
            self.timer -= self.FRAME_TIME
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def move(self, player_pos, dt):
        super().move(player_pos)
        self.animate(dt)