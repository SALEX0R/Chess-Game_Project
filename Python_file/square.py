class Square:
    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    def __init__(self, row, col, piece=None):
        """
        Initialize a Square object with its row, column, and an optional piece.

        Args:
            row (int): The row index of the square.
            col (int): The column index of the square.
            piece (Piece, optional): The chess piece placed on the square (default is None).
        """
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __eq__(self, other):
        """
        Compare two Square objects for equality based on their row and column.

        Args:
            other (Square): The other Square object to compare.

        Returns:
            bool: True if the squares are equal, False otherwise.
        """
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        """
        Check if the square has a chess piece.

        Returns:
            bool: True if the square has a piece, False otherwise.
        """
        return self.piece is not None

    def isempty(self):
        """
        Check if the square is empty (no piece).

        Returns:
            bool: True if the square is empty, False otherwise.
        """
        return not self.has_piece()

    def has_team_piece(self, color):
        """
        Check if the square has a chess piece of the specified color.

        Args:
            color (str): The color of the chess piece ('white' or 'black').

        Returns:
            bool: True if the square has a piece of the specified color, False otherwise.
        """
        return self.has_piece() and self.piece.color == color

    def has_enemy_piece(self, color):
        """
        Check if the square has a chess piece of an enemy color.

        Args:
            color (str): The color of the chess piece ('white' or 'black').

        Returns:
            bool: True if the square has a piece of an enemy color, False otherwise.
        """
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color):
        """
        Check if the square is empty or has a chess piece of an enemy color.

        Args:
            color (str): The color of the chess piece ('white' or 'black').

        Returns:
            bool: True if the square is empty or has a piece of an enemy color, False otherwise.
        """

        return self.isempty() or self.has_enemy_piece(color)

    @staticmethod
    def in_range(*args):
        """
        Check if the given values are within the valid range [0, 7] for a chessboard.

        Args:
            *args: Variable number of integer arguments to check.

        Returns:
            bool: True if all values are within the range, False otherwise.
        """
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    @staticmethod
    def get_alphacol(col):
        """
        Get the alphabetic column label for the given column index.

        Args:
            col (int): The column index (0-7).

        Returns:
            str: The alphabetic column label ('a' to 'h').
        """
        return Square.ALPHACOLS[col]
    