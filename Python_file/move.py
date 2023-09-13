class Move:
    def __init__(self, initial, final):
        # `initial` and `final` are instances of the `Square` class
        self.initial = initial
        self.final = final

    def __str__(self):
        # Create a string representation of the move
        return f'({self.initial.col}, {self.initial.row}) -> ({self.final.col}, {self.final.row})'

    def __eq__(self, other):
        # Compare moves for equality based on their initial and final squares
        return self.initial == other.initial and self.final == other.final
