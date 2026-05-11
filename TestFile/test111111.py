import pygame
import sys
from time import sleep

# Init pygame
pygame.init()

# Screen size
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Centered Map")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 80, 80)

# Zones (relative positions)
zones = {
    "start": (0, 0),
    "zone1": (150, 0),
    "zone2": (300, 100),
    "zone3": (150, 200),
    "goal": (400, 200)
}

# Connections
lines = [
    ("start", "zone1"),
    ("zone1", "zone2"),
    ("zone1", "zone3"),
    ("zone2", "goal"),
    ("zone3", "goal")
]

# -------- CENTER MAP --------
# Find map size
xs = [pos[0] for pos in zones.values()]
ys = [pos[1] for pos in zones.values()]

map_width = max(xs) - min(xs)
map_height = max(ys) - min(ys)

# Offset to center map
offset_x = (WIDTH - map_width) // 2
offset_y = (HEIGHT - map_height) // 2

# Move all zones to center
centered_zones = {}
for name, (x, y) in zones.items():
    centered_zones[name] = (x + offset_x, y + offset_y)

# Font
font = pygame.font.SysFont(None, 24)

# Main loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # Draw lines
    for a, b in lines:
        pygame.draw.line(screen, BLACK, centered_zones[a], centered_zones[b], 3)

    # Draw zones
    for name, pos in centered_zones.items():
        color = BLUE

        if name == "start":
            color = GREEN
        elif name == "goal":
            color = RED

        pygame.draw.circle(screen, color, pos, 25)

        text = font.render(name, True, BLACK)
        screen.blit(text, (pos[0] - 20, pos[1] - 40))

    pygame.display.flip()

pygame.quit()
sys.exit()