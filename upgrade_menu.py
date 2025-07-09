import pygame
from config import *
from ui import Button


class UpgradeMenu:
    def __init__(self, screen, money, player):
        self.screen = screen
        self.money = money
        self.player = player
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 15)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 25)

        self.continue_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 70,
            300, 60,
            "Next day", GREEN, (150, 255, 150)
        )

        self.main_menu_button = Button(
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 140,
            300, 60,
            "Back to Main Menu", RED, (255, 150, 150)
        )

        self.upgrades = [
            {"name": "Strength", "price": 250, "description": "+5 damage"},
            {"name": "Speed", "price": 300, "description": "+5 speed"},
            {"name": "Health", "price": 200, "description": "+10 max HP"},
            {"name": "Rate of fire", "price": 250, "description": "-2 delay"},
            {"name": "Ammo capacity", "price": 300, "description": "+15 bullets"},
            {"name": "Medkit", "price": 200, "description": "+1 medkit"},
            {"name": "Reload speed", "price": 250, "description": "-0.2 reload time"},
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

            if self.continue_button.is_clicked(mouse_pos, mouse_click):
                return "resume"
            if self.main_menu_button.is_clicked(mouse_pos, mouse_click):
                return "main_menu"

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
                    if self.money >= self.upgrades[i]["price"]:
                        if self.player.apply_upgrade(upgrade_name):  # Пробуем применить улучшение
                            self.money -= self.upgrades[i]["price"]

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

            self.continue_button.draw(self.screen)
            self.main_menu_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return "resume"