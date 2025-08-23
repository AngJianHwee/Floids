# settings.py

import pygame

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_CAPTION = "Boids Simulation"

# Boids settings
BOID_COUNT = 50
PERCEPTION_RADIUS = 75
SEPARATION_RADIUS = 25
MAX_SPEED = 3
MAX_FORCE = 0.05

# Flocking rule weights
COHESION_WEIGHT = 1.0
ALIGNMENT_WEIGHT = 1.5
SEPARATION_WEIGHT = 2.0

# Parameter ranges for UI sliders
PARAM_RANGES = {
    "PERCEPTION_RADIUS": {"min": 50, "max": 200, "initial": PERCEPTION_RADIUS, "step": 5},
    "SEPARATION_RADIUS": {"min": 10, "max": 50, "initial": SEPARATION_RADIUS, "step": 1},
    "MAX_SPEED": {"min": 1, "max": 10, "initial": MAX_SPEED, "step": 0.5},
    "MAX_FORCE": {"min": 0.01, "max": 0.1, "initial": MAX_FORCE, "step": 0.01},
    "COHESION_WEIGHT": {"min": 0.0, "max": 3.0, "initial": COHESION_WEIGHT, "step": 0.1},
    "ALIGNMENT_WEIGHT": {"min": 0.0, "max": 3.0, "initial": ALIGNMENT_WEIGHT, "step": 0.1},
    "SEPARATION_WEIGHT": {"min": 0.0, "max": 3.0, "initial": SEPARATION_WEIGHT, "step": 0.1},
}

# Frame Rates
FPS_OPTIONS = {
    "slow": 1,
    "fast": 5,
    "very_fast": 30,
    "extremely_fast": 120,
}
DEFAULT_FPS = FPS_OPTIONS["extremely_fast"]

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)

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
