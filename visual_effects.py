"""
Enhanced visual effects system for SuperNova.
Advanced screen effects, transitions, and visual feedback.
"""

import pygame
import math
import random


class ScreenEffect:
    """Base class for screen effects."""
    
    def __init__(self, duration_ms):
        self.duration_ms = duration_ms
        self.elapsed_ms = 0
        self.is_active = True
    
    def update(self, delta_ms):
        """Update effect."""
        self.elapsed_ms += delta_ms
        if self.elapsed_ms >= self.duration_ms:
            self.is_active = False
    
    def get_progress(self):
        """Get effect progress (0.0 to 1.0)."""
        if self.duration_ms == 0:
            return 1.0
        return min(1.0, self.elapsed_ms / self.duration_ms)
    
    def apply(self, surface):
        """Apply effect to surface. Override in subclass."""
        pass


class ScreenShakeEffect(ScreenEffect):
    """Screen shake effect."""
    
    def __init__(self, intensity=5, duration_ms=100):
        super().__init__(duration_ms)
        self.intensity = intensity
        self.offset = [0, 0]
    
    def update(self, delta_ms):
        """Update shake."""
        super().update(delta_ms)
        
        # Decrease intensity over time
        progress = self.get_progress()
        current_intensity = self.intensity * (1 - progress)
        
        # Random offset
        self.offset[0] = random.uniform(-current_intensity, current_intensity)
        self.offset[1] = random.uniform(-current_intensity, current_intensity)
    
    def get_offset(self):
        """Get offset to apply to screen."""
        return self.offset


class ScreenFlashEffect(ScreenEffect):
    """Screen flash effect."""
    
    def __init__(self, color=(255, 255, 255), intensity=0.5, duration_ms=100):
        super().__init__(duration_ms)
        self.color = color
        self.intensity = intensity
    
    def get_alpha(self):
        """Get current alpha."""
        progress = self.get_progress()
        # Fade out after peak
        if progress < 0.5:
            return int(255 * self.intensity * (progress * 2))
        else:
            return int(255 * self.intensity * ((1 - progress) * 2))
    
    def apply(self, surface):
        """Apply flash to surface."""
        alpha = self.get_alpha()
        if alpha > 0:
            flash_surface = pygame.Surface(surface.get_size())
            flash_surface.fill(self.color)
            flash_surface.set_alpha(alpha)
            surface.blit(flash_surface, (0, 0))


class ChromaticAberrationEffect(ScreenEffect):
    """Chromatic aberration (color separation) effect."""
    
    def __init__(self, amount=3, duration_ms=100):
        super().__init__(duration_ms)
        self.amount = amount
    
    def apply(self, surface, screen_size):
        """Apply chromatic aberration."""
        progress = self.get_progress()
        current_amount = int(self.amount * (1 - progress))
        
        if current_amount == 0:
            return surface
        
        # Create copies for each color channel
        width, height = screen_size
        original = surface.copy()
        
        # Shift red channel
        surface.fill((0, 0, 0))
        red_shift = pygame.Surface((width + current_amount * 2, height), pygame.SRCALPHA)
        red_bits = pygame.surfarray.pixels3d(original)
        # This is simplified - full implementation would use proper channel separation
        
        return surface


class PixelateEffect(ScreenEffect):
    """Pixelation effect."""
    
    def __init__(self, pixel_size=4, duration_ms=200):
        super().__init__(duration_ms)
        self.pixel_size = pixel_size
    
    def apply(self, surface):
        """Apply pixelation."""
        progress = self.get_progress()
        
        if progress >= 1.0:
            return surface
        
        # Calculate size based on progress
        current_size = max(1, int(self.pixel_size * (1 - progress)))
        
        # Scale down and up for pixelation effect
        width, height = surface.get_size()
        small = pygame.transform.scale(surface, (width // current_size, height // current_size))
        pixelated = pygame.transform.scale(small, (width, height))
        
        return pixelated


class GlitchEffect(ScreenEffect):
    """Digital glitch effect."""
    
    def __init__(self, intensity=0.1, duration_ms=150):
        super().__init__(duration_ms)
        self.intensity = intensity
        self.glitch_lines = []
    
    def update(self, delta_ms):
        """Update glitch."""
        super().update(delta_ms)
        
        # Randomly generate glitch lines
        if random.random() < 0.3:
            self.glitch_lines.append({
                "y": random.randint(0, 600),
                "height": random.randint(10, 50),
                "offset": random.randint(-10, 10)
            })
        
        # Remove old lines
        self.glitch_lines = [line for line in self.glitch_lines if random.random() < 0.8]
    
    def apply(self, surface, glitch_lines=None):
        """Apply glitch effect."""
        if glitch_lines is None:
            glitch_lines = self.glitch_lines
        
        result = surface.copy()
        
        for line in glitch_lines:
            y = line["y"]
            height = line["height"]
            offset = line["offset"]
            
            if y + height < result.get_height():
                # Extract scanline
                scanline = result.subsurface((0, y, result.get_width(), height))
                # Shift it
                shifted = pygame.transform.rotate(scanline, 0)
                result.blit(shifted, (offset, y))
        
        return result


class ColorShiftEffect(ScreenEffect):
    """Color shift effect."""
    
    def __init__(self, target_color=(255, 100, 100), intensity=0.3, duration_ms=200):
        super().__init__(duration_ms)
        self.target_color = target_color
        self.intensity = intensity
    
    def apply(self, surface):
        """Apply color shift."""
        progress = self.get_progress()
        
        # Fade in then out
        if progress < 0.5:
            current_alpha = int(255 * self.intensity * (progress * 2))
        else:
            current_alpha = int(255 * self.intensity * ((1 - progress) * 2))
        
        if current_alpha > 0:
            overlay = pygame.Surface(surface.get_size())
            overlay.fill(self.target_color)
            overlay.set_alpha(current_alpha)
            surface.blit(overlay, (0, 0))


class EffectsManager:
    """Manages all screen effects."""
    
    def __init__(self, screen_size=(800, 600)):
        self.screen_size = screen_size
        self.effects = []
    
    def add_shake(self, intensity=5, duration_ms=100):
        """Add screen shake."""
        self.effects.append(ScreenShakeEffect(intensity, duration_ms))
    
    def add_flash(self, color=(255, 255, 255), intensity=0.5, duration_ms=100):
        """Add screen flash."""
        self.effects.append(ScreenFlashEffect(color, intensity, duration_ms))
    
    def add_glitch(self, intensity=0.1, duration_ms=150):
        """Add glitch effect."""
        self.effects.append(GlitchEffect(intensity, duration_ms))
    
    def add_color_shift(self, color=(255, 100, 100), intensity=0.3, duration_ms=200):
        """Add color shift."""
        self.effects.append(ColorShiftEffect(color, intensity, duration_ms))
    
    def add_pixelate(self, pixel_size=4, duration_ms=200):
        """Add pixelation."""
        self.effects.append(PixelateEffect(pixel_size, duration_ms))
    
    def update(self, delta_ms):
        """Update all effects."""
        for effect in self.effects[:]:
            effect.update(delta_ms)
            if not effect.is_active:
                self.effects.remove(effect)
    
    def get_shake_offset(self):
        """Get shake offset from active shake effects."""
        for effect in self.effects:
            if isinstance(effect, ScreenShakeEffect) and effect.is_active:
                return effect.get_offset()
        return [0, 0]
    
    def apply_effects(self, surface):
        """Apply all active effects to surface."""
        result = surface.copy()
        
        for effect in self.effects:
            if isinstance(effect, ScreenFlashEffect) and effect.is_active:
                effect.apply(result)
            elif isinstance(effect, GlitchEffect) and effect.is_active:
                result = effect.apply(result)
            elif isinstance(effect, ColorShiftEffect) and effect.is_active:
                effect.apply(result)
            elif isinstance(effect, PixelateEffect) and effect.is_active:
                result = effect.apply(result)
        
        return result


class TransitionEffect:
    """Smooth screen transitions."""
    
    def __init__(self, transition_type="fade", duration_ms=500):
        self.transition_type = transition_type
        self.duration_ms = duration_ms
        self.elapsed_ms = 0
        self.is_complete = False
    
    def update(self, delta_ms):
        """Update transition."""
        self.elapsed_ms += delta_ms
        if self.elapsed_ms >= self.duration_ms:
            self.is_complete = True
    
    def get_alpha(self):
        """Get alpha for transition."""
        progress = min(1.0, self.elapsed_ms / self.duration_ms)
        
        if self.transition_type == "fade":
            return int(255 * progress)
        elif self.transition_type == "fade_out":
            return int(255 * (1 - progress))
        
        return 255
    
    def draw(self, surface):
        """Draw transition overlay."""
        if self.is_complete:
            return
        
        overlay = pygame.Surface(surface.get_size())
        overlay.fill((0, 0, 0))
        overlay.set_alpha(self.get_alpha())
        surface.blit(overlay, (0, 0))
