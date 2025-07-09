import pygame
from config import *
from ui import Button

class InfoScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.small_font = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)

        self.back_button = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70,100, 50,"Back", RED, (255, 150, 150))

        self.info_lines = [
            "Zombie Survival Game",
            "",
            "Control:",
            "WASD or arrows - movement",
            "Space - shooting",
            "ESC/p - pause",
            "SHIFT - change direction",
            "H - use medkit",
            "",
            "Authors: [Kukulyansky Raman and Paniavin Alexander]",
            "Version 1.0"
        ]

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return True

            self.back_button.check_hover(mouse_pos)
            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return True

            self.screen.fill((40, 45, 50))  # Фон

            title = self.font.render("Info", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            for i, line in enumerate(self.info_lines):
                text = self.small_font.render(line, True, WHITE)
                self.screen.blit(text, (50, 150 + i * 40))

            self.back_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return True
