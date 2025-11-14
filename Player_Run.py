import pygame

from Bird import Bird
from Pipe import Pipe

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    running = True
    clock = pygame.time.Clock()
    FPS = 60
    bird = Bird(screen.get_height()//2)
    pipe = Pipe(screen.get_width(), screen.get_height())

    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        screen.fill((255, 255, 255))
        bird.draw(screen)
        pipe.draw(screen)

        bird.update(dt)
        pipe.update(dt)

        pygame.display.flip()
        clock.tick(FPS)



    pygame.quit()

if __name__ == "__main__":
    run_game()