import pygame
import sys
import random
import subprocess

pygame.init()
GUI = pygame.display.set_mode((800, 600))
pygame.display.set_caption("The incredible guessing game")
run = True
coords = [(100, 100), (200, 200), (300, 150), (400, 250)]  # Example coordinates
current_coord_index = 0
triangle_x, triangle_y = coords[current_coord_index]
speed = 1  # Adjust for desired speed
triangle_width = 20
triangle_height = 20
paused = False
clock = pygame.time.Clock()
frame_rate = 30  # Default frame rate

# Button dimensions and positions
button_width = 80
button_height = 30
button_color = (100, 100, 100)
button_text_color = (255, 255, 255)

# Calculate positions for bottom right corner
button_x = 700 - button_width  # 800 - 100
button_y_start = 600 - 5 * button_height    # Start from bottom, leaving space for buttons
button_spacing = button_height + 10  # Space between buttons

play_pause_button_rect = pygame.Rect(button_x, button_y_start, button_width, button_height)
slow_button_rect = pygame.Rect(button_x, button_y_start + button_spacing, button_width, button_height)
fast_button_rect = pygame.Rect(button_x, button_y_start + 2 * button_spacing, button_width, button_height)
very_fast_button_rect = pygame.Rect(button_x, button_y_start + 3 * button_spacing, button_width, button_height)

font = pygame.font.Font(None, 24)  # Default font, size 24


def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def move_towards_next_coord():
    global triangle_x, triangle_y, current_coord_index

    target_x, target_y = coords[current_coord_index]

    dx = target_x - triangle_x
    dy = target_y - triangle_y

    if dx != 0:
        triangle_x += speed * (dx / max(abs(dx), abs(dy)))
    if dy != 0:
        triangle_y += speed * (dy / max(abs(dx), abs(dy)))

    # Check if close enough to the target coordinate
    if abs(triangle_x - target_x) < speed and abs(triangle_y - target_y) < speed:
        triangle_x, triangle_y = target_x, target_y  # Snap to target
        current_coord_index = (current_coord_index + 1) % len(coords)  # Move to the next coordinate


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_pause_button_rect.collidepoint(event.pos):
                paused = not paused
            elif slow_button_rect.collidepoint(event.pos):
                frame_rate = 1
            elif fast_button_rect.collidepoint(event.pos):
                frame_rate = 5
            elif very_fast_button_rect.collidepoint(event.pos):
                frame_rate = 30

    GUI.fill((0, 0, 0))

    # Draw buttons
    draw_button(GUI, play_pause_button_rect, button_color, "Play/Pause" if not paused else "Resume")
    draw_button(GUI, slow_button_rect, button_color, "1 FPS")
    draw_button(GUI, fast_button_rect, button_color, "5 FPS")
    draw_button(GUI, very_fast_button_rect, button_color, "30 FPS")

    # Adjust triangle position to center it
    triangle_points = (
        (triangle_x - triangle_width / 2, triangle_y - triangle_height / 2),
        (triangle_x + triangle_width / 2, triangle_y - triangle_height / 2),
        (triangle_x, triangle_y + triangle_height / 2)
    )
    pygame.draw.polygon(GUI, (255, 255, 0), triangle_points)

    # Draw coordinate indicators
    for i, (x, y) in enumerate(coords):
        color = (255, 0, 0) if i == current_coord_index else (0, 255, 0)  # Highlight current target
        pygame.draw.circle(GUI, color, (x, y), 5)

    if not paused:
        move_towards_next_coord()

    pygame.display.update()
    clock.tick(frame_rate)

pygame.quit()
sys.exit()

