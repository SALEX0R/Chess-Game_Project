import copy
from const import *
from square import Square
from piece import *
from move import Move

class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # Console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # Pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        # King Castling
        if isinstance(piece, King):
            if self.castling(initial, final):
                difference = final.col - initial.col
                rook = piece.left_rook if difference < 0 else piece.right_rook
                # Recursion
                if rook.moves: # Check if rook.moves is not empty
                    self.move(rook, rook.moves[-1])

        # Move
        piece.moved = True

        # Clear valid moves
        piece.clear_moves()
        
        # Set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        # Cloning our board
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    P = temp_board.squares[row][col].piece  # P = Piece
                    temp_board.calc_moves(P, row, col, bool=False)
                    for M in P.moves:  # M = moves
                        if isinstance(M.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):
        # Calculate all the possible (valid) moves of a specific piece on a specific location

        def pawn_moves():
            # Steps
            steps = 1 if piece.moved else 2

            # Vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # Create a new move
                        move = Move(initial, final)

                        # Checking check
                        if bool:
                            if not self.in_check(piece, move):
                                # Append new move
                                piece.add_move(move)
                        else:
                            # Append new move
                            piece.add_move(move)
                    # Blocked
                    else:
                        break
                # Not in range
                else:
                    break

            # Diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # Create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create a new move
                        move = Move(initial, final)
                        # Checking check
                        if bool:
                            if not self.in_check(piece, move):
                                # Append new move
                                piece.add_move(move)
                        else:
                            # Append new move
                            piece.add_move(move)

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # Create squares of the new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create a new move
                        move = Move(initial, final)
                        # Checking check
                        if bool:
                            if not self.in_check(piece, move):
                                # Append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # Append new move
                            piece.add_move(move)

        def straightline_moves(incrs):  # Stand for increments
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # Create square of the possible move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # Create a possible new move
                        move = Move(initial, final)
                        # Empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # Checking check
                            if bool:
                                if not self.in_check(piece, move):
                                    # Append new move
                                    piece.add_move(move)
                            else:
                                # Append new move
                                piece.add_move(move)

                        # Has enemy piece = break + add move
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # Checking check
                            if bool:
                                if not self.in_check(piece, move):
                                    # Append new move
                                    piece.add_move(move)
                            else:
                                # Append new move
                                piece.add_move(move)
                            break

                        # Has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # Not in range
                    else:
                        break

                    # Incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():  # Adjacents
            adjs = [
                (row - 1, col + 0),  # Up
                (row - 1, col + 1),  # Up-right
                (row + 0, col + 1),  # Right
                (row + 1, col + 1),  # Down-right
                (row + 1, col + 0),  # Down
                (row + 1, col - 1),  # Down-left
                (row + 0, col - 1),  # Left
                (row - 1, col - 1)  # Up-left
            ]

            # Normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # Create squares of the new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)  # piece = piece
                        # Create a new move
                        move = Move(initial, final)
                        # Checking check
                        if bool:
                            if not self.in_check(piece, move):
                                # Append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            # Append new move
                            piece.add_move(move)

            # Castling moves
            if not piece.moved:

                # Queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for coloumn in range(1, 4):
                            # Castling is not possible because there are pieces in between
                            if self.squares[row][coloumn].has_piece():
                                break

                            if coloumn == 3:
                                # Adds left rook to king
                                piece.left_rook = left_rook

                                # Rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                move_R = Move(initial, final)

                                # King move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move_K = Move(initial, final)

                                # Checking check
                                if bool:
                                    if not self.in_check(piece, move_K) and not self.in_check(left_rook, move_R):
                                        # Append new move to Rook
                                        left_rook.add_move(move_R)
                                        # Append new move to King
                                        piece.add_move(move_K)
                                else:
                                    # Append new move to Rook
                                    left_rook.add_move(move_R)
                                    # Append new move to king
                                    piece.add_move(move_K)

                # King castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for coloumn in range(5, 7):
                            # Castling is not possible because there are pieces in between
                            if self.squares[row][coloumn].has_piece():
                                break

                            if coloumn == 6:
                                # Adds right rook to king
                                piece.right_rook = right_rook

                                # Rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                move_R = Move(initial, final)

                                # King move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move_K = Move(initial, final)

                                # Checking check
                                if bool:
                                    if not self.in_check(piece, move_K) and not self.in_check(right_rook, move_R):
                                        # Append new move to Rook
                                        right_rook.add_move(move_R)
                                        # Append new move to King
                                        piece.add_move(move_K)
                                else:
                                    # Append new move to Rook
                                    right_rook.add_move(move_R)
                                    # Append new move to king
                                    piece.add_move(move_K)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # Up-right row-col
                (-1, -1),  # Up-left
                (1, 1),  # Down-right
                (1, -1)  # Down left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # Up
                (0, 1),  # Right
                (1, 0),  # Down
                (0, -1)  # Left
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # Up-right row-col
                (-1, -1),  # Up-left
                (1, 1),  # Down-right
                (1, -1),  # Down left
                (-1, 0),  # Up
                (0, 1),  # Right
                (1, 0),  # Down
                (0, -1)  # Left
            ])

        elif isinstance(piece, King):
            king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
