import pygame
import random
import math

class DamageNumber:
    def __init__(self, x, y, amount, is_crit=False, is_heal=False):
        self.x = x
        self.y = y
        self.amount = amount
        self.is_crit = is_crit
        self.is_heal = is_heal
        self.life = 60 # frames
        self.max_life = 60
        self.vy = random.uniform(-3, -1)
        self.vx = random.uniform(-1, 1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface, font):
        if self.life > 0:
            alpha = max(0, min(255, int((self.life / self.max_life) * 255)))
            
            if self.is_heal:
                color = (50, 255, 50)
                text = f"+{self.amount}"
            elif self.is_crit:
                color = (255, 200, 0)
                text = f"{self.amount}!"
            else:
                color = (255, 50, 50)
                text = f"-{self.amount}"

            surf = font.render(text, True, color)
            surf.set_alpha(alpha)
            # Center the text
            rect = surf.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(surf, rect)

class DamageNumberManager:
    def __init__(self):
        self.numbers = []
        pygame.font.init()
        self.font = pygame.font.Font(None, 28)
        self.crit_font = pygame.font.Font(None, 36)

    def add(self, x, y, amount, is_crit=False, is_heal=False):
        self.numbers.append(DamageNumber(x, y, amount, is_crit, is_heal))

    def update(self):
        for num in self.numbers[:]:
            num.update()
            if num.life <= 0:
                self.numbers.remove(num)

    def draw(self, surface):
        for num in self.numbers:
            if num.is_crit:
                num.draw(surface, self.crit_font)
            else:
                num.draw(surface, self.font)

class CompanionDrone:
    def __init__(self, id, total_drones):
        self.id = id
        self.total_drones = total_drones
        self.angle = (this.id / this.total_drones) * math.pi * 2
        self.distance = 60
        self.shoot_timer = 0
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (100, 200, 255), (7, 7), 7)
        self.rect = self.image.get_rect()

    def update(self, player_rect, time_passed):
        self.angle += 0.05
        self.rect.centerx = player_rect.centerx + math.cos(self.angle) * self.distance
        self.rect.centery = player_rect.centery + math.sin(self.angle) * self.distance
        self.shoot_timer += 1
        return self.shoot_timer >= 60 # returns true when ready to shoot

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class DroneManager:
    def __init__(self):
        self.drones = []
        self.drone_count = 0

    def add_drone(self):
        self.drone_count += 1
        self.drones = []
        for i in range(self.drone_count):
            self.drones.append(CompanionDrone(i, self.drone_count))

    def update(self, player_rect, bullet_group, bullet_class):
        for drone in self.drones:
            if drone.update(player_rect, 1) and drone.rect.bottom > 0:
                drone.shoot_timer = 0
                b = bullet_class(drone.rect.centerx, drone.rect.top)
                # scale down bullet damage for drone
                b.speed = 12
                # smaller visual for drone bullet
                small_img = pygame.transform.scale(b.image, (b.rect.width//2, b.rect.height//2))
                b.image = small_img
                b.rect = b.image.get_rect(center=(drone.rect.centerx, drone.rect.top))
                bullet_group.add(b)

    def draw(self, surface):
        for drone in self.drones:
            drone.draw(surface)

class DashSystem:
    def __init__(self):
        self.is_dashing = False
        self.cooldown = 0
        self.dash_time = 0
        self.max_cooldown = 120 # 2 seconds
        self.dash_duration = 15 # Frames
        self.speed_mult = 3
        self.afterimages = []

    def try_dash(self):
        if self.cooldown <= 0 and not self.is_dashing:
            self.is_dashing = True
            self.dash_time = self.dash_duration
            self.cooldown = self.max_cooldown
            return True
        return False

    def update(self, player):
        if self.cooldown > 0:
            self.cooldown -= 1
            
        if self.is_dashing:
            self.dash_time -= 1
            # add afterimage
            if self.dash_time % 2 == 0: # every other frame
                img = player.image.copy()
                img.set_alpha(128)
                self.afterimages.append({
                    "img": img,
                    "rect": player.rect.copy(),
                    "life": 15
                })
            if self.dash_time <= 0:
                self.is_dashing = False

        # update afterimages
        for ai in self.afterimages[:]:
            ai["life"] -= 1
            ai["img"].set_alpha(int((ai["life"]/15)*128))
            if ai["life"] <= 0:
                self.afterimages.remove(ai)

    def draw(self, surface):
        for ai in self.afterimages:
            surface.blit(ai["img"], ai["rect"])

class UltimateSystem:
    def __init__(self):
        self.charge = 0
        self.max_charge = 1000
        self.is_active = False
        self.active_time = 0
        self.max_active_time = 300 # 5 seconds of bullet time

    def add_charge(self, amount):
        if not self.is_active:
            self.charge = min(self.max_charge, self.charge + amount)

    def try_activate(self):
        if self.charge >= self.max_charge and not self.is_active:
            self.is_active = True
            self.charge = 0
            self.active_time = self.max_active_time
            return True
        return False

    def update(self):
        time_scale = 1.0
        if self.is_active:
            self.active_time -= 1
            time_scale = 0.3 # Slowmo for enemies
            if self.active_time <= 0:
                self.is_active = False
        return time_scale

    def draw_ui(self, surface, screen_width, screen_height):
        # Draw ultimate bar at the bottom
        bar_w = 400
        bar_h = 10
        bar_x = screen_width // 2 - bar_w // 2
        bar_y = screen_height - 30
        
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
        
        if self.is_active:
            fill_w = int((self.active_time / self.max_active_time) * bar_w)
            pygame.draw.rect(surface, (255, 255, 0), (bar_x, bar_y, fill_w, bar_h))
        else:
            fill_w = int((self.charge / self.max_charge) * bar_w)
            color = (0, 255, 255) if self.charge >= self.max_charge else (0, 150, 200)
            pygame.draw.rect(surface, color, (bar_x, bar_y, fill_w, bar_h))
            if self.charge >= self.max_charge:
                 font = pygame.font.Font(None, 24)
                 text = font.render("Press Y/Enter for ULTIMATE", True, (255, 255, 255))
                 surface.blit(text, (bar_x + bar_w//2 - text.get_width()//2, bar_y - 20))

class LevelSystem:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.required_xp = 100
        self.show_level_up = False
        self.available_perks = []
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)

        self.perk_pool = [
            {"name": "Drone +1", "desc": "Adds a companion drone", "type": "drone"},
            {"name": "Max Health UP", "desc": "+50 Max Health and restores it", "type": "health"},
            {"name": "Faster Firerate", "desc": "Reduces shoot delay", "type": "firerate"},
            {"name": "Speed UP", "desc": "Increases player movement speed", "type": "speed"}
        ]

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.required_xp:
            self.xp -= self.required_xp
            self.level += 1
            self.required_xp = int(self.required_xp * 1.5)
            self.show_level_up = True
            # pick 3 random perks
            self.available_perks = random.sample(self.perk_pool, min(3, len(self.perk_pool)))
            return True
        return False

    def draw_ui(self, surface, screen_width):
        font = pygame.font.Font(None, 24)
        text = font.render(f"Lv {self.level} XP: {self.xp}/{self.required_xp}", True, (200, 200, 255))
        surface.blit(text, (screen_width // 2 - text.get_width()//2, 10))

    def draw_menu(self, surface, width, height, selected_idx):
        if not self.show_level_up: return
        
        # Transparent overlay
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        title = self.font_large.render("LEVEL UP! CHOOSE A PERK", True, (255, 255, 0))
        surface.blit(title, (width//2 - title.get_width()//2, 100))

        for i, perk in enumerate(self.available_perks):
            rect = pygame.Rect(width//2 - 200, 200 + i * 100, 400, 80)
            color = (100, 100, 200) if i == selected_idx else (50, 50, 100)
            pygame.draw.rect(surface, color, rect, border_radius=10)
            pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=10)
            
            name_txt = self.font_large.render(perk["name"], True, (255,255,255))
            desc_txt = self.font_small.render(perk["desc"], True, (200,200,200))
            
            surface.blit(name_txt, (rect.x + 20, rect.y + 10))
            surface.blit(desc_txt, (rect.x + 20, rect.y + 50))
