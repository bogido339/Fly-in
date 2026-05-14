import pygame


class DrawerError(Exception):
    pass


class Drawer:
    def __init__(self):
        self.bg_color = (20, 20, 20)
        self.line_color = (100, 150, 255)
        self.default_zone_color = (255, 0, 255)
        self.text_color = (255, 255, 255)

    def draw(self, graph):
        pygame.init()
        pygame.font.init()

        WIDTH, HEIGHT = 800, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("FLY-IN")

        font = pygame.font.SysFont("Arial", 14, bold=True)

        clock = pygame.time.Clock()
        running = True

        zoom = 1.0
        camera_x = 0
        camera_y = 0

        SCALE = 100
        
        def world_to_screen(x, y):
            w, h = screen.get_size()
            sx = (x - camera_x) * zoom + w / 2
            sy = (y - camera_y) * zoom + h / 2
            return int(sx), int(sy)

        def get_zone_color(zone):
            color_name = getattr(zone, 'color', None)
            if color_name:
                try:

                    return pygame.Color(color_name)
                except ValueError:
                    pass
            return self.default_zone_color

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    zoom += event.y * 0.1
                    zoom = max(0.2, min(3.0, zoom))

            keys = pygame.key.get_pressed()
            
            pan_speed = 10 / zoom
            if keys[pygame.K_LEFT]:
                camera_x -= pan_speed
            if keys[pygame.K_RIGHT]:
                camera_x += pan_speed
            if keys[pygame.K_UP]:
                camera_y -= pan_speed
            if keys[pygame.K_DOWN]:
                camera_y += pan_speed

            screen.fill(self.bg_color)

            # draw connections
            if hasattr(graph, 'connections'):
                for connection in graph.connections:
                    start_zone = getattr(connection, 'start', None)
                    end_zone = getattr(connection, 'end', None)
                    
                    if not start_zone or not end_zone:
                        continue

                    x1, y1 = start_zone.location
                    x2, y2 = end_zone.location

                    px1, py1 = world_to_screen(x1 * SCALE, y1 * SCALE)
                    px2, py2 = world_to_screen(x2 * SCALE, y2 * SCALE)
                    
                    line_thickness = max(1, int(4 * zoom))
                    pygame.draw.line(screen, self.line_color, (px1, py1), (px2, py2), line_thickness)

            # draw zones
            if hasattr(graph, 'zones'):
                zones = graph.zones.values()
                
                for zone in zones:
                    x, y = zone.location
                    pos = world_to_screen(x * SCALE, y * SCALE)
                    radius = max(6, int(15 * zoom))

                    zone_color = get_zone_color(zone)
                    pygame.draw.circle(screen, zone_color, pos, radius)
                    
                    outline_thickness = max(1, int(2 * zoom))
                    pygame.draw.circle(screen, (255, 255, 255), pos, radius, outline_thickness)
                    
                    if hasattr(zone, 'name'):
                        text_surface = font.render(zone.name, True, self.text_color)
                        text_rect = text_surface.get_rect(center=(pos[0], pos[1] + radius + 12))
                        screen.blit(text_surface, text_rect)
                for zone in graph.path:
                    x, y = zone.location
                    pos = world_to_screen(x * SCALE, y * SCALE)
                    radius = max(6, int(15 * zoom))

                    zone_color = (255, 255, 255)
                    pygame.draw.circle(screen, zone_color, pos, radius)
                    
                    outline_thickness = max(1, int(2 * zoom))
                    pygame.draw.circle(screen, (255, 255, 255), pos, radius, outline_thickness)
                    
                    if hasattr(zone, 'name'):
                        text_surface = font.render(zone.name, True, self.text_color)
                        text_rect = text_surface.get_rect(center=(pos[0], pos[1] + radius + 12))
                        screen.blit(text_surface, text_rect)


            pygame.display.flip()
            clock.tick(60)

        pygame.quit()