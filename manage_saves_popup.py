import pygame
from config import *
from ui import Button
class ManageSavesPopup:
    def __init__(self, screen, save_manager):
        self.screen = screen
        self.save_manager = save_manager
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)
        self.saves = self.save_manager.get_all_saves()
        self.selected_save_index = -1
        self.scroll_offset = 0
        self.max_visible_saves = 3  
        self.save_area_height = 360  
        self.save_area_top = 150    
        self.back_button = Button(
            50, SCREEN_HEIGHT - 70,
            120, 50,
            "Back", RED, (255, 150, 150)
        )
        button_width = 140
        button_height = 50
        button_spacing = 30
        total_width = button_width * 2 + button_spacing
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        button_y = SCREEN_HEIGHT - 70
        self.delete_button = Button(
            start_x, button_y,
            button_width, button_height,
            "Delete", (180, 70, 70), (200, 100, 100)
        )
        self.continue_button = Button(
            start_x + button_width + button_spacing, button_y,
            button_width, button_height,
            "Continue", GREEN, (150, 255, 150)
        )
        self.save_buttons = []
        self.create_save_buttons()
    def create_save_buttons(self):
        self.save_buttons = []
        for i, save in enumerate(self.saves):
            color = (70, 70, 70)
            hover_color = (100, 100, 100)
            button = Button(
                SCREEN_WIDTH // 2 - 400, self.save_area_top + i * 120,
                800, 100,
                save["save_name"], color, hover_color
            )
            self.save_buttons.append(button)
    def handle_scroll(self, event):
        if event.type == pygame.MOUSEWHEEL:
            max_scroll = max(0, (len(self.saves) - self.max_visible_saves) * 120)
            self.scroll_offset = max(0, min(self.scroll_offset - event.y * 30, max_scroll))
    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "exit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                self.handle_scroll(event)
            self.back_button.check_hover(mouse_pos)
            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return "exit"
            for i, button in enumerate(self.save_buttons):
                button.rect.y = self.save_area_top + i * 120 - self.scroll_offset
                if (button.rect.bottom < self.save_area_top or 
                    button.rect.top > self.save_area_top + self.save_area_height):
                    continue
                button.check_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    self.selected_save_index = i
            if self.selected_save_index != -1:
                self.delete_button.check_hover(mouse_pos)
                if self.delete_button.is_clicked(mouse_pos, mouse_click):
                    filename = self.saves[self.selected_save_index]["filename"]
                    self.save_manager.delete_save_by_filename(filename)
                    self.saves.pop(self.selected_save_index)
                    self.selected_save_index = -1
                    max_scroll = max(0, (len(self.saves) - self.max_visible_saves) * 120)
                    self.scroll_offset = min(self.scroll_offset, max_scroll)
                    self.create_save_buttons()
            if len(self.saves) < 6:
                self.continue_button.check_hover(mouse_pos)
                if self.continue_button.is_clicked(mouse_pos, mouse_click):
                    return "continue"
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return "exit"
    def draw(self):
        self.screen.fill((40, 45, 50))
        title = self.font_large.render("Manage Saves", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 43))
        self.screen.blit(title, title_rect)
        limit_text = self.font_medium.render(f"Save limit reached: {len(self.saves)}/6", True, (255, 150, 150))
        limit_rect = limit_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(limit_text, limit_rect)
        instruction_text = self.font_small.render("Select a save to delete, then click Delete to continue", True, (200, 200, 200))
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, 110))
        self.screen.blit(instruction_text, instruction_rect)
        save_area_rect = pygame.Rect(0, self.save_area_top, SCREEN_WIDTH, self.save_area_height)
        for i, button in enumerate(self.save_buttons):
            if (button.rect.bottom < self.save_area_top or 
                button.rect.top > self.save_area_top + self.save_area_height):
                continue
            if i == self.selected_save_index:
                button.color = (100, 50, 50)
                button.hover_color = (120, 70, 70)
            else:
                button.color = (70, 70, 70)
                button.hover_color = (100, 100, 100)
            button.draw(self.screen)
            save = self.saves[i]
            info_text = f"Player: {save['player_name']} | Day: {save['day']} | Wave: {save['wave']} | Money: {save['money']}$"
            info_surface = self.font_small.render(info_text, True, (200, 200, 200))
            info_rect = info_surface.get_rect()
            info_rect.centerx = button.rect.centerx
            info_rect.top = button.rect.centery + 10
            self.screen.blit(info_surface, info_rect)
        if len(self.saves) > self.max_visible_saves:
            scrollbar_height = self.save_area_height
            scrollbar_width = 20
            scrollbar_x = SCREEN_WIDTH - 30
            scrollbar_y = self.save_area_top
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height))
            scroll_ratio = self.max_visible_saves / len(self.saves)
            scroll_handle_height = int(scrollbar_height * scroll_ratio)
            max_scroll = max(0, (len(self.saves) - self.max_visible_saves) * 120)
            scroll_position = 0 if max_scroll == 0 else self.scroll_offset / max_scroll
            scroll_handle_y = scrollbar_y + int(scroll_position * (scrollbar_height - scroll_handle_height))
            pygame.draw.rect(self.screen, (200, 200, 200), 
                           (scrollbar_x, scroll_handle_y, scrollbar_width, scroll_handle_height))
        if self.selected_save_index != -1:
            self.delete_button.draw(self.screen)
        if len(self.saves) < 6:
            self.continue_button.draw(self.screen)
        else:
            cant_continue_text = self.font_small.render("Delete a save to continue", True, (255, 150, 150))
            cant_continue_rect = cant_continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
            self.screen.blit(cant_continue_text, cant_continue_rect)
        self.back_button.draw(self.screen)
