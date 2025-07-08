import pygame
from config import *
from info_screen import InfoScreen
from ui import Button, draw_menu
from game_window import GameWindow

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Survival")
    clock = pygame.time.Clock()

    background = pygame.image.load(BG_IMAGE_PATH).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    buttons = [
        Button(SCREEN_WIDTH // 2 - 100, 200, 200, 60, "Start", GREEN, (150, 255, 150)),
        Button(SCREEN_WIDTH // 2 - 100, 280, 200, 60, "Info", GRAY, (200, 200, 200)),
        Button(SCREEN_WIDTH // 2 - 100, 360, 200, 60, "Records", GRAY, (200, 200, 200)),
        Button(SCREEN_WIDTH // 2 - 100, 440, 200, 60, "Exit", RED, (255, 150, 150)),
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
                elif button.text == "Start":
                    game = GameWindow(screen)
                    game.run()
                elif button.text == "Info":
                    info = InfoScreen(screen)
                    should_continue = info.run()
                    if not should_continue:
                        running = False
                elif button.text == "Records":
                    print("Таблица рекордов...")

        draw_menu(screen, buttons)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()