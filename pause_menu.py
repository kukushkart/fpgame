import pygame
from config import *
from ui import Button

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)

        self.overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((211, 211, 211, 128))

        button_width = 300
        button_height = 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2

        self.buttons = [
            Button(center_x, SCREEN_HEIGHT // 2 - 80, button_width, button_height, "Return to game", GREEN, (150, 255, 150)),
            Button(center_x, SCREEN_HEIGHT // 2 + 20, button_width, button_height, "Exit", RED, (255, 150, 150)),
        ]

    def run(self, background, player, zombies):
        is_paused = True

        while is_paused:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    return "resume"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True

            for button in self.buttons:
                button.check_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if button.text == "Return to game":
                        return "resume"
                    elif button.text == "Exit":
                        return "quit"

            # Сначала отрисовываем игровой фон
            self.screen.blit(background, (0, 0))
            
            # Затем игрока
            player.draw(self.screen)
            
            # Затем зомби
            for zombie in zombies:
                zombie.draw()
            
            # Затем полупрозрачный оверлей
            self.screen.blit(self.overlay, (0, 0))

            title = self.font.render("PAUSED", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

            for button in self.buttons:
                button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return "resume"
