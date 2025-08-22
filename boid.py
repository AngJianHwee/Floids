import pygame
import math
import random
from settings import *

class Boid:
    def __init__(self):
        self.position = pygame.math.Vector2(random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT))
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.acceleration = pygame.math.Vector2(0, 0)
        self.size = (10, 20) # Default size for boids
        self.color = WHITE # Default color

    def _apply_force(self, force):
        self.acceleration += force

    def _seek(self, target):
        desired = (target - self.position).normalize() * MAX_SPEED
        steer = desired - self.velocity
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def _cohesion(self, boids):
        center_of_mass = pygame.math.Vector2(0, 0)
        count = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                center_of_mass += other.position
                count += 1
        if count > 0:
            center_of_mass /= count
            return self._seek(center_of_mass)
        return pygame.math.Vector2(0, 0)

    def _alignment(self, boids):
        avg_velocity = pygame.math.Vector2(0, 0)
        count = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < PERCEPTION_RADIUS:
                avg_velocity += other.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            avg_velocity.normalize_ip()
            avg_velocity *= MAX_SPEED
            steer = avg_velocity - self.velocity
            if steer.length() > MAX_FORCE:
                steer.scale_to_length(MAX_FORCE)
            return steer
        return pygame.math.Vector2(0, 0)

    def _separation(self, boids):
        steer = pygame.math.Vector2(0, 0)
        count = 0
        for other in boids:
            distance = self.position.distance_to(other.position)
            if other != self and distance < SEPARATION_RADIUS:
                diff = self.position - other.position
                diff.normalize_ip()
                diff /= distance # Weight by distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
            if steer.length() > 0:
                steer.normalize_ip()
                steer *= MAX_SPEED
                steer -= self.velocity
                if steer.length() > MAX_FORCE:
                    steer.scale_to_length(MAX_FORCE)
            return steer
        return pygame.math.Vector2(0, 0)

    def update(self, all_boids):
        self.acceleration *= 0 # Reset acceleration each frame

        cohesion_force = self._cohesion(all_boids) * COHESION_WEIGHT
        alignment_force = self._alignment(all_boids) * ALIGNMENT_WEIGHT
        separation_force = self._separation(all_boids) * SEPARATION_WEIGHT

        self._apply_force(cohesion_force)
        self._apply_force(alignment_force)
        self._apply_force(separation_force)

        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        
        self.position += self.velocity

        # Wrap around screen edges
        if self.position.x < 0: self.position.x = SCREEN_WIDTH
        if self.position.x > SCREEN_WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = SCREEN_HEIGHT
        if self.position.y > SCREEN_HEIGHT: self.position.y = 0

    def draw(self, screen):
        # Calculate rotation based on velocity
        angle_rad = math.atan2(self.velocity.y, self.velocity.x)
        
        # Define triangle points relative to its center
        points = [
            (self.size[1] / 2, 0),             # Tip
            (-self.size[1] / 2, -self.size[0] / 2), # Back top
            (-self.size[1] / 2, self.size[0] / 2)  # Back bottom
        ]

        rotated_points = []
        cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)

        for x, y in points:
            rotated_x = (x * cos_a - y * sin_a) + self.position.x
            rotated_y = (x * sin_a + y * cos_a) + self.position.y
            rotated_points.append((rotated_x, rotated_y))
        
        pygame.draw.polygon(screen, self.color, rotated_points)
