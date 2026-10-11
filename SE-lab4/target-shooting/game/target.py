"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame
import random


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
        # Assign random x/y velocities with at least two different speed tiers
        speed_tier = random.choice([2, 6])  # 2 = slow target, 6 = fast target
        
        # Multiply by a random direction (-1 or 1) and add a slight random angle variance
        self.vx = random.choice([-1, 1]) * random.uniform(0.7, 1.3) * speed_tier
        self.vy = random.choice([-1, 1]) * random.uniform(0.7, 1.3) * speed_tier

    def move(self, screen_width, screen_height):
        """Advances the target's position and handles edge bouncing."""
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off left/right edges
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -1
        elif self.x + self.radius >= screen_width:
            self.x = screen_width - self.radius
            self.vx *= -1
            
        # Bounce off top/bottom edges
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.vy *= -1
        elif self.y + self.radius >= screen_height:
            self.y = screen_height - self.radius
            self.vy *= -1

    def get_bounding_rect(self):
        """A square bounding box around the circle."""
        return pygame.Rect(
            self.x - self.radius, 
            self.y - self.radius, 
            self.radius * 2, 
            self.radius * 2
        )