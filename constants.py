import pygame
pygame.font.init()
# Constants
WIDTH, HEIGHT = 900, 700
FPS = 60
FONT_TITLE = pygame.font.SysFont('Arial', 24, bold=True)
FONT_BUTTON = pygame.font.SysFont('Arial', 14, bold=True)
FONT_NORMAL = pygame.font.SysFont('Arial', 12)
FONT_SMALL = pygame.font.SysFont('Arial', 10)
FONT_COURIER = pygame.font.SysFont('Courier', 10)

# Colors
BG_COLOR = (44, 62, 80)
FRAME_COLOR = (52, 73, 94)
TEXT_COLOR = (236, 240, 241)
BUTTON_GREEN = (39, 174, 96)
BUTTON_BLUE = (52, 152, 219)
BUTTON_ORANGE = (230, 126, 34)
BUTTON_RED = (231, 76, 60)
BUTTON_GRAY = (149, 165, 166)