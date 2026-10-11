"""
GameEngine: owns the targets and handles player clicks, scoring, and game state.
"""

import random
import pygame

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28
BASE_POINTS = 100
ROUND_TIME = 30.0  # 30-second rounds


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Resets all game variables for a fresh round."""
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 1
        
        self.state = "PLAYING"
        self.time_left = ROUND_TIME
        self.last_time = pygame.time.get_ticks()

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)
        return Target(x, y, radius=TARGET_RADIUS)

    def handle_click(self, pos):
        if self.state == "GAME_OVER":
            # Any click restarts the game
            self.reset()
            return

        target = check_hit(self.targets, pos)
        if target is not None:
            self.hits += 1
            self.score += BASE_POINTS * self.combo
            self.combo += 1
            
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            self.misses += 1
            self.combo = 1

    def handle_keydown(self, key):
        """Allows spacebar restarts if hooked up to the main event loop."""
        if self.state == "GAME_OVER" and key == pygame.K_SPACE:
            self.reset()

    def update(self):
        """Updates game state every frame."""
        current_time = pygame.time.get_ticks()
        dt = (current_time - self.last_time) / 1000.0
        self.last_time = current_time

        if self.state == "GAME_OVER":
            return

        # Update timer
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.state = "GAME_OVER"

        # Move targets
        for target in self.targets:
            target.move(WIDTH, HEIGHT)

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)
        renderer.draw_hud(surface, font, self.score, self.combo, self.hits, self.misses, self.time_left)
        
        if self.state == "GAME_OVER":
            renderer.draw_game_over(surface, font, self.score)