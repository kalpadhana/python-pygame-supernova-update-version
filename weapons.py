"""
Advanced weapons system for SuperNova.
Includes different weapon types, firing patterns, and special effects.
"""

import pygame
import math
import random


class WeaponType:
    """Defines a weapon type."""
    
    def __init__(self, name, fire_rate, spread, damage, speed, ammo_consumption=1, color=(255, 255, 0)):
        self.name = name
        self.fire_rate = fire_rate  # milliseconds between shots
        self.spread = spread  # Angle spread for gun spread
        self.damage = damage  # Damage per bullet
        self.speed = speed  # Bullet speed
        self.ammo_consumption = ammo_consumption  # Ammo used per shot
        self.color = color


class WeaponSystem:
    """Manages player weapons and firing."""
    
    def __init__(self):
        self.weapons = {
            "basic": WeaponType(
                name="Basic Blaster",
                fire_rate=100,
                spread=0,
                damage=10,
                speed=15,
                ammo_consumption=1,
                color=(255, 255, 0)
            ),
            "spread": WeaponType(
                name="Spread Gun",
                fire_rate=150,
                spread=20,
                damage=8,
                speed=12,
                ammo_consumption=3,
                color=(255, 150, 0)
            ),
            "rapid": WeaponType(
                name="Rapid Fire",
                fire_rate=50,
                spread=5,
                damage=5,
                speed=13,
                ammo_consumption=1,
                color=(100, 200, 255)
            ),
            "plasma": WeaponType(
                name="Plasma Cannon",
                fire_rate=200,
                spread=0,
                damage=20,
                speed=10,
                ammo_consumption=5,
                color=(200, 100, 255)
            ),
            "ion": WeaponType(
                name="Ion Beam",
                fire_rate=250,
                spread=3,
                damage=15,
                speed=18,
                ammo_consumption=2,
                color=(0, 255, 200)
            ),
        }
        
        self.current_weapon = "basic"
        self.last_shot_time = 0
        self.ammo = 1000
        self.max_ammo = 1000
    
    def get_current_weapon(self):
        """Get current weapon type."""
        return self.weapons[self.current_weapon]
    
    def switch_weapon(self, weapon_name):
        """Switch to different weapon."""
        if weapon_name in self.weapons:
            self.current_weapon = weapon_name
            return True
        return False
    
    def can_fire(self, current_time):
        """Check if weapon can fire."""
        weapon = self.get_current_weapon()
        return (current_time - self.last_shot_time >= weapon.fire_rate and 
                self.ammo >= weapon.ammo_consumption)
    
    def fire(self, player_pos, direction, current_time):
        """Fire weapon and return bullets to spawn.
        
        Returns:
            List of (bullet_pos, bullet_direction) tuples
        """
        if not self.can_fire(current_time):
            return []
        
        weapon = self.get_current_weapon()
        self.last_shot_time = current_time
        self.ammo -= weapon.ammo_consumption
        
        bullets = []
        
        # Calculate number of bullets based on weapon
        if weapon.name == "Spread Gun":
            bullet_count = 3
        elif weapon.name == "Rapid Fire":
            bullet_count = 1
        elif weapon.name == "Plasma Cannon":
            bullet_count = 1
        elif weapon.name == "Ion Beam":
            bullet_count = 2
        else:  # Basic
            bullet_count = 1
        
        # Generate bullets
        for i in range(bullet_count):
            if bullet_count == 1:
                angle_offset = 0
            else:
                # Spread bullets
                angle_offset = (i - bullet_count // 2) * weapon.spread
            
            # Calculate direction with spread
            angle_rad = math.radians(direction + angle_offset)
            bullet_dir = (math.cos(angle_rad), math.sin(angle_rad))
            
            bullets.append({
                "pos": player_pos,
                "dir": bullet_dir,
                "speed": weapon.speed,
                "damage": weapon.damage,
                "color": weapon.color,
                "weapon": weapon.name
            })
        
        return bullets
    
    def add_ammo(self, amount):
        """Add ammo."""
        self.ammo = min(self.ammo + amount, self.max_ammo)
    
    def consume_ammo(self, amount):
        """Consume ammo."""
        self.ammo = max(0, self.ammo - amount)
    
    def get_ammo_percent(self):
        """Get ammo as percentage."""
        return (self.ammo / self.max_ammo) * 100
    
    def get_weapon_names(self):
        """Get list of available weapons."""
        return list(self.weapons.keys())
    
    def get_weapon_info(self, weapon_name):
        """Get weapon information."""
        if weapon_name not in self.weapons:
            return None
        
        w = self.weapons[weapon_name]
        return {
            "name": w.name,
            "damage": w.damage,
            "fire_rate": w.fire_rate,
            "speed": w.speed,
            "ammo_cost": w.ammo_consumption
        }


class SpecialAbility:
    """Special weapon abilities that recharge over time."""
    
    def __init__(self, name, cooldown_ms, effect_radius=100, damage=50):
        self.name = name
        self.cooldown_ms = cooldown_ms
        self.effect_radius = effect_radius
        self.damage = damage
        self.last_used = 0
    
    def can_use(self, current_time):
        """Check if ability is ready."""
        return current_time - self.last_used >= self.cooldown_ms
    
    def use(self, current_time):
        """Use the ability."""
        if self.can_use(current_time):
            self.last_used = current_time
            return True
        return False
    
    def get_cooldown_percent(self, current_time):
        """Get cooldown as percentage."""
        elapsed = current_time - self.last_used
        return min(100, int((elapsed / self.cooldown_ms) * 100))


class AbilitySystem:
    """Manages special abilities."""
    
    def __init__(self):
        self.abilities = {
            "blast": SpecialAbility("Plasma Burst", cooldown_ms=5000, effect_radius=150, damage=100),
            "shield": SpecialAbility("Protective Shield", cooldown_ms=8000, effect_radius=80, damage=0),
            "slow": SpecialAbility("Time Slow", cooldown_ms=10000, effect_radius=400, damage=0),
        }
        self.current_ability = "blast"
    
    def get_current_ability(self):
        """Get current selected ability."""
        return self.abilities[self.current_ability]
    
    def use_ability(self, current_time):
        """Use current ability."""
        ability = self.get_current_ability()
        if ability.use(current_time):
            return ability
        return None
    
    def get_ability_cooldown(self, current_time):
        """Get current ability cooldown percentage."""
        ability = self.get_current_ability()
        return ability.get_cooldown_percent(current_time)
