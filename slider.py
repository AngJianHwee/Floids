import pygame
from settings import FONT, WHITE, BUTTON_COLOR, BUTTON_SELECTED_COLOR

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label, step=1, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.step = step
        self.text_color = text_color
        self.dragging = False

        self.handle_radius = height // 2
        self._update_handle_pos()

    def _update_handle_pos(self):
        # Calculate handle position based on current value
        # Ensure value is within min_val and max_val
        self.value = max(self.min_val, min(self.max_val, self.value))
        
        # Calculate the normalized position (0 to 1) of the handle
        normalized_value = (self.value - self.min_val) / (self.max_val - self.min_val)
        
        # Calculate the x-coordinate for the handle's center
        # The handle can move from self.rect.left + handle_radius to self.rect.right - handle_radius
        self.handle_x = self.rect.left + self.handle_radius + \
                        normalized_value * (self.rect.width - 2 * self.handle_radius)
        
        self.handle_pos = (int(self.handle_x), self.rect.centery)

    def handle_event(self, event):
        value_changed = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                value_changed = self._set_value_from_mouse(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                value_changed = self._set_value_from_mouse(event.pos)
        return value_changed

    def _set_value_from_mouse(self, mouse_pos):
        # Calculate the new handle_x based on mouse_pos.x
        # Constrain mouse_x to the draggable area of the slider
        mouse_x = max(self.rect.left + self.handle_radius, 
                      min(self.rect.right - self.handle_radius, mouse_pos[0]))
        
        # Calculate the normalized position (0 to 1)
        normalized_pos = (mouse_x - (self.rect.left + self.handle_radius)) / \
                         (self.rect.width - 2 * self.handle_radius)
        
        # Convert normalized position back to value, applying step
        new_value = self.min_val + normalized_pos * (self.max_val - self.min_val)
        
        # Apply stepping
        new_value = round(new_value / self.step) * self.step
        
        # Ensure value is within bounds after stepping
        new_value = max(self.min_val, min(self.max_val, new_value))

        if new_value != self.value:
            self.value = new_value
            self._update_handle_pos()
            return True
        return False

    def draw(self, screen):
        # Draw slider track
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect, border_radius=3)
        
        # Draw filled portion of the track (optional, but good for visual feedback)
        fill_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, BUTTON_SELECTED_COLOR, fill_rect, border_radius=3)

        # Draw handle
        pygame.draw.circle(screen, WHITE, self.handle_pos, self.handle_radius)
        pygame.draw.circle(screen, BUTTON_SELECTED_COLOR, self.handle_pos, self.handle_radius - 2)

        # Draw label and value
        label_surface = FONT.render(f"{self.label}: {self.value:.1f}", True, self.text_color)
        label_rect = label_surface.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
        screen.blit(label_surface, label_rect)

