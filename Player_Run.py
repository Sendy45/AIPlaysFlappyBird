import pygame

from Bird import Bird
from Pipe import Pipe

def circle_rect_collision(cx, cy, r, rect):

    # Finding the closest point of the rect to the circle
    # min(cx, rect.right) - prevents always picking the right side
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top, min(cy, rect.bottom))

    # Calculating distance to the point
    dx = cx - closest_x
    dy = cy - closest_y

    # Collides if distance < radius
    return dx * dx + dy * dy < r * r

def bird_pipe_collision(bird: Bird, pipe: Pipe):
    top_rect = pipe.get_top_part()
    bottom_rect = pipe.get_bottom_part()

    return (
            circle_rect_collision(bird.x, bird.y, bird.radius, top_rect) or
            circle_rect_collision(bird.x, bird.y, bird.radius, bottom_rect)
    )

def bird_walls_collision(bird: Bird, screen: pygame.Surface):
    return bird.y + bird.radius > screen.get_height() or bird.y - bird.radius < 0


def run_game() -> int:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    score = 0

    running = True
    clock = pygame.time.Clock()
    FPS = 60
    bird = Bird(screen.get_height()//2)

    pipes = [Pipe(screen.get_width(), screen.get_height())]

    pipe_interval = 400

    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        screen.fill((0, 200, 255))

        bird.draw(screen)
        bird.update(dt)

        for pipe in pipes:
            pipe.update(dt)
            pipe.draw(screen)

        if bird_pipe_collision(bird, pipes[0]) or bird_walls_collision(bird, screen):
            running = False

        if pipes[-1].get_top_part().x < pipe_interval:
            pipes.append(Pipe(screen.get_width(), screen.get_height()))

        if pipes[0].get_top_part().right < 0:
            pipes.pop(0)
            score += 1

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    return score

if __name__ == "__main__":
    print(run_game())