import pygame
import os
from config import *
from player import Player
from zombies import Zombie
from pause_menu import PauseMenu
from ui import Button
from upgrade_menu import UpgradeMenu
from records_menu import RecordsScreen
from wave_manager import WAVES_CONFIG
from bluezombie import BlueZombie

class BloodEffect:
    """
    Анимация брызг крови из трёх кадров.
    """

    def __init__(self, pos, frames, frame_time=0.08):
        self.pos = pos  # центр эффекта (x,y)
        self.frames = frames  # список Surface
        self.frame_time = frame_time
        self.timer = 0.0
        self.current = 0
        self.done = False

    def update(self, dt):
        if self.done:
            return
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer -= self.frame_time
            self.current += 1
            if self.current >= len(self.frames):
                self.done = True

    def draw(self, surface):
        if not self.done:
            img = self.frames[self.current]
            rect = img.get_rect(center=self.pos)
            surface.blit(img, rect)


class GameWindow:
    def __init__(self, screen, player_name="", skin="assets/images/test_survivor.png"):
        self.screen = screen
        self.player_name = player_name
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.player = Player(skin)  # Передаем skin в Player

        self.day = 1
        self.wave = 1
        self.money = 500
        self.paused = False

        self.background = self.load_background()

        self.zombies = []
        self.dying_zombies = []
        self.zombie_spawn_timer = 0

        self.debug_font = pygame.font.Font(None, 30)

        self.game_paused = False

        self.exit_button = Button(
            SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50,
            200, 60, "Exit", RED, (255, 150, 150)
        )

        self.blood_frames = []
        for i in (1, 2, 3):
            path = os.path.join("assets", "images", f"blood_frame_{i}.png")
            try:
                img = pygame.image.load(path).convert_alpha()
            except Exception as e:
                print(f"Cannot load {path}: {e}")
                img = pygame.Surface((20, 20), pygame.SRCALPHA)
                pygame.draw.circle(img, (200, 0, 0), (10, 10), 10)
            self.blood_frames.append(img)

        self.blood_effects = []

        self.current_wave = 0
        self.zombies_to_spawn = 0
        self.wave_timer = 0.0
        self.day_completed = False
        self.waves = WAVES_CONFIG.get(self.day, [])
        self.spawn_interval = 1.0

    def load_background(self):
        try:
            bg = pygame.image.load(GAME_BG_IMAGE_PATH).convert()
            return pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Invalid bg download attempt. Using standard bg")
            bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            bg.fill((50, 70, 90))
            pygame.draw.rect(bg, (80, 100, 60), (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
            return bg

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                if event.key == pygame.K_p:
                    self.toggle_pause()
                if event.key == pygame.K_h:
                    self.player.use_medkit()
                if event.key == pygame.K_RETURN and self.day_completed:
                    self.paused = True

        if self.game_over:
            self.exit_button.check_hover(mouse_pos)

            if self.exit_button.is_clicked(mouse_pos, mouse_click):
                records = RecordsScreen(self.screen)
                records.add_record(self.player_name, self.day, self.wave, self.money)
                self.running = False

    def show_upgrade_menu(self):
        menu = UpgradeMenu(self.screen, self.money, self.player)
        result = menu.run()
        self.money = menu.money

        if result == "quit" or result == "main_menu":
            records = RecordsScreen(self.screen)
            records.add_record(self.player_name, self.day, self.wave, self.money)
            return False
        return True

    def toggle_pause(self):
        self.game_paused = not self.game_paused

    def reset_game(self):
        self.game_over = False
        self.player = Player()  # Здесь skin не передаем, так как reset_game не вызывается после выбора скина
        self.zombies = []
        self.dying_zombies = []
        self.blood_effects = []
        self.zombie_spawn_timer = 0
        self.game_paused = False
        self.day = 1
        self.wave = 1
        self.money = 500
        self.paused = False
        self.current_wave = 0
        self.zombies_to_spawn = 0
        self.wave_timer = 0.0
        self.day_completed = False
        self.waves = WAVES_CONFIG.get(self.day, [])

    def handle_pause(self):
        if self.game_paused:
            pause_menu = PauseMenu(self.screen)
            result = pause_menu.run(self.background, self.player, self.zombies)

            if result == "quit":
                return False
            elif result == "resume":
                self.game_paused = False

        return True

    def spawn_and_update_zombies(self, dt):
        if self.day_completed or self.game_over:
            return

        if len(self.zombies) == 0 and self.zombies_to_spawn == 0 and self.current_wave < len(self.waves):
            self.wave_timer += dt
            wave = self.waves[self.current_wave]
            if self.wave_timer >= wave["delay"]:
                self.zombies_to_spawn = wave["zombie_count"]
                self.wave_timer = 0.0
                self.current_wave += 1
                self.wave = self.current_wave

        if self.zombies_to_spawn > 0:
            self.zombie_spawn_timer += dt
            if self.zombie_spawn_timer >= self.spawn_interval:
                frame_paths = [
                    "assets/images/гт1ле.png",
                    "assets/images/гт2ле.png",
                    "assets/images/гт3ле.png",
                ]
                self.zombies.append(
                    BlueZombie(self.screen, self.day,
                                   frame_paths=frame_paths,
                                   frame_time=0.12)
                )
                self.zombies_to_spawn -= 1
                self.zombie_spawn_timer = 0.0

        player_pos = self.player.rect.center
        for z in self.zombies[:]:
            z.move(player_pos, dt)
            if z.is_off_screen():
                self.zombies.remove(z)

        if self.current_wave >= len(self.waves) and len(self.zombies) == 0 and self.zombies_to_spawn == 0:
            self.day_completed = True

    def handle_collisions(self, dt):
        if self.game_over:
            return

        for zombie in self.zombies:
            if self.player.rect.colliderect(zombie.rect):
                if zombie.attack_timer > 0:
                    zombie.attack_timer -= dt
                else:
                    # Зомби атакует игрока
                    self.player.health -= zombie.damage
                    if self.player.health <= 0:
                        self.player.health = 0
                        self.game_over = True
                    self.player.damage_text = f"-{zombie.damage}"  # Устанавливаем текст урона
                    self.player.damage_timer = 1.0  # Устанавливаем таймер для текста

                    # Перезагрузка таймера атаки
                    zombie.attack_timer = zombie.attack_delay

    def handle_bullet_zombie_collisions(self):
        for bullet in self.player.bullets[:]:
            for z in self.zombies[:]:
                if bullet.rect.colliderect(z.rect):
                    z.health -= bullet.damage
                    self.player.bullets.remove(bullet)
                    eff = BloodEffect(z.rect.center, self.blood_frames)
                    self.blood_effects.append(eff)

                    if z.health <= 0:
                        # Проверяем, что зомби еще не в списке умирающих
                        already_dying = any(zombie == z for zombie, _ in self.dying_zombies)
                        if not already_dying:
                            self.dying_zombies.append((z, eff))
                        self.zombies.remove(z)
                        self.money += 10
                    break

    def update(self, dt):
        if not self.game_paused and not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.update(keys, dt)
            self.player.update_bullets()
            # Уменьшаем hurt_timer, если он больше 0
            # if hasattr(self, 'hurt_timer') and self.hurt_timer > 0:
            # self.hurt_timer -= dt

    def update_blood_effects(self, dt):
        for eff in self.blood_effects[:]:
            eff.update(dt)
            if eff.done:
                self.blood_effects.remove(eff)
                # удалить связанного зомби
                for pair in self.dying_zombies:
                    if pair[1] is eff:
                        self.dying_zombies.remove(pair)
                        break

    def draw_health_bar(self, x, y, width, height, current_health, max_health):
        border_rect = pygame.Rect(x - 2, y - 2, width + 4, height + 4)
        pygame.draw.rect(self.screen, BLACK, border_rect)

        red_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, RED, red_rect)

        if current_health > 0:
            green_width = int((current_health / max_health) * width)
            green_rect = pygame.Rect(x, y, green_width, height)
            pygame.draw.rect(self.screen, GREEN, green_rect)

        font = pygame.font.Font(FONT_NAME, 20)
        health_text = f"{current_health}/{max_health}"
        text_surface = font.render(health_text, True, WHITE)

        shadow_surface = font.render(health_text, True, BLACK)

        text_x = x + (width - text_surface.get_width()) // 2
        text_y = y + (height - text_surface.get_height()) // 2

        self.screen.blit(shadow_surface, (text_x + 1, text_y + 1))
        self.screen.blit(text_surface, (text_x, text_y))

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.player.draw(self.screen)
        for z in self.zombies:
            z.draw()

        for z, eff in self.dying_zombies:
            z.draw()
            eff.draw(self.screen)

        # Отрисовываем эффекты крови
        for eff in self.blood_effects:
            eff.draw(self.screen)

        font = pygame.font.Font(FONT_NAME, 30)
        pos_text = f"Pos: ({self.player.rect.x},{self.player.rect.y})"
        ammo_text = f"Ammo: {self.player.current_ammo}/{self.player.magazine_size}"
        reload_text = "Reloading..." if self.player.is_reloading else ""

        self.screen.blit(font.render(pos_text, True, WHITE), (10, 10))
        self.draw_health_bar(10, 50, 200, 30, self.player.health, self.player.max_health)
        self.screen.blit(font.render(ammo_text, True, WHITE), (10, 90))
        self.screen.blit(font.render(f"Medkits: {self.player.medkits} (H)", True, WHITE), (10, 120))
        self.screen.blit(font.render(reload_text, True, RED), (10, 150))

        self.player.draw_bullets(self.screen)

        day_wave_font = pygame.font.Font(FONT_NAME, 45)
        day_text = day_wave_font.render(f"Day: {self.day}", True, WHITE)
        wave_text = day_wave_font.render(f"Wave: {self.wave}", True, WHITE)

        self.screen.blit(day_text, (SCREEN_WIDTH // 2 - day_text.get_width() // 2, 20))
        self.screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 90))

        money_font = pygame.font.Font(FONT_NAME, 35)
        money_text = money_font.render(f"Money: {self.money}$", True, (255, 215, 0))
        self.screen.blit(money_text, (SCREEN_WIDTH - money_text.get_width() - 20, 20))

        if self.day_completed:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.Font(FONT_NAME, 50)
            text = font.render("Press Enter to continue", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            go_font = pygame.font.Font(FONT_NAME, 80)
            go_surf = go_font.render("Game Over", True, RED)
            x = SCREEN_WIDTH // 2 - go_surf.get_width() // 2
            y = SCREEN_HEIGHT // 2 - go_surf.get_height() // 2 - 50
            self.screen.blit(go_surf, (x, y))

            self.exit_button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            if not self.handle_pause():
                break

            if not self.paused and not self.day_completed:
                self.update(dt)
                if not self.game_over:
                    self.spawn_and_update_zombies(dt)
                    self.handle_bullet_zombie_collisions()
                    self.handle_collisions(dt)
                    self.update_blood_effects(dt)
            elif self.paused:
                if not self.show_upgrade_menu():
                    break
                self.paused = False
                if self.day_completed:
                    self.day += 1
                    self.current_wave = 0
                    self.wave = 1
                    self.zombies_to_spawn = 0
                    self.wave_timer = 0.0
                    self.day_completed = False
                    self.waves = WAVES_CONFIG.get(self.day, [])
                    self.zombies = []

            self.draw()