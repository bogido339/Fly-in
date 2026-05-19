import pygame
import sys

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 600, 400
MIN_WIDTH, MIN_HEIGHT = 300, 300

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Square Example")

clock = pygame.time.Clock()

# Square settings
square_size = 100
square_color = (0, 255, 0)  # Green
warning_color = (255, 0, 0)  # Red
background_color = (30, 30, 30)

font = pygame.font.SysFont("Arial", 24, bold=True)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get current window size
    current_width, current_height = screen.get_size()

    # Fill background
    screen.fill(background_color)

    # Check window size
    if current_width < MIN_WIDTH or current_height < MIN_HEIGHT:
        warning_text = font.render(
            "Warning: Window is too small!",
            True,
            warning_color
        )

        text_rect = warning_text.get_rect(
            center=(current_width // 2, current_height // 2)
        )

        screen.blit(warning_text, text_rect)

    else:
        # Draw square in center
        square_x = (current_width - square_size) // 2
        square_y = (current_height - square_size) // 2

        pygame.draw.rect(
            screen,
            square_color,
            (square_x, square_y, square_size, square_size)
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()