"""
hit_detection: figures out whether a click landed on a target.
"""
import math


def check_hit(targets, click_pos):
    """
    Returns the target that was clicked, or None if the click missed
    every target.
    """
    click_x, click_y = click_pos
    
    for target in targets:
        # Calculate the distance between click and the target's center
        distance = math.hypot(target.x - click_x, target.y - click_y)
        
        # If the distance is less than or equal to the radius, it's a hit
        if distance <= target.radius:
            return target
            
    return None