import pygame

WAVES_CONFIG = {
    1: [
        {"zombie_count": 4, "delay": 0},
        {"zombie_count": 4, "delay": 5}
    ],
    2: [
        {"zombie_count": 4, "delay": 0},
        {"zombie_count": 6, "delay": 5},
        {"zombie_count": 6, "delay": 5}
    ],
    3: [
        {"zombie_count": 6, "delay": 0},
        {"zombie_count": 6, "delay": 5},
        {"zombie_count": 8, "delay": 5},
        {"zombie_count": 10, "delay": 3},
        {"zombie_count": 10, "delay": 3}
    ],
    4: [
        {"zombie_count": 8, "delay": 0},
        {"zombie_count": 9, "delay": 5},
        {"zombie_count": 5, "delay": 3},
        {"zombie_count": 8, "delay": 3},
        {"zombie_count": 14, "delay": 7}
    ],
    5: [
        {"zombie_count": 10, "delay": 0},
        {"zombie_count": 10, "delay": 5},
        {"zombie_count": 8, "delay": 5},
        {"zombie_count": 6, "delay": 5},
        {"zombie_count": 20, "delay": 5}
    ]
}