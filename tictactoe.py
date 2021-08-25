"""
Tic Tac Toe Player
"""
import math
import copy
import time

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X always goes first
    # if number of moves on board is odd, then it's O's turn
    # else, it's X's turn
    empty_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                empty_count += 1
    if empty_count % 2 != 0:
        return X
    else:
        return O
    raise NotImplementedError

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # actions = for blank spaces: place turn in blank space
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                actions.add((i, j))
    return actions
    raise NotImplementedError

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # result = action + current state
    i = action[0]
    j = action[1]
    if board[i][j] == None:
        result_board = copy.deepcopy(board)
        result_board[i][j] = player(board)
        return result_board
    else:
        raise NotImplementedError
    raise NotImplementedError

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if three in a row or board full, game is over
    mark = 'X'
    for j in range(2):
        # check for horizontal 3-in-a-row
        for i in range(3):
            if board[i][0] == mark and board[i][1] == mark and board[i][2] == mark:
                return True
        # check for vertical 3-in-a-row
        for i in range(3):
            if board[0][i] == mark and board[1][i] == mark and board[2][i] == mark:
                return True
        # check for diagonal top left to bottom right 3-in-a-row
        if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
            return True
        # check for diagonal top right to bottom left 3-in-a-row
        if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
            return True
        mark = 'O'
    # if there is no 3 in a row, check for blank spaces
    # if blank space is detected, game is not over (because no 3-in-a-row and board not filled yet)
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                return False
    return True

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # if X has three in a row, return 1
    # if O has three in a row, return -1
    # else, it's a draw. Return 0
    mark = 'X'
    for j in range(2):
        # check for horizontal 3-in-a-row
        for i in range(3):
            if board[i][0] == mark and board[i][1] == mark and board[i][2] == mark:
                return mark
        # check for vertical 3-in-a-row
        for i in range(3):
            if board[0][i] == mark and board[1][i] == mark and board[2][i] == mark:
                return mark
        # check for diagonal top left to bottom right 3-in-a-row
        if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
            return mark
        # check for diagonal top right to bottom left 3-in-a-row
        if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
            return mark
        mark = 'O'
    # if there is no 3 in a row, check for blank spaces
    # if blank space is detected, game is not over (because no 3-in-a-row and board not filled yet)
    blank_space_count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                blank_space_count += 1
    if blank_space_count == 0:
        return None
    raise NotImplementedError

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    elif winner(board) == None:
        return 0
    raise NotImplementedError

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # looks at future turns until end game is reached, then chooses the path with the highest or lowest value (depending on whether you're playing as X or O)
    #look at current game state
    #consider each move ai bot can make
    #then, from each of those moves, consider each move oponent would likely take
    #repeat until end of game
    #choose path with optimal value
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = -math.inf
        # for every possible action, calculate largest value poss given what action the oponent would likely take
        for action in actions(board):
            v = max(v, min_value(result(board, action), alpha, beta))
            # use alpha beta pruning - skip sub optimal nodes for max efficiency
            if v >= beta:
                return v
            if v > alpha:
                alpha = v
        return v

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action), alpha, beta))
            if v <= alpha:
                return v
            if v < beta:
                beta = v
        return v
    if player(board) == 'X':
        start = time.time()
        bestv = -math.inf
        # for each possible move, return what move opponent O could do and pick the one with the best end result
        for action in actions(board):
            v = min_value(result(board, action),-math.inf, math.inf)
            if v > bestv:
                bestv = v
                optimalMove = action
        end = time.time()
        total = end - start
        # prints compute time for move for ease of understanding/comparing program efficiency
        print("X compute time:", total)
        return optimalMove

    if player(board) == 'O':
        start = time.time()
        bestv = math.inf
        for action in actions(board):
            v = max_value(result(board, action),-math.inf, math.inf)
            if v < bestv:
                bestv = v
                optimalMove = action
        end = time.time()
        total = end - start
        print("O compute time:", total)
        return optimalMove
    
    raise NotImplementedError



