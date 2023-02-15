import pygame
from variables import *


class View:
    def __init__(self):
        pass

    def draw_board(self, board, screen):
        for c in range(Column):
            for r in range(Row):
                pygame.draw.rect(screen, Background, (c * SquareSize, r * SquareSize + SquareSize, SquareSize, SquareSize))
                pygame.draw.circle(screen, Black, (
                    int(c * SquareSize + SquareSize / 2), int(r * SquareSize + SquareSize + SquareSize / 2)), Radius)

        for c in range(Column):
            for r in range(Row):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, Red, (
                        int(c * SquareSize + SquareSize / 2), Height - int(r * SquareSize + SquareSize / 2)), Radius)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, Yellow, (
                        int(c * SquareSize + SquareSize / 2), Height - int(r * SquareSize + SquareSize / 2)), Radius)
        pygame.display.update()

