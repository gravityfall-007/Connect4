from model import Model
from view import View
from variables import *


class Controller:
    def __init__(self, screen):
        self.model = Model()
        self.view = View()
        self.screen = screen

    def win_check(self, piece):
        # Checking Horizontal pieces for a win
        for col in range(Column - 3):
            for row in range(Row):
                if self.model.board[row][col] == piece and self.model.board[row][col + 1] == piece and \
                        self.model.board[row][col + 2] == piece and \
                        self.model.board[row][col + 3] == piece:
                    return True

        # Checking vertical pieces for a win
        for col in range(Column):
            for row in range(Row - 3):
                if self.model.board[row][col] == piece and self.model.board[row + 1][col] == piece and \
                        self.model.board[row + 2][col] == piece and \
                        self.model.board[row + 3][col] == piece:
                    return True

        # Checking upward diagonal pieces for a win
        for col in range(Column - 3):
            for row in range(Row - 3):
                if self.model.board[row][col] == piece and self.model.board[row + 1][col + 1] == piece and \
                        self.model.board[row + 2][
                            col + 2] == piece and self.model.board[row + 3][col + 3] == piece:
                    return True

        # checking downward diagonal pieces for a win
        for col in range(Column - 3):
            for row in range(3, Row):
                if self.model.board[row][col] == piece and self.model.board[row - 1][col + 1] == piece and \
                        self.model.board[row - 2][
                            col + 2] == piece and self.model.board[row - 3][col + 3] == piece:
                    return True
