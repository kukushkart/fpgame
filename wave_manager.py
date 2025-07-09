import pygame

WAVES_CONFIG = {
    1: [  # День 1
        {"zombie_count": 4, "delay": 0},    # Волна 1: 4 зомби, начинается сразу
        {"zombie_count": 4, "delay": 5}     # Волна 2: 4 зомби, через 5 секунд
    ],
    2: [  # День 2
        {"zombie_count": 4, "delay": 0},    # Волна 1: 4 зомби
        {"zombie_count": 6, "delay": 5},    # Волна 2: 6 зомби
        {"zombie_count": 6, "delay": 5}     # Волна 3: 6 зомби
    ]}