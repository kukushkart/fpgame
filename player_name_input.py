import pygame
from config import *
from ui import Button


class PlayerNameInput:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.small_font = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)

        self.player_name = ""
        self.active_input = True

        self.start_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100,
            300, 60, "Next", GREEN, (150, 255, 150)
        )
        self.back_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 170,
            300, 60, "Back", RED, (255, 150, 150)
        )

        self.input_width = 400
        self.input_height = 60
        self.input_x = SCREEN_WIDTH // 2 - self.input_width // 2
        self.input_y = SCREEN_HEIGHT // 2 - 30

        self.input_rect = pygame.Rect(
            self.input_x, self.input_y,
            self.input_width, self.input_height
        )
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_active

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True
                        if self.input_rect.collidepoint(event.pos):
                            self.active_input = True
                            self.color = self.color_active
                        else:
                            self.active_input = False
                            self.color = self.color_passive

                if event.type == pygame.KEYDOWN and self.active_input:
                    if event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if self.player_name.strip():
                            return self.player_name.strip()
                    else:
                        if len(self.player_name) < 15:
                            self.player_name += event.unicode

            self.start_button.check_hover(mouse_pos)
            self.back_button.check_hover(mouse_pos)

            if self.start_button.is_clicked(mouse_pos, mouse_click):
                if self.player_name.strip():
                    return self.player_name.strip()
            elif self.back_button.is_clicked(mouse_pos, mouse_click):
                return None

            self.screen.fill((40, 45, 50))

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("Enter Your Name", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

            pygame.draw.rect(self.screen, self.color, self.input_rect, 2, border_radius=10)

            text_surface = self.small_font.render(self.player_name, True, WHITE)
            text_x = self.input_rect.x + (self.input_rect.width - text_surface.get_width()) // 2
            text_y = self.input_rect.y + (self.input_rect.height - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (text_x, text_y))

            hint = self.small_font.render("(Press Enter to confirm)", True, (150, 150, 150))
            self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, self.input_rect.bottom + 10))

            self.start_button.draw(self.screen)
            self.back_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return None