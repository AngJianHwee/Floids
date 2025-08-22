# main.py

import pygame
import sys
from settings import *
from triangle import Triangle
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
        self.triangles = []
        self._create_scene_objects()

    def _create_scene_objects(self):
        """Create and add all triangles to the scene."""
        # Path for the first triangle
        path1 = [(100, 100), (200, 200), (300, 150), (400, 250), (150, 350)]
        triangle1 = Triangle(coords=path1, speed=2, color=YELLOW)
        self.triangles.append(triangle1)

        # --- ADD MORE TRIANGLES HERE ---
        # It's now this easy to add another one with a different path and look
        path2 = [(700, 500), (600, 400), (500, 500), (600, 550)]
        triangle2 = Triangle(coords=path2, speed=1, color=CYAN, size=(15, 25))
        self.triangles.append(triangle2)
        
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
        for triangle in self.triangles:
            triangle.update()

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw path coordinates
        all_coords = [c for t in self.triangles for c in t.coords]
        for i, (x, y) in enumerate(all_coords):
            pygame.draw.circle(self.screen, GREEN, (x, y), 5)

        # Draw triangles and their info
        for i, triangle in enumerate(self.triangles):
            triangle.draw(self.screen)
            # Display info text for each triangle
            info_text = FONT.render(f"T{i+1}: {triangle.get_info()}", True, WHITE)
            self.screen.blit(info_text, (10, 10 + i * 20))
        
        self.ui_manager.draw(self.screen, self.paused, self.frame_rate)
        
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()