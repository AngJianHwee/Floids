# ui.py

import pygame
from settings import (
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_SELECTED_COLOR,
    BUTTON_TEXT_COLOR, FONT, SCREEN_WIDTH, SCREEN_HEIGHT, FPS_OPTIONS
)

class UIManager:
    def __init__(self):
        button_x = SCREEN_WIDTH - BUTTON_WIDTH - 20
        button_y_start = SCREEN_HEIGHT - (BUTTON_HEIGHT + 10) * ( len(FPS_OPTIONS) + 1)
        spacing = BUTTON_HEIGHT + 10

        self.buttons = {
            "play_pause": {"rect": pygame.Rect(button_x, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "slow": {"rect": pygame.Rect(button_x, button_y_start + spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "fast": {"rect": pygame.Rect(button_x, button_y_start + 2 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "very_fast": {"rect": pygame.Rect(button_x, button_y_start + 3 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "extremely_fast": {"rect": pygame.Rect(button_x, button_y_start + 4 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
        }

    def handle_event(self, event):
        """
        Checks for button clicks and returns the action to perform.
        Returns a tuple (action_type, value) e.g., ('set_fps', 30) or ('toggle_pause', None)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["play_pause"]["rect"].collidepoint(event.pos):
                return 'toggle_pause', None
            if self.buttons["slow"]["rect"].collidepoint(event.pos):
                return 'set_fps', FPS_OPTIONS["slow"]
            if self.buttons["fast"]["rect"].collidepoint(event.pos):
                return 'set_fps', FPS_OPTIONS["fast"]
            if self.buttons["very_fast"]["rect"].collidepoint(event.pos):
                return 'set_fps', FPS_OPTIONS["very_fast"]
            if self.buttons["extremely_fast"]["rect"].collidepoint(event.pos):
                return 'set_fps', FPS_OPTIONS["extremely_fast"]
        return None, None

    def draw(self, screen, paused, current_fps):
        """Draws all UI elements."""
        # Draw Play/Pause button
        pause_text = "Resume" if paused else "Pause"
        pause_color = BUTTON_SELECTED_COLOR if paused else BUTTON_COLOR
        self._draw_button(screen, self.buttons["play_pause"]["rect"], pause_color, pause_text)
        
        # Draw speed buttons
        self._draw_button(screen, self.buttons["slow"]["rect"], 
                          BUTTON_SELECTED_COLOR if current_fps == FPS_OPTIONS["slow"] and not paused else BUTTON_COLOR, "Slow")
        self._draw_button(screen, self.buttons["fast"]["rect"], 
                          BUTTON_SELECTED_COLOR if current_fps == FPS_OPTIONS["fast"] and not paused else BUTTON_COLOR, "Fast")
        self._draw_button(screen, self.buttons["very_fast"]["rect"], 
                          BUTTON_SELECTED_COLOR if current_fps == FPS_OPTIONS["very_fast"] and not paused else BUTTON_COLOR, "V. Fast")
        self._draw_button(screen, self.buttons["extremely_fast"]["rect"], 
                          BUTTON_SELECTED_COLOR if current_fps == FPS_OPTIONS["extremely_fast"] and not paused else BUTTON_COLOR, "E. Fast")

    def _draw_button(self, screen, rect, color, text):
        """Helper function to draw a single button."""
        pygame.draw.rect(screen, color, rect)
        text_surface = FONT.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
