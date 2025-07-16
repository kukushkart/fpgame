import pygame
from config import *
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius = 10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius = 10)
        if not pygame.font.get_init():
            pygame.font.init()
        font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        text_surface = font.render(self.text, True, WHITE)
        shadow_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click
def draw_menu(screen, buttons):
    if not pygame.font.get_init():
        pygame.font.init()
    title_font = pygame.font.Font(FONT_NAME, FONT_SIZE + 20)
    title_text = title_font.render("Last Breath", True, WHITE)
    title_shadow = title_font.render("Last Breath", True, BLACK)
    title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
    title_y = 100
    screen.blit(title_shadow, (title_x + 3, title_y + 3))
    screen.blit(title_text, (title_x, title_y))
    for button in buttons:
        button.draw(screen)
