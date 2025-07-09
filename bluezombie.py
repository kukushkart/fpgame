import pygame
import random
from pygame.math import Vector2
from config import ZOMBIE_SIZE, ZOMBIE_IMAGE_PATH, SCREEN_WIDTH, SCREEN_HEIGHT
from zombies import Zombie

class BlueZombie(Zombie):
    def __init__(self, screen, day=1,
                 frame_paths=None, frame_time=0.15):
        # frame_paths — список путей к изображению каждого кадра
        super().__init__(screen, day)

        if frame_paths is None:
            # Если не передали — подгрузим 3 одинаковых из стандартного
            frame_paths = [ZOMBIE_IMAGE_PATH] * 3

        # Загружаем и масштабируем все кадры
        self.frames = []
        for path in frame_paths:
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception as e:
                print(f"Не удалось загрузить {path}: {e}")
                img = pygame.Surface((ZOMBIE_SIZE, ZOMBIE_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(img, (0,255,0), img.get_rect())
            img = pygame.transform.smoothscale(img, (self.size, self.size))
            self.frames.append(img)

        # Параметры анимации
        self.current_frame = 0
        self.frame_time = frame_time    # сколько секунд держать каждый кадр
        self.timer = 0.0

        # Первая картинка-анимашка
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def animate(self, dt):
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer -= self.frame_time
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            # обновляем текущую картинку
            self.image = self.frames[self.current_frame]

    # Переопределим метод move, чтобы в нём двигаться и анимироваться
    def move(self, player_pos, dt):
        # сначала базовое движение
        super().move(player_pos)
        # потом обновляем кадр анимации
        self.animate(dt)

    # draw оставляем без изменений, он уже блыоторисует self.image