"""
GameEngine: owns the targets and handles player clicks.
"""

import random

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
BASE_POINTS = 100


class GameEngine:
    def __init__(self):
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 1

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)
        return Target(x, y, radius=TARGET_RADIUS)

    def handle_click(self, pos):
        target = check_hit(self.targets, pos)
        if target is not None:
            # Register hit: Add score based on combo, increment stats
            self.hits += 1
            self.score += BASE_POINTS * self.combo
            self.combo += 1  # Increase multiplier for the next consecutive hit
            
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            # Register miss: Reset combo multiplier
            self.misses += 1
            self.combo = 1

    def update(self):
        """Updates game state every frame."""
        for target in self.targets:
            target.move(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)
        renderer.draw_hud(surface, font, self.score, self.combo, self.hits, self.misses)