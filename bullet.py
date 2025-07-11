import pygame
from config import *
class Bullet:
    def __init__(self, x, y, direction, damage):
        self.speed = 10
        self.damage = damage
        self.direction = direction
        try:
            self.image = pygame.image.load(BULLET_PATH).convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 15))
            if direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
        except:
            self.image = pygame.Surface((30, 10), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, (255, 215, 0), (0, 0, 30, 10))
        self.rect = self.image.get_rect()
        self.rect.midleft = (x - 9 if direction == 1 else x, y - 4)
    def update(self):
        self.rect.x += self.speed * self.direction
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    def is_off_screen(self):
        return (self.rect.right < 0 if self.direction == -1
                else self.rect.left > SCREEN_WIDTH)