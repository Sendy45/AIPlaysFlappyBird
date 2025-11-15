import math
import pygame
from Bird import Bird
from Pipe import Pipe

# Calc distance between circle and rect
def circle_rect_dist(cx, cy, rect) -> float:
    # Finding the closest point of the rect to the circle
    # min(cx, rect.right) - prevents always picking the right side
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))

    # Calculating distance to the point
    dx = cx - closest_x
    dy = cy - closest_y

    return math.sqrt(dx * dx + dy * dy)

# Check if circle and rect collide
def circle_rect_collision(cx, cy, r, rect) -> bool:

    # Collides if distance < radius
    return circle_rect_dist(cx, cy, rect) < r

# Check if bird and pipe collide
def bird_pipe_collision(bird: Bird, pipe: Pipe) -> bool:
    # Pipe is made of 2 rects
    top_rect = pipe.get_top_part()
    bottom_rect = pipe.get_bottom_part()

    # Return if bird collide with one of the rects
    return (
            circle_rect_collision(bird.x, bird.y, bird.radius, top_rect) or
            circle_rect_collision(bird.x, bird.y, bird.radius, bottom_rect)
    )

# Check if bird and walls collide
def bird_walls_collision(bird: Bird, screen: pygame.Surface) -> bool:
    return (bird.y + bird.radius > screen.get_height()  # bottom
            or bird.y - bird.radius < 0) # top