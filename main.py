import os
import pygame
from config import *
from info_screen import InfoScreen
from ui import Button, draw_menu
from game_window import GameWindow
from records_menu import RecordsScreen
from player_name_input import PlayerNameInput
from character_select import CharacterSelectScreen
import ctypes

if os.name == "nt":
    ctypes.windll.user32.SetProcessDPIAware()

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Survival")
    clock = pygame.time.Clock()
    background = pygame.image.load(BG_IMAGE_PATH).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    buttons = [
        Button(SCREEN_WIDTH // 2 - 100, 200, 200, 60, "New Game", GREEN, (150, 255, 150)),
        Button(SCREEN_WIDTH // 2 - 100, 280, 200, 60, "Load Game", (70, 130, 180), (100, 150, 200)),
        Button(SCREEN_WIDTH // 2 - 100, 360, 200, 60, "Info", GRAY, (200, 200, 200)),
        Button(SCREEN_WIDTH // 2 - 100, 440, 200, 60, "Records", GRAY, (200, 200, 200)),
        Button(SCREEN_WIDTH // 2 - 100, 520, 200, 60, "Exit", RED, (255, 150, 150)),
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(WHITE)

        for button in buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                if button.text == "Exit":
                    running = False
                elif button.text == "New Game":
                    name_input = PlayerNameInput(screen)
                    player_name = name_input.run()
                    if player_name is not None:
                        char_select = CharacterSelectScreen(screen)
                        selected_skin = char_select.run()
                        if selected_skin is not None:
                            game = GameWindow(screen, player_name, selected_skin)
                            game.run()
                elif button.text == "Load Game":
                    print("Loading game... (coming soon)")
                elif button.text == "Info":
                    info = InfoScreen(screen)
                    should_continue = info.run()
                    if not should_continue:
                        running = False
                elif button.text == "Records":
                    records = RecordsScreen(screen)
                    should_continue = records.run()
                    if not should_continue:
                        running = False

        draw_menu(screen, buttons)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()