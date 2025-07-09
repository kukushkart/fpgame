import pygame
import os
import random
import math

from config import *
from player import Player
from zombies import Zombie
from pause_menu import PauseMenu
from ui import Button, draw_menu
from pygame.math import Vector2

class BloodEffect:
    """
    Анимация брызг крови из трёх кадров.
    """
    def __init__(self, pos, frames, frame_time=0.08):
        self.pos = pos            # центр эффекта (x,y)
        self.frames = frames      # список Surface
        self.frame_time = frame_time
        self.timer = 0.0
        self.current = 0
        self.done = False

    def update(self, dt):
        if self.done:
            return
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer -= self.frame_time
            self.current += 1
            if self.current >= len(self.frames):
                self.done = True

    def draw(self, surface):
        if not self.done:
            img = self.frames[self.current]
            rect = img.get_rect(center=self.pos)
            surface.blit(img, rect)


class GameWindow:
    def __init__(self, screen, player_name="", skin=PLAYER_IMAGE_PATH):
        self.screen = screen
        self.player_name = player_name
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        # фон
        try:
            bg = pygame.image.load(GAME_BG_IMAGE_PATH).convert()
            self.background = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 70, 90))

        # игрок
        self.player = Player(skin)

        # списки зомби
        self.zombies = []
        self.dying_zombies = []    # <-- для «умирающих» зомби
        self.zombie_spawn_timer = 0

        # урон от столкновения
        self.damage_timer = 0.0

        # Загрузка кадров крови
        self.blood_frames = []
        for i in (1, 2, 3):
            path = os.path.join("assets", "images", f"blood_frame_{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception as e:
                print(f"Cannot load {path}: {e}")
                img = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(img, (200,0,0), (10,10), 10)
            self.blood_frames.append(img)

        self.blood_effects = []

        # шрифт для отладки
        self.debug_font = pygame.font.Font(None, 30)

    def spawn_and_update_zombies(self):
        self.zombie_spawn_timer += 1
        if self.zombie_spawn_timer >= 60:
            self.zombie_spawn_timer = 0
            self.zombies.append(Zombie(self.screen))

        for z in self.zombies[:]:
            z.move(self.player.rect.center)
            if z.is_off_screen():
                self.zombies.remove(z)

    def handle_collisions(self, dt):
        if self.game_over:
            return
        if any(self.player.rect.colliderect(z.rect) for z in self.zombies):
            self.damage_timer += dt
            if self.damage_timer >= 2.0:
                self.damage_timer = 0.0
                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.health = 0
                    self.game_over = True
        else:
            self.damage_timer = 0.0

    def handle_bullet_zombie_collisions(self):
        """
        При попадании пули в зомби:
         - создаём BloodEffect
         - удаляем пулю
         - зомби переводим в dying_zombies,
           а из основного списка убираем
        """
        for bullet in self.player.bullets[:]:
            for z in self.zombies[:]:
                if bullet.rect.colliderect(z.rect):
                    eff = BloodEffect(z.rect.center, self.blood_frames)
                    self.blood_effects.append(eff)

                    # удаляем пулю
                    self.player.bullets.remove(bullet)
                    # зомби «переходит» в умирающие
                    self.zombies.remove(z)
                    self.dying_zombies.append((z, eff))
                    break

    def update_blood_effects(self, dt):
        for eff in self.blood_effects[:]:
            eff.update(dt)
            if eff.done:
                self.blood_effects.remove(eff)
                # удалить связанного зомби
                for pair in self.dying_zombies:
                    if pair[1] is eff:
                        self.dying_zombies.remove(pair)
                        break

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.player.update_bullets()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)

        # живые зомби
        for z in self.zombies:
            z.draw()

        # умирающие (отрисовка зомби + эффекта крови)
        for z, eff in self.dying_zombies:
            z.draw()
            eff.draw(self.screen)

        # пули
        self.player.draw_bullets(self.screen)

        # HUD
        pos_text = f"Pos: ({self.player.rect.x},{self.player.rect.y})"
        hp_text  = f"HP: {self.player.health}"
        self.screen.blit(self.debug_font.render(pos_text, True, WHITE), (10,10))
        self.screen.blit(self.debug_font.render(hp_text,  True, WHITE), (10,40))

        # Game Over
        if self.game_over:
            go_font = pygame.font.Font(FONT_NAME, 80)
            go_surf = go_font.render("Game Over", True, RED)
            x = SCREEN_WIDTH//2 - go_surf.get_width()//2
            y = SCREEN_HEIGHT//2 - go_surf.get_height()//2
            self.screen.blit(go_surf, (x,y))

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            if not self.game_over:
                self.update()
                self.spawn_and_update_zombies()
                self.handle_bullet_zombie_collisions()
                self.handle_collisions(dt)
                self.update_blood_effects(dt)
            self.draw()
        pygame.quit()