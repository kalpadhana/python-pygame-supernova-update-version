"""
Advanced UI menu system for SuperNova.
Includes pause menu, settings menu, and game mode selection.
"""

import pygame


class MenuButton:
    """Interactive menu button."""
    
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.color = (100, 200, 255)
        self.hover_color = (150, 230, 255)
        self.text_color = (255, 255, 255)
    
    def draw(self, surface):
        """Draw button."""
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos):
        """Update button state."""
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def click(self):
        """Handle click."""
        if self.action:
            return self.action()
        return True


class PauseMenu:
    """In-game pause menu."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.active = False
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        button_width = 200
        button_height = 50
        center_x = width // 2 - button_width // 2
        
        self.buttons = [
            MenuButton(center_x, 200, button_width, button_height, "Resume", self.font_small, self.resume),
            MenuButton(center_x, 270, button_width, button_height, "Settings", self.font_small, self.settings),
            MenuButton(center_x, 340, button_width, button_height, "Main Menu", self.font_small, self.main_menu),
            MenuButton(center_x, 410, button_width, button_height, "Quit", self.font_small, self.quit_game),
        ]
        
        self.selection = 0
        self.result = None
    
    def resume(self):
        """Resume game."""
        self.active = False
        self.result = "resume"
        return False
    
    def settings(self):
        """Open settings."""
        self.result = "settings"
        return False
    
    def main_menu(self):
        """Return to main menu."""
        self.active = False
        self.result = "menu"
        return False
    
    def quit_game(self):
        """Quit game."""
        self.active = False
        self.result = "quit"
        return False
    
    def toggle(self):
        """Toggle pause menu."""
        self.active = not self.active
        self.result = None
    
    def draw(self, surface):
        """Draw pause menu."""
        if not self.active:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # Title
        title = self.font_large.render("PAUSED", True, (100, 200, 255))
        title_rect = title.get_rect(center=(self.width // 2, 100))
        surface.blit(title, title_rect)
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.hovered:
                    button.click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.resume()
            elif event.key == pygame.K_UP:
                self.selection = (self.selection - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selection = (self.selection + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                self.buttons[self.selection].click()


class SettingsMenu:
    """Game settings menu."""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.active = True
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)
        
        button_width = 150
        button_height = 40
        center_x = width // 2 - button_width // 2
        
        self.settings = {
            "master_volume": 100,
            "music_volume": 80,
            "sfx_volume": 100,
            "display_fps": True,
            "particle_effects": True,
        }
        
        self.buttons = [
            MenuButton(center_x, 450, button_width, button_height, "Back", self.font_small, self.back),
        ]
        
        self.result = None
    
    def back(self):
        """Return from settings."""
        self.active = False
        self.result = "back"
        return False
    
    def draw(self, surface):
        """Draw settings menu."""
        if not self.active:
            return
        
        surface.fill((15, 15, 35))
        
        # Title
        title = self.font_large.render("SETTINGS", True, (100, 200, 255))
        title_rect = title.get_rect(center=(self.width // 2, 50))
        surface.blit(title, title_rect)
        
        # Settings
        y = 150
        for key, value in self.settings.items():
            if isinstance(value, bool):
                text = self.font_small.render(f"{key}: {'ON' if value else 'OFF'}", True, (230, 230, 250))
            else:
                text = self.font_small.render(f"{key}: {value}%", True, (230, 230, 250))
            surface.blit(text, (100, y))
            y += 50
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.hovered:
                    button.click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.back()


class GameModeSelectorMenu:
    """Menu for selecting game mode."""
    
    def __init__(self, modes_list, width=800, height=600):
        self.width = width
        self.height = height
        self.modes = modes_list  # List of (mode_name, description) tuples
        self.selected = 0
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 28)
        self.active = True
        self.result = None
        
        button_width = 150
        button_height = 40
        center_x = width // 2 - button_width // 2
        
        self.buttons = [
            MenuButton(center_x - 100, 520, button_width, button_height, "Select", self.font_small, self.select),
            MenuButton(center_x + 100, 520, button_width, button_height, "Back", self.font_small, self.back),
        ]
    
    def select(self):
        """Select current mode."""
        self.active = False
        self.result = ("select", self.selected)
        return False
    
    def back(self):
        """Return to menu."""
        self.active = False
        self.result = ("back", None)
        return False
    
    def draw(self, surface):
        """Draw mode selector."""
        if not self.active:
            return
        
        surface.fill((15, 15, 35))
        
        # Title
        title = self.font_large.render("SELECT GAME MODE", True, (100, 200, 255))
        title_rect = title.get_rect(center=(self.width // 2, 50))
        surface.blit(title, title_rect)
        
        # Mode list
        y = 150
        for i, (mode_name, description) in enumerate(self.modes):
            if i == self.selected:
                # Highlighted
                pygame.draw.rect(surface, (100, 200, 255), (50, y - 5, self.width - 100, 60), 3)
                color = (150, 230, 255)
            else:
                color = (230, 230, 250)
            
            name_text = self.font_small.render(mode_name, True, color)
            desc_text = self.font_small.render(description, True, (180, 180, 200))
            surface.blit(name_text, (80, y))
            surface.blit(desc_text, (80, y + 30))
            y += 100
        
        # Draw buttons
        for button in self.buttons:
            button.draw(surface)
    
    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.update(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.hovered:
                    button.click()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.modes)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.modes)
            elif event.key == pygame.K_RETURN:
                self.select()
            elif event.key == pygame.K_ESCAPE:
                self.back()
