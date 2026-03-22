"""
Game modes system for SuperNova.
Includes Survival, Time Attack, Endless, and Arcade modes.
"""

import json
import os


class GameMode:
    """Defines a game mode."""
    
    def __init__(self, name, description, rules):
        self.name = name
        self.description = description
        self.rules = rules  # Dict with mode-specific rules


class GameModeManager:
    """Manages different game modes and rules."""
    
    def __init__(self):
        self.current_mode = "survival"
        self.modes = {
            "survival": GameMode(
                name="Survival",
                description="Survive as long as possible. Game ends when health reaches 0.",
                rules={
                    "time_limit": None,
                    "target_score": None,
                    "spawn_wave": True,
                    "enemy_scaling": True,
                    "score_per_enemy": 100,
                    "score_per_boss": 500
                }
            ),
            "time_attack": GameMode(
                name="Time Attack",
                description="Score as many points as possible in 3 minutes.",
                rules={
                    "time_limit": 180000,  # 3 minutes in ms
                    "target_score": None,
                    "spawn_wave": True,
                    "enemy_scaling": True,
                    "score_per_enemy": 150,
                    "score_per_boss": 750
                }
            ),
            "endless": GameMode(
                name="Endless",
                description="How many waves can you survive? Enemies get stronger each wave.",
                rules={
                    "time_limit": None,
                    "target_score": None,
                    "spawn_wave": True,
                    "enemy_scaling": True,
                    "progressive_difficulty": True,
                    "score_per_enemy": 100,
                    "score_per_boss": 500
                }
            ),
            "arcade": GameMode(
                name="Arcade",
                description="Classic mode. Achieve 5000 points to win!",
                rules={
                    "time_limit": None,
                    "target_score": 5000,
                    "spawn_wave": False,
                    "enemy_scaling": False,
                    "score_per_enemy": 100,
                    "score_per_boss": 500
                }
            ),
        }
        self.load()
    
    def get_current(self):
        """Get current game mode."""
        return self.modes.get(self.current_mode, self.modes["survival"])
    
    def set_mode(self, mode_name):
        """Set game mode."""
        if mode_name in self.modes:
            self.current_mode = mode_name
            return True
        return False
    
    def get_mode_names(self):
        """Get list of mode names."""
        return list(self.modes.keys())
    
    def get_mode_list(self):
        """Get list of mode objects with descriptions."""
        return [(name, self.modes[name].description) for name in self.modes.keys()]
    
    def check_win_condition(self, score, elapsed_time_ms):
        """Check if win condition is met.
        
        Returns:
            (is_win, reason)
        """
        mode = self.get_current()
        rules = mode.rules
        
        # Check target score
        if rules.get("target_score") and score >= rules["target_score"]:
            return True, f"Score goal reached: {score}"
        
        # Check time limit reached
        if rules.get("time_limit") and elapsed_time_ms >= rules["time_limit"]:
            return True, f"Time limit reached!"
        
        return False, ""
    
    def check_lose_condition(self, player_hp, elapsed_time_ms):
        """Check if lose condition is met.
        
        Returns:
            (is_lose, reason)
        """
        # Health depleted
        if player_hp <= 0:
            return True, "Health depleted"
        
        return False, ""
    
    def get_rules(self):
        """Get current mode rules."""
        return self.get_current().rules
    
    def save(self, filename="game_modes.json"):
        """Save game mode preference."""
        data = {"current_mode": self.current_mode}
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self, filename="game_modes.json"):
        """Load game mode preference."""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                    self.current_mode = data.get("current_mode", "survival")
            except:
                pass


class GameState:
    """Tracks overall game state and progress."""
    
    def __init__(self):
        self.score = 0
        self.elapsed_time = 0  # milliseconds
        self.enemies_defeated = 0
        self.bosses_defeated = 0
        self.wave = 1
        self.is_game_over = False
        self.is_won = False
        self.reason = ""
    
    def add_enemy_kill(self, base_score, difficulty_multiplier=1.0):
        """Add score for enemy kill."""
        score = int(base_score * difficulty_multiplier)
        self.score += score
        self.enemies_defeated += 1
        return score
    
    def add_boss_kill(self, base_score, difficulty_multiplier=1.0):
        """Add score for boss kill."""
        score = int(base_score * difficulty_multiplier)
        self.score += score
        self.bosses_defeated += 1
        return score
    
    def next_wave(self):
        """Progress to next wave."""
        self.wave += 1
    
    def set_game_over(self, is_won=False, reason=""):
        """Mark game as over."""
        self.is_game_over = True
        self.is_won = is_won
        self.reason = reason
    
    def reset(self):
        """Reset game state."""
        self.score = 0
        self.elapsed_time = 0
        self.enemies_defeated = 0
        self.bosses_defeated = 0
        self.wave = 1
        self.is_game_over = False
        self.is_won = False
        self.reason = ""
