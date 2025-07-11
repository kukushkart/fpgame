import pygame
import random
from pygame.math import Vector2
from config import ZOMBIE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
from zombies import Zombie
class AnimatedZombie(Zombie):
    FRAMES = []
    FRAMES_LEFT = []
    FRAME_TIME = 0.15
    def __init__(self, screen, day=1):
        super().__init__(screen, day)
        self.frames_left = []
        for path in self.FRAMES:
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception as e:
                print(f"Не удалось загрузить {path}: {e}")
                img = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(img, (255,0,255), img.get_rect())
            img = pygame.transform.smoothscale(img, (self.size, self.size))
            self.frames_left.append(img)
        if self.FRAMES_LEFT:
            self.frames_right = []
            for path in self.FRAMES_LEFT:
                try:
                    img = pygame.image.load(path).convert_alpha()
                except Exception as e:
                    print(f"Не удалось загрузить {path}: {e}")
                    img = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
                    pygame.draw.rect(img, (255,0,255), img.get_rect())
                img = pygame.transform.smoothscale(img, (self.size, self.size))
                self.frames_right.append(img)
        else:
            self.frames_right = [pygame.transform.flip(img, True, False)
                                 for img in self.frames_left]
        self.current_frame = 0
        self.timer = 0.0
        self.facing_right = False
        if self.frames_left:
            self.image = self.frames_left[0]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
    def animate(self, dt):
        frames = self.frames_right if self.facing_right else self.frames_left
        if not frames:
            return
        self.timer += dt
        if self.timer >= self.FRAME_TIME:
            self.timer -= self.FRAME_TIME
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]
    def move(self, player_pos, dt):
        old_x = self.pos.x
        super().move(player_pos)
        dx = self.pos.x - old_x
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))
        self.animate(dt)
