import pygame
from config import *
from ui import Button


class CharacterSelectScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.small_font = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)

        try:
            self.skin1 = pygame.image.load("assets/images/test_survivor.png").convert_alpha()
            self.skin2 = pygame.image.load("assets/images/test_survivor_v2.png").convert_alpha()
        except Exception as e:
            print(f"Cannot load character skins: {e}. Using fallback.")
            self.skin1 = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.circle(self.skin1, (255, 0, 0), (75, 75), 75)
            self.skin2 = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.circle(self.skin2, (0, 255, 0), (75, 75), 75)

        self.skin1 = pygame.transform.smoothscale(self.skin1, (150, 150))
        self.skin2 = pygame.transform.smoothscale(self.skin2, (150, 150))

        self.skin1_rect = pygame.Rect(SCREEN_WIDTH // 4 - 75, SCREEN_HEIGHT // 2 - 75, 150, 150)
        self.skin2_rect = pygame.Rect(3 * SCREEN_WIDTH // 4 - 75, SCREEN_HEIGHT // 2 - 75, 150, 150)

        self.skin1_border = pygame.Rect(SCREEN_WIDTH // 4 - 80, SCREEN_HEIGHT // 2 - 80, 160, 160)
        self.skin2_border = pygame.Rect(3 * SCREEN_WIDTH // 4 - 80, SCREEN_HEIGHT // 2 - 80, 160, 160)

        self.start_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 170,
            300, 60, "Start Game", GREEN, (150, 255, 150)
        )
        self.return_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100,
            300, 60, "Return", RED, (255, 150, 150)
        )

        self.selected_skin = None  # Хранит путь к выбранному скину
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                    if self.skin1_rect.collidepoint(mouse_pos):
                        self.selected_skin = "assets/images/test_survivor.png"
                    elif self.skin2_rect.collidepoint(mouse_pos):
                        self.selected_skin = "assets/images/test_survivor_v2.png"

            self.start_button.check_hover(mouse_pos)
            self.return_button.check_hover(mouse_pos)

            if self.start_button.is_clicked(mouse_pos, mouse_click) and self.selected_skin:
                return self.selected_skin
            elif self.return_button.is_clicked(mouse_pos, mouse_click):
                return None

            self.screen.fill((40, 45, 50))

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            title = self.font.render("Select Your Character", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

            pygame.draw.rect(self.screen,
                             self.color_active if self.selected_skin == "assets/images/test_survivor.png" else self.color_passive,
                             self.skin1_border, 2, border_radius=10)
            pygame.draw.rect(self.screen,
                             self.color_active if self.selected_skin == "assets/images/test_survivor_v2.png" else self.color_passive,
                             self.skin2_border, 2, border_radius=10)

            self.screen.blit(self.skin1, self.skin1_rect)
            self.screen.blit(self.skin2, self.skin2_rect)

            skin1_label = self.small_font.render("Kukulyanskiy Raman", True, WHITE)
            skin2_label = self.small_font.render("Paniavin Alexander", True, WHITE)
            self.screen.blit(skin1_label,
                             (SCREEN_WIDTH // 4 - skin1_label.get_width() // 2, self.skin1_rect.bottom + 10))
            self.screen.blit(skin2_label,
                             (3 * SCREEN_WIDTH // 4 - skin2_label.get_width() // 2, self.skin2_rect.bottom + 10))

            self.start_button.draw(self.screen)
            self.return_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return None