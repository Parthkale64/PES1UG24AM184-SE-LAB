"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def get_bounding_rect(self):
        """A square bounding box around the circle."""
        # Offset the top-left corner by the radius so (x,y) remains the center
        return pygame.Rect(
            self.x - self.radius, 
            self.y - self.radius, 
            self.radius * 2, 
            self.radius * 2
        )