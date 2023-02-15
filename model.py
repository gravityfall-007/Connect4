import numpy as np
from variables import *


class Model:
    def __init__(self):
        self.board = np.zeros((Row, Column))

    def draw_boards(self, row, col, piece):
        self.board[row][col] = piece

    def print_board(self):
        print(np.flip(self.board, 0))

    def is_valid_location(self, col):
        return self.board[5][col] == 0

    def get_next_open_row(self, col):
        for i in range(Row):
            if self.board[i][col] == 0:
                return i
