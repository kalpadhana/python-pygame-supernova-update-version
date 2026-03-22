# ████████████████████████████████████████████████████████████████████████████████
# ██                          LEADERBOARD SYSTEM                                ██
# ████████████████████████████████████████████████████████████████████████████████

import json
import os
from datetime import datetime

LEADERBOARD_FILE = 'leaderboard.json'

class Leaderboard:
    """Modern leaderboard system with persistent storage"""
    
    def __init__(self, max_entries=10):
        self.max_entries = max_entries
        self.scores = []
        self.load()
        
    def load(self):
        """Load leaderboard from file"""
        if os.path.exists(LEADERBOARD_FILE):
            try:
                with open(LEADERBOARD_FILE, 'r') as f:
                    self.scores = json.load(f)
            except:
                self.scores = []
        else:
            self.scores = []
            
    def save(self):
        """Save leaderboard to file"""
        try:
            with open(LEADERBOARD_FILE, 'w') as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            print(f"Error saving leaderboard: {e}")
            
    def add_score(self, score, player_name="Player"):
        """Add a new score to leaderboard"""
        entry = {
            'name': player_name[:15],  # Limit name length
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.scores.append(entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:self.max_entries]
        self.save()
        
    def get_rank(self, score):
        """Get rank of a score"""
        rank = 1
        for entry in self.scores:
            if entry['score'] > score:
                rank += 1
        return rank
        
    def is_high_score(self, score):
        """Check if score qualifies for leaderboard"""
        return len(self.scores) < self.max_entries or score > self.scores[-1]['score']
        
    def get_scores(self):
        """Get all scores sorted"""
        return self.scores
        
    def get_high_score(self):
        """Get highest score"""
        if self.scores:
            return self.scores[0]['score']
        return 0
        
    def clear(self):
        """Clear leaderboard"""
        self.scores = []
        self.save()

class GameStats:
    """Track game statistics"""
    
    def __init__(self):
        self.stats_file = 'game_stats.json'
        self.stats = {
            'total_games': 0,
            'total_score': 0,
            'enemies_defeated': 0,
            'bosses_defeated': 0,
            'playtime_seconds': 0,
            'highest_wave': 0
        }
        self.load()
        
    def load(self):
        """Load stats from file"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    self.stats = json.load(f)
            except:
                pass
                
    def save(self):
        """Save stats to file"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
            
    def add_game(self, score, enemies, bosses, playtime):
        """Add a completed game to stats"""
        self.stats['total_games'] += 1
        self.stats['total_score'] += score
        self.stats['enemies_defeated'] += enemies
        self.stats['bosses_defeated'] += bosses
        self.stats['playtime_seconds'] += playtime
        if score > self.stats.get('highest_wave', 0):
            self.stats['highest_wave'] = score
        self.save()
        
    def get_stats(self):
        """Get all stats"""
        return self.stats
        
    def get_average_score(self):
        """Get average score per game"""
        if self.stats['total_games'] == 0:
            return 0
        return self.stats['total_score'] // self.stats['total_games']
