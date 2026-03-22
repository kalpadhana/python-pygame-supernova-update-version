

# ████████████████████████████████████████████████████████████████████████████████
# ██                        MODERN PARTICLE EFFECTS                             ██
# ████████████████████████████████████████████████████████████████████████████████

import pygame
import random
import math

class Particle:
    """Individual particle for particle effects"""
    def __init__(self, x, y, vx, vy, lifetime, color=(100, 200, 255), size=5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size
        self.gravity = 0.1
        
    def update(self, dt=1/60):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += self.gravity
        self.lifetime -= dt
        
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = int((self.lifetime / self.max_lifetime) * 255)
            size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)

class ParticleSystem:
    """Manages multiple particle effects"""
    def __init__(self):
        self.particles = []
        
    def add_particle(self, particle):
        self.particles.append(particle)
        
    def emit_burst(self, x, y, count=20, speed_range=(2, 8), 
                   color=(100, 200, 255), lifetime=1.0):
        """Create a burst of particles"""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            
            particle = Particle(x, y, vx, vy, lifetime, color)
            self.add_particle(particle)
            
    def emit_line(self, x1, y1, x2, y2, count=15, 
                  color=(100, 200, 255), lifetime=0.8):
        """Create particles along a line"""
        for i in range(count):
            t = i / count
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            
            angle = math.atan2(y2 - y1, x2 - x1)
            vx = random.uniform(-1, 3) * math.cos(angle)
            vy = random.uniform(-1, 3) * math.sin(angle)
            
            particle = Particle(x, y, vx, vy, lifetime, color)
            self.add_particle(particle)
            
    def emit_ring(self, x, y, radius=100, count=30, 
                  color=(100, 200, 255), lifetime=1.0):
        """Create particles in a ring pattern"""
        for i in range(count):
            angle = (2 * math.pi * i) / count
            vx = radius * math.cos(angle) * 2
            vy = radius * math.sin(angle) * 2
            
            particle = Particle(x, y, vx, vy, lifetime, color, size=4)
            self.add_particle(particle)
            
    def update(self, dt=1/60):
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update(dt)
            
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)
            
    def get_count(self):
        return len(self.particles)

class ScreenShake:
    """Screen shake effect"""
    def __init__(self, intensity=5, duration=0.2):
        self.intensity = intensity
        self.duration = duration
        self.elapsed = 0
        
    def update(self, dt=1/60):
        if self.elapsed < self.duration:
            self.elapsed += dt
            return True
        return False
        
    def get_offset(self):
        if self.elapsed < self.duration:
            progress = self.elapsed / self.duration
            shake_amount = self.intensity * (1 - progress)
            return (random.uniform(-shake_amount, shake_amount),
                   random.uniform(-shake_amount, shake_amount))
        return (0, 0)

class ScreenFlash:
    """Screen flash effect"""
    def __init__(self, color=(255, 255, 255), duration=0.1):
        self.color = color
        self.duration = duration
        self.elapsed = 0
        
    def update(self, dt=1/60):
        if self.elapsed < self.duration:
            self.elapsed += dt
            return True
        return False
        
    def get_alpha(self):
        if self.elapsed < self.duration:
            progress = self.elapsed / self.duration
            return int(255 * (1 - progress))
        return 0
        
    def draw(self, screen):
        if self.elapsed < self.duration:
            flash_surface = pygame.Surface((screen.get_width(), screen.get_height()))
            flash_surface.set_alpha(self.get_alpha())
            flash_surface.fill(self.color)
            screen.blit(flash_surface, (0, 0))

class GlitchEffect:
    """Digital glitch effect"""
    def __init__(self, duration=0.3):
        self.duration = duration
        self.elapsed = 0
        self.glitch_lines = []
        
    def update(self, dt=1/60):
        if self.elapsed < self.duration:
            self.elapsed += dt
            # Generate random glitch lines
            self.glitch_lines = [(random.randint(0, 720), random.randint(5, 50)) 
                                for _ in range(random.randint(3, 8))]
            return True
        return False
        
    def get_progress(self):
        return min(1.0, self.elapsed / self.duration)
        
    def apply(self, screen):
        if self.elapsed < self.duration:
            surface_copy = screen.copy()
            for y, height in self.glitch_lines:
                if random.choice([True, False]):
                    offset = random.randint(-10, 10)
                    screen.blit(surface_copy, (offset, y), 
                               (0, y, screen.get_width(), height))
