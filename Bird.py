import pygame
from Genome import Genome

class Bird:
    # Change in velocity on flap
    flap_strength = 300
    def __init__(self, y: int):
        self.x = 40
        self.y = y # Screen Height // 2
        self.radius = 30
        self.velocity = 0
        self.gravity = 800
        self.genome = Genome(4, 6, 1) # NN
        self.score = 0 # Pipes cleared
        self.fitness = 0 # GA fitness function
        self.alive = True

    # Free falling calc
    def update(self, dt):
        self.velocity += self.gravity * dt
        self.y += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)

    # Set velocity to flap_strength
    def flap(self):
        self.velocity = -Bird.flap_strength # positive velocity going down
