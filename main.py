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
            elif action == 'reset':
                self.boids = []
                self._create_boids()
                self.paused = False # Unpause on reset

    def update(self):
        for boid in self.boids:
            boid.update(self.boids)

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw boids
        for boid in self.boids:
            boid.draw(self.screen)
        
        self.ui_manager.draw(self.screen, self.paused, self.frame_rate)

        # Draw legend
        self._draw_legend(self.screen)
        
        pygame.display.flip()

    def _draw_legend(self, screen):
        """Draws a legend for the Boids simulation."""
        legend_x = 10
        legend_y = SCREEN_HEIGHT - 160  # Adjusted slightly for more space
        line_height = 25
        width = 220
        height = 150

        # --- This is the key change for transparency ---
        # 1. Create a new surface for the legend with per-pixel alpha
        legend_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 2. Fill the surface with a semi-transparent color
        legend_surface.fill((30, 30, 30, 180)) 
        
        # 3. Blit this transparent surface onto the main screen
        screen.blit(legend_surface, (legend_x, legend_y))
        # ----------------------------------------------------

        # Legend items: (Text, Color, Value)
        legend_items = [
            ("Perception Radius", BLUE, PERCEPTION_RADIUS),
            ("Separation Radius", RED, SEPARATION_RADIUS),
            ("Cohesion Weight", CYAN, COHESION_WEIGHT),
            ("Alignment Weight", GREEN, ALIGNMENT_WEIGHT),
            ("Separation Weight", RED, SEPARATION_WEIGHT),
            
        ]
        
        # Draw the text and indicators on top of the transparent background
        for i, (text, color, value) in enumerate(legend_items):
            # Improved: Display text uses the specified color for clarity
            display_text = f"{text}: {value}"
            text_surface = FONT.render(display_text, True, color)
            
            # Position the text relative to the top-left of the legend area
            text_rect = text_surface.get_rect(topleft=(legend_x + 25, legend_y + 10 + i * line_height))
            screen.blit(text_surface, text_rect)
            
            # Draw color indicator circle
            pygame.draw.circle(screen, color, (legend_x + 15, legend_y + 22 + i * line_height), 5)
if __name__ == "__main__":
    game = Game()
    game.run()
