import pygame
import sys
import random
import subprocess


pygame.init()
GUI = pygame.display.set_mode((800,600))
pygame.display.set_caption("The incredible guessing game")
run = True
coords = [(100, 100), (200, 200), (300, 150), (400, 250)]  # Example coordinates
current_coord_index = 0
triangle_x, triangle_y = coords[current_coord_index]
speed = 1  # Adjust for desired speed
triangle_width = 20
triangle_height = 20


def move_towards_next_coord():
    global triangle_x, triangle_y, current_coord_index

    target_x, target_y = coords[current_coord_index]

    dx = target_x - triangle_x
    dy = target_y - triangle_y

    if dx != 0:
        triangle_x += speed * (dx / max(abs(dx), abs(dy)) )
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

    GUI.fill((0, 0, 0))
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

    move_towards_next_coord()

    pygame.display.update()

pygame.quit()
sys.exit()
