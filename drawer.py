import pygame


class DrawerError(Exception):
    pass


class Drawer:
    def __init__(self):
        self.bg_color = (20, 20, 20)
        self.line_color = (100, 150, 255)
        self.default_zone_color = (255, 0, 255)
        self.text_color = (255, 255, 255)

        self.zoom = 1.0
        self.camera_x = 0
        self.camera_y = 0

    def world_to_screen(self, x, y):
        w, h = self.screen.get_size()
        sx = (x - self.camera_x) * self.zoom + w / 2
        sy = (y - self.camera_y) * self.zoom + h / 2
        return int(sx), int(sy)

    def get_zone_color(self, zone):
        color_name = getattr(zone, 'color', None)
        if color_name:
            try:
                return pygame.Color(color_name)
            except ValueError:
                pass
        return self.default_zone_color

    def draw_zones(self):
        zones = self.graph.zones.values()

        for zone in zones:
            x, y = zone.location
            pos = self.world_to_screen(x * self.SCALE, y * self.SCALE)
            radius = max(6, int(15 * self.zoom))

            zone_color = self.get_zone_color(zone)
            pygame.draw.circle(self.screen, zone_color, pos, radius)

            outline_thickness = max(1, int(2 * self.zoom))
            pygame.draw.circle(self.screen, (255, 255, 255), pos, radius, outline_thickness)

            # if hasattr(zone, 'name'):
                # text_surface = self.font.render(zone.name, True, self.text_color)
                # text_rect = text_surface.get_rect(center=(pos[0], pos[1] + radius + 12))
                # self.screen.blit(text_surface, text_rect)

    def draw_connections(self):
        for connection in self.graph.connections.values():
            start_zone = getattr(connection, 'start', None)
            end_zone = getattr(connection, 'end', None)

            if not start_zone or not end_zone:
                continue

            x1, y1 = start_zone.location
            x2, y2 = end_zone.location

            if start_zone in self.graph.path and end_zone in self.graph.path:
                self.line_color = (255, 255, 0)
            else:
                self.line_color = (100, 150, 255)

            px1, py1 = self.world_to_screen(x1 * self.SCALE, y1 * self.SCALE)
            px2, py2 = self.world_to_screen(x2 * self.SCALE, y2 * self.SCALE)

            line_thickness = max(1, int(4 * self.zoom))
            pygame.draw.line(self.screen, self.line_color, (px1, py1), (px2, py2), line_thickness)

    def draw_drones(self):
        for drone in self.simulator.drones:
            if drone.current_location is None:
                continue

            x, y = drone.current_location.location
            pos = self.world_to_screen(x * self.SCALE, y * self.SCALE)
            radius = max(6, int(8 * self.zoom))

            drone_color = (0, 0, 0)
            pygame.draw.circle(self.screen, drone_color, pos, radius)

            outline_thickness = max(1, int(2 * self.zoom))
            pygame.draw.circle(self.screen, (255, 255, 255), pos, radius, outline_thickness)

            text_surface = self.font.render(str(drone.drone_id), True, self.text_color)
            text_rect = text_surface.get_rect(center=(pos[0], pos[1] + radius + 12))
            self.screen.blit(text_surface, text_rect)

    def process_controls(self):
        keys = pygame.key.get_pressed()

        pan_speed = 10 / self.zoom
        if keys[pygame.K_LEFT]:
            self.camera_x -= pan_speed
        if keys[pygame.K_RIGHT]:
            self.camera_x += pan_speed
        if keys[pygame.K_UP]:
            self.camera_y -= pan_speed
        if keys[pygame.K_DOWN]:
            self.camera_y += pan_speed
        # if keys[pygame.K_SPACE]:
        #     self.simulator.run()

    def draw_all(self, graph, simulator):
        pygame.init()
        pygame.font.init()

        WIDTH, HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("FLY-IN")

        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.graph = graph
        self.simulator = simulator
        self.SCALE = 100

        clock = pygame.time.Clock()
        running = True

        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEWHEEL:
                    self.zoom += event.y * 0.1
                    self.zoom = max(0.2, min(3.0, self.zoom))

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.simulator.run()

            self.process_controls()

            self.screen.fill(self.bg_color)

            self.draw_connections()
            self.draw_zones()
            self.draw_drones()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()