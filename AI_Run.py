import math
import random

import pygame
import numpy as np
from Bird import Bird
from Pipe import Pipe
from Genome import Genome

def initialize_population(pop_size: int, y: int):
    return [Bird(y) for _ in range(pop_size)]

def selection(population: list[Bird], y: int, elites: int):
    # sort population by score and get the top birds
    elites = sorted(population, key=lambda x: x.fitness, reverse=True)[:elites]
    new_population = elites.copy()

    while len(new_population) < len(population):
        p1, p2 = random.sample(elites, 2)

        child = Genome.crossover(p1.genome, p2.genome)

        # create new bird
        new_bird = Bird(y)
        new_bird.genome.weights = child
        new_bird.genome.mutate()
        new_population.append(new_bird)

    return new_population

def circle_rect_dist(cx, cy, rect):
    # Finding the closest point of the rect to the circle
    # min(cx, rect.right) - prevents always picking the right side
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))

    # Calculating distance to the point
    dx = cx - closest_x
    dy = cy - closest_y

    return math.sqrt(dx * dx + dy * dy)

def circle_rect_collision(cx, cy, r, rect):

    # Collides if distance < radius
    return circle_rect_dist(cx, cy, rect) < r

def bird_pipe_collision(bird: Bird, pipe: Pipe):
    top_rect = pipe.get_top_part()
    bottom_rect = pipe.get_bottom_part()

    return (
            circle_rect_collision(bird.x, bird.y, bird.radius, top_rect) or
            circle_rect_collision(bird.x, bird.y, bird.radius, bottom_rect)
    )

def bird_walls_collision(bird: Bird, screen: pygame.Surface):
    return bird.y + bird.radius > screen.get_height() or bird.y - bird.radius < 0


def run_simulation(birds: list[Bird], screen: pygame.Surface, total_score: int) -> list[Bird]:
    pygame.init()

    clock = pygame.time.Clock()
    FPS = 60

    time_passed = 0

    pipes = [Pipe(screen.get_width(), screen.get_height())]

    pipe_interval = 400

    best_score = 0

    while True:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return birds

        screen.fill((0, 200, 255))

        for bird in (b for b in birds if b.alive):
            # Inputs for NN
            top_pipe_dist = circle_rect_dist(bird.x, bird.y, pipes[0].get_top_part())
            bottom_pipe_dist = circle_rect_dist(bird.x, bird.y, pipes[0].get_bottom_part())
            x = np.array([bird.y, bird.velocity, top_pipe_dist, bottom_pipe_dist])
            # Decide whether to flap or not
            bird.flap() if bird.genome.forward(x) > 0.5 else None

            bird.draw(screen)
            bird.update(dt)

            # Bird died to height
            if bird_walls_collision(bird, screen):
                bird.fitness += time_passed
                bird.fitness -= 100 # punish
                bird.alive = False

            # Bird died to pipe
            if bird_pipe_collision(bird, pipes[0]):
                bird.fitness += time_passed
                bird.fitness -= 50
                bird.alive = False


        # Draw and move pipes
        for pipe in pipes:
            pipe.update(dt)
            pipe.draw(screen)

        # Add new pipe
        if pipes[-1].get_top_part().x < pipe_interval:
            pipes.append(Pipe(screen.get_width(), screen.get_height()))

        # Delete passed pipe and add scores
        if pipes[0].get_top_part().right < 0:
            pipes.pop(0)

            for b in (x for x in birds if x.alive):
                b.fitness += 100 # Treat
                b.score += 1
                if b.score > best_score:
                    best_score = b.score
                if b.score >= total_score:
                    b.alive = False

        # End run
        if not any(b.alive for b in birds):
            return birds

        # Show current score
        font = pygame.font.Font(None, 100)  # None = default font
        img = font.render(str(best_score), True, "red")
        screen.blit(img, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)
        time_passed += dt

if __name__ == "__main__":
    generations = 50
    pop_size = 100
    total_score = 5
    screen = pygame.display.set_mode((800, 600))
    init_y = screen.get_height()//2
    birds = initialize_population(pop_size, init_y)

    for gen in range(generations):

        birds = run_simulation(birds, screen, total_score)

        print(max(b.score for b in birds))

        birds = selection(birds, init_y, 5)

        for b in birds:
            b.alive = True
            b.score = 0
            b.fitness = 0
            b.y = init_y
            b.velocity = 0

        if gen % 10 == 0:
            total_score += 5

    print(birds[0].genome.weights)
