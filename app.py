from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Game state
tttgrid = [""] * 9
current_player = "X"
game_mode = None

# Winning combinations
WIN_COMBINATIONS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
]

def check_winner():
    """Check if there's a winner or a tie."""
    for combo in WIN_COMBINATIONS:
        if tttgrid[combo[0]] == tttgrid[combo[1]] == tttgrid[combo[2]] != "":
            return tttgrid[combo[0]]

    if "" not in tttgrid:
        return "Tie"

    return None

def minimax(board, depth, is_maximizing):
    """AI Move Calculation using Minimax Algorithm."""
    scores = {"X": -1, "O": 1, "Tie": 0}

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

def best_move():
    """Determine the best move for AI."""
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def make_move():
    global current_player, game_mode

    data = request.json
    position = data["position"]
    game_mode = data["mode"]

    if tttgrid[position] == "":
        tttgrid[position] = current_player

        # Check if player won
        winner = check_winner()
        if winner:
            return jsonify({"grid": tttgrid, "message": f"{winner} wins!"})

        # Switch player
        if game_mode == "1v1":
            current_player = "O" if current_player == "X" else "X"
        else:
            # AI move for 1vBot mode
            ai_move = best_move()
            if ai_move is not None:
                tttgrid[ai_move] = "O"
                winner = check_winner()
                if winner:
                    return jsonify({"grid": tttgrid, "message": f"{winner} wins!"})

    return jsonify({"grid": tttgrid, "message": "Your Turn!"})

@app.route("/reset", methods=["POST"])
def reset_game():
    global board, current_player, game_over

    board = [""] * 9  # Reset the board
    current_player = "X"  # X always starts
    game_over = False  # Reset game state

    return jsonify({'message': "Game Reset!", 'board': board, 'current_player': current_player})

if __name__ == "__main__":
    app.run(debug=True)
