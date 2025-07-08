import pygame
from config import *
from bullet import Bullet

class Player:
    def __init__(self):
        try:
            self.original_image = pygame.image.load("assets/images/test_survivor.png").convert_alpha()
        except:
            print("Invalid creating survivor attempt! Making smth else")
            self.original_image = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(self.original_image, (255, 0, 0), (50, 50), 50)

        self.image = pygame.transform.smoothscale(self.original_image, (150, 150))
        self.rect = self.image.get_rect()

        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)

        self.speed = 4

        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 10  # Уменьшаем задержку для более частой стрельбы
        self.facing_right = True

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(830, self.rect.right)
        self.rect.top = max(458, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

    def shoot(self):
        direction = 1 if self.facing_right else -1
        x = self.rect.right if self.facing_right else self.rect.left
        self.bullets.append(Bullet(x, self.rect.centery, direction))
        self.shoot_cooldown = self.shoot_delay

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def draw_bullets(self, surface):
        for bullet in self.bullets:
            bullet.draw(surface)

    def draw(self, surface):
        surface.blit(self.image, self.rect)