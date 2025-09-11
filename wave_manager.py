import pygame
import math
import random
from custom_zombies import BlueZombie, GreenZombie, RedZombie, PurpleZombie, HatZombie, VioletZombie, LimeZombie, CyanZombie

def generate_advanced_wave_config(day):
    base_waves = 2 + math.floor(day / 2.5)
    base_zombies = 4 + day * 1.8
    
    waves = []
    wave_types = ['normal', 'swarm', 'boss', 'mixed']
    
    for wave in range(base_waves):
        if day < 3:
            wave_type = 'normal'
        else:
            weights = [0.6, 0.2, 0.1, 0.1]
            wave_type = random.choices(wave_types, weights=weights)[0]

        wave_multiplier = 0.6 + (wave / base_waves) * 0.8
        base_count = math.floor(base_zombies * wave_multiplier)

        if wave_type == 'normal':
            zombie_count = base_count
            delay = max(1.0, 7 - day / 6)
            zombie_types = get_normal_zombie_types(day)
            
        elif wave_type == 'swarm':
            zombie_count = math.floor(base_count * 1.5)
            delay = max(2.0, 9 - day / 5)
            zombie_types = get_swarm_zombie_types(day)
            
        elif wave_type == 'boss':
            zombie_count = max(1, math.floor(base_count * 0.4))
            delay = max(3.0, 8 - day / 7)
            zombie_types = get_boss_zombie_types(day)
            
        else:
            zombie_count = math.floor(base_count * 1.2)
            delay = max(1.5, 6 - day / 8)
            zombie_types = get_mixed_zombie_types(day)

        zombie_count = math.floor(zombie_count * random.uniform(0.9, 1.1))
        delay = round(delay * random.uniform(0.9, 1.1), 1)
        
        waves.append({
            "zombie_count": max(2, zombie_count),
            "delay": max(0.5, delay),
            "type": wave_type,
            "zombie_types": zombie_types
        })
    
    return waves

def get_normal_zombie_types(day):
    all_zombies = [GreenZombie, LimeZombie, BlueZombie, HatZombie]
    if day >= 3:
        all_zombies.extend([CyanZombie, VioletZombie])
    if day >= 5:
        all_zombies.extend([RedZombie, PurpleZombie])
    return all_zombies

def get_swarm_zombie_types(day):
    swarm_zombies = [GreenZombie, LimeZombie, HatZombie]
    if day >= 4:
        swarm_zombies.append(CyanZombie)
    return swarm_zombies

def get_boss_zombie_types(day):
    boss_zombies = [PurpleZombie, RedZombie]
    if day >= 4:
        boss_zombies.append(VioletZombie)
    if day >= 6:
        boss_zombies.append(BlueZombie)
    return boss_zombies

def get_mixed_zombie_types(day):
    return get_normal_zombie_types(day)

def get_wave_config(day):
    return generate_advanced_wave_config(day)

WAVES_CONFIG = {
    1: [
        {"zombie_count": 4, "delay": 5, "type": "normal"},
        {"zombie_count": 4, "delay": 5, "type": "normal"}
    ],
    2: [
        {"zombie_count": 4, "delay": 5, "type": "normal"},
        {"zombie_count": 6, "delay": 5, "type": "normal"},
        {"zombie_count": 6, "delay": 5, "type": "normal"}
    ],
    3: [
        {"zombie_count": 6, "delay": 5, "type": "normal"},
        {"zombie_count": 6, "delay": 3, "type": "swarm"},
        {"zombie_count": 8, "delay": 3, "type": "normal"},
        {"zombie_count": 10, "delay": 5, "type": "normal"},
        {"zombie_count": 10, "delay": 5, "type": "normal"}
    ]
}
