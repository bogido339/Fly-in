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
        camera_x = 200
        camera_y = 0

        SCALE = 100
        

        def world_to_screen(x, y):
            w, h = screen.get_size()

            sx = (x - camera_x) * zoom + w / 2
            sy = (y - camera_y) * zoom + h / 2

            return int(sx), int(sy)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEWHEEL:
                    zoom += event.y * 0.1
                    zoom = max(0.3, min(3, zoom))

            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                camera_x += 5 / zoom

            if keys[pygame.K_RIGHT]:
                camera_x -= 5 / zoom

            if keys[pygame.K_UP]:
                camera_y += 5 / zoom

            if keys[pygame.K_DOWN]:
                camera_y -= 5 / zoom

            screen.fill((0, 0, 0))

            # Draw connections
            for connection in graph.connections:
                x1, y1 = connection.start.location
                x2, y2 = connection.end.location

                px1, py1 = world_to_screen(x1 * SCALE, y1 * SCALE)
                px2, py2 = world_to_screen(x2 * SCALE, y2 * SCALE)

                pygame.draw.line(screen, (0, 0, 255), (px1, py1), (px2, py2), 5)

            # Draw zones
            for zone in graph.zones.values():
                x, y = zone.location

                pos = world_to_screen(x * SCALE, y * SCALE)

                pygame.draw.circle(screen, (255, 0, 255), pos, int(30 * zoom))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
