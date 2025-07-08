import pygame
from config import *
from player import Player
from pause_menu import PauseMenu


class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = self.load_background()

        self.player = Player()

        self.debug_font = pygame.font.Font(None, 30)

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

    def update(self):
        if not self.game_paused:
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.player.update_bullets()

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        self.player.draw(self.screen)

        self.player.draw_bullets(self.screen)

        debug_info = [
            f"Position: ({self.player.rect.x}, {self.player.rect.y})"
        ]

        for i, text in enumerate(debug_info):
            text_surface = self.debug_font.render(text, True, WHITE)
            self.screen.blit(text_surface, (10, 10 + i * 30))


        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()

            if not self.handle_pause():
                break

            self.update()
            self.draw()
            self.clock.tick(60)