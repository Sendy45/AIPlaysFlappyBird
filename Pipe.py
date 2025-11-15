import random

import pygame

class Pipe:
    opening = 200 # gap length
    width = 80
    velocity = 200 # on x axis
    def __init__(self, x: int, scree_height: int):
        # Generate opening in random place
        y_opening = random.randint(40, 300)
        # Pipe made out of 2 rects
        self._top_part = pygame.Rect(x, 0, Pipe.width, y_opening)
        self._bottom_part = pygame.Rect(x, y_opening + Pipe.opening, Pipe.width, scree_height - y_opening - Pipe.opening)

    def get_top_part(self):
        return self._top_part

    def get_bottom_part(self):
        return self._bottom_part

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self._top_part)
        pygame.draw.rect(screen, (0, 255, 0), self._bottom_part)

    def update(self, dt):
        self._top_part.x -= Pipe.velocity * dt
        self._bottom_part.x -= Pipe.velocity * dt
