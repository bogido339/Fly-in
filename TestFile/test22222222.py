# import pygame

# pygame.init()
# screen = pygame.display.set_mode((500, 500))

# CELL_SIZE = 50

# points = [
#     (0, 0),
#     (0, 1),
#     (1, 1),
#     (2, 2),
# ]

# def grid_to_screen(x, y):
#     return x * CELL_SIZE, y * CELL_SIZE

# running = True
# while running:
#     screen.fill((0, 0, 0))

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     for x, y in points:
#         px, py = grid_to_screen(x, y)
#         pygame.draw.circle(screen, (0, 255, 0), (px + 25, py + 25), 10)

#     pygame.display.flip()

# pygame.quit()



import pygame
from time import sleep

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# clock = pygame.time.Clock()

zoom = 1
camera_x = 0
camera_y = 0


class Zone:
    def __init__(self, x, y):
        self.x = x
        self.y = y


zones = [
    Zone(-200, 0),
    Zone(0, -100),
    Zone(0, 100),
    Zone(200, 0),
]

connections = [
    (0,1),
    (0,2),
    (1,3),
    (2,3)
]


def world_to_screen(x, y):
    w, h = screen.get_size()

    sx = (x - camera_x) * zoom + w / 2
    sy = (y - camera_y) * zoom + h / 2

    return (int(sx), int(sy))


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            zoom += event.y * 0.1
            zoom = max(0.3, min(3, zoom))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        camera_x -= 5 / zoom
    if keys[pygame.K_RIGHT]:
        camera_x += 5 / zoom
    if keys[pygame.K_UP]:
        camera_y -= 5 / zoom
    if keys[pygame.K_DOWN]:
        camera_y += 5 / zoom

    screen.fill((0,0,0))

    # رسم الخطوط
    for c in connections:
        p1 = world_to_screen(zones[c[0]].x, zones[c[0]].y)
        p2 = world_to_screen(zones[c[1]].x, zones[c[1]].y)

        pygame.draw.line(screen, (255,255,255), p1, p2, 4)

    # رسم الدوائر
    for z in zones:
        pos = world_to_screen(z.x, z.y)

        pygame.draw.circle(screen, (100,200,255), pos, int(25 * zoom))
    pygame.display.flip()
    # clock.tick(60)

pygame.quit()



import pygame


class DrawerError(Exception):
    pass


class Drawer:
    def __init__(self):
        pass

    def draw(self, graph):
        pygame.init()

        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("FLY-IN")

        clock = pygame.time.Clock()
        running = True

        zoom = 1.0
        camera_x = 0
        camera_y = 0

        SCALE = 100   # distance between nodes

        def world_to_screen(x, y):
            w, h = screen.get_size()

            sx = (x - camera_x) * zoom + w / 2
            sy = (y - camera_y) * zoom + h / 2

            return int(sx), int(sy)

        while running:
            # ---------------- EVENTS ----------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEWHEEL:
                    zoom += event.y * 0.1
                    zoom = max(0.3, min(5, zoom))

            # ---------------- KEYBOARD ----------------
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                camera_x -= 10 / zoom

            if keys[pygame.K_RIGHT]:
                camera_x += 10 / zoom

            if keys[pygame.K_UP]:
                camera_y -= 10 / zoom

            if keys[pygame.K_DOWN]:
                camera_y += 10 / zoom

            # ---------------- DRAW ----------------
            screen.fill((0, 0, 0))

            # Draw connections
            for connection in graph.connections.values():
                x1, y1 = connection.start.location
                x2, y2 = connection.end.location

                px1, py1 = world_to_screen(x1 * SCALE, y1 * SCALE)
                px2, py2 = world_to_screen(x2 * SCALE, y2 * SCALE)

                pygame.draw.line(screen, (0, 0, 255), (px1, py1), (px2, py2), 5)

            # Draw zones
            for zone in graph.zones.values():
                x, y = zone.location

                pos = world_to_screen(x * SCALE, y * SCALE)

                pygame.draw.circle(screen, (255, 0, 255), pos, int(20 * zoom))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()