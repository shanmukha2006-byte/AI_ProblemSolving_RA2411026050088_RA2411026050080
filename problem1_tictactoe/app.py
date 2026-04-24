from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    global nodes_explored
    nodes_explored += 1

    score = evaluate(board)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not is_moves_left(board):
        return 0

    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    best = max(best, minimax(board, depth + 1, not is_maximizing))
                    board[i][j] = ''
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    best = min(best, minimax(board, depth + 1, not is_maximizing))
                    board[i][j] = ''
        return best

# Alpha-Beta Pruning algorithm
def alpha_beta(board, depth, is_maximizing, alpha, beta):
    global nodes_explored
    nodes_explored += 1

    score = evaluate(board)
    if score == 10:
        return score - depth
    if score == -10:
        return score + depth
    if not is_moves_left(board):
        return 0

    if is_maximizing:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    best = max(best, alpha_beta(board, depth + 1, not is_maximizing, alpha, beta))
                    board[i][j] = ''
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    best = min(best, alpha_beta(board, depth + 1, not is_maximizing, alpha, beta))
                    board[i][j] = ''
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def find_best_move(board, algo="minimax"):
    global nodes_explored
    nodes_explored = 0
    best_val = -1000
    best_move = (-1, -1)

    start_time = time.perf_counter()

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = 'O'
                if algo == "minimax":
                    move_val = minimax(board, 0, False)
                else:
                    move_val = alpha_beta(board, 0, False, -1000, 1000)
                board[i][j] = ''

                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000 # ms

    return best_move, nodes_explored, execution_time

def evaluate(board):
    for row in range(3):
        if board[row][0] == board[row][1] and board[row][1] == board[row][2]:
            if board[row][0] == 'O': return 10
            elif board[row][0] == 'X': return -10
    for col in range(3):
        if board[0][col] == board[1][col] and board[1][col] == board[2][col]:
            if board[0][col] == 'O': return 10
            elif board[0][col] == 'X': return -10
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == 'O': return 10
        elif board[0][0] == 'X': return -10
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == 'O': return 10
        elif board[0][2] == 'X': return -10
    return 0

def is_moves_left(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                return True
    return False

def check_winner(board):
    score = evaluate(board)
    if score == 10: return 'O'
    if score == -10: return 'X'
    if not is_moves_left(board): return 'Tie'
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.json
    board = data.get('board')
    algo = data.get('algo') # "minimax" or "alphabeta"

    winner = check_winner(board)
    if winner:
        return jsonify({"status": "game_over", "winner": winner})

    # AI move
    move, nodes, time_taken = find_best_move(board, algo)
    
    if move != (-1, -1):
        board[move[0]][move[1]] = 'O'
    
    winner = check_winner(board)
    
    return jsonify({
        "status": "game_over" if winner else "continue",
        "board": board,
        "winner": winner,
        "nodes_explored": nodes,
        "execution_time_ms": time_taken,
        "ai_move": move
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
