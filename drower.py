# import pygame


# class Drower:
#     def __init__(self):
#         pass

#     def drow(self, graph):
#         print(type(graph))
#         pygame.init()

#         # Create game window (width, height)
#         # screen = pygame.display.set_mode((800, 600))
#         screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
#         # Change window title
#         pygame.display.set_caption("FLY-IN")

#         # Create clock to control FPS
#         clock = pygame.time.Clock()

#         # Running variable for game loop
#         running = True

#         while running:

#             for event in pygame.event.get():
#                 # If user clicks X button
#                 if event.type == pygame.QUIT:
#                     running = False

#             # Keyboard input
#             # keys = pygame.key.get_pressed()

#             # # Move square with arrows
#             # if keys[pygame.K_LEFT]:
#             #     x -= 5

#             # if keys[pygame.K_RIGHT]:
#             #     x += 5

#             # if keys[pygame.K_UP]:
#             #     y -= 5

#             # if keys[pygame.K_DOWN]:
#             #     y += 5

#             # Black = (0,0,0)
#             screen.fill((0, 0, 0))

#             # Draw circle
#             # (screen, color, center, radius)
#             zones = graph.zones.values()
#             for zone in zones:
#                 x, y = zone.location
#                 print(x, y)
#                 pygame.draw.circle(screen, (0, 255, 0), ((x*10)+60, (y*10)+60), 10)

#             # Draw line: (screen, color, start, end, width)
#             pygame.draw.line(screen, (0, 0, 255), (260, 200), (300, 200), 5)
          

#             # Update screen: (Show all drawings)
#             pygame.display.update()

#             # FPS = Frames Per Second: (Limit speed to 60 FPS)
#             clock.tick(60)

#         # Quit pygame
#         pygame.quit()


import pygame

class DrowerError(Exception):
    pass

class Drower:
    def __init__(self):
        pass

    def drow(self, graph):
        pygame.init()

        screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption("FLY-IN")

        clock = pygame.time.Clock()
        running = True

        CELL_SIZE = 90
        OFFSET = 150
        def world_to_screen(x, y):
            return x * CELL_SIZE + OFFSET, y * CELL_SIZE + OFFSET

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill((0, 0, 0))

            zones = graph.zones.values()


            for connection in graph.connections:
                if connection.start is None or connection.end is None:
                    raise DrowerError("Bad connection")

                x1, y1 = connection.start.location
                x2, y2 = connection.end.location

                px1, py1 = world_to_screen(x1, y1)
                px2, py2 = world_to_screen(x2, y2)
                pygame.draw.line(screen, (0, 0, 255), (px1, py1), (px2, py2), 5)

            for zone in zones:
                x, y = zone.location

                px, py = world_to_screen(x, y)

                pygame.draw.circle(screen, (255, 0, 255), (px, py), 30)


            pygame.display.update()
            clock.tick(100)

        pygame.quit()