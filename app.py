from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Tic Tac Toe board
tttgrid = [""] * 9
player = "X"

def check_winner():
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in win_combinations:
        if tttgrid[combo[0]] == tttgrid[combo[1]] == tttgrid[combo[2]] != "":
            return tttgrid[combo[0]]
    
    if "" not in tttgrid:
        return "tie"
    
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    global tttgrid, player

    data = request.get_json()
    pos = data["position"]
    
    if tttgrid[pos] == "":
        tttgrid[pos] = player
        winner = check_winner()
        
        if winner:
            return jsonify({"winner": winner, "grid": tttgrid})

        player = "O" if player == "X" else "X"
    
    return jsonify({"grid": tttgrid, "next": player})

@app.route("/reset", methods=["POST"])
def reset():
    global tttgrid, player
    tttgrid = [""] * 9
    player = "X"
    return jsonify({"message": "Game reset", "grid": tttgrid, "next": player})

if __name__ == "__main__":
    app.run(debug=True)