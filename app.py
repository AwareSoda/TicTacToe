from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Tic-Tac-Toe Game Variables
tttgrid = [""] * 9
player = "X"
game_over = False

# Winning Combinations
win_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

# Minimax AI Function
def minimax(board, depth, is_maximizing):
    scores = {"X": -1, "O": 1, "tie": 0}

    winner = check_winner()
    if winner:
        return scores[winner]

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

# Best move for AI
def best_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if tttgrid[i] == "":
            tttgrid[i] = "O"
            score = minimax(tttgrid, 0, False)
            tttgrid[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

# Check for a winner
def check_winner():
    for combo in win_combinations:
        if tttgrid[combo[0]] == tttgrid[combo[1]] == tttgrid[combo[2]] != "":
            return tttgrid[combo[0]]
    if "" not in tttgrid:
        return "tie"
    return None

# Route to serve the game page
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle player moves
@app.route('/move', methods=['POST'])
def player_move():
    global player, game_over
    if game_over:
        return jsonify({"message": "Game over!"})

    data = request.json
    pos = data.get("position")

    if tttgrid[pos] == "":
        tttgrid[pos] = player
        winner = check_winner()

        if winner:
            game_over = True
            return jsonify({"winner": winner, "grid": tttgrid})

        # AI Move
        ai_pos = best_move()
        if ai_pos is not None:
            tttgrid[ai_pos] = "O"
            winner = check_winner()
            if winner:
                game_over = True
                return jsonify({"winner": winner, "grid": tttgrid})

    return jsonify({"grid": tttgrid})

# API route to reset the game
@app.route('/reset', methods=['POST'])
def reset_game():
    global tttgrid, player, game_over
    tttgrid = [""] * 9
    player = "X"
    game_over = False
    return jsonify({"message": "Game reset", "grid": tttgrid})

if __name__ == '__main__':
    app.run(debug=True)
