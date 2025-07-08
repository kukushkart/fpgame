import pygame
from config import *


class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.running = True
        self.background = self.load_background()

    def load_background(self):
        try:
            bg = pygame.image.load(GAME_BG_IMAGE_PATH).convert()
            return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print(f"Invalid download of game bg: {GAME_BG_IMAGE_PATH}")
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg.fill((50, 50, 70))
            pygame.draw.rect(bg, (80, 80, 80), (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
            return bg

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        text = self.font.render("Game scene", True, WHITE)
        text_shadow = self.font.render("Game scene", True, (30, 30, 30))

        self.screen.blit(text_shadow,
                         (SCREEN_WIDTH // 2 - text.get_width() // 2 + 3,
                          SCREEN_HEIGHT // 2 + 3))
        self.screen.blit(text,
                         (SCREEN_WIDTH // 2 - text.get_width() // 2,
                          SCREEN_HEIGHT // 2))

        pygame.display.flip()