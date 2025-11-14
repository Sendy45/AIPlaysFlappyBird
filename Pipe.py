import pygame
from pygame import surface


class Pipe:
    opening = 200
    width = 80
    velocity = 200
    def __init__(self, x: int, scree_height: int):
        y_opening = 80
        self._top_part = pygame.Rect(x, 0, Pipe.width, y_opening)
        self._bottom_part = pygame.Rect(x, y_opening + Pipe.opening, Pipe.width, scree_height - y_opening - Pipe.opening)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self._top_part)
        pygame.draw.rect(screen, (0, 255, 0), self._bottom_part)

    def update(self, dt):
        self._top_part.x -= Pipe.velocity * dt
        self._bottom_part.x -= Pipe.velocity * dt
