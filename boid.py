import pygame
import math
import random
import settings # Import settings as a module to access its attributes dynamically

class Boid:
    def __init__(self):
        self.position = pygame.math.Vector2(random.uniform(0, settings.SCREEN_WIDTH), random.uniform(0, settings.SCREEN_HEIGHT))
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * settings.MAX_SPEED
        self.acceleration = pygame.math.Vector2(0, 0)
        self.size = (10, 20) # Default size for boids
        self.color = settings.WHITE # Default color
        # random 0.1 probability
        if random.random() < 0.1:
            self._render_forces = True
        else:
            self._render_forces = False

    def _apply_force(self, force):
        self.acceleration += force

    def _seek(self, target):
        desired = (target - self.position).normalize() * settings.MAX_SPEED
        steer = desired - self.velocity
        if steer.length() > settings.MAX_FORCE:
            steer.scale_to_length(settings.MAX_FORCE)
        return steer

    def _cohesion(self, boids):
        center_of_mass = pygame.math.Vector2(0, 0)
        count = 0
        for other in boids:
            if other != self and self.position.distance_to(other.position) < settings.PERCEPTION_RADIUS:
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
            if other != self and self.position.distance_to(other.position) < settings.PERCEPTION_RADIUS:
                avg_velocity += other.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            avg_velocity.normalize_ip()
            avg_velocity *= settings.MAX_SPEED
            steer = avg_velocity - self.velocity
            if steer.length() > settings.MAX_FORCE:
                steer.scale_to_length(settings.MAX_FORCE)
            return steer
        return pygame.math.Vector2(0, 0)

    def _separation(self, boids):
        steer = pygame.math.Vector2(0, 0)
        count = 0
        for other in boids:
            distance = self.position.distance_to(other.position)
            if other != self and distance < settings.SEPARATION_RADIUS:
                diff = self.position - other.position
                diff.normalize_ip()
                diff /= distance # Weight by distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
            if steer.length() > 0:
                steer.normalize_ip()
                steer *= settings.MAX_SPEED
                steer -= self.velocity
                if steer.length() > settings.MAX_FORCE:
                    steer.scale_to_length(settings.MAX_FORCE)
            return steer
        return pygame.math.Vector2(0, 0)

    def update(self, all_boids):
        self.acceleration *= 0 # Reset acceleration each frame

        cohesion_force = self._cohesion(all_boids) * settings.COHESION_WEIGHT
        alignment_force = self._alignment(all_boids) * settings.ALIGNMENT_WEIGHT
        separation_force = self._separation(all_boids) * settings.SEPARATION_WEIGHT
        
        # save the forces to self
        self._cohesion_force = cohesion_force
        self._alignment_force = alignment_force
        self._separation_force = separation_force

        self._apply_force(cohesion_force)
        self._apply_force(alignment_force)
        self._apply_force(separation_force)

        self.velocity += self.acceleration
        if self.velocity.length() > settings.MAX_SPEED:
            self.velocity.scale_to_length(settings.MAX_SPEED)
        
        self.position += self.velocity

        # Wrap around screen edges
        if self.position.x < 0: self.position.x = settings.SCREEN_WIDTH
        if self.position.x > settings.SCREEN_WIDTH: self.position.x = 0
        if self.position.y < 0: self.position.y = settings.SCREEN_HEIGHT
        if self.position.y > settings.SCREEN_HEIGHT: self.position.y = 0

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
        
        if self._render_forces:
            # draw the cohesion , alignment, and separation force
            pygame.draw.line(screen, settings.CYAN, self.position, self.position + self._cohesion_force * 500, 3)
            pygame.draw.line(screen, settings.GREEN, self.position, self.position + self._alignment_force * 500, 3)
            pygame.draw.line(screen, settings.RED, self.position, self.position + self._separation_force * 500, 3)
            

            # Draw perception and separation circles
            pygame.draw.circle(screen, settings.YELLOW, (int(self.position.x), int(self.position.y)), settings.PERCEPTION_RADIUS, 1)
            pygame.draw.circle(screen, settings.RED, (int(self.position.x), int(self.position.y)), settings.SEPARATION_RADIUS, 1)
