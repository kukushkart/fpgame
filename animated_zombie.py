# animated_zombie.py

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

        # загрузим «левающие» кадры
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

        # загрузим «правые» кадры, если указаны, иначе просто перевернём
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
            # автоген через флип
            self.frames_right = [pygame.transform.flip(img, True, False)
                                 for img in self.frames_left]

        # инициализация анимации
        self.current_frame = 0
        self.timer = 0.0
        # флаг направления: по умолчанию смотрим влево (если ваши кадры — левые)
        self.facing_right = False

        # ставим первый кадр
        if self.frames_left:
            self.image = self.frames_left[0]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)

    def animate(self, dt):
        # выбираем нужный список кадров
        frames = self.frames_right if self.facing_right else self.frames_left
        if not frames:
            return

        self.timer += dt
        if self.timer >= self.FRAME_TIME:
            self.timer -= self.FRAME_TIME
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.image = frames[self.current_frame]

    def move(self, player_pos, dt):
        # запомним старую X для детекции направления
        old_x = self.pos.x

        # выполняем стандартный ход из базового класса
        super().move(player_pos)

        # теперь определяем, куда мы действительно двинулись
        dx = self.pos.x - old_x
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False
        # если dx==0 — оставляем прежний флаг

        # обновляем rect (только если сменился размер/позиция)
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # запускаем анимацию с учётом dt
        self.animate(dt)