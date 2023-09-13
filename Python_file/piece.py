import os

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name  # Name of the piece (e.g., 'pawn', 'knight', etc.)
        self.color = color  # Color of the piece ('white' or 'black')
        
        # Assign a positive or negative value based on piece color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign  # Value of the piece
        self.moves = []  # List to store valid moves
        self.moved = False  # Boolean value to track if the piece has moved
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self, size=80):
        # Generate the path to the piece's image based on color and name
        self.texture = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')

    def add_move(self, move):
        self.moves.append(move)  # Add a valid move to the list

    def clear_moves(self):
        self.moves = []  # Clear the list of valid moves

class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1  # Direction the pawn can move
        super().__init__('pawn', color, 1.0)  # Initialize with the piece's name and value

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        self.left_rook = None  # Reference to the left rook for castling
        self.right_rook = None  # Reference to the right rook for castling
        super().__init__('king', color, 10000.0)
