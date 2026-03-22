"""
Sound effects system for SuperNova.
Manages loading, caching, and playing sound effects with volume control.
"""

import pygame
import os
from pathlib import Path


class SoundEffect:
    """Wrapper for a single sound effect."""
    
    def __init__(self, sound, volume=1.0):
        self.sound = sound
        self.volume = volume
        if sound:
            self.sound.set_volume(volume)
    
    def play(self, loops=0):
        """Play the sound."""
        if self.sound:
            self.sound.play(loops)
    
    def stop(self):
        """Stop the sound."""
        if self.sound:
            self.sound.stop()
    
    def set_volume(self, volume):
        """Set sound volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.sound:
            self.sound.set_volume(self.volume)


class SoundManager:
    """Manages all game sounds."""
    
    def __init__(self, sound_dir="game_sounds"):
        self.sound_dir = sound_dir
        self.sounds = {}
        self.master_volume = 100
        self.music_volume = 80
        self.sfx_volume = 100
        self.muted = False
        
        # Initialize mixer
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound files."""
        # Define sound paths
        sound_files = {
            # Weapon sounds
            "shoot_basic": "shooting/basic_shot.wav",
            "shoot_spread": "shooting/spread_shot.wav",
            "shoot_rapid": "shooting/rapid_shot.wav",
            "shoot_plasma": "shooting/plasma_shot.wav",
            
            # Damage sounds
            "hit": "damage/hit.wav",
            "player_hit": "damage/player_hit.wav",
            "player_death": "damage/death.wav",
            
            # Explosion sounds
            "explosion": "explosions/explosion.wav",
            "explosion_large": "explosions/explosion_large.wav",
            "explosion_boss": "explosions/explosion_boss.wav",
            
            # Power-up sounds
            "pickup_health": "refill/health_pickup.wav",
            "pickup_ammo": "refill/ammo_pickup.wav",
            "pickup_shield": "refill/shield_pickup.wav",
            "pickup_speed": "refill/speed_pickup.wav",
        }
        
        # Load sounds
        for key, relative_path in sound_files.items():
            full_path = os.path.join(self.sound_dir, relative_path)
            try:
                if os.path.exists(full_path):
                    sound = pygame.mixer.Sound(full_path)
                    self.sounds[key] = SoundEffect(sound, self._get_volume("sfx"))
                else:
                    # Create silent sound if file doesn't exist
                    self.sounds[key] = SoundEffect(None, self._get_volume("sfx"))
            except Exception as e:
                print(f"Could not load sound {key}: {e}")
                self.sounds[key] = SoundEffect(None, self._get_volume("sfx"))
    
    def _get_volume(self, volume_type):
        """Get volume level."""
        if self.muted:
            return 0.0
        
        volume_map = {
            "master": self.master_volume,
            "music": self.music_volume,
            "sfx": self.sfx_volume
        }
        
        volume = volume_map.get(volume_type, self.sfx_volume)
        return (self.master_volume / 100.0) * (volume / 100.0)
    
    def play(self, sound_key):
        """Play a sound effect."""
        if sound_key in self.sounds:
            self.sounds[sound_key].set_volume(self._get_volume("sfx"))
            self.sounds[sound_key].play()
    
    def set_master_volume(self, volume):
        """Set master volume (0-100)."""
        self.master_volume = max(0, min(100, volume))
        self._update_all_volumes()
    
    def set_music_volume(self, volume):
        """Set music volume (0-100)."""
        self.music_volume = max(0, min(100, volume))
        self._update_all_volumes()
    
    def set_sfx_volume(self, volume):
        """Set SFX volume (0-100)."""
        self.sfx_volume = max(0, min(100, volume))
        self._update_all_volumes()
    
    def _update_all_volumes(self):
        """Update all sound volumes."""
        for sound in self.sounds.values():
            sound.set_volume(self._get_volume("sfx"))
    
    def toggle_mute(self):
        """Toggle mute."""
        self.muted = not self.muted
        if self.muted:
            pygame.mixer.stop()
    
    def stop_all(self):
        """Stop all sounds."""
        pygame.mixer.stop()
    
    def get_volume_percent(self):
        """Get current master volume percentage."""
        return self.master_volume


class SoundEventBus:
    """Centralized event system for sound triggering."""
    
    def __init__(self, sound_manager):
        self.sound_manager = sound_manager
        self.event_map = {
            "player_shoot": "shoot_basic",
            "player_hit": "player_hit",
            "player_death": "player_death",
            "enemy_hit": "hit",
            "enemy_death": "explosion",
            "boss_death": "explosion_boss",
            "power_up_collected": "pickup_health",
        }
    
    def trigger_event(self, event_name):
        """Trigger a sound event."""
        if event_name in self.event_map:
            self.sound_manager.play(self.event_map[event_name])
    
    def trigger_custom(self, sound_key):
        """Trigger a specific sound."""
        self.sound_manager.play(sound_key)
