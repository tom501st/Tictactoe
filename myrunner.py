import pygame, sys
# import numpy as np
import tictactoe as ttt
import time, math

pygame.init()

WIDTH = 600
HEIGHT = 500
BOARD_ROWS = 3
BOARD_COLS = 3
TILE_SIZE = 134

GREEN = (200, 220, 184)
PURPLE = (206, 201, 223)
YELLOW = (253, 241, 202)
PEACH = (237, 204, 182)
BLUE = (178, 198, 222)
WHITE = (225, 225, 225)

board = ttt.initial_state()

smallFont = pygame.font.Font("OpenSans-Regular.ttf", 20)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
medFont = pygame.font.Font("OpenSans-Regular.ttf", 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption( 'TIC TAC TOE' )


def draw_lines():
    # vertical lines
    pygame.draw.line(screen, WHITE, (233, 70), (233, 472), 10)
    pygame.draw.line(screen, WHITE, (367, 70), (367, 472), 10)
    # horizontal lines
    pygame.draw.line(screen, WHITE, (99, 204), (501, 204), 10)
    pygame.draw.line(screen, WHITE, (99, 338), (501, 338), 10)

def draw_X(pos):
    """
    draws an 'X' at a given position
    """
    X_line1 = pygame.draw.line(screen, WHITE, (pos[0] - 30, pos[1] - 30), (pos[0] + 30, pos[1] + 30), 10)
    X_line2 = pygame.draw.line(screen, WHITE, (pos[0] - 30, pos[1] + 30), (pos[0] + 30, pos[1] - 30), 10)

def draw_O(pos):
    """
    draws an 'O' at a given position
    """
    O_circle = pygame.draw.circle(screen, WHITE, pos, 35, 8)

def draw_board():
    for y in range(BOARD_ROWS):
        for x in range(BOARD_COLS):
            pos = [(166 + (x * TILE_SIZE)), (137 + (y * TILE_SIZE))]
            if board[y][x] == 'X':
                draw_X(pos)
            elif board[y][x] == 'O':
                draw_O(pos)

def draw_message():
    """
    writes a message saying whether it is the user's turn or whether the AI is currently thinking.
    """
    if ttt.player(board) == AIuser:
        message_text = "AI thinking..."
        time.sleep(0.5)
    if ttt.player(board) == user:
        message_text = "It's your turn."
    message = largeFont.render(message_text, True, WHITE)
    messageRect = message.get_rect()
    messageRect.center = ((WIDTH / 2), 30)
    screen.blit(message, messageRect)

def winner_message():
    """
    writes a message designed for the end of the game, telling who won.
    """
    winner = ttt.winner(board)
    if winner == AIuser:
        message_text = "AI wins."
    elif winner == None:
        message_text = "It's a draw."
    else:
        message_text = "Wait...what? You won!?"
    message = largeFont.render(message_text, True, WHITE)
    messageRect = message.get_rect()
    messageRect.center = ((WIDTH / 2), 30)
    screen.blit(message, messageRect)

def play_again():
    """
    renders a clickable 'play again' button.
    """
    play_again_text = medFont.render("Play again", True, WHITE)
    rect = play_again_text.get_rect()
    rect.center = ((WIDTH / 2), 28)
    button = pygame.Rect((WIDTH / 4), 290, 240, 45)
    button.center = ((WIDTH / 2), 30)
    pygame.draw.rect(screen, PEACH, button, border_radius = 25)
    screen.blit(play_again_text, rect)

    if event.type == pygame.MOUSEBUTTONUP:
        if button.collidepoint(pygame.mouse.get_pos()):
            return True

user = None
winner_message_shown = False

# mainloop
while True:
    # constantly checks if quit button is pressed by checking each
    # event (clicks, mouse moves etc.) and seeing if it is of type pygame.QUIT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(PURPLE)

    if user == None:
        # display start screen
        # write title and subtitle
        title = largeFont.render("Play TIC-TAC-TOE vs. AI", True, WHITE)
        subtitle = smallFont.render("GUI and AI by Tom Choi", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((WIDTH / 2), 65)
        subtitleRect = subtitle.get_rect()
        subtitleRect.center = ((WIDTH / 2), 105)
        screen.blit(title, titleRect)
        screen.blit(subtitle, subtitleRect)

        # write play as X and draw button
        playX = largeFont.render("Play as X", True, WHITE)
        xRect = playX.get_rect()
        xRect.center = ((WIDTH / 4), 290)
        playXbutton = pygame.Rect((WIDTH / 4), 290, 240, 75)
        playXbutton.center = xRect.center
        pygame.draw.rect(screen, PEACH, playXbutton, border_radius = 25)
        screen.blit(playX, xRect)

        # write play as O and draw button
        playO = largeFont.render("Play as O", True, WHITE)
        oRect = playO.get_rect()
        oRect.center = ((WIDTH / 4) * 3, 290)
        playObutton = pygame.Rect((WIDTH / 4) * 3, 290, 240, 75)
        playObutton.center = oRect.center
        pygame.draw.rect(screen, PEACH, playObutton, border_radius = 25)
        screen.blit(playO, oRect)

        # create parameters to check if button is clicked
        if event.type == pygame.MOUSEBUTTONUP:
            if playXbutton.collidepoint(pygame.mouse.get_pos()):
                user = ttt.X
                AIuser = ttt.O

            if playObutton.collidepoint(pygame.mouse.get_pos()):
                user = ttt.O
                AIuser = ttt.X
    else:
        draw_lines()
        draw_board()
        if ttt.terminal(board):
            if winner_message_shown == False:
                winner_message()
                pygame.display.flip()
                time.sleep(4)
                winner_message_shown = True
            else:
                if play_again():
                    user = None
                    board = ttt.initial_state()
                    winner_message_shown = False

        else:
            draw_message()
            if ttt.player(board) == user:
                # Wait for user input
                # Find where user clicked on screen and map it to a board position
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    # If mouse click is within the tictactoe board
                    if 99 < mouseX < 501 and 70 < mouseY < 472:
                        clicked_col = int((mouseX-99) // TILE_SIZE)
                        clicked_row = int((mouseY-70) // TILE_SIZE)
                        if board[clicked_row][clicked_col] == None:
                            board = ttt.result(board, (clicked_row, clicked_col))
                            draw_board()

            # If it is the AI's turn
            else:
                pygame.display.flip()
                time.sleep(0.7)
                turn_pos = (ttt.minimax(board))
                board = ttt.result(board, turn_pos)
                draw_board()

    # updates screen at end of each loop
    pygame.display.flip()


#       TO DO:
#           - fix minimax not playing optimal move when player makes a sub-optimal move
