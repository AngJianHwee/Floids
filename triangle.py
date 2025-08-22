# triangle.py

import pygame
import math
from settings import RED

class Triangle:
    def __init__(self, coords, start_pos_index=0, speed=1, size=(20, 30), color=(255, 255, 0)):
        """
        Initializes a Triangle object.
        :param coords: A list of (x, y) tuples representing the path.
        :param start_pos_index: The index in coords where the triangle should start.
        :param speed: The movement speed in pixels per frame.
        :param size: A tuple (width, height) for the triangle.
        :param color: The color of the triangle.
        """
        self.coords = [pygame.math.Vector2(c) for c in coords]
        self.current_coord_index = start_pos_index
        self.position = pygame.math.Vector2(self.coords[self.current_coord_index])
        self.target = self.coords[self.current_coord_index]

        self.speed = speed
        self.width, self.height = size
        self.color = color
        
        self.rotation = 0
        self.rotation_speed_alpha = 0.1 # How quickly it turns

    def update(self):
        """Updates the triangle's position and rotation for one frame."""
        if self.position.distance_to(self.target) < self.speed:
            # Snap to target and get the next one
            self.position.update(self.target)
            self.current_coord_index = (self.current_coord_index + 1) % len(self.coords)
            self.target = self.coords[self.current_coord_index]
        
        if self.position != self.target:
            direction = (self.target - self.position).normalize()
            self.position += direction * self.speed
            
            # Calculate angle towards the target
            target_angle = math.degrees(math.atan2(direction.y, direction.x))
            
            # Smoothly rotate towards the target angle
            angle_difference = (target_angle - self.rotation + 180) % 360 - 180
            self.rotation += angle_difference * self.rotation_speed_alpha

    def draw(self, screen):
        """Draws the triangle and its debug direction line on the screen."""
        # --- Draw the triangle polygon ---
        points = [
            (self.height / 2, 0),             # Tip
            (-self.height / 2, -self.width / 2), # Back top
            (-self.height / 2, self.width / 2)  # Back bottom
        ]

        rotated_points = []
        angle_rad = math.radians(self.rotation)
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)

        for x, y in points:
            rotated_x = (x * cos_a - y * sin_a) + self.position.x
            rotated_y = (x * sin_a + y * cos_a) + self.position.y
            rotated_points.append((rotated_x, rotated_y))
        
        pygame.draw.polygon(screen, self.color, rotated_points)
        
        # --- Draw debug direction line ---
        direction_end = (
            self.position.x + math.cos(angle_rad) * self.height,
            self.position.y + math.sin(angle_rad) * self.height
        )
        pygame.draw.line(screen, RED, self.position, direction_end, 2)

    def get_info(self):
        """Returns a formatted string with the triangle's current status."""
        return (
            f"Target: {self.current_coord_index + 1}/{len(self.coords)} | "
            f"Rotation: {self.rotation:.1f}° | "
            f"Position: ({int(self.position.x)}, {int(self.position.y)})"
        )