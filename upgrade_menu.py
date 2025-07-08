import pygame
from config import *
from ui import Button


class UpgradeMenu:
    def __init__(self, screen, money):
        self.screen = screen
        self.money = money
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
                SCREEN_WIDTH // 2 - 400 + col * 270,
                200 + row * 150,
                250, 120,
                f"{upgrade['name']}\n{upgrade['price']}$",
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
                return "continue"

            for i, button in enumerate(self.upgrade_buttons):
                button.check_hover(mouse_pos)
                if button.is_clicked(mouse_pos, mouse_click):
                    if self.money >= self.upgrades[i]["price"]:
                        self.money -= self.upgrades[i]["price"]
                        print(f"Already bought: {self.upgrades[i]['name']}")

            self.screen.fill((30, 30, 40))

            title = self.font_large.render("Shop", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            money_text = self.font_medium.render(f"Money: {self.money}$", True, (255, 215, 0))
            self.screen.blit(money_text, (SCREEN_WIDTH // 2 - money_text.get_width() // 2, 120))

            for i, button in enumerate(self.upgrade_buttons):
                button.draw(self.screen)

                desc = self.font_small.render(self.upgrades[i]["description"], True, (200, 200, 200))
                self.screen.blit(desc, (
                    button.rect.centerx - desc.get_width() // 2,
                    button.rect.centery + 30
                ))

            self.continue_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return "continue"