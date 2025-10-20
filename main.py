# main.py

import sys
import pygame
import settings # Import settings as a module to access its attributes dynamically
from boid import Boid
from ui import UIManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.GAME_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.frame_rate = settings.DEFAULT_FPS
        
        # Pass the settings module to UIManager so it can modify parameters directly
        self.ui_manager = UIManager(settings) 
        self.boids = []
        self._create_boids()

    def _create_boids(self):
        """Create and add all boids to the scene."""
        for _ in range(settings.BOID_COUNT):
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
            elif action == 'update_param':
                # Parameter was updated via slider, no direct action needed here
                # The settings module itself has been updated by UIManager
                pass

    def update(self):
        for boid in self.boids:
            boid.update(self.boids)

    def draw(self):
        self.screen.fill(settings.BLACK)
        
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
        legend_y = settings.SCREEN_HEIGHT - 160  # Adjusted slightly for more space
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

        # Legend items: (Text, Color, Value) - now dynamically fetching from settings
        legend_items = [
            ("Perception Radius", settings.WHITE, settings.PERCEPTION_RADIUS),
            ("Separation Radius", settings.YELLOW, settings.SEPARATION_RADIUS),
            ("Cohesion Weight", settings.RED, settings.COHESION_WEIGHT),
            ("Alignment Weight", settings.GREEN, settings.ALIGNMENT_WEIGHT),
            ("Separation Weight", settings.CYAN, settings.SEPARATION_WEIGHT),
            ("Max Speed", settings.BLUE, settings.MAX_SPEED),
            ("Max Force", settings.WHITE, settings.MAX_FORCE),
        ]
        
        
        # Draw the text and indicators on top of the transparent background
        for i, (text, color, value) in enumerate(legend_items):
            # Improved: Display text uses the specified color for clarity
            display_text = f"{text}: {value:.1f}" # Format to one decimal place for consistency
            text_surface = settings.FONT.render(display_text, True, color)
            
            # Position the text relative to the top-left of the legend area
            text_rect = text_surface.get_rect(topleft=(legend_x + 25, legend_y - 30 + i * line_height))
            screen.blit(text_surface, text_rect)
            
            # Draw color indicator circle (only for the original 5 parameters)
            if i < 2 :
                pygame.draw.circle(screen, color, (legend_x + 15, legend_y - 30 + 7 + i * line_height), 5)
            elif 2 <= i < 5:
                pygame.draw.line(screen, color, (legend_x + 10, legend_y - 30 + 7 + i * line_height), (legend_x + 20, legend_y - 30 + 7 + i * line_height), 3)
            else:
                pass # No indicator for Max Speed and Max Force
if __name__ == "__main__":
    game = Game()
    game.run()
