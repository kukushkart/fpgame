import pygame
from config import *
from ui import Button
from save_manager import SaveManager
from manage_saves_popup import ManageSavesPopup


class SavePopup:
    def __init__(self, screen, default_name=""):
        self.screen = screen
        self.default_name = default_name
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE - 5)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 15)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 25)

        self.save_manager = SaveManager()
        self.can_save = self.save_manager.can_create_save()

        self.background = screen.copy()

        self.popup_width = 450
        self.popup_height = 300 if not self.can_save else 250
        self.popup_x = SCREEN_WIDTH // 2 - self.popup_width // 2
        self.popup_y = SCREEN_HEIGHT // 2 - self.popup_height // 2

        self.input_text = default_name
        self.input_active = True
        self.cursor_visible = True
        self.cursor_timer = 0

        save_color = GREEN if self.can_save else (100, 100, 100)
        save_hover_color = (150, 255, 150) if self.can_save else (120, 120, 120)
        
        self.save_button = Button(
            self.popup_x + 50, self.popup_y + self.popup_height - 80,
            150, 50, "Save", save_color, save_hover_color
        )
        
        self.cancel_button = Button(
            self.popup_x + 250, self.popup_y + self.popup_height - 80,
            150, 50, "Cancel", RED, (255, 150, 150)
        )
    
    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
                    elif event.key == pygame.K_RETURN:
                        if self.input_text.strip():
                            return self.input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isprintable() and len(self.input_text) < 30:
                            self.input_text += event.unicode
            
            self.save_button.check_hover(mouse_pos)
            self.cancel_button.check_hover(mouse_pos)
            
            if self.cancel_button.is_clicked(mouse_pos, mouse_click):
                return None
            
            if self.save_button.is_clicked(mouse_pos, mouse_click):
                if self.can_save and self.input_text.strip():
                    return self.input_text.strip()

            self.screen.blit(self.background, (0, 0))

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(self.popup_x, self.popup_y, self.popup_width, self.popup_height)
            pygame.draw.rect(self.screen, (60, 60, 70), popup_rect)
            pygame.draw.rect(self.screen, WHITE, popup_rect, 3)

            title_text = self.font_large.render("Save Game", True, WHITE)
            title_rect = title_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 40))
            self.screen.blit(title_text, title_rect)

            if self.can_save:
                hint_text = self.font_small.render("Enter save name:", True, (200, 200, 200))
                hint_rect = hint_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 80))
                self.screen.blit(hint_text, hint_rect)

                input_rect = pygame.Rect(self.popup_x + 50, self.popup_y + 100, self.popup_width - 100, 40)
                pygame.draw.rect(self.screen, WHITE, input_rect)
                pygame.draw.rect(self.screen, BLACK, input_rect, 2)
            else:
                limit_text1 = self.font_medium.render("Save limit reached!", True, RED)
                limit_rect1 = limit_text1.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 80))
                self.screen.blit(limit_text1, limit_rect1)
                
                limit_text2 = self.font_small.render("You can have maximum 6 saves.", True, (200, 200, 200))
                limit_rect2 = limit_text2.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 110))
                self.screen.blit(limit_text2, limit_rect2)
                
                limit_text3 = self.font_small.render("Please delete some saves first.", True, (200, 200, 200))
                limit_rect3 = limit_text3.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 140))
                self.screen.blit(limit_text3, limit_rect3)

            if self.can_save:
                input_surface = self.font_medium.render(self.input_text, True, BLACK)
                input_text_rect = input_surface.get_rect()
                input_text_rect.left = input_rect.left + 5
                input_text_rect.centery = input_rect.centery
                self.screen.blit(input_surface, input_text_rect)

                if self.cursor_visible:
                    cursor_x = input_text_rect.right + 2
                    cursor_y1 = input_rect.top + 5
                    cursor_y2 = input_rect.bottom - 5
                    pygame.draw.line(self.screen, BLACK, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2)

            self.save_button.draw(self.screen)
            self.cancel_button.draw(self.screen)
            
            pygame.display.flip()
        
        return None


class UpgradePopup:
    def __init__(self, screen, upgrade_info, money):
        self.screen = screen
        self.upgrade_info = upgrade_info
        self.money = money
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE - 5)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 15)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 25)

        self.background = screen.copy()

        self.popup_width = 400
        self.popup_height = 300
        self.popup_x = SCREEN_WIDTH // 2 - self.popup_width // 2
        self.popup_y = SCREEN_HEIGHT // 2 - self.popup_height // 2

        can_buy = money >= upgrade_info["price"] and upgrade_info["name"] != "Coming soon"

        if can_buy:
            buy_color = GREEN
            buy_hover_color = (150, 255, 150)
        else:
            buy_color = (100, 100, 100)
            buy_hover_color = (120, 120, 120)

        self.buy_button = Button(
            self.popup_x + 50, self.popup_y + self.popup_height - 80,
            130, 50, "Buy", buy_color, buy_hover_color
        )

        self.back_button = Button(
            self.popup_x + 220, self.popup_y + self.popup_height - 80,
            130, 50, "Back", RED, (255, 150, 150)
        )

        self.can_buy = can_buy

    def run(self):
        running = True

        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "back"

            self.buy_button.check_hover(mouse_pos)
            self.back_button.check_hover(mouse_pos)

            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return "back"

            if self.buy_button.is_clicked(mouse_pos, mouse_click) and self.can_buy:
                return "buy"

            self.screen.blit(self.background, (0, 0))

            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            popup_rect = pygame.Rect(self.popup_x, self.popup_y, self.popup_width, self.popup_height)
            pygame.draw.rect(self.screen, (60, 60, 70), popup_rect)
            pygame.draw.rect(self.screen, WHITE, popup_rect, 3)

            title_text = self.font_large.render(self.upgrade_info["name"], True, WHITE)
            title_rect = title_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 40))
            self.screen.blit(title_text, title_rect)

            price_text = self.font_medium.render(f"Price: {self.upgrade_info['price']}$", True, (255, 215, 0))
            price_rect = price_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 80))
            self.screen.blit(price_text, price_rect)

            desc_text = self.font_medium.render(self.upgrade_info["description"], True, (200, 200, 200))
            desc_rect = desc_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 120))
            self.screen.blit(desc_text, desc_rect)

            money_text = self.font_small.render(f"Your money: {self.money}$", True, (255, 215, 0))
            money_rect = money_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 160))
            self.screen.blit(money_text, money_rect)

            if not self.can_buy and self.upgrade_info["name"] != "Coming soon":
                warning_text = self.font_small.render("Not enough money!", True, RED)
                warning_rect = warning_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 190))
                self.screen.blit(warning_text, warning_rect)

            if self.upgrade_info["name"] == "Coming soon":
                coming_text = self.font_small.render("This upgrade is not available yet", True, GRAY)
                coming_rect = coming_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 180))
                self.screen.blit(coming_text, coming_rect)

            self.buy_button.draw(self.screen)
            self.back_button.draw(self.screen)

            pygame.display.flip()

        return "back"


class UpgradeMenu:
    def __init__(self, screen, money, player, day=1, wave=1, player_name=""):
        self.screen = screen
        self.money = money
        self.player = player
        self.day = day
        self.wave = wave
        self.player_name = player_name
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 15)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 25)
        
        self.save_manager = SaveManager()

        button_width = 180
        button_height = 60
        button_spacing = 20
        total_width = button_width * 3 + button_spacing * 2
        start_x = SCREEN_WIDTH // 2 - total_width // 2
        button_y = SCREEN_HEIGHT - 70
        
        self.main_menu_button = Button(
            start_x, button_y,
            button_width, button_height,
            "Main Menu", RED, (255, 150, 150)
        )
        
        self.save_button = Button(
            start_x + button_width + button_spacing, button_y,
            button_width, button_height,
            "Save Game", (70, 130, 180), (100, 150, 200)
        )
        
        self.continue_button = Button(
            start_x + (button_width + button_spacing) * 2, button_y,
            button_width, button_height,
            "Next Day", GREEN, (150, 255, 150)
        )

        self.upgrades = [
            {"name": "Strength", "price": 250, "description": "+5 damage"},
            {"name": "Speed", "price": 300, "description": "+5 speed"},
            {"name": "Health", "price": 200, "description": "+10 max HP"},
            {"name": "Rate of fire", "price": 250, "description": "-0.2s delay"},
            {"name": "Ammo capacity", "price": 300, "description": "+15 bullets"},
            {"name": "Medkit", "price": 200, "description": "+1 medkit"},
            {"name": "Reload speed", "price": 250, "description": "-0.2s reload time"},
            {"name": "Coming soon", "price": 0, "description": "*******"},
            {"name": "Coming soon", "price": 0, "description": "*******"}
        ]

        self.upgrade_buttons = []
        for i, upgrade in enumerate(self.upgrades):
            row = i // 3
            col = i % 3
            btn = Button(
                SCREEN_WIDTH // 2 - 410 + col * 280,
                200 + row * 160,
                265, 135,
                upgrade['name'],
                (70, 70, 70), (100, 100, 100)
            )
            self.upgrade_buttons.append(btn)

    def _draw_player_stats(self):
        stats_font = pygame.font.Font(FONT_NAME, 30)

        left_x = 120
        y_start = 40
        line_height = 40

        left_stats = [
            f"Strength: {self.player.damage}",
            f"Speed: {self.player.speed}",
            f"Max Health: {self.player.max_health}",
            f"Current Health: {self.player.health}",
            f"Medkits: {self.player.medkits}"
        ]

        for i, stat in enumerate(left_stats):
            stat_text = stats_font.render(stat, True, WHITE)
            self.screen.blit(stat_text, (left_x, y_start + i * line_height))

        right_x = SCREEN_WIDTH - 310

        right_stats = [
            f"Rate of fire: {self.player.shoot_delay / 10:.1f}s",
            f"Ammo capacity: {self.player.magazine_size}",
            f"Reload speed: {self.player.reload_time:.1f}s"
        ]

        for i, stat in enumerate(right_stats):
            stat_text = stats_font.render(stat, True, WHITE)
            self.screen.blit(stat_text, (right_x, y_start + i * line_height))

    def draw_main_screen(self):
        self.screen.fill((30, 30, 40))

        self._draw_player_stats()

        title = self.font_large.render("Shop", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

        money_text = self.font_medium.render(f"Money: {self.money}$", True, (255, 215, 0))
        self.screen.blit(money_text, (SCREEN_WIDTH // 2 - money_text.get_width() // 2, 120))

        for i, button in enumerate(self.upgrade_buttons):
            button.draw(self.screen)

            price_text = self.font_small.render(f"{self.upgrades[i]['price']}$", True, (255, 215, 0))
            self.screen.blit(price_text, (
                button.rect.centerx - price_text.get_width() // 2,
                button.rect.centery + 12
            ))

            desc = self.font_small.render(self.upgrades[i]["description"], True, (200, 200, 200))
            self.screen.blit(desc, (
                button.rect.centerx - desc.get_width() // 2,
                button.rect.centery + 40
            ))

        self.main_menu_button.draw(self.screen)
        self.save_button.draw(self.screen)
        self.continue_button.draw(self.screen)

    def run(self):
        paused = True

        while paused:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                    return "resume"

            self.continue_button.check_hover(mouse_pos)
            self.main_menu_button.check_hover(mouse_pos)
            self.save_button.check_hover(mouse_pos)

            if self.continue_button.is_clicked(mouse_pos, mouse_click):
                return "resume"
            if self.main_menu_button.is_clicked(mouse_pos, mouse_click):
                return "main_menu"
            if self.save_button.is_clicked(mouse_pos, mouse_click):
                self.draw_main_screen()
                pygame.display.flip()

                # Проверяем лимит сохранений
                if not self.save_manager.can_create_save():
                    # Показываем меню управления сохранениями
                    manage_saves_popup = ManageSavesPopup(self.screen, self.save_manager)
                    result = manage_saves_popup.run()
                    
                    if result != "continue":
                        continue  # Пользователь отменил или закрыл меню

                from datetime import datetime
                default_name = f"{self.player_name}_Day{self.day}_Wave{self.wave}_{datetime.now().strftime('%m%d_%H%M')}"

                save_popup = SavePopup(self.screen, default_name)
                save_name = save_popup.run()
                
                if save_name:
                    success = self.save_manager.save_game(self.player, self.day, self.wave, self.money, self.player_name, save_name)
                    if success:
                        print(f"Game saved successfully as '{save_name}'!")
                    else:
                        print("Failed to save game!")

            for i, button in enumerate(self.upgrade_buttons):
                button.check_hover(mouse_pos)
                upgrade_name = self.upgrades[i]["name"]

                if upgrade_name == "Ammo capacity" and self.player.ammo_capacity_bought:
                    button.color = (50, 50, 50)
                    button.hover_color = (50, 50, 50)
                    continue
                else:
                    button.color = (70, 70, 70)
                    button.hover_color = (100, 100, 100)

                if button.is_clicked(mouse_pos, mouse_click):
                    self.draw_main_screen()
                    pygame.display.flip()

                    popup = UpgradePopup(self.screen, self.upgrades[i], self.money)
                    result = popup.run()

                    if result == "quit":
                        return "quit"
                    elif result == "buy":
                        if self.player.apply_upgrade(upgrade_name):
                            self.money -= self.upgrades[i]["price"]
                            self.draw_main_screen()
                            pygame.display.flip()

            self.draw_main_screen()
            pygame.display.flip()
            self.clock.tick(60)

        return "resume"