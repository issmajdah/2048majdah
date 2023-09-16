# 2048
# importing pygame
import pygame
import random

pygame.init()

# setup for the game window
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 100
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (245, 255, 255),
          2: (224, 255, 255),
          4: (179, 238, 238),
          8: (176, 224, 230),
          16: (173, 216, 230),
          32: (135, 206, 235),
          64: (135, 206, 250),
          128: (176, 196, 222),
          256: (100, 149, 237),
          512: (95, 158, 160),
          1024: (112, 128, 144),
          2048: (70, 130, 180),
          'light text': (105, 105, 105),
          'dark text': (0, 0, 0),
          'bg': (47, 79, 79),
          'other': (119, 136, 153)}

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
tile_new = True
init_count = 0
die = ''
score = 0
# change the name
file = open('highest_score', 'r')
init_high = int(file.readline())
file.close()
highest_score = init_high


# the texts that appears if the board got filled with tiles "game over"
def draw_over():
    pygame.draw.rect(screen, 'white', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'black')
    game_over_text2 = font.render('Press Enter To Restart', True, 'black')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction from the arrow keys on your laptops
def take_turn(dier, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if dier == 'UP':
        for i in range(4):
            for j in range(4):
                move = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            move += 1
                    if move > 0:
                        board[i - move][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - move - 1][j] == board[i - move][j] and not merged[i - move][j] \
                            and not merged[i - move - 1][j]:
                        board[i - move - 1][j] *= 2
                        score += board[i - move - 1][j]
                        board[i - move][j] = 0
                        merged[i - move - 1][j] = True

    elif dier == 'DOWN':
        for i in range(3):
            for j in range(4):
                move = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        move += 1
                if move > 0:
                    board[2 - i + move][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + move <= 3:
                    if board[2 - i + move][j] == board[3 - i + move][j] and not merged[3 - i + move][j] \
                         and not merged[2 - i + move][j]:
                        board[3 - i + move][j] *= 2
                        score += board[3 - i + move][j]
                        board[2 - i + move][j] = 0
                        merged[3 - i + move][j] = True

    elif dier == 'LEFT':
        for i in range(4):
            for j in range(4):
                move = 0
                for q in range(j):
                    if board[i][q] == 0:
                        move += 1
                if move > 0:
                    board[i][j - move] = board[i][j]
                    board[i][j] = 0
                if board[i][j - move] == board[i][j - move - 1] and not merged[i][j - move - 1] \
                        and not merged[i][j - move]:
                    board[i][j - move - 1] *= 2
                    score += board[i][j - move - 1]
                    board[i][j - move] = 0
                    merged[i][j - move - 1] = True

    elif dier == 'RIGHT':
        for i in range(4):
            for j in range(4):
                move = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        move += 1
                if move > 0:
                    board[i][3 - j + move] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + move <= 3:
                    if board[i][4 - j + move] == board[i][3 - j + move] and not merged[i][4 - j + move] \
                             and not merged[i][3 - j + move]:
                        board[i][4 - j + move] *= 2
                        score += board[i][4 - j + move]
                        board[i][3 - j + move] = 0
                        merged[i][4 - j + move] = True
    return board


# the first 2 tiles in the empty spaces when you start the games
def new_pieces(board):
    count = 0
    full = False
    # to find an empty space in the board and fill it with a random tile
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board where you can see your highest score and your current score
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'DimGrey')
    high_score_text = font.render(f'High Score: {highest_score}', True, 'DimGray')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))
    pass


# drawing the tiles that fills the empty spaces in the board
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if tile_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        tile_new = False
        init_count += 1
    if die != '':
        board_values = take_turn(die, board_values)
        die = ''
        tile_new = True
    if game_over:
        draw_over()
        if highest_score > init_high:
            file = open('highest_score', 'w')
            file.write(f'{highest_score}')
            file.close()
            init_high = highest_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            # for the directions to move the tiles
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                die = 'UP'
            elif event.key == pygame.K_DOWN:
                die = 'DOWN'
            elif event.key == pygame.K_LEFT:
                die = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                die = 'RIGHT'

            # to clear the board and restart the game back from 0
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)]for _ in range(4)]
                    tile_new = True
                    init_count = 0
                    score = 0
                    die = ''
                    game_over = False
    # after the game ends this replaces your old high score with your new high score if there is any
    if score > highest_score:
        highest_score = score

    pygame.display.flip()
pygame.quit()
