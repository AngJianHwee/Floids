# ui.py

import pygame
from settings import (
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_SELECTED_COLOR,
    BUTTON_TEXT_COLOR, FONT, SCREEN_WIDTH, SCREEN_HEIGHT, FPS_OPTIONS, PARAM_RANGES
)
from slider import Slider # Import the new Slider class

class UIManager:
    def __init__(self, settings_module):
        self.settings = settings_module # Reference to the settings module for dynamic updates

        # UI element dimensions and positioning
        slider_width = 150
        slider_height = 20
        slider_x = SCREEN_WIDTH - slider_width - 150 # Position sliders to the left of buttons
        slider_y_start = 20
        slider_spacing = slider_height + 20 # More spacing for sliders

        self.sliders = []
        current_y = slider_y_start

        # Create sliders for each parameter in PARAM_RANGES
        for param_name, props in PARAM_RANGES.items():
            slider = Slider(
                slider_x, current_y, slider_width, slider_height,
                props["min"], props["max"], props["initial"], param_name, props["step"]
            )
            self.sliders.append(slider)
            current_y += slider_spacing

        # Position buttons below the sliders
        button_x = SCREEN_WIDTH - BUTTON_WIDTH - 20
        button_y_start = current_y + 20 # Start buttons below the last slider
        spacing = BUTTON_HEIGHT + 10

        self.buttons = {
            "play_pause": {"rect": pygame.Rect(button_x, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "slow": {"rect": pygame.Rect(button_x, button_y_start + spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "fast": {"rect": pygame.Rect(button_x, button_y_start + 2 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "very_fast": {"rect": pygame.Rect(button_x, button_y_start + 3 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "extremely_fast": {"rect": pygame.Rect(button_x, button_y_start + 4 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
            "reset": {"rect": pygame.Rect(button_x, button_y_start + 5 * spacing, BUTTON_WIDTH, BUTTON_HEIGHT)},
        }

    def handle_event(self, event):
        """
        Checks for button clicks and slider interactions, returning actions to perform.
        Returns a tuple (action_type, value) e.g., ('set_fps', 30), ('toggle_pause', None),
        or ('update_param', {'name': 'PERCEPTION_RADIUS', 'value': 100})
        """
        # Handle slider events
        for i, slider in enumerate(self.sliders):
            if slider.handle_event(event):
                # Update the corresponding setting directly
                setattr(self.settings, slider.label, slider.value)
                return 'update_param', {'name': slider.label, 'value': slider.value}

        # Handle button events
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
            if self.buttons["reset"]["rect"].collidepoint(event.pos):
                return 'reset', None
        return None, None

    def draw(self, screen, paused, current_fps):
        """Draws all UI elements."""
        # Draw sliders
        for slider in self.sliders:
            slider.draw(screen)

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
        
        # Draw Reset button
        self._draw_button(screen, self.buttons["reset"]["rect"], BUTTON_COLOR, "Reset")

    def _draw_button(self, screen, rect, color, text):
        """Helper function to draw a single button."""
        pygame.draw.rect(screen, color, rect)
        text_surface = FONT.render(text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)
