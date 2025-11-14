import pygame
class Bird:
    flap_strength = 250
    def __init__(self, y: int):
        self.x = 40
        self.y = y # Screen Height // 2
        self.radius = 20
        self.velocity = 0
        self.gravity = 500

    def update(self, dt):
        self.velocity += self.gravity * dt
        self.y += self.velocity * dt

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)

    def flap(self):
        self.velocity = -Bird.flap_strength
