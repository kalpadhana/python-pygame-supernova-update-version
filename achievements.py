"""
Achievements system for SuperNova game.
Tracks player accomplishments and unlockable badges.
"""

import json
import os
from datetime import datetime


class Achievement:
    """Individual achievement/badge definition."""
    
    def __init__(self, id, name, description, criteria, icon_char="★"):
        self.id = id
        self.name = name
        self.description = description
        self.criteria = criteria  # Dict with progress thresholds
        self.icon_char = icon_char
        self.unlocked = False
        self.unlock_date = None
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "unlocked": self.unlocked,
            "unlock_date": self.unlock_date
        }


class AchievementSystem:
    """Manages achievements and badges."""
    
    def __init__(self, save_file="achievements.json"):
        self.save_file = save_file
        self.achievements = {}
        self.progress = {}
        self._init_achievements()
        self.load()
    
    def _init_achievements(self):
        """Initialize all achievements."""
        achievements_data = [
            ("first_blood", "First Blood", "Defeat your first enemy", {"enemies": 1}),
            ("headhunter", "Headhunter", "Defeat 10 enemies", {"enemies": 10}),
            ("genocide", "Genocide", "Defeat 50 enemies", {"enemies": 50}),
            ("boss_slayer", "Boss Slayer", "Defeat your first boss", {"bosses": 1}),
            ("champion", "Champion", "Defeat 5 bosses", {"bosses": 5}),
            ("survivor", "Survivor", "Reach 1000 score", {"score": 1000}),
            ("legend", "Legend", "Reach 10000 score", {"score": 10000}),
            ("sharpshooter", "Sharpshooter", "Fire 1000 bullets", {"bullets": 1000}),
            ("damage_dealer", "Damage Dealer", "Deal 5000 total damage", {"damage": 5000}),
            ("no_hit", "Untouchable", "Complete a game without taking damage", {"no_damage": True}),
            ("speedrun", "Speed Runner", "Complete a game in under 60 seconds", {"speedrun": True}),
            ("collector", "Collector", "Collect 20 power-ups", {"powerups": 20}),
        ]
        
        for ach_id, name, desc, criteria in achievements_data:
            self.achievements[ach_id] = Achievement(ach_id, name, desc, criteria)
            self.progress[ach_id] = 0
    
    def update_progress(self, metric, value):
        """Update progress for a specific metric.
        
        Args:
            metric: The metric to track (enemies, bosses, score, bullets, damage, etc.)
            value: The value to add or set
        """
        if metric == "enemies":
            self.progress["enemies"] = self.progress.get("enemies", 0) + value
            self._check_achievement("first_blood", {"enemies": 1})
            self._check_achievement("headhunter", {"enemies": 10})
            self._check_achievement("genocide", {"enemies": 50})
        
        elif metric == "bosses":
            self.progress["bosses"] = self.progress.get("bosses", 0) + value
            self._check_achievement("boss_slayer", {"bosses": 1})
            self._check_achievement("champion", {"bosses": 5})
        
        elif metric == "score":
            self.progress["score"] = max(self.progress.get("score", 0), value)
            self._check_achievement("survivor", {"score": 1000})
            self._check_achievement("legend", {"score": 10000})
        
        elif metric == "bullets":
            self.progress["bullets"] = self.progress.get("bullets", 0) + value
            self._check_achievement("sharpshooter", {"bullets": 1000})
        
        elif metric == "damage":
            self.progress["damage"] = self.progress.get("damage", 0) + value
            self._check_achievement("damage_dealer", {"damage": 5000})
        
        elif metric == "powerups":
            self.progress["powerups"] = self.progress.get("powerups", 0) + value
            self._check_achievement("collector", {"powerups": 20})
    
    def complete_special(self, achievement_id):
        """Unlock a special achievement."""
        if achievement_id in self.achievements and not self.achievements[achievement_id].unlocked:
            self.achievements[achievement_id].unlocked = True
            self.achievements[achievement_id].unlock_date = datetime.now().isoformat()
            return True
        return False
    
    def _check_achievement(self, ach_id, criteria):
        """Check if achievement should be unlocked."""
        if ach_id in self.achievements and not self.achievements[ach_id].unlocked:
            ach = self.achievements[ach_id]
            for key, threshold in criteria.items():
                if self.progress.get(key, 0) >= threshold:
                    self.complete_special(ach_id)
    
    def get_unlocked(self):
        """Get all unlocked achievements."""
        return [ach for ach in self.achievements.values() if ach.unlocked]
    
    def get_progress(self, ach_id):
        """Get progress percentage for an achievement."""
        if ach_id not in self.achievements:
            return 0
        ach = self.achievements[ach_id]
        if ach.unlocked:
            return 100
        
        # Calculate progress based on criteria
        for key, threshold in ach.criteria.items():
            current = self.progress.get(key, 0)
            if isinstance(threshold, (int, float)):
                return min(100, int((current / threshold) * 100))
        
        return 0
    
    def save(self):
        """Save achievements to JSON file."""
        data = {
            "achievements": {ach_id: ach.to_dict() for ach_id, ach in self.achievements.items()},
            "progress": self.progress
        }
        with open(self.save_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self):
        """Load achievements from JSON file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    for ach_id, ach_data in data.get("achievements", {}).items():
                        if ach_id in self.achievements:
                            self.achievements[ach_id].unlocked = ach_data.get("unlocked", False)
                            self.achievements[ach_id].unlock_date = ach_data.get("unlock_date")
                    self.progress = data.get("progress", {})
            except:
                pass
    
    def display_achievements(self, surface, font):
        """Draw achievements panel on screen."""
        unlocked = self.get_unlocked()
        if not unlocked:
            return
        
        y = 60
        for i, ach in enumerate(unlocked[:5]):  # Show top 5
            text = font.render(f"★ {ach.name}", True, (255, 215, 0))
            surface.blit(text, (20, y + i * 30))
