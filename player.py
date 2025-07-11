import pygame
from config import *
from bullet import Bullet


class Player:
    def __init__(self, skin="assets/images/pixel_pers_static.png"):
        self.skin_path = skin
        
        # Load all animation frames
        try:
            # Static frames
            self.static_right = pygame.image.load("assets/images/pixel_pers_static.png").convert_alpha()
            self.static_left = pygame.image.load("assets/images/pixel_pers_static_reverse.png").convert_alpha()
            
            # Movement frames
            self.mov_1_right = pygame.image.load("assets/images/pixel_pers_mov_1.png").convert_alpha()
            self.mov_1_left = pygame.image.load("assets/images/pixel_pers_mov_1_reverse.png").convert_alpha()
            self.mov_2_right = pygame.image.load("assets/images/pixel_pers_mov_2.png").convert_alpha()
            self.mov_2_left = pygame.image.load("assets/images/pixel_pers_mov_2_reverse.png").convert_alpha()
            
        except Exception as e:
            print(f"Error loading player sprites: {e}. Using fallback.")
            # Create fallback sprites
            self.static_right = pygame.Surface((110, 110), pygame.SRCALPHA)
            pygame.draw.circle(self.static_right, (255, 0, 0), (55, 55), 55)
            self.static_left = pygame.transform.flip(self.static_right, True, False)
            self.mov_1_right = self.static_right.copy()
            self.mov_1_left = self.static_left.copy()
            self.mov_2_right = self.static_right.copy()
            self.mov_2_left = self.static_left.copy()
        
        # Scale all sprites
        self.static_right = pygame.transform.smoothscale(self.static_right, (110, 110))
        self.static_left = pygame.transform.smoothscale(self.static_left, (110, 110))
        self.mov_1_right = pygame.transform.smoothscale(self.mov_1_right, (110, 110))
        self.mov_1_left = pygame.transform.smoothscale(self.mov_1_left, (110, 110))
        self.mov_2_right = pygame.transform.smoothscale(self.mov_2_right, (110, 110))
        self.mov_2_left = pygame.transform.smoothscale(self.mov_2_left, (110, 110))
        
        # Animation variables
        self.animation_timer = 0
        self.animation_speed = 10  # frames between animation changes
        self.animation_frame = 0  # 0 = mov_1, 1 = mov_2
        self.is_moving = False
        
        self.image = self.static_right
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)

        self.damage_text = ""
        self.damage_timer = 0.0

        self.base_speed = 4
        self.speed = self.base_speed

        self.base_damage = 10
        self.damage = self.base_damage

        self.base_max_health = 100
        self.max_health = self.base_max_health
        self.health = self.max_health

        self.base_shoot_delay = 20
        self.shoot_delay = self.base_shoot_delay
        self.shoot_cooldown = 0

        self.base_reload_time = 2.0
        self.reload_time = self.base_reload_time
        self.reload_timer = 0.0
        self.is_reloading = False

        self.base_magazine_size = 30
        self.magazine_size = self.base_magazine_size
        self.current_ammo = self.magazine_size

        self.facing_right = True
        self.bullets = []

        self.ammo_capacity_bought = False
        self.medkits = 0
        self.shift_pressed = False
    
    def flip_direction(self):
        self.facing_right = not self.facing_right
        self.update_sprite()

    def apply_upgrade(self, upgrade_name):
        if upgrade_name == "Strength":
            self.damage += 5
            return True

        elif upgrade_name == "Speed":
            self.speed += 5
            return True

        elif upgrade_name == "Health":
            self.max_health += 10
            self.health += 10
            return True

        elif upgrade_name == "Rate of fire":
            self.shoot_delay = max(10, self.shoot_delay - 2)
            return True

        elif upgrade_name == "Ammo capacity" and not self.ammo_capacity_bought:
            self.magazine_size += 15
            self.current_ammo = self.magazine_size
            self.ammo_capacity_bought = True
            return True

        elif upgrade_name == "Medkit":
            self.medkits += 1
            return True

        elif upgrade_name == "Reload speed":
            self.reload_time -= 0.2
            return True

        return False

    def use_medkit(self):
        if self.medkits > 0 and self.health < self.max_health:
            self.health = min(self.max_health, self.health + 50)
            self.medkits -= 1
            return True
        return False

    def update_sprite(self):
        """Update the current sprite based on movement and direction"""
        if self.is_moving:
            # Use animation frames
            if self.facing_right:
                self.image = self.mov_1_right if self.animation_frame == 0 else self.mov_2_right
            else:
                self.image = self.mov_1_left if self.animation_frame == 0 else self.mov_2_left
        else:
            # Use static frames
            self.image = self.static_right if self.facing_right else self.static_left
    
    def update(self, keys, dt=1/60.0):
        # Check for direction flip
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            if not hasattr(self, 'shift_pressed') or not self.shift_pressed:
                self.flip_direction()
                self.shift_pressed = True
        else:
            self.shift_pressed = False
        
        # Check for movement
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            moving = True
        
        self.is_moving = moving
        
        # Update animation
        if self.is_moving:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.animation_frame = 1 - self.animation_frame  # Toggle between 0 and 1
        else:
            self.animation_timer = 0
            self.animation_frame = 0
        
        # Update sprite
        self.update_sprite()

        if keys[pygame.K_r] and not self.is_reloading and self.current_ammo < self.magazine_size:
            self.start_reload()

        if self.is_reloading:
            self.reload_timer -= dt
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

        if self.damage_timer > 0:
            self.damage_timer -= dt
        else:
            self.damage_text = ""

    def shoot(self):
        if self.current_ammo > 0:
            direction = 1 if self.facing_right else -1
            if self.facing_right:
                x = self.rect.right
            else:
                x = self.rect.left
            
            self.bullets.append(Bullet(x, self.rect.centery, direction, self.damage))
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

        if self.damage_text and self.damage_timer > 0:
            font = pygame.font.Font(FONT_NAME, 40)
            damage_surface = font.render(self.damage_text, True, (255, 0, 0))

            text_x = self.rect.centerx - damage_surface.get_width() // 2
            text_y = self.rect.top - 30

            float_offset = int((1.0 - self.damage_timer) * 20)
            text_y -= float_offset

            alpha = int(255 * self.damage_timer)
            damage_surface.set_alpha(alpha)

            surface.blit(damage_surface, (text_x, text_y))