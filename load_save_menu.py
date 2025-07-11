import pygame
from config import *
from ui import Button
from save_manager import SaveManager
class LoadSaveMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)
        self.save_manager = SaveManager()
        self.saves = self.save_manager.get_all_saves()[:6]
        self.selected_save_index = -1
        self.scroll_offset = 0
        self.max_visible_saves = 4
        self.back_button = Button(
            50, SCREEN_HEIGHT - 70,
            120, 50,
            "Back", RED, (255, 150, 150)
        )
        button_width = 140
        button_height = 50
        button_spacing = 20
        total_width = button_width * 2 + button_spacing
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        button_y = SCREEN_HEIGHT - 70
        self.start_button = Button(
            start_x, button_y,
            button_width, button_height,
            "Start", GREEN, (150, 255, 150)
        )
        self.delete_button = Button(
            start_x + button_width + button_spacing, button_y,
            button_width, button_height,
            "Delete", (180, 70, 70), (200, 100, 100)
        )
        self.save_buttons = []
        self.create_save_buttons()
    def create_save_buttons(self):
        self.save_buttons = []
        for i, save in enumerate(self.saves):
            if i == self.selected_save_index:
                color = (100, 150, 100)
                hover_color = (120, 180, 120)
            else:
                color = (70, 70, 70)
                hover_color = (100, 100, 100)
            button = Button(
                SCREEN_WIDTH // 2 - 400, 150 + i * 120,
                800, 100,
                save["save_name"], color, hover_color
            )
            self.save_buttons.append(button)
    def refresh_saves(self):
        self.saves = self.save_manager.get_all_saves()[:6]
        self.selected_save_index = -1
        self.create_save_buttons()
    def draw_save_info(self, save, button_rect):
        info_text = f"Player: {save['player_name']} | Day: {save['day']} | Wave: {save['wave']} | Money: {save['money']}$"
        info_surface = self.font_small.render(info_text, True, (200, 200, 200))
        info_rect = info_surface.get_rect()
        info_rect.centerx = button_rect.centerx
        info_rect.top = button_rect.centery + 10
        self.screen.blit(info_surface, info_rect)
    def handle_scroll(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset = max(0, min(self.scroll_offset - event.y * 30, 
                                          max(0, len(self.saves) - self.max_visible_saves) * 120))
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                self.handle_scroll(event)
            self.back_button.check_hover(mouse_pos)
            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return None
            for i, button in enumerate(self.save_buttons):
                if i >= len(self.saves):
                    break
                button.rect.y = 150 + i * 120 - self.scroll_offset
                if button.rect.bottom < 100 or button.rect.top > SCREEN_HEIGHT - 120:
                    continue
                button.check_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    self.selected_save_index = i
                    self.create_save_buttons()
            if self.selected_save_index >= 0:
                self.start_button.check_hover(mouse_pos)
                if self.start_button.is_clicked(mouse_pos, mouse_click):
                    return self.saves[self.selected_save_index]["filename"]
                self.delete_button.check_hover(mouse_pos)
                if self.delete_button.is_clicked(mouse_pos, mouse_click):
                    filename = self.saves[self.selected_save_index]["filename"]
                    if self.save_manager.delete_save_by_filename(filename):
                        self.refresh_saves()
            self.screen.fill((40, 45, 50))
            title = self.font_large.render("Load Game", True, WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(title, title_rect)
            if not self.saves:
                no_saves_text = self.font_medium.render("No save files found", True, (200, 200, 200))
                no_saves_rect = no_saves_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(no_saves_text, no_saves_rect)
            else:
                for i, button in enumerate(self.save_buttons):
                    if i >= len(self.saves):
                        break
                    if button.rect.bottom < 100 or button.rect.top > SCREEN_HEIGHT - 120:
                        continue
                    button.draw(self.screen)
                    self.draw_save_info(self.saves[i], button.rect)
                if len(self.saves) > self.max_visible_saves:
                    scroll_height = int((self.max_visible_saves / len(self.saves)) * 400)
                    scroll_pos = int((self.scroll_offset / (len(self.saves) - self.max_visible_saves)) / 120 * (400 - scroll_height))
                    pygame.draw.rect(self.screen, (100, 100, 100), 
                                   (SCREEN_WIDTH - 30, 150, 20, 400))
                    pygame.draw.rect(self.screen, (200, 200, 200), 
                                   (SCREEN_WIDTH - 30, 150 + scroll_pos, 20, scroll_height))
            self.back_button.draw(self.screen)
            if self.selected_save_index >= 0:
                self.start_button.draw(self.screen)
                self.delete_button.draw(self.screen)
                selected_text = self.font_small.render("Selected: " + self.saves[self.selected_save_index]["save_name"], True, (150, 255, 150))
                selected_rect = selected_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))
                self.screen.blit(selected_text, selected_rect)
            pygame.display.flip()
            self.clock.tick(60)
        return None
