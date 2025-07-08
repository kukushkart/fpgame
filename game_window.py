import pygame
from config import *
from player import Player
from zombies import Zombie

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

        # таймер урона
        self.damage_timer = 0.0

    def load_background(self):
        try:
            bg = pygame.image.load(GAME_BG_IMAGE_PATH).convert()
            return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Invalid attempt of downloading bg. Using standart bg")
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
                    # при Game Over тоже закрываем
                    self.running = False

    def spawn_and_update_zombies(self):
        # спавн раз в секунду (60 фреймов)
        self.zombie_spawn_timer += 1
        if self.zombie_spawn_timer >= 60:
            self.zombie_spawn_timer = 0
            self.zombies.append(Zombie(self.screen))

        # движение и удаление вышедших
        for z in self.zombies[:]:
            z.move()
            if z.is_off_screen():
                self.zombies.remove(z)

    def handle_collisions(self, dt):
        if self.game_over:
            return

        # проверяем пересечение rect'ов
        collided = any(self.player.rect.colliderect(z.rect) for z in self.zombies)
        if collided:
            self.damage_timer += dt
            if self.damage_timer >= 2.0:
                self.damage_timer = 0.0
                self.player.health -= 5
                if self.player.health <= 0:
                    self.player.health = 0
                    self.game_over = True
        else:
            # если хотите сбрасывать таймер при выходе из контакта:
            # self.damage_timer = 0.0
            pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)

        for z in self.zombies:
            z.draw()

        font = pygame.font.Font(FONT_NAME, 30)
        # позиция и здоровье
        pos_text = f"Pos: ({self.player.rect.x},{self.player.rect.y})"
        hp_text  = f"HP: {self.player.health}"
        self.screen.blit(font.render(pos_text, True, WHITE), (10, 10))
        self.screen.blit(font.render(hp_text,  True, WHITE), (10, 40))

        # если проиграли — рисуем красным «Game Over»
        if self.game_over:
            go_font = pygame.font.Font(FONT_NAME, 80)
            go_surf = go_font.render("Game Over", True, RED)
            x = SCREEN_WIDTH // 2  - go_surf.get_width()  // 2
            y = SCREEN_HEIGHT // 2 - go_surf.get_height() // 2
            self.screen.blit(go_surf, (x, y))

        pygame.display.flip()

    def run(self):
        while self.running:
            # dt в секундах
            dt = self.clock.tick(60) / 1000.0

            self.handle_events()

            if not self.game_over:
                self.update()
                self.spawn_and_update_zombies()
                self.handle_collisions(dt)

            self.draw()