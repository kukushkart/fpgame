# config.py

import pygame

# Размеры главного окна
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY  = (100, 100, 100)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Шрифт
pygame.font.init()
FONT_NAME = 'assets/fonts/BebasNeue-Regular.ttf'
FONT_SIZE = 50

# Пути к изображениям
BG_IMAGE_PATH      = "assets/images/zombie_bg_big.png"
GAME_BG_IMAGE_PATH = "assets/images/main_bg.png"
PLAYER_IMAGE_PATH  = "assets/images/player.png"
ZOMBIE_IMAGE_PATH  = "assets/images/zombie.png"

ZOMBIE_SIZE = 100

BULLET_PATH = "assets/images/bullet.png"