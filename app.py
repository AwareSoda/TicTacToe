from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9
current_player = "X"
game_mode = None

def check_winner():
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for (a, b, c) in win_conditions:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None

def minimax(board, depth, is_maximizing):
    scores = {"X": -1, "O": 1, "tie": 0}

    winner = check_winner()
    if winner:
        return scores.get(winner, 0)

    if "" not in board:
        return scores["tie"]

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

def best_bot_move():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/set_mode", methods=["POST"])
def set_mode():
    global game_mode
    data = request.get_json()
    game_mode = data["mode"]
    return jsonify(success=True)

@app.route("/move", methods=["POST"])
def move():
    global current_player
    data = request.get_json()
    cell = data["cell"]

    if board[cell] == "":
        board[cell] = current_player
        winner = check_winner()
        if winner:
            return jsonify(success=True, winner=winner)
        if "" not in board:
            return jsonify(success=True, draw=True)

        current_player = "O" if current_player == "X" else "X"
        return jsonify(success=True)

    return jsonify(success=False)

@app.route("/bot_move", methods=["POST"])
def bot_move():
    global current_player
    if game_mode != "1vBot" or current_player != "O":
        return jsonify(success=False)

    bot_choice = best_bot_move()
    if bot_choice is not None:
        board[bot_choice] = "O"
        winner = check_winner()
        if winner:
            return jsonify(success=True, cell=bot_choice, winner=winner)
        if "" not in board:
            return jsonify(success=True, cell=bot_choice, draw=True)

        current_player = "X"
        return jsonify(success=True, cell=bot_choice)

    return jsonify(success=False)

@app.route("/reset", methods=["POST"])
def reset():
    global board, current_player, game_mode
    board = [""] * 9
    current_player = "X"
    game_mode = None
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
