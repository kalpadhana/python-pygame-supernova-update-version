"""
Advanced enemy types system for SuperNova.
Defines new enemy types with different behaviors, speeds, and abilities.
"""

import pygame
import random
import math


class EnemyType:
    """Defines an enemy type with specific characteristics."""
    
    def __init__(self, name, hp, speed, damage, size, color, points, special_ability=None):
        self.name = name
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.size = size
        self.color = color
        self.points = points
        self.special_ability = special_ability


class AdvancedEnemyTypeManager:
    """Manages different enemy types."""
    
    def __init__(self):
        self.enemy_types = {
            "scout": EnemyType(
                name="Scout",
                hp=20,
                speed=6,
                damage=5,
                size=15,
                color=(100, 200, 100),
                points=50,
                special_ability="fast"
            ),
            "tank": EnemyType(
                name="Tank",
                hp=60,
                speed=2,
                damage=15,
                size=25,
                color=(150, 100, 50),
                points=150,
                special_ability="tough"
            ),
            "shooter": EnemyType(
                name="Shooter",
                hp=30,
                speed=3,
                damage=10,
                size=18,
                color=(255, 100, 100),
                points=100,
                special_ability="ranged"
            ),
            "drone": EnemyType(
                name="Drone",
                hp=15,
                speed=7,
                damage=3,
                size=12,
                color=(200, 200, 50),
                points=40,
                special_ability="swarm"
            ),
            "phantom": EnemyType(
                name="Phantom",
                hp=25,
                speed=8,
                damage=8,
                size=14,
                color=(150, 100, 255),
                points=120,
                special_ability="evasive"
            ),
            "shielded": EnemyType(
                name="Shielded",
                hp=80,
                speed=2.5,
                damage=12,
                size=22,
                color=(100, 150, 255),
                points=180,
                special_ability="shield"
            ),
        }
    
    def get_enemy_type(self, type_name):
        """Get enemy type by name."""
        return self.enemy_types.get(type_name)
    
    def get_random_enemy_type(self, difficulty_level=1):
        """Get random enemy type based on difficulty.
        
        Args:
            difficulty_level: 1-5, where higher means tougher enemies
        """
        available = []
        
        # Easy difficulty - only basic enemies
        if difficulty_level <= 1:
            available = ["scout", "drone"]
        # Medium difficulty
        elif difficulty_level <= 2:
            available = ["scout", "drone", "shooter"]
        # Hard difficulty
        elif difficulty_level <= 3:
            available = ["tank", "shooter", "drone"]
        # Very hard
        elif difficulty_level <= 4:
            available = ["tank", "shooter", "phantom", "scout"]
        # Nightmare
        else:
            available = ["tank", "phantom", "shielded", "shooter"]
        
        return random.choice(available)
    
    def get_all_types(self):
        """Get all available enemy types."""
        return list(self.enemy_types.keys())


class EnemyBehavior:
    """Handles different enemy behaviors."""
    
    @staticmethod
    def scout_behavior(enemy, player, delta_time):
        """Fast, simple movement toward player."""
        if player:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                enemy.velocity_x = (dx / dist) * enemy.speed * 1.2
                enemy.velocity_y = (dy / dist) * enemy.speed * 1.2
    
    @staticmethod
    def tank_behavior(enemy, player, delta_time):
        """Slow, heavy movement. Charges periodically."""
        if player:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                # Periodic charge attack
                if enemy.spawn_time % 3000 < 500:  # Charge every 3 seconds
                    speed_mult = 3
                else:
                    speed_mult = 1
                
                enemy.velocity_x = (dx / dist) * enemy.speed * speed_mult
                enemy.velocity_y = (dy / dist) * enemy.speed * speed_mult
    
    @staticmethod
    def shooter_behavior(enemy, player, delta_time):
        """Maintains distance from player and periodically shoots."""
        if player:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            # Keep distance or circle player
            if dist < 200:  # Too close
                # Move away
                if dist > 0:
                    enemy.velocity_x = -(dx / dist) * enemy.speed
                    enemy.velocity_y = -(dy / dist) * enemy.speed
            else:
                # Circle around player
                time_factor = enemy.spawn_time * 0.001
                enemy.velocity_x = math.cos(time_factor) * enemy.speed * 0.5
                enemy.velocity_y = math.sin(time_factor) * enemy.speed * 0.5
    
    @staticmethod
    def drone_behavior(enemy, player, delta_time):
        """Swarm behavior - moves in pattern with other drones."""
        if player:
            # Spiral pattern around player
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                time_factor = enemy.spawn_time * 0.002
                angle = math.atan2(dy, dx) + math.sin(time_factor) * 0.5
                
                enemy.velocity_x = math.cos(angle) * enemy.speed
                enemy.velocity_y = math.sin(angle) * enemy.speed
    
    @staticmethod
    def phantom_behavior(enemy, player, delta_time):
        """Erratic, evasive movement."""
        if player:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            if dist > 0:
                # Calculate target direction
                target_x = (dx / dist) * enemy.speed
                target_y = (dy / dist) * enemy.speed
                
                # Add evasive randomness
                if random.random() < 0.1:
                    enemy.velocity_x = target_x + random.uniform(-3, 3)
                    enemy.velocity_y = target_y + random.uniform(-3, 3)
                else:
                    # Smoothly approach
                    enemy.velocity_x = enemy.velocity_x * 0.8 + target_x * 0.2
                    enemy.velocity_y = enemy.velocity_y * 0.8 + target_y * 0.2
    
    @staticmethod
    def shielded_behavior(enemy, player, delta_time):
        """Defensive movement with shield mechanics."""
        if player:
            dx = player.rect.centerx - enemy.rect.centerx
            dy = player.rect.centery - enemy.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            
            # Move slowly but deliberately
            if dist > 0:
                enemy.velocity_x = (dx / dist) * enemy.speed * 0.8
                enemy.velocity_y = (dy / dist) * enemy.speed * 0.8


# Behavior mapping
BEHAVIOR_MAP = {
    "fast": EnemyBehavior.scout_behavior,
    "tough": EnemyBehavior.tank_behavior,
    "ranged": EnemyBehavior.shooter_behavior,
    "swarm": EnemyBehavior.drone_behavior,
    "evasive": EnemyBehavior.phantom_behavior,
    "shield": EnemyBehavior.shielded_behavior,
}


def get_behavior_function(ability_name):
    """Get behavior function for enemy ability."""
    return BEHAVIOR_MAP.get(ability_name, EnemyBehavior.scout_behavior)
