import numpy as np
import pygame
import sys
import math
import random

Row = 6
Column = 7
SquareSize = 100
Width = Column * SquareSize
Height = (Row + 1) * SquareSize
size = (Width, Height)
Background = (45, 90, 226)
Black = (0, 0, 0)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
Radius = int(SquareSize / 2 - 7)

Player = 0
AI = 1

Empty = 0
Player_Piece = 1
AI_Piece = 2
Window_Length = 4



def create_board():
    board = np.zeros((6,7))
    return board
def draw_boards(board, row, col, piece):
    board[row][col] = piece

def print_board(board):
    print(np.flip(board, 0))

def is_valid_location(board, col):
    return board[5][col] == 0

def get_next_open_row(board, col):
    for i in range(Row):
        if board[i][col] ==0:
            return i

def win_check(board, piece):
    # Checking Horizontal pieces for a win
    for col in range(Column-3):
        for row in range(Row):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # Checking vertical pieces for a win
    for col in range(Column):
        for row in range(Row - 3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # Checking upward diagonal pieces for a win
    for col in range(Column-3):
        for row in range(Row - 3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    # checking downward diagonal pieces for a win
    for col in range(Column-3):
        for row in range(3, Row):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True


def draw_board(board):
    for col in range(Column):
        for row in range(Row):
            pygame.draw.rect(screen, Background, (col * SquareSize, (row * SquareSize + SquareSize), SquareSize, SquareSize))
            pygame.draw.circle(screen, Black, (int(col * SquareSize + SquareSize / 2), int(row * SquareSize + SquareSize + SquareSize / 2)), Radius)

    for col in range(Column):
        for row in range(Row):
            if board[row][col] == 1:
                pygame.draw.circle(screen, Red, (
                int(col * SquareSize + SquareSize / 2), Height - int(row * SquareSize + SquareSize / 2)), Radius)
            elif board[row][col] == 2:
                pygame.draw.circle(screen, Yellow, (
                int(col * SquareSize + SquareSize / 2), Height - int(row * SquareSize + SquareSize / 2)), Radius)
    pygame.display.update()

def evaluate_window(window, piece):
	score = 0
	opp_piece = Player_Piece
	if piece == Player_Piece:
		opp_piece = AI_Piece

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(Empty) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(Empty) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(Empty) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, Column//2])]
	center_count = center_array.count(piece)
	score += center_count * 3


	## Score Vertical
	for c in range(Column):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(Row-3):
			window = col_array[r:r+Window_Length]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(Row-3):
		for c in range(Column-3):
			window = [board[r+i][c+i] for i in range(Window_Length)]
			score += evaluate_window(window, piece)

	for r in range(Row-3):
		for c in range(Column-3):
			window = [board[r+3-i][c+i] for i in range(Window_Length)]
			score += evaluate_window(window, piece)

	return score


def get_valid_locations(board):
	valid_locations = []
	for col in range(Column):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations


def pick_best_move(board, piece):

	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		draw_boards(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

def is_terminal_node(board):
	return win_check(board, Player_Piece) or win_check(board, AI_Piece) or len(get_valid_locations(board)) == 0


def minimax(board, depth, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if win_check(board, AI_Piece):
				return (None, 100000000000000)
			elif win_check(board, Player_Piece):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_Piece))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			draw_boards(b_copy, row, col, AI_Piece)
			new_score = minimax(b_copy, depth-1, False)[1]
			if new_score > value:
				value = new_score
				column = col
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			draw_boards(b_copy, row, col, Player_Piece)
			new_score = minimax(b_copy, depth-1, True)[1]
			if new_score < value:
				value = new_score
				column = col
		return column, value

def reset_board(screen):
    for col in range(Column):
        for row in range(Row):
            board[row][col] = 0
            pygame.draw.rect(screen, Background, (col * SquareSize, (row * SquareSize + SquareSize), SquareSize, SquareSize))
            pygame.draw.circle(screen, Black, (int(col * SquareSize + SquareSize / 2), int(row * SquareSize + SquareSize + SquareSize / 2)), Radius)


board = create_board()
print_board(board)
game_over = False
#turn = 0
turn = random.randint(Player, AI)

# Start the screen
pygame.init()
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
font = pygame.font.SysFont("monospace", 50, bold=True, italic=True)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_board(screen)

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
            # Player 1 input
            if turn == Player:
                PositionX = event.pos[0]   # getting position from mouse click
                col = int(math.floor(PositionX/SquareSize))  # math.floor to round up the value
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    draw_boards(board, row, col, Player_Piece)

                    if win_check(board, Player_Piece):
                        label = font.render('Player 1 Won', 1, Red)
                        screen.blit(label, (250,50))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)


    # Player 2/AI input
    if turn == AI and not game_over:
        #col = pick_best_move(board, AI_Piece)
        col, minimax_score = minimax(board, 3, True)   # When the value of depth is more than 4 it take more time to
                                                       #process & execute since it checks all the possible position.

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            draw_boards(board, row, col, AI_Piece)
            if win_check(board, 2):
                label = font.render('Player 2 Won', 2, Yellow)
                screen.blit(label, (250,50))
                game_over = True


        print_board(board)
        draw_board(board)

        turn += 1
        turn = turn % 2

    if game_over:
        pygame.time.wait(2000)

