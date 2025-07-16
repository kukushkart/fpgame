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
            self.skin = pygame.image.load("assets/images/pixel_pers_static.png").convert_alpha()
        except Exception as e:
            print(f"Cannot load character skins: {e}. Using fallback.")
            self.skin = pygame.Surface((120, 120), pygame.SRCALPHA)
            pygame.draw.circle(self.skin, (255, 0, 0), (60, 60), 60)
        self.skin = pygame.transform.smoothscale(self.skin, (120, 120))
        self.skin_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 60, 120, 120)
        self.skin_border = pygame.Rect(SCREEN_WIDTH // 2 - 65, SCREEN_HEIGHT // 2 - 65, 130, 130)
        self.start_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 170,
            300, 60, "Start The Game", GREEN, (150, 255, 150)
        )
        self.return_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100,
            300, 60, "Return", RED, (255, 150, 150)
        )
        self.selected_skin = "assets/images/pixel_pers_static.png"
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
                    if self.skin_rect.collidepoint(mouse_pos):
                        self.selected_skin = "assets/images/pixel_pers_static.png"
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
            pygame.draw.rect(self.screen, self.color_active, self.skin_border, 2, border_radius=10)
            self.screen.blit(self.skin, self.skin_rect)
            skin_label = self.small_font.render("Your Character", True, WHITE)
            self.screen.blit(skin_label,
                             (SCREEN_WIDTH // 2 - skin_label.get_width() // 2, self.skin_rect.bottom + 10))
            self.start_button.draw(self.screen)
            self.return_button.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        return None