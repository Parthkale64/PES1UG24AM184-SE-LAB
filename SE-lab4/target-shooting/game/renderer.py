"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 25, 35)
COLOR_TEXT = (255, 255, 255)
COLOR_COMBO = (255, 215, 0)
COLOR_TIME_LOW = (255, 100, 100)


def draw_scene(surface, targets):
    surface.fill(COLOR_BG)
    for target in targets:
        pygame.draw.circle(surface, target.color, (int(target.x), int(target.y)), target.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(target.x), int(target.y)), target.radius, 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT, center=False):
    """Helper to draw text, optionally centering it on the given position."""
    surf = font.render(text, True, color)
    if center:
        rect = surf.get_rect(center=pos)
        surface.blit(surf, rect)
    else:
        surface.blit(surf, pos)


def draw_hud(surface, font, score, combo, hits, misses, time_left):
    """Draws all on-screen statistics."""
    # Draw Score & Combo
    draw_text(surface, font, f"Score: {score}", (10, 10))
    
    combo_color = COLOR_COMBO if combo > 1 else COLOR_TEXT
    draw_text(surface, font, f"Combo: {combo}x", (10, 40), color=combo_color)
    
    # Draw Hits/Misses
    draw_text(surface, font, f"Hits: {hits}  Misses: {misses}", (10, HEIGHT - 35))

    # Draw Timer (Right-aligned, turns red at 5 seconds)
    time_color = COLOR_TIME_LOW if time_left <= 5 else COLOR_TEXT
    time_str = f"Time: {max(0, int(time_left))}s"
    time_surf = font.render(time_str, True, time_color)
    surface.blit(time_surf, (WIDTH - time_surf.get_width() - 15, 10))


def draw_game_over(surface, font, final_score):
    """Draws the game over overlay and final score."""
    # Dark semi-transparent background overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(190)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    
    # Game Over Text
    draw_text(surface, font, "TIME'S UP!", (WIDTH // 2, HEIGHT // 2 - 40), color=COLOR_TIME_LOW, center=True)
    draw_text(surface, font, f"Final Score: {final_score}", (WIDTH // 2, HEIGHT // 2), color=COLOR_COMBO, center=True)
    draw_text(surface, font, "Click anywhere or press SPACE to restart", (WIDTH // 2, HEIGHT // 2 + 50), color=COLOR_TEXT, center=True)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)