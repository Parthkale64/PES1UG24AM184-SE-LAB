"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 25, 35)
COLOR_TEXT = (255, 255, 255)
COLOR_COMBO = (255, 200, 50)  # Highlight color for active combos


def draw_scene(surface, targets):
    surface.fill(COLOR_BG)
    for target in targets:
        pygame.draw.circle(surface, target.color, (int(target.x), int(target.y)), target.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(target.x), int(target.y)), target.radius, 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_hud(surface, font, score, combo, hits, misses):
    """Draws the Heads Up Display with score, combo, and stats."""
    # Main stats row
    stats_text = f"Score: {score}    Hits: {hits}    Misses: {misses}"
    draw_text(surface, font, stats_text, (10, 10))
    
    # Combo multiplier (drawn below the main stats)
    combo_text = f"Combo: {combo}x"
    # Highlight the combo text in gold if the player has a streak going
    color = COLOR_COMBO if combo > 1 else COLOR_TEXT
    draw_text(surface, font, combo_text, (10, 40), color=color)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)