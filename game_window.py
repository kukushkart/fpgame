import pygame
from config import *
from player import Player


class GameWindow:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = self.load_background()

        self.player = Player()

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
                    self.running = False

    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)

        font = pygame.font.Font(None, 30)
        debug_text = f"Position: ({self.player.rect.x}, {self.player.rect.y})"
        text_surface = font.render(debug_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)