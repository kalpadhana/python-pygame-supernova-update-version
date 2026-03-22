# ████████████████████████████████████████████████████████████████████████████████
# ██                         MODERN UI SYSTEM - GLASSMORPHISM                   ██
# ████████████████████████████████████████████████████████████████████████████████

import pygame
import math

# === COLORS ===
PRIMARY_COLOR = (100, 200, 255)      # Bright cyan/blue
SECONDARY_COLOR = (255, 100, 200)    # Pink/magenta
ACCENT_COLOR = (100, 255, 200)       # Cyan/teal
DARK_BG = (15, 15, 35)               # Very dark blue
LIGHT_TEXT = (230, 230, 250)         # Light blue-white
WARNING_COLOR = (255, 100, 100)      # Red warning

class GlassPanel:
    """Create glassmorphism effect panel"""
    def __init__(self, x, y, width, height, alpha=180, border_color=PRIMARY_COLOR, border_width=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.alpha = alpha
        self.border_color = border_color
        self.border_width = border_width
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
    def draw(self, screen):
        # Draw semi-transparent background
        glass_color = (*DARK_BG, self.alpha)
        pygame.draw.rect(self.surface, glass_color, (0, 0, self.width, self.height), border_radius=10)
        
        # Draw glowing border
        pygame.draw.rect(self.surface, (*self.border_color, 200), 
                        (0, 0, self.width, self.height), 
                        width=self.border_width, border_radius=10)
        
        # Draw top highlight for glass effect
        highlight_height = 2
        highlight_color = (*self.border_color, 100)
        pygame.draw.line(self.surface, highlight_color, (5, 5), (self.width - 5, 5), 2)
        
        screen.blit(self.surface, (self.x, self.y))

class ModernButton:
    """Modern glassmorphism button with animations"""
    def __init__(self, x, y, width, height, text, font_size=32, color=PRIMARY_COLOR):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont('Segoe UI', font_size, bold=True)
        self.color = color
        self.hover = False
        self.click_time = 0
        self.animation_progress = 0
        self.alpha = 200
        
    def update(self, mouse_pos, dt=1/60):
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Smooth animation
        target_alpha = 255 if self.hover else 200
        self.alpha += (target_alpha - self.alpha) * 0.1
        
        if self.click_time > 0:
            self.click_time -= dt
            self.animation_progress = max(0, self.click_time / 0.2)
        
    def draw(self, screen):
        # Draw glass panel
        panel = GlassPanel(self.rect.x, self.rect.y, self.rect.width, 
                          self.rect.height, int(self.alpha), self.color, 2)
        panel.draw(screen)
        
        # Draw pulsing glow effect on hover
        if self.hover:
            glow_surface = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            glow_color = (*self.color, 50)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, self.rect.width + 10, self.rect.height + 10), 
                           border_radius=12)
            screen.blit(glow_surface, (self.rect.x - 5, self.rect.y - 5))
        
        # Draw text
        text_surface = self.font.render(self.text, True, LIGHT_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self):
        return self.hover and self.click_time <= 0

class ModernHealthBar:
    """Modern animated health bar with glassmorphism"""
    def __init__(self, x, y, width=200, height=30, max_hp=200):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.display_hp = max_hp  # For smooth animation
        self.label = "HEALTH"
        
    def update(self, current_hp, dt=1/60):
        self.current_hp = current_hp
        # Smooth transition
        self.display_hp += (current_hp - self.display_hp) * 0.15
        
    def draw(self, screen):
        # Draw background panel
        panel = GlassPanel(self.x - 5, self.y - 5, self.width + 10, 
                          self.height + 20, 200, PRIMARY_COLOR, 1)
        panel.draw(screen)
        
        # Draw label
        font_small = pygame.font.SysFont('Segoe UI', 16, bold=True)
        label_text = font_small.render(self.label, True, PRIMARY_COLOR)
        screen.blit(label_text, (self.x, self.y - 5))
        
        # Draw health bar background
        bar_rect = pygame.Rect(self.x, self.y + 15, self.width, self.height)
        pygame.draw.rect(screen, (50, 50, 80), bar_rect, border_radius=5)
        pygame.draw.rect(screen, PRIMARY_COLOR, bar_rect, width=1, border_radius=5)
        
        # Draw health bar fill with gradient effect
        fill_width = max(0, (self.display_hp / self.max_hp) * self.width)
        fill_rect = pygame.Rect(self.x, self.y + 15, fill_width, self.height)
        
        # Color changes based on health
        if self.display_hp > self.max_hp * 0.5:
            bar_color = ACCENT_COLOR
        elif self.display_hp > self.max_hp * 0.25:
            bar_color = (255, 200, 100)  # Orange
        else:
            bar_color = WARNING_COLOR
        
        pygame.draw.rect(screen, bar_color, fill_rect, border_radius=5)
        
        # Draw HP text
        font = pygame.font.SysFont('Segoe UI', 20, bold=True)
        hp_text = font.render(f"{int(self.display_hp)}/{int(self.max_hp)}", True, LIGHT_TEXT)
        text_rect = hp_text.get_rect(center=bar_rect.center)
        screen.blit(hp_text, text_rect)

class ModernScore:
    """Modern score display with animations"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.score = 0
        self.display_score = 0
        self.hi_score = 0
        self.pop_ups = []  # For floating score notifications
        
    def update(self, dt=1/60):
        # Smooth score animation
        self.display_score += (self.score - self.display_score) * 0.15
        
        # Update pop-ups
        self.pop_ups = [p for p in self.pop_ups if p['lifetime'] > 0]
        for popup in self.pop_ups:
            popup['lifetime'] -= dt
            
    def add_score(self, amount):
        self.score += amount
        if self.score > self.hi_score:
            self.hi_score = self.score
        self.pop_ups.append({
            'amount': amount,
            'x': self.x,
            'y': self.y,
            'lifetime': 1.0
        })
        
    def draw(self, screen):
        font_large = pygame.font.SysFont('Segoe UI', 48, bold=True)
        font_small = pygame.font.SysFont('Segoe UI', 24, bold=True)
        
        # Draw main score with glass panel
        panel = GlassPanel(self.x - 20, self.y - 20, 250, 80, 200, SECONDARY_COLOR, 2)
        panel.draw(screen)
        
        score_text = font_large.render(f"{int(self.display_score)}", True, SECONDARY_COLOR)
        screen.blit(score_text, (self.x, self.y))
        
        # Draw high score
        hi_score_text = font_small.render(f"HI: {int(self.hi_score)}", True, ACCENT_COLOR)
        screen.blit(hi_score_text, (self.x, self.y + 40))
        
        # Draw pop-up scores
        for popup in self.pop_ups:
            alpha = int(255 * (popup['lifetime'] / 1.0))
            popup_text = pygame.font.SysFont('Segoe UI', 32, bold=True).render(
                f"+{popup['amount']}", True, ACCENT_COLOR
            )
            popup_text.set_alpha(alpha)
            y_offset = (1.0 - popup['lifetime']) * 50
            screen.blit(popup_text, (popup['x'] + 100, popup['y'] - y_offset))

class LoadingScreen:
    """Modern loading screen with animation"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.progress = 0
        self.max_progress = 100
        
    def update(self, dt=1/60):
        if self.progress < self.max_progress:
            self.progress += 100 * dt
            
    def draw(self, screen):
        screen.fill(DARK_BG)
        
        # Draw loading panel
        panel_width = 400
        panel_height = 200
        panel_x = (self.width - panel_width) // 2
        panel_y = (self.height - panel_height) // 2
        
        panel = GlassPanel(panel_x, panel_y, panel_width, panel_height, 220, PRIMARY_COLOR, 2)
        panel.draw(screen)
        
        # Draw loading text
        font = pygame.font.SysFont('Segoe UI', 40, bold=True)
        title_text = font.render("SUPERNOVA", True, PRIMARY_COLOR)
        title_rect = title_text.get_rect(center=(self.width // 2, panel_y + 40))
        screen.blit(title_text, title_rect)
        
        # Draw progress bar
        bar_width = 300
        bar_height = 20
        bar_x = (self.width - bar_width) // 2
        bar_y = panel_y + 120
        
        pygame.draw.rect(screen, (50, 50, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=10)
        pygame.draw.rect(screen, PRIMARY_COLOR, (bar_x, bar_y, bar_width, bar_height), width=1, border_radius=10)
        
        fill_width = (self.progress / self.max_progress) * bar_width
        pygame.draw.rect(screen, ACCENT_COLOR, (bar_x, bar_y, fill_width, bar_height), border_radius=10)

class SmoothTransition:
    """Smooth fade transition between screens"""
    def __init__(self, duration=0.5):
        self.duration = duration
        self.elapsed = 0
        self.is_active = False
        
    def start(self):
        self.is_active = True
        self.elapsed = 0
        
    def update(self, dt=1/60):
        if self.is_active:
            self.elapsed += dt
            if self.elapsed >= self.duration:
                self.is_active = False
                return True
        return False
    
    def get_alpha(self):
        if not self.is_active:
            return 0
        return int((self.elapsed / self.duration) * 255)
    
    def draw_fade(self, screen):
        if self.is_active:
            fade_surface = pygame.Surface((screen.get_width(), screen.get_height()))
            fade_surface.set_alpha(self.get_alpha())
            fade_surface.fill((0, 0, 0))
            screen.blit(fade_surface, (0, 0))
