import pygame
from config import *
from player import Player
from zombies import Zombie
from pause_menu import PauseMenu
from ui import Button
from upgrade_menu import UpgradeMenu
import random
import math
from pygame.math import Vector2

class BloodParticle:
    def __init__(self, pos):
        # pos — кортеж (x, y), центр всплеска
        self.pos = Vector2(pos)
        # случайное направление
        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 5)
        self.vel = Vector2(math.cos(angle), math.sin(angle)) * speed
        # время жизни
        self.life = random.uniform(0.5, 0.8)
        self.initial_life = self.life
        # размер пятнышка
        self.radius = random.randint(2, 4)

    def update(self, dt):
        self.life -= dt
        self.pos += self.vel

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = max(0, int(255 * (self.life / self.initial_life)))
        surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        color = (200, 0, 0, alpha)
        pygame.draw.circle(surf, color, (self.radius, self.radius), self.radius)
        surface.blit(surf, (self.pos.x - self.radius, self.pos.y - self.radius))


class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.day = 1
        self.wave = 1
        self.money = 500
        self.paused = False

        self.background = self.load_background()
        self.player = Player()

        self.zombies = []
        self.zombie_spawn_timer = 0
        self.damage_timer = 0.0

        self.particles = []

        self.debug_font = pygame.font.Font(None, 30)

        self.game_paused = False

        self.new_game_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
            200, 60, "New Game", GREEN, (150, 255, 150)
        )
        self.exit_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 130,
            200, 60, "Exit", RED, (255, 150, 150)
        )

    def load_background(self):
        try:
            bg = pygame.image.load(GAME_BG_IMAGE_PATH).convert()
            return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Invalid bg download attempt. Using standart bg")
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg.fill((50, 70, 90))
            pygame.draw.rect(bg, (80, 100, 60), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
            return bg

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                if event.key == pygame.K_p:
                    self.toggle_pause()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.paused = not self.paused

        if self.game_over:
            self.new_game_button.check_hover(mouse_pos)
            self.exit_button.check_hover(mouse_pos)

            if self.new_game_button.is_clicked(mouse_pos, mouse_click):
                self.reset_game()
            elif self.exit_button.is_clicked(mouse_pos, mouse_click):
                self.running = False

    def show_upgrade_menu(self):
        menu = UpgradeMenu(self.screen, self.money)
        result = menu.run()

        self.money = menu.money

        if result == "quit":
            return False
        elif result == "continue":
            self.day += 1
            self.wave = 1
            return True
        elif result == "resume":
            return True

        return True

    def toggle_pause(self):
        self.game_paused = not self.game_paused

    def reset_game(self):
        self.game_over = False
        self.player = Player()
        self.zombies = []
        self.zombie_spawn_timer = 0
        self.damage_timer = 0.0
        self.game_paused = False
        self.day = 1
        self.wave = 1
        self.money = 500
        self.paused = False

    def handle_pause(self):
        if self.game_paused:
            pause_menu = PauseMenu(self.screen)
            result = pause_menu.run(self.background, self.player, self.zombies)

            if result == "quit":
                return False
            elif result == "resume":
                self.game_paused = False

        return True

    def spawn_and_update_zombies(self):
        self.zombie_spawn_timer += 1
        if self.zombie_spawn_timer >= 60:
            self.zombie_spawn_timer = 0
            self.zombies.append(Zombie(self.screen))

        player_pos = self.player.rect.center
        for z in self.zombies[:]:
            z.move(player_pos)
            if z.is_off_screen():
                self.zombies.remove(z)

    def handle_collisions(self, dt):
        if self.game_over:
            return

        # Проверяем, сталкивается ли игрок с каким-либо зомби
        collided = any(self.player.rect.colliderect(z.rect) for z in self.zombies)

        if collided:
            if self.damage_timer <= 0.0:
                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.health = 0
                    self.game_over = True
                self.damage_timer = 1.5
            else:
                self.damage_timer -= dt
        else:
            self.damage_timer = 0.0

    def handle_bullet_zombie_collisions(self):
        for bullet in self.player.bullets[:]:
            for z in self.zombies[:]:
                if bullet.rect.colliderect(z.rect):
                    for _ in range(12):
                        self.particles.append(BloodParticle(z.rect.center))
                    z.health -= bullet.damage
                    self.player.bullets.remove(bullet)
                    if z.health <= 0:
                        self.zombies.remove(z)
                        self.money += 10
                    break

    def update_particles(self, dt):
        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)


    def update(self):
        if not self.game_paused and not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.player.update_bullets()

    def draw_health_bar(self, x, y, width, height, current_health, max_health):
        border_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(self.screen, BLACK, border_rect)

        red_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, RED, red_rect)

        if current_health > 0:
            green_width = int((current_health / max_health) * width)
            green_rect = pygame.Rect(x, y, green_width, height)
            pygame.draw.rect(self.screen, GREEN, green_rect)

        font = pygame.font.Font(FONT_NAME, 20)
        health_text = f"{current_health}/{max_health}"
        text_surface = font.render(health_text, True, WHITE)

        shadow_surface = font.render(health_text, True, BLACK)

        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2

        self.screen.blit(shadow_surface, (text_x + 1, text_y + 1))
        self.screen.blit(text_surface, (text_x, text_y))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for z in self.zombies:
            z.draw()

        font = pygame.font.Font(FONT_NAME, 30)
        pos_text = f"Pos: ({self.player.rect.x},{self.player.rect.y})"
        ammo_text = f"Ammo: {self.player.current_ammo}/{self.player.magazine_size}"
        reload_text = "Reloading..." if self.player.is_reloading else ""

        self.screen.blit(font.render(pos_text, True, WHITE), (10, 10))
        self.draw_health_bar(10, 50, 200, 30, self.player.health, self.player.max_health)
        self.screen.blit(font.render(ammo_text, True, WHITE), (10, 90))
        self.screen.blit(font.render(reload_text, True, RED), (10, 120))

        self.player.draw_bullets(self.screen)

        day_text = self.debug_font.render(f"Day: {self.day} | Волна: {self.wave}", True, WHITE)
        self.screen.blit(day_text, (SCREEN_WIDTH - day_text.get_width() - 10, 10))

        money_text = self.debug_font.render(f"Money: {self.money}$", True, (255, 215, 0))
        self.screen.blit(money_text, (SCREEN_WIDTH - money_text.get_width() - 10, 40))

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            go_font = pygame.font.Font(FONT_NAME, 80)
            go_surf = go_font.render("Game Over", True, RED)
            x = SCREEN_WIDTH // 2 - go_surf.get_width() // 2
            y = SCREEN_HEIGHT // 2 - go_surf.get_height() // 2 - 50
            self.screen.blit(go_surf, (x, y))

            self.new_game_button.draw(self.screen)
            self.exit_button.draw(self.screen)

            for p in self.particles:
                p.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            if not self.handle_pause():
                break

            if not self.paused:
                self.update()
                if not self.game_over:
                    self.spawn_and_update_zombies()
                    self.handle_bullet_zombie_collisions()
                    self.handle_collisions(dt)
                    self.handle_bullet_zombie_collisions()
                    self.update_particles(dt)
            else:
                if not self.show_upgrade_menu():
                    break
                self.paused = False

            self.draw()
