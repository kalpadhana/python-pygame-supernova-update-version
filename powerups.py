"""
Power-up system for SuperNova game.
Includes health, shield, ammo, and speed boost power-ups.
"""

import pygame
import random
import math


class PowerUp(pygame.sprite.Sprite):
    """Base class for all power-ups."""
    
    def __init__(self, x, y, powerup_type, image=None):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.powerup_type = powerup_type  # "health", "shield", "ammo", "speed"
        self.rotation = 0
        self.pulse = 0
        
        # Create surface if no image provided
        if image:
            self.image = image
        else:
            self.image = self._create_surface()
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity_y = random.uniform(-2, 0)  # Slight upward drift
        self.lifetime = 10000  # 10 seconds in milliseconds
        self.spawn_time = pygame.time.get_ticks()
    
    def _create_surface(self):
        """Create power-up surface based on type."""
        size = 25
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        if self.powerup_type == "health":
            # Red cross for health
            pygame.draw.circle(surface, (255, 0, 0), (size//2, size//2), size//2)
            pygame.draw.line(surface, (255, 255, 255), (size//4, size//2), (3*size//4, size//2), 3)
            pygame.draw.line(surface, (255, 255, 255), (size//2, size//4), (size//2, 3*size//4), 3)
        
        elif self.powerup_type == "shield":
            # Blue shield
            points = [(size//2, 0), (size, size//3), (size, size), (size//2, 2*size//3), (0, size), (0, size//3)]
            pygame.draw.polygon(surface, (0, 100, 255), points)
            pygame.draw.polygon(surface, (100, 200, 255), points, 2)
        
        elif self.powerup_type == "ammo":
            # Yellow ammo box
            pygame.draw.rect(surface, (255, 255, 0), (0, 0, size, size))
            pygame.draw.rect(surface, (200, 200, 0), (0, 0, size, size), 2)
            # Draw bullet symbol
            pygame.draw.circle(surface, (255, 100, 0), (size//3, size//3), 2)
            pygame.draw.circle(surface, (255, 100, 0), (2*size//3, size//3), 2)
            pygame.draw.circle(surface, (255, 100, 0), (size//3, 2*size//3), 2)
            pygame.draw.circle(surface, (255, 100, 0), (2*size//3, 2*size//3), 2)
        
        elif self.powerup_type == "speed":
            # Green lightning bolt for speed
            pygame.draw.polygon(surface, (0, 255, 100), [
                (size//2, 0), (size, size//3), (size//2 + 5, size//2),
                (size, size), (size//2, 2*size//3), (size//2 - 5, size//2)
            ])
        
        return surface
    
    def update(self, screen_height=600):
        """Update power-up position and animation."""
        self.y += self.velocity_y
        self.velocity_y = min(self.velocity_y + 0.1, 2)  # Apply gravity
        
        # Rotation animation
        self.rotation = (self.rotation + 2) % 360
        
        # Pulse animation
        self.pulse = (self.pulse + 0.05) % (2 * math.pi)
        scale_factor = 1 + 0.2 * math.sin(self.pulse)
        
        # Rotate and scale image
        rotated = pygame.transform.rotate(self.image, self.rotation)
        scaled = pygame.transform.scale(rotated, 
                                        (int(rotated.get_width() * scale_factor),
                                         int(rotated.get_height() * scale_factor)))
        
        self.image = scaled
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
        # Remove if fallen off screen or expired
        if self.y > screen_height or pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()
    
    def get_effect(self):
        """Return the effect parameters for this power-up."""
        effects = {
            "health": {"heal": 30},
            "shield": {"shield": 50, "duration": 5000},
            "ammo": {"ammo": 100},
            "speed": {"speed_boost": 0.5, "duration": 3000}
        }
        return effects.get(self.powerup_type, {})


class PowerUpManager:
    """Manages power-up spawning and effects."""
    
    def __init__(self):
        self.powerups = pygame.sprite.Group()
        self.spawn_chance = 0.02  # 2% chance per frame when enemy dies
        self.active_effects = {}  # Track active power-up effects
    
    def spawn_random(self, x, y):
        """Spawn a random power-up at position."""
        if random.random() < self.spawn_chance:
            powerup_type = random.choice(["health", "shield", "ammo", "speed"])
            powerup = PowerUp(x, y, powerup_type)
            self.powerups.add(powerup)
            return powerup
        return None
    
    def spawn_specific(self, x, y, powerup_type):
        """Spawn a specific power-up type."""
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.add(powerup)
        return powerup
    
    def update(self, screen_height=600):
        """Update all power-ups."""
        self.powerups.update(screen_height)
        
        # Update active effects (remove expired ones)
        current_time = pygame.time.get_ticks()
        expired = [key for key, data in self.active_effects.items() 
                   if current_time > data['expires_at']]
        for key in expired:
            del self.active_effects[key]
    
    def draw(self, surface):
        """Draw all power-ups."""
        self.powerups.draw(surface)
    
    def check_collision(self, player):
        """Check for collisions with player and return collected power-ups."""
        collected = []
        for powerup in pygame.sprite.spritecollide(player, self.powerups, True):
            collected.append(powerup)
            effect = powerup.get_effect()
            
            # Apply health effect
            if "heal" in effect:
                player.hp = min(player.hp + effect["heal"], player.max_hp)
            
            # Apply ammo effect
            if "ammo" in effect:
                player.ammo += effect["ammo"]
            
            # Apply shield effect
            if "shield" in effect:
                effect_key = "shield"
                self.active_effects[effect_key] = {
                    "value": effect["shield"],
                    "expires_at": pygame.time.get_ticks() + effect["duration"],
                    "type": "shield"
                }
                player.shield = effect["shield"]
            
            # Apply speed effect
            if "speed_boost" in effect:
                effect_key = "speed"
                self.active_effects[effect_key] = {
                    "value": effect["speed_boost"],
                    "expires_at": pygame.time.get_ticks() + effect["duration"],
                    "type": "speed"
                }
                player.speed_boost = effect["speed_boost"]
        
        return collected
    
    def is_shield_active(self):
        """Check if shield power-up is active."""
        return "shield" in self.active_effects
    
    def get_shield_value(self):
        """Get current shield value."""
        if "shield" in self.active_effects:
            return self.active_effects["shield"]["value"]
        return 0
    
    def is_speed_active(self):
        """Check if speed boost is active."""
        return "speed" in self.active_effects
    
    def get_speed_boost(self):
        """Get current speed boost value."""
        if "speed" in self.active_effects:
            return self.active_effects["speed"]["value"]
        return 0
