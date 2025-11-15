import random
import pygame
import numpy as np
from Bird import Bird
from Pipe import Pipe
from Genome import Genome
from collision_detection import bird_walls_collision, bird_pipe_collision, circle_rect_dist

# Create population of birds
def initialize_population(pop_size: int, y: int):
    return [Bird(y) for _ in range(pop_size)]

# Create new population from given one
def selection(population: list[Bird], y: int, elites: int):
    # Selection - sort population by score and get the top birds
    elites = sorted(population, key=lambda x: x.fitness, reverse=True)[:elites]
    new_population = elites.copy()

    # Fill population with children
    while len(new_population) < len(population):
        # Pick two parents from elites
        p1, p2 = random.sample(elites, 2)

        # Create child
        child = Genome.crossover(p1.genome, p2.genome)

        # create new bird
        new_bird = Bird(y)
        new_bird.genome.weights = child
        # Mutate child
        new_bird.genome.mutate()
        new_population.append(new_bird)

    return new_population

# Run the game with given birds for length of given max score
def run_simulation(birds: list[Bird], screen: pygame.Surface, max_score: int) -> list[Bird]:
    # pygame settings init
    pygame.init()
    clock = pygame.time.Clock()
    FPS = 60

    # Create first pipe
    pipes = [Pipe(screen.get_width(), screen.get_height())]

    time_passed = 0 # time passed - for fitness function - better fitness the more time passed
    pipe_interval = 400 # distance between pipes
    best_score = 0 # current best score

    # Game loop
    while True:
        dt = clock.tick(FPS) / 1000

        # Close event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return birds

        # Clear screen
        screen.fill((0, 200, 255))

        # Update for alive birds
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
            pipes.pop(0) # delete pipe

            # Pipe cleared
            for b in (x for x in birds if x.alive):
                b.fitness += 100 # Treat
                b.score += 1
                # update best score
                if b.score > best_score:
                    best_score = b.score
                # check for max score limit
                if b.score >= max_score:
                    b.alive = False

        # End run
        if not any(b.alive for b in birds):
            return birds

        # Show current score
        font = pygame.font.Font(None, 100)  # None = default font
        img = font.render(str(best_score), True, "red")
        screen.blit(img, (0, 0))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)
        time_passed += dt

# Run GA
def train_genome(screen: pygame.Surface, generations: int = 50, pop_size: int = 100, max_score: int = 5):
    # init population
    init_y = screen.get_height() // 2
    birds = initialize_population(pop_size, init_y)

    # Gen loop
    for gen in range(generations):

        # run game on current population
        birds = run_simulation(birds, screen, max_score)
        # create new population by selection, crossover and mutating
        birds = selection(birds, init_y, 5)

        # reset birds params except for genome
        for b in birds:
            b.alive = True
            b.score = 0
            b.fitness = 0
            b.y = init_y
            b.velocity = 0

        # every 5 gens increase max_score by 5
        if gen % 5 == 0:
            max_score += 5

    # Return best weights
    return birds[0].genome.weights

if __name__ == "__main__":

    screen = pygame.display.set_mode((800, 600))

    bird = Bird(screen.get_height()//2)
    # Best weights - from training
    bird.genome.weights = np.array([ 0.42179982, 0.50880687, -0.74054395, -0.43076414, -0.70014576,  0.8971643,
  0.38076831,  0.075512,   -0.04179982, -0.26675065,  0.42908472,  0.40489284,
  0.59961381,  0.00573561,  0.72654361,  0.36895138, -0.08859479, -0.96075517,
 -0.34951418,  0.38071202, -0.12728991, -0.26444388, -0.30919908,  0.96273918,
  0.27207973, -0.29574524, -0.3959629,   0.78704471,  0.12151073,  0.70993961,
  0.84372252, -0.20440398, -0.7753562,   0.73168496,  0.8655118,  -0.59712017,
  0.71850694])

    print(run_simulation([bird], screen, float('inf'))[0].score)