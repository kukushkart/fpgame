import pygame
import os
from config import *
from ui import Button


class RecordsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE - 10)
        self.small_font = pygame.font.Font(FONT_NAME, FONT_SIZE - 20)

        self.back_button = Button(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 70, 100, 50, "Back", RED, (255, 150, 150))
        self.clear_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50, "Clear Records", GRAY,
                                   (200, 200, 200))

        self.records_file = "records.dat"
        self.records = self.load_records()

    def load_records(self):
        if not os.path.exists(self.records_file):
            return []

        try:
            with open(self.records_file, "r") as f:
                records = []
                for line in f.readlines():
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        records.append({
                            "name": parts[0],
                            "day": int(parts[1]),
                            "wave": int(parts[2]),
                            "money": int(parts[3])
                        })
                records.sort(key=lambda x: (-x["day"], -x["wave"], -x["money"]))
                return records[:10]
        except:
            return []

    def save_records(self):
        with open(self.records_file, "w") as f:
            for record in self.records:
                f.write(f"{record['name']},{record['day']},{record['wave']},{record['money']}\n")

    def add_record(self, name, day, wave, money):
        if not name:
            name = "Unknown"
        self.records.append({
            "name": name,
            "day": day,
            "wave": wave,
            "money": money
        })
        self.records.sort(key=lambda x: (-x["day"], -x["wave"], -x["money"]))
        self.records = self.records[:10]
        self.save_records()

    def clear_records(self):
        self.records = []
        if os.path.exists(self.records_file):
            os.remove(self.records_file)

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
                    return True

            self.back_button.check_hover(mouse_pos)
            self.clear_button.check_hover(mouse_pos)

            if self.back_button.is_clicked(mouse_pos, mouse_click):
                return True
            if self.clear_button.is_clicked(mouse_pos, mouse_click):
                self.clear_records()

            self.screen.fill((40, 45, 50))

            title = self.font.render("Top 10 Records", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

            headers = ["Rank", "Name", "Day", "Wave", "Money"]
            header_x = [50, 150, 300, 450, 600]

            for i, header in enumerate(headers):
                text = self.small_font.render(header, True, (255, 215, 0))  # Золотой цвет
                self.screen.blit(text, (header_x[i], 150))

            for i, record in enumerate(self.records):
                if i >= 10:
                    break

                y_pos = 200 + i * 40

                rank_text = self.small_font.render(f"{i + 1}.", True, WHITE)
                self.screen.blit(rank_text, (header_x[0], y_pos))

                name_text = self.small_font.render(record["name"][:12], True, WHITE)  # Обрезаем длинные имена
                self.screen.blit(name_text, (header_x[1], y_pos))

                day_text = self.small_font.render(str(record["day"]), True, WHITE)
                wave_text = self.small_font.render(str(record["wave"]), True, WHITE)
                money_text = self.small_font.render(str(record["money"]), True, (0, 255, 0))

                self.screen.blit(day_text, (header_x[2], y_pos))
                self.screen.blit(wave_text, (header_x[3], y_pos))
                self.screen.blit(money_text, (header_x[4], y_pos))

            self.back_button.draw(self.screen)
            self.clear_button.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

        return True