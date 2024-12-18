import math
import sys

X = 'X'
O = 'O'
EMPTY = None

def initial_state():
    '''
    returns starting state of the board.
    '''
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    '''
    returns player who has the next turn on a board.
    '''
    count_X = 0
    count_O = 0
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_X += 1
            if board[i][j] == O:
                count_O += 1

    if count_O >= count_X:
        return X
    else:
        return O

def actions(board):
    '''
    returns set of all possible actions (i, j) available on the board.
    '''
    actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    '''
    returns the board that results from making move (i, j) on the board.
    '''
    new_board = board

    actual_player = player(new_board)

    new_board[action[0]][action[1]] = actual_player

    return new_board


def winner(board):
    '''
    returns the winner of the game, if there is one.
    '''

    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]
        
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]
        
    # Verificar as diagonais, não faço ideia de como usa um for para verificar, mas como só
    # são possíveis 2 diagonais está tudo bem utilizar um código força bruta para verificar
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    
    return None


def terminal(board):
    '''
    returns True if game is over, False otherwise.
    '''
    winner = utility(board)

    if winner != 0:
        return True
    
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    return False

    return True


def utility(board):
    '''
    returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    '''
    win = winner(board)
    if win == X:
        return 1
    if win == O:
        return -1
    else:
        return 0


def minimax(board):
    '''
    returns the optimal action for the current player on the board.
    '''
    best_move = EMPTY
    ai_letter = player(board)
    is_min = False

    if ai_letter == X:
        best_score = -math.inf
    else:
        best_score = math.inf
        is_min = True

    if is_min: # Estamos minimizando (computador é o O)
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = ai_letter
                    score = evaluate(board, False)
                    board[row][column] = EMPTY
                    if score < best_score:
                        best_score = score
                        best_move = (row, column)
                
    else: # Estamos maximizando (computador é o X)
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = ai_letter
                    score = evaluate(board, True)
                    board[row][column] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (row, column)
    
    return best_move
    
def evaluate(board, is_min):

    if terminal(board):
        return utility(board)

    if is_min: # Estamos minimizando
        best_score = math.inf
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = O
                    score = evaluate(board, False)
                    board[row][column] = EMPTY
                    if score < best_score:
                        best_score = score
        return best_score
                
    else: # Estamos maximizando
        best_score = -math.inf
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = X
                    score = evaluate(board, True)
                    board[row][column] = EMPTY
                    if score > best_score:
                        best_score = score
        return best_score

# NOT IMPLEMENTED, IT DIDNT WORK
    
def minimax_prunning(board):
    '''
    returns the optimal action for the current player on the board using Alpha-Beta Prunning.
    '''

    best_move = EMPTY
    ai_letter = player(board)
    is_min = False

    if ai_letter == X:
        best_score = -math.inf
    else:
        best_score = math.inf
        is_min = True

    if is_min: # Estamos minimizando (computador é o O)
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = ai_letter
                    score = alpha_beta_prunning(board, -math.inf, math.inf, ai_letter)
                    board[row][column] = EMPTY
                    if score[2] < best_score:
                        best_score = score[2]
                        best_move = (score[0], score[1])
                
    else: # Estamos maximizando (computador é o X)
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = ai_letter
                    score = alpha_beta_prunning(board, -math.inf, math.inf, ai_letter)
                    board[row][column] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (row, column)
    
    return best_move
    
def alpha_beta_prunning(board, alpha, beta, playing):
    r = 0
    c = 0

    if terminal(board):
        return [r, c, utility(board)]

    else:
        for row in range(3):
            for column in range(3):
                if board[row][column] == EMPTY:
                    board[row][column] = playing
                    if playing == X:
                        score = alpha_beta_prunning(board, alpha, beta, O)
                        if score[2] > alpha:
                            alpha = score[2]
                            r = row
                            c = column
                    else:
                        score = alpha_beta_prunning(board, alpha, beta, X)
                        if score[2] < beta:
                            beta = score[2]
                            r = row
                            c = column

                    board[row][column] = EMPTY

                    if alpha >= beta:
                        break

        if playing == X:
            return [r, c, alpha]
        else:
            return [r, c, beta]