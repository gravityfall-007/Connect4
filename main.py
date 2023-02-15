import pygame
import sys
import math
from variables import *
from controller import Controller

pygame.display.set_caption('Connect 4')


def main():
    global game_over
    while not game_over:

        # Starting the game
        pygame.init()
        screen = pygame.display.set_mode(size)
        game_over = False
        restartNow = False
        turn = 0
        # Instantiation of game
        connect4 = Controller(screen)
        connect4.model.print_board()

        # initializing the font
        font = pygame.font.SysFont("monospace", 50, bold=True, italic=True)

        # Instantiation of board
        connect4.view.draw_board(connect4.model.board, screen)
        pygame.display.update()

        while not (game_over or restartNow):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restartNow = True

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, Black, (0, 0, Width, SquareSize))
                    PositionX = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(screen, Red, (PositionX, int(SquareSize / 2)), Radius)
                    else:
                        pygame.draw.circle(screen, Yellow, (PositionX, int(SquareSize / 2)), Radius)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, Black, (0, 0, Width, SquareSize))
                    # player 1 turn
                    if turn == 0:
                        PositionX = event.pos[0]
                        col = int(math.floor(PositionX / SquareSize))

                        if connect4.model.is_valid_location(col):
                            row = connect4.model.get_next_open_row(col)
                            connect4.model.draw_boards(row, col, 1)
                            connect4.view.draw_board(connect4.model.board, screen)

                            if connect4.win_check(1):
                                label = font.render('Player 1 Won', 1, Red)
                                screen.blit(label, (250, 50))
                                pygame.display.update()
                                game_over = True

                    # player 2 turn
                    else:
                        PositionX = event.pos[0]
                        col = int(math.floor(PositionX / SquareSize))

                        if connect4.model.is_valid_location(col):
                            row = connect4.model.get_next_open_row(col)
                            connect4.model.draw_boards(row, col, 2)
                            connect4.view.draw_board(connect4.model.board, screen)

                            if connect4.win_check(2):
                                label = font.render('Player 2 Won', 2, Yellow)
                                screen.blit(label, (250, 50))
                                pygame.display.update()
                                game_over = True

                    connect4.model.print_board()

                    turn += 1
                    turn = turn % 2

                    if game_over:
                        pygame.time.wait(2000)


if __name__ == '__main__':
    main()
