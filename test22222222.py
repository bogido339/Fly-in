import pygame

pygame.init()
screen = pygame.display.set_mode((500, 500))

CELL_SIZE = 50

points = [
    (0, 0),
    (0, 1),
    (1, 1),
    (2, 2),
]

def grid_to_screen(x, y):
    return x * CELL_SIZE, y * CELL_SIZE

running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for x, y in points:
        px, py = grid_to_screen(x, y)
        pygame.draw.circle(screen, (0, 255, 0), (px + 25, py + 25), 10)

    pygame.display.flip()

pygame.quit()