"""
Difficulty levels and game settings system.
Controls game difficulty, enemy spawning, and progression.
"""

import json
import os


class DifficultyLevel:
    """Defines settings for a specific difficulty."""
    
    def __init__(self, name, enemy_spawn_rate, enemy_damage_mult, player_health, boss_spawn_interval, score_multiplier):
        self.name = name
        self.enemy_spawn_rate = enemy_spawn_rate  # Lower = more frequent
        self.enemy_damage_mult = enemy_damage_mult  # Damage multiplier for enemies
        self.player_health = player_health  # Starting health
        self.boss_spawn_interval = boss_spawn_interval  # Ticks between boss spawns
        self.score_multiplier = score_multiplier  # Score multiplier


class GameDifficulty:
    """Manages game difficulty levels and settings."""
    
    def __init__(self, save_file="game_difficulty.json"):
        self.save_file = save_file
        self.current_difficulty = "normal"
        self.progression_level = 0  # Progressive difficulty increase
        self.difficulty_levels = {
            "easy": DifficultyLevel(
                name="Easy",
                enemy_spawn_rate=150,
                enemy_damage_mult=0.5,
                player_health=200,
                boss_spawn_interval=8000,
                score_multiplier=0.75
            ),
            "normal": DifficultyLevel(
                name="Normal",
                enemy_spawn_rate=100,
                enemy_damage_mult=1.0,
                player_health=150,
                boss_spawn_interval=6000,
                score_multiplier=1.0
            ),
            "hard": DifficultyLevel(
                name="Hard",
                enemy_spawn_rate=70,
                enemy_damage_mult=1.5,
                player_health=100,
                boss_spawn_interval=4000,
                score_multiplier=1.5
            ),
            "nightmare": DifficultyLevel(
                name="Nightmare",
                enemy_spawn_rate=50,
                enemy_damage_mult=2.0,
                player_health=80,
                boss_spawn_interval=3000,
                score_multiplier=2.0
            ),
        }
        self.load()
    
    def get_current(self):
        """Get current difficulty settings."""
        return self.difficulty_levels.get(self.current_difficulty, self.difficulty_levels["normal"])
    
    def set_difficulty(self, difficulty):
        """Set difficulty level."""
        if difficulty in self.difficulty_levels:
            self.current_difficulty = difficulty
            return True
        return False
    
    def get_difficulty_names(self):
        """Get list of difficulty names."""
        return list(self.difficulty_levels.keys())
    
    def increase_progression(self):
        """Increase game progression (harder over time)."""
        self.progression_level += 1
        # Every 5 progression levels, spawn enemies faster
        if self.current_difficulty == "easy":
            if self.progression_level % 8 == 0:
                self.difficulty_levels["easy"].enemy_spawn_rate = max(100, self.difficulty_levels["easy"].enemy_spawn_rate - 10)
        elif self.current_difficulty == "normal":
            if self.progression_level % 6 == 0:
                self.difficulty_levels["normal"].enemy_spawn_rate = max(70, self.difficulty_levels["normal"].enemy_spawn_rate - 10)
        elif self.current_difficulty == "hard":
            if self.progression_level % 4 == 0:
                self.difficulty_levels["hard"].enemy_spawn_rate = max(50, self.difficulty_levels["hard"].enemy_spawn_rate - 10)
        else:  # nightmare
            if self.progression_level % 3 == 0:
                self.difficulty_levels["nightmare"].enemy_spawn_rate = max(35, self.difficulty_levels["nightmare"].enemy_spawn_rate - 10)
    
    def get_adjusted_value(self, base_value, value_type="damage"):
        """Get value adjusted by difficulty and progression.
        
        Args:
            base_value: The base game value
            value_type: Type of value being adjusted ("damage", "health", "spawn", etc.)
        """
        current = self.get_current()
        
        if value_type == "damage":
            return base_value * current.enemy_damage_mult
        elif value_type == "spawn_rate":
            return current.enemy_spawn_rate
        elif value_type == "score":
            return int(base_value * current.score_multiplier)
        elif value_type == "health":
            return current.player_health
        
        return base_value
    
    def save(self):
        """Save difficulty settings."""
        data = {
            "current_difficulty": self.current_difficulty,
            "progression_level": self.progression_level
        }
        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load difficulty settings."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.current_difficulty = data.get("current_difficulty", "normal")
                    self.progression_level = data.get("progression_level", 0)
            except:
                pass
