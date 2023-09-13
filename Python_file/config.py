import pygame
import os

from sound import Sound
from theme import Theme

class Config:
    def __init__(self):
        # Initialize a list of themes
        self.themes = []
        self._add_themes()

        # Initialize the current theme and font
        self.index = 0
        self.theme = self.themes[self.index]
        self.font = pygame.font.SysFont('monospace', 14, bold=True)

        # Initialize sound effects
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))

    def change_theme(self):
        # Cycle through available themes
        self.index = (self.index + 1) % len(self.themes)
        self.theme = self.themes[self.index]

    def _add_themes(self):
        # Define color themes and add them to the list
        blue = Theme((127, 255, 212), (69, 139, 116), (201, 201, 201), (87, 87, 87), '#C86464', '#C84646')
        pink = Theme((255, 182, 193), (219, 112, 147), (255, 255, 255), (0, 0, 0), '#FF69B5', '#FF1493')
        gray = Theme((211, 211, 211), (169, 169, 169), (255, 255, 255), (0, 0, 0), '#A9A9A9', '#808080')

        self.themes = [blue, pink, gray]
