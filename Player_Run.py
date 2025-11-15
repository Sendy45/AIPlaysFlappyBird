import pygame

from Bird import Bird
from Pipe import Pipe
from collision_detection import bird_walls_collision, bird_pipe_collision

def run_game() -> int:
    # pygame settings init
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    running = True
    clock = pygame.time.Clock()
    FPS = 60

    bird = Bird(screen.get_height()//2)
    pipes = [Pipe(screen.get_width(), screen.get_height())]

    pipe_interval = 400 # distance between pipes

    # Game loop
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            # Close event
            if event.type == pygame.QUIT:
                running = False

            # Flap on space key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        # Clear screen
        screen.fill((0, 200, 255))

        # Update and draw bird
        bird.draw(screen)
        bird.update(dt)

        # Draw and move pipes
        for pipe in pipes:
            pipe.update(dt)
            pipe.draw(screen)

        # Bird died
        if bird_pipe_collision(bird, pipes[0]) or bird_walls_collision(bird, screen):
            running = False

        # Add new pipe
        if pipes[-1].get_top_part().x < pipe_interval:
            pipes.append(Pipe(screen.get_width(), screen.get_height()))

        # Pipe cleared
        if pipes[0].get_top_part().right < 0:
            pipes.pop(0) # delete pipe
            bird.score += 1 # increase score

        # Show current score
        font = pygame.font.Font(None, 100)  # None = default font
        img = font.render(str(bird.score), True, "red")
        screen.blit(img, (0, 0))

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return bird.score

if __name__ == "__main__":
    print(run_game())