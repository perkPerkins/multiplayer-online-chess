import colors
import pygame
import piece as Piece
WIDTH = 700
ROWS = 8


class Node:
    def __init__(self, row, col, cube_width, color):
        self.row = row
        self.col = col
        self.x = (row * cube_width) + 75
        self.y = (col * cube_width) + 75
        self.color = color
        self.piece = None
        self.width = cube_width

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))
        if self.piece:
            rect = window.get_rect()
            rect.topleft = self.x, self.y
            window.blit(self.piece.img, (self.x + 7, self.y + 6))


class Board:
    def __init__(self):
        self.board = self.make_grid()

    def make_grid(self):
        grid = []
        gap = WIDTH // ROWS
        for y in range(ROWS):
            grid.append([])
            for x in range(ROWS):
                if y % 2 == 0:
                    if x % 2 == 0:
                        grid[y].append(Node(y, x, gap, (240, 255, 240)))  # white
                    else:
                        grid[y].append(Node(y, x, gap, (46, 139, 87)))  # green
                else:
                    if x % 2 == 0:
                        grid[y].append(Node(y, x, gap, (46, 139, 87)))
                    else:
                        grid[y].append(Node(y, x, gap, (240, 255, 240)))
        return grid

    def is_within_bounds(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def is_possible_move(self, row, col, player_color):
        if self.is_within_bounds(row, col):
            if self.board[row][col].piece:
                return self.board[row][col].piece.color != player_color
            return True
        return False

    def is_valid_move(self, old_row, old_col, new_row, new_col, player_color):
        if self.is_possible_move(new_row, new_col, player_color):
            # IF NOT IN CHECK:
            if self.board[old_row][old_col].piece.type == "pawn":
                return self.is_valid_pawn__move(old_row, old_col, new_row, new_col, player_color)
            elif self.board[old_row][old_col].piece.type == "rook":
                return self.is_valid_rook_move(old_row, old_col, new_row, new_col, player_color)
            elif self.board[old_row][old_col].piece.type == "knight":
                return self.is_valid_knight_move(old_row, old_col, new_row, new_col, player_color)
            elif self.board[old_row][old_col].piece.type == "bishop":
                return self.is_valid_bishop_move(old_row, old_col, new_row, new_col, player_color)
            elif self.board[old_row][old_col].piece.type == "queen":
                return self.is_valid_queen_move(old_row, old_col, new_row, new_col, player_color)
            else:
                return self.is_valid_king_move(old_row, old_col, new_row, new_col, player_color)
        return False

    def is_moving_backwards(self, old_col, new_col, player_color):
        if player_color == "black":
            return new_col < old_col
        return new_col > old_col

    def is_valid_pawn__move(self, old_row, old_col, new_row, new_col, player_color):
        if abs(old_row - new_row) == 0 and abs(old_col - new_col) == 2 and \
                not self.board[old_row][old_col].piece.has_moved and not self.board[new_row][new_col].piece:
            if player_color == "black":
                if self.board[old_row][old_col + 1].piece:
                    return False
            else:
                if self.board[old_row][old_col - 1].piece:
                    return False
            return True

        elif abs(old_row - new_row) == 0 and abs(old_col - new_col) == 1 and not self.board[new_row][new_col].piece and \
                not self.is_moving_backwards(old_col, new_col, player_color):
            return True

        elif abs(old_col - new_col) == 1 and abs(old_row - new_row) == 1 and self.board[new_row][new_col].piece and \
                not self.is_moving_backwards(old_col, new_col, player_color):
            if self.board[new_row][new_col].piece.color != player_color:
                return True
        return False

    def is_valid_rook_move(self, old_row, old_col, new_row, new_col, player_color):
        if old_row == new_row or old_col == new_col:
            if old_row == new_row:
                high = max(old_col, new_col)
                low = min(old_col, new_col)
                for i in range(low + 1, high):
                    if self.board[new_row][i].piece:
                        return False
            else:
                high = max(old_row, new_row)
                low = min(old_row, new_row)
                for i in range(low + 1, high):
                    if self.board[i][new_col].piece:
                        return False
            if not self.board[new_row][new_col].piece:
                return True
            elif self.board[new_row][new_col].piece.color != player_color:
                    return True
        return False

    def is_valid_knight_move(self, old_row, old_col, new_row, new_col, player_color):
        if abs(old_row - new_row) == 2 and abs(old_col - new_col) == 1:
            if not self.board[new_row][new_col].piece:
                return True
            return self.board[new_row][new_col].piece.color != player_color

        elif abs(old_row - new_row) == 1 and abs(old_col - new_col) == 2:
            if not self.board[new_row][new_col].piece:
                return True
            return self.board[new_row][new_col].piece.color != player_color

    def is_valid_bishop_move(self, old_row, old_col, new_row, new_col, player_color):
        if abs(old_row - new_row) == abs(old_col - new_col):
            if old_row == old_col:
                low = min(old_row, new_row)
                high = max(old_row, new_row)
                for i in range(low + 1, high):
                    if self.board[i][i].piece:
                        return False
            elif old_row < new_row and old_col > new_col:
                col = old_col - 1
                for i in range(old_row + 1, new_row):
                    if self.board[i][col].piece:
                        return False
                    col -= 1
            elif old_row < new_row and old_col < new_col:
                col = old_col + 1
                for i in range(old_row + 1, new_row):
                    if self.board[i][col].piece:
                        return False
                    col += 1
            else:
                row = old_row - 1
                for i in range(old_col + 1, new_col):
                    if self.board[row][i].piece:
                        return False
                    row -= 1
            if not self.board[new_row][new_col].piece:
                return True
            return self.board[new_row][new_col].piece != player_color
        return False

    def is_valid_king_move(self, old_row, old_col, new_row, new_col, player_color):
        # Castle
        if not self.board[old_row][old_col].piece.has_moved and abs(old_row - new_row) == 2 and old_col == new_col:
            if new_row == 2:    # rook side castle
                if self.board[old_row - 1][old_col].piece or self.board[new_row - 1][old_col].piece:
                    return False
                if self.board[new_row - 2][new_col].piece:
                    if self.board[new_row - 2][new_col].piece.has_moved:
                        return False
                else:
                    return False
            else:   # king side castle
                if self.board[old_row + 1][old_col].piece:
                    return False
                if self.board[new_row + 1][new_col].piece:
                    if self.board[new_row + 1][new_col].piece.has_moved:
                        return False
                else:
                    return False
            return True
        if (abs(old_row - new_row) == 1 and abs(old_col - new_col) == 1) or \
            (abs(old_row - new_row) == 1 and abs(old_col - new_col) == 0) or \
             (abs(old_row - new_row) == 0 and abs(old_col - new_col) == 1):
            if not self.board[new_row][new_col].piece:
                return True
            return self.board[new_row][new_col].piece.color != player_color
        return False

    def is_valid_queen_move(self, old_row, old_col, new_row, new_col, player_color):
        return self.is_valid_bishop_move(old_row, old_col, new_row, new_col, player_color) or \
            self.is_valid_rook_move(old_row, old_col, new_row, new_col, player_color)

