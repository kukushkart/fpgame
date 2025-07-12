import pygame
import os
from config import *
from ui import Button
class InfoScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(FONT_NAME, FONT_SIZE)
        self.font_medium = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.font_small = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)
        self.current_section = "main"
        self.zombie_scroll_offset = 0
        self.back_button = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 50, "Back", RED, (255, 150, 150))
        self.zombie_info = [
            {"image": "з2пр.png", "name": "Green zombie","description": "Classical zombie.\nMedium speed and health.\nMinimal damage."},
            {"image": "с2пр.png", "name": "Lime zombie","description": "Classical zombie.\nMedium speed and health.\nMinimal damage."},
            {"image": "л2пр.png", "name": "Violet zombie","description": "Unknown zombie.\nrandom???\nrandom???"},
            {"image": "гт2пр.png", "name": "Blue zombie", "description": "Smart zombie\n.Large Detection Radius, Medium speed and health\nMedium damage."},
            {"image": "к2пр.png", "name": "Red zombie", "description": "Strong zombie.\nLess speed, more health.\nMedium damage."},
            {"image": "ф2пр.png", "name": "Purple zombie", "description": "Strong zombie\nLess speed, more health.\nMedium damage."},
            {"image": "ц2пр.png", "name": "Cyan zombie", "description": "Smart zombie\n.Large Detection Radius, Medium speed and health\nMedium damage."},
            {"image": "шл2пр.png", "name": "Zombie with a hat", "description": "Fast zombie.\nMore speed, less health.\nMaximum damage."}
        ]
        self.zombie_images = {}
        for zombie in self.zombie_info:
            try:
                image_path = os.path.join("assets", "images", zombie["image"])
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (80, 80))
                self.zombie_images[zombie["image"]] = image
            except Exception as e:
                print(f"Invalid attempt of downloading image {zombie['image']}: {e}")
                placeholder = pygame.Surface((80, 80), pygame.SRCALPHA)
                pygame.draw.rect(placeholder, (128, 128, 128), (0, 0, 80, 80))
                self.zombie_images[zombie["image"]] = placeholder
        button_width = 200
        button_height = 60
        button_spacing = 20
        start_y = 200
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        self.info_buttons = [
            Button(center_x, start_y, button_width, button_height, "Controls", (70, 130, 180), (100, 150, 200)),
            Button(center_x, start_y + (button_height + button_spacing) * 1, button_width, button_height, "About Zombie", (70, 130, 180), (100, 150, 200)),
            Button(center_x, start_y + (button_height + button_spacing) * 2, button_width, button_height, "About Game", (70, 130, 180), (100, 150, 200)),
            Button(center_x, start_y + (button_height + button_spacing) * 3, button_width, button_height, "Authors", (70, 130, 180), (100, 150, 200))
        ]
        self.sections = {
            "controls": [
                "Game Controls:",
                "",
                "WASD or arrows - movement",
                "Space - shooting",
                "ESC/p - pause",
                "SHIFT - change direction",
                "H - use medkit",
                "R - reload weapon",
                "M - open upgrade menu"
            ],
            "about_game": [
                "About Game:",
                "",
                "Information about the game will be added here..."
            ],
            "authors": [
                "Authors:",
                "",
                "Kukulyansky Raman",
                "Paniavin Alexander",
                "",
                "Version 1.0",
                "2025 Zombie Survival Game"
            ]
        }
    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.current_section == "main":
                        return True
                    else:
                        self.current_section = "main"
                        self.zombie_scroll_offset = 0
                if event.type == pygame.MOUSEWHEEL and self.current_section == "about_zombie":
                    scroll_speed = 30
                    self.zombie_scroll_offset -= event.y * scroll_speed
                    max_scroll = max(0, len(self.zombie_info) * 120 - (SCREEN_HEIGHT - 200))
                    self.zombie_scroll_offset = max(0, min(self.zombie_scroll_offset, max_scroll))
            self.back_button.check_hover(mouse_pos)
            if self.back_button.is_clicked(mouse_pos, mouse_click):
                if self.current_section == "main":
                    return True
                else:
                    self.current_section = "main"
            if self.current_section == "main":
                for button in self.info_buttons:
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, mouse_click):
                        if button.text == "Controls":
                            self.current_section = "controls"
                        elif button.text == "About Zombie":
                            self.current_section = "about_zombie"
                        elif button.text == "About Game":
                            self.current_section = "about_game"
                        elif button.text == "Authors":
                            self.current_section = "authors"
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        return True
    def draw(self):
        self.screen.fill((40, 45, 50))  
        if self.current_section == "main":
            title = self.font_large.render("Info", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
            for button in self.info_buttons:
                button.draw(self.screen)
        elif self.current_section == "about_zombie":
            title = self.font_large.render("About Zombies", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
            start_y = 120
            zombie_height = 123  
            for i, zombie in enumerate(self.zombie_info):
                y_pos = start_y + i * zombie_height - self.zombie_scroll_offset
                if y_pos < -zombie_height or y_pos > SCREEN_HEIGHT:
                    continue
                image = self.zombie_images.get(zombie["image"])
                if image:
                    self.screen.blit(image, (50, y_pos))
                name_text = self.font_medium.render(zombie["name"], True, WHITE)
                self.screen.blit(name_text, (150, y_pos))
                description_lines = zombie["description"].split("\n")
                for j, desc_line in enumerate(description_lines):
                    desc_text = self.font_small.render(desc_line, True, (200, 200, 200))
                    self.screen.blit(desc_text, (150, y_pos + 33 + j * 23))  
                if i < len(self.zombie_info) - 1:
                    pygame.draw.line(self.screen, (80, 80, 80), 
                                   (50, y_pos + zombie_height - 10), 
                                   (SCREEN_WIDTH - 50, y_pos + zombie_height - 10), 2)
        else:
            section_title = self.current_section.replace("_", " ").title()
            title = self.font_large.render(section_title, True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
            lines = self.sections.get(self.current_section, [])
            for i, line in enumerate(lines):
                if i == 0:  
                    text = self.font_medium.render(line, True, WHITE)
                else:
                    text = self.font_small.render(line, True, (200, 200, 200))
                self.screen.blit(text, (50, 120 + i * 35))
        self.back_button.draw(self.screen)
