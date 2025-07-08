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

        self.max_health = 100
        self.health = self.max_health

        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 20
        self.facing_right = True

        self.magazine_size = 30
        self.current_ammo = self.magazine_size
        self.reload_time = 2.0
        self.reload_timer = 0.0
        self.is_reloading = False

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        if keys[pygame.K_r] and not self.is_reloading and self.current_ammo < self.magazine_size:
            self.start_reload()

        if self.is_reloading:
            self.reload_timer -= 1/60.0
            if self.reload_timer <= 0:
                self.finish_reload()

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0 and not self.is_reloading:
            self.shoot()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(830, self.rect.right)
        self.rect.top = max(458, self.rect.top)
        self.rect.bottom = min(SCREEN_HEIGHT, self.rect.bottom)

    def shoot(self):
        if self.current_ammo > 0:
            direction = 1 if self.facing_right else -1
            x = self.rect.right if self.facing_right else self.rect.left
            self.bullets.append(Bullet(x, self.rect.centery, direction))
            self.current_ammo -= 1
            self.shoot_cooldown = self.shoot_delay

            if self.current_ammo == 0:
                self.start_reload()
    
    def start_reload(self):
        self.is_reloading = True
        self.reload_timer = self.reload_time
    
    def finish_reload(self):
        self.is_reloading = False
        self.current_ammo = self.magazine_size
        self.reload_timer = 0.0

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