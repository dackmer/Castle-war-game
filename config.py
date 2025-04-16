import pygame

# Screen settings
WIDTH, HEIGHT = 1000, 800  # Increased for better UI layout

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

Button_COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}

COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "gray": (128, 128, 128),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128)
}

# add more soldier class or up level of the castle
#

# Fonts
pygame.init()
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 24)