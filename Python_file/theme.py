from color import Color

class Theme:
    def __init__(self, light_bg, dark_bg, light_trace, dark_trace, light_moves, dark_moves):
        """
        Initialize a Theme object with color attributes for the background, trace, and moves.

        Args:
            light_bg (tuple): RGB tuple representing the light background color.
            dark_bg (tuple): RGB tuple representing the dark background color.
            light_trace (tuple): RGB tuple representing the light trace color.
            dark_trace (tuple): RGB tuple representing the dark trace color.
            light_moves (tuple): RGB tuple representing the light moves color.
            dark_moves (tuple): RGB tuple representing the dark moves color.
        """
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
