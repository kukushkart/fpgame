import pygame
from config import *
from player import Player
from zombies import Zombie
from pause_menu import PauseMenu

class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False

        self.background = self.load_background()
        self.player = Player()

        # спавн зомби
        self.zombies = []
        self.zombie_spawn_timer = 0

        # таймер урона от зомби
        self.damage_timer = 0.0
        self.game_paused = False

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_p:
                    self.toggle_pause()

    def toggle_pause(self):
        self.game_paused = not self.game_paused

    def handle_pause(self):
        if self.game_paused:
            pause_menu = PauseMenu(self.screen)
            result = pause_menu.run(self.background, self.player)
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
        for z in self.zombies[:]:
            z.move()
            if z.is_off_screen():
                self.zombies.remove(z)

    def handle_collisions(self, dt):
        if self.game_over:
            return
        collided = any(self.player.rect.colliderect(z.rect) for z in self.zombies)
        if collided:
            self.damage_timer += dt
            if self.damage_timer >= 2.0:
                self.damage_timer = 0.0
                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.health = 0
                    self.game_over = True

    def handle_bullet_zombie_collisions(self):
        for bullet in self.player.bullets[:]:
            for z in self.zombies[:]:
                if bullet.rect.colliderect(z.rect):
                    # наносящей пуле урон
                    z.health -= bullet.damage
                    # уничтожаем пулю
                    self.player.bullets.remove(bullet)
                    # если зомби мёртв — удаляем
                    if z.health <= 0:
                        self.zombies.remove(z)
                    break

    def update(self):
        if not self.game_paused:
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.player.update_bullets()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for z in self.zombies:
            z.draw()
        # HUD
        font = pygame.font.Font(FONT_NAME, 30)
        self.screen.blit(font.render(f"Pos: ({self.player.rect.x},{self.player.rect.y})", True, WHITE), (10,10))
        self.screen.blit(font.render(f"HP: {self.player.health}", True, WHITE), (10,40))
        if self.game_over:
            go_font = pygame.font.Font(FONT_NAME, 80)
            go_surf = go_font.render("Game Over", True, RED)
            x = SCREEN_WIDTH//2 - go_surf.get_width()//2
            y = SCREEN_HEIGHT//2 - go_surf.get_height()//2
            self.screen.blit(go_surf, (x, y))
        self.player.draw_bullets(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            if not self.handle_pause():
                break
            self.update()
            if not self.game_over:
                self.spawn_and_update_zombies()
                self.handle_bullet_zombie_collisions()
                self.handle_collisions(dt)
            self.draw()
        pygame.quit()