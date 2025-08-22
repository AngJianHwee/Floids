# main.py

import pygame
import sys
from settings import *
from boid import Boid
from ui import UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.frame_rate = DEFAULT_FPS
        
        self.ui_manager = UIManager()
        self.boids = []
        self._create_boids()

    def _create_boids(self):
        """Create and add all boids to the scene."""
        for _ in range(BOID_COUNT):
            self.boids.append(Boid())
        
    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
            self.draw()
            self.clock.tick(self.frame_rate)
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            action, value = self.ui_manager.handle_event(event)
            if action == 'toggle_pause':
                self.paused = not self.paused
            elif action == 'set_fps':
                self.frame_rate = value
                self.paused = False # Unpause when speed is changed

    def update(self):
        for boid in self.boids:
            boid.update(self.boids)

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw boids
        for boid in self.boids:
            boid.draw(self.screen)
        
        self.ui_manager.draw(self.screen, self.paused, self.frame_rate)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
