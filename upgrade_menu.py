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
            SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100,
            300, 60,
            "Continue the day", GREEN, (150, 255, 150)
        )

        self.upgrades = [
            {"name": "Strength", "price": 200, "description": "+20% damage"},
            {"name": "Speed", "price": 200, "description": "+15% speed"},
            {"name": "Health", "price": 250, "description": "+50 HP"},
            {"name": "Rate of fire", "price": 300, "description": "-25% delay"},
            {"name": "Ammo capacity", "price": 300, "description": "+5 bullets"},
            {"name": "Micro-Uzi", "price": 800, "description": "Funny thing"},
            {"name": "Shotgun", "price": 1100, "description": "Good at close range"},
            {"name": "M1 garand", "price": 1700, "description": "Killer thing"},
            {"name": "M4", "price": 1400, "description": "Good one"}
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
            if self.continue_button.is_clicked(mouse_pos, mouse_click):
                return "resume"

            for i, button in enumerate(self.upgrade_buttons):
                button.check_hover(mouse_pos)
                upgrade_name = self.upgrades[i]["name"]

                # Особый случай для Ammo capacity
                if upgrade_name == "Ammo capacity" and self.player.ammo_capacity_bought:
                    button.color = (50, 50, 50)  # Серый цвет
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

            pygame.display.flip()
            self.clock.tick(60)

        return "resume"