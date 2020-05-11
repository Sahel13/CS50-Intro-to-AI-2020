"""
Tic Tac Toe Player
"""

import math
import copy

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
    Works by counting the number of non-empty elements of the board
    """
    numPlays = 0
    for row in board:
        for element in row:
            if element is not None:
                numPlays += 1
    if numPlays % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    setOfActions = set()
    for row in range(0, 3):
        for column in range(0, 3):
            if not board[row][column]:
                setOfActions.add((row, column))
    return setOfActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, column = action
    if board[row][column] is not None:
        raise Exception("The action is invalid for the given board")
    else:
        newBoard = copy.deepcopy(board)
        newBoard[row][column] = player(board)
        return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check horizontally
    for row in range(0, 3):
        if board[row][0] == board[row][1] == board[row][2] is not None:
            if board[row][0] == X:
                return X
            else:
                return O
    # Check vertically
    for column in range(0, 3):
        if board[0][column] == board[1][column] == board[2][column] is not None:
            if board[0][column] == X:
                return X
            else:
                return O
    # Check diagonally
    if (board[0][0] == board[1][1] == board[2][2] is not None) or (board[0][2] == board[1][1] == board[2][0] is not None):
        if board[1][1] == X:
            return X
        else:
            return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        for element in row:
            if element is None:
                return False
    return True
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise. Only called when game has ended.
    """
    whoWon = winner(board)
    if whoWon == X:
        return 1
    elif whoWon == O:
        return -1
    else:
        return 0


# def minimax(board): # Minimax without alpha-beta pruning
#     """
#     Returns the optimal action for the current player on the board.
#     """
#     if terminal(board):
#         return None
    
#     def maxValue(board):
#         if terminal(board):
#             return utility(board), None
#         v = -math.inf
#         optAction = None
#         for action in actions(board):
#             u, x = minValue(result(board, action))
#             if v < u:
#                 v = u
#                 optAction = action
#         return (v, optAction)
    
#     def minValue(board):
#         if terminal(board):
#             return utility(board), None
#         v = math.inf
#         optAction = None
#         for action in actions(board):
#             u, x = maxValue(result(board, action))
#             if v > u:
#                 v = u
#                 optAction = action
#         return (v, optAction)

#     if player(board) == X:
#         v, action = maxValue(board)
#     else:
#         v, action = minValue(board)
    
#     return action

def minimax(board): # Minimax with alpha-beta pruning
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    def maxValue(board, worst):
        if terminal(board):
            return utility(board), None
        v = -math.inf
        optAction = None
        best = None
        for action in actions(board):
            u, _ = minValue(result(board, action), best)
            if v < u:
                v = u
                optAction = action
                best = v
            if (worst is not None) and (v >= worst):
                break
        return (v, optAction)
    
    def minValue(board, best):
        if terminal(board):
            return utility(board), None
        v = math.inf
        optAction = None
        worst = None
        for action in actions(board):
            u, _ = maxValue(result(board, action), worst)
            if v > u:
                v = u
                optAction = action
                worst = v
            if (best is not None) and (v <= best):
                break
        return (v, optAction)

    if player(board) == X:
        v, action = maxValue(board, None)
    else:
        v, action = minValue(board, None)
    
    return action
