# settings.py

import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_CAPTION = "The incredible guessing game"

# Frame Rates
FPS_OPTIONS = {
    "slow": 1,
    "fast": 5,
    "very_fast": 30
}
DEFAULT_FPS = FPS_OPTIONS["very_fast"]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)

# Button settings
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30
BUTTON_COLOR = (100, 100, 100)
BUTTON_SELECTED_COLOR = (50, 50, 50)
BUTTON_TEXT_COLOR = WHITE

# Font
try:
    pygame.font.init()
    FONT = pygame.font.Font(None, 24)
except pygame.error:
    print("Warning: Font could not be loaded.")
    FONT = None