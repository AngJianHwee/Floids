import pygame
import sys
import math

pygame.init()
GUI = pygame.display.set_mode((800, 600))
pygame.display.set_caption("The incredible guessing game")
run = True
coords = [(100, 100), (200, 200), (300, 150), (400, 250)]  # Example coordinates
current_coord_index = 0
position = pygame.math.Vector2(coords[current_coord_index])  # Current position
direction = pygame.math.Vector2(0, 0)  # Initial direction
speed = 1  # Adjust for desired speed
triangle_width = 20
triangle_height = 30  # Increased height for a longer triangle
paused = False
clock = pygame.time.Clock()
frame_rate = 30  # Default frame rate
triangle_rotation = 0  # Initial rotation angle
rotation_speed_alpha = 0.1  # Adjust for desired rotation speed

# Button dimensions and positions
button_width = 80
button_height = 30
button_color = (100, 100, 100)
button_selected_color = (50, 50, 50)  # Darker when selected
button_text_color = (255, 255, 255)

# Calculate positions for bottom right corner
button_x = 700 - button_width  # 800 - 100
button_y_start = 600 - 5 * button_height    # Start from bottom, leaving space for buttons
button_spacing = button_height + 10  # Space between buttons

play_pause_button_rect = pygame.Rect(button_x, button_y_start, button_width, button_height)
slow_button_rect = pygame.Rect(button_x, button_y_start + button_spacing, button_width, button_height)
fast_button_rect = pygame.Rect(button_x, button_y_start + 2 * button_spacing, button_width, button_height)
very_fast_button_rect = pygame.Rect(button_x, button_y_start + 3 * button_spacing, button_width, button_height)

# Store button states
button_states = {
    "play_pause": False,
    "slow": False,
    "fast": False,
    "very_fast": False
}

font = pygame.font.Font(None, 24)  # Default font, size 24


def draw_button(screen, rect, color, text):
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, button_text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def move_towards_next_coord():
    global current_coord_index, position, triangle_rotation
    target = pygame.math.Vector2(coords[current_coord_index])
    if position != target:
        direction = (target - position).normalize()
        position += direction * speed
        # Calculate angle towards the target
        target_angle = math.degrees(math.atan2(direction.y, direction.x))
        # Smoothly rotate towards the target angle
        angle_difference = (target_angle - triangle_rotation) % 360
        if angle_difference > 180:
            angle_difference -= 360  # Take the shortest path
        triangle_rotation += angle_difference * rotation_speed_alpha  # Adjust rotation speed

        # Check if the triangle is close enough to the target coordinate
        if position.distance_to(target) < speed:
            position = target  # Snap to the target to avoid overshooting
    else:
        # Move to the next coordinate
        current_coord_index = (current_coord_index + 1) % len(coords)


def draw_triangle(screen, position, rotation, width, height, color):
    # Define triangle points relative to the center, pointing to the RIGHT by default (0 degrees)
    # The 'height' is now the length from tip to base.
    # The 'width' is the width of the base.
    points = [
        (height / 2, 0),                 # Tip
        (-height / 2, -width / 2),       # Back top
        (-height / 2, width / 2)         # Back bottom
    ]

    # Rotate points around the origin (0,0) and then translate them
    rotated_points = []
    angle_rad = math.radians(rotation)  # Convert rotation to radians

    for x, y in points:
        # Standard 2D rotation formula
        rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad) + position[0]  # Use index [0] for x
        rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad) + position[1]  # Use index [1] for y
        rotated_points.append((rotated_x, rotated_y))

    pygame.draw.polygon(screen, color, rotated_points)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_pause_button_rect.collidepoint(event.pos):
                paused = not paused
                button_states["play_pause"] = not button_states["play_pause"]
                button_states["slow"] = False
                button_states["fast"] = False
                button_states["very_fast"] = False
            elif slow_button_rect.collidepoint(event.pos):
                frame_rate = 1
                button_states["slow"] = True
                button_states["fast"] = False
                button_states["very_fast"] = False
                button_states["play_pause"] = False
            elif fast_button_rect.collidepoint(event.pos):
                frame_rate = 5
                button_states["fast"] = True
                button_states["slow"] = False
                button_states["very_fast"] = False
                button_states["play_pause"] = False
            elif very_fast_button_rect.collidepoint(event.pos):
                frame_rate = 30
                button_states["very_fast"] = True
                button_states["slow"] = False
                button_states["fast"] = False
                button_states["play_pause"] = False

    GUI.fill((0, 0, 0))

    # Draw buttons
    draw_button(GUI, play_pause_button_rect, button_selected_color if button_states["play_pause"] else button_color, "Play/Pause" if not paused else "Resume")
    draw_button(GUI, slow_button_rect, button_selected_color if button_states["slow"] else button_color, "1 FPS")
    draw_button(GUI, fast_button_rect, button_selected_color if button_states["fast"] else button_color, "5 FPS")
    draw_button(GUI, very_fast_button_rect, button_selected_color if button_states["very_fast"] else button_color, "30 FPS")

    draw_triangle(GUI, position, triangle_rotation, triangle_width, triangle_height, (255, 255, 0))
    
    # Draw direction line
    direction_end = (position.x + math.cos(math.radians(triangle_rotation)) * triangle_height,
                        position.y + math.sin(math.radians(triangle_rotation)) * triangle_height)
    pygame.draw.line(GUI, (255, 0, 0), (position.x, position.y), direction_end, 2)

    # Add text about current coordinate and position and rotation
    text_surface = font.render(
        f"Current Coord: {current_coord_index + 1}/{len(coords)} | Rotation: {triangle_rotation:.2f}° | Position: {position} | Speed: {speed}",
        True, (255, 255, 255))
    GUI.blit(text_surface, (10, 10))

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







