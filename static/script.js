document.addEventListener("DOMContentLoaded", function () {
    let currentPlayer = "X";  
    let gameMode = null;
    let gameOver = false;

    function updateStatus(message) {
        document.getElementById("status").innerText = message;
    }

    window.startGame = function (mode) {
        gameMode = mode;
        fetch("/set_mode", {
            method: "POST",
            body: JSON.stringify({ mode }),
            headers: { "Content-Type": "application/json" }
        }).then(() => {
            document.getElementById("mode-selection").style.display = "none";
            document.getElementById("game-container").style.display = "block";
            updateStatus("Player X's turn");
        });
    };

    window.makeMove = function (cellIndex) {
        if (gameOver || !gameMode) return;

        fetch("/move", {
            method: "POST",
            body: JSON.stringify({ cell: cellIndex }),
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`cell-${cellIndex}`).innerText = currentPlayer;
                if (data.winner) {
                    updateStatus(`${data.winner} wins!`);
                    gameOver = true;
                } else if (data.draw) {
                    updateStatus("It's a draw!");
                    gameOver = true;
                } else {
                    currentPlayer = (currentPlayer === "X") ? "O" : "X";
                    updateStatus(`Player ${currentPlayer}'s turn`);

                    if (gameMode === "1vBot" && currentPlayer === "O") {
                        setTimeout(botMove, 500);
                    }
                }
            }
        });
    };

    function botMove() {
        fetch("/bot_move", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById(`cell-${data.cell}`).innerText = "O";
                if (data.winner) {
                    updateStatus("Bot wins!");
                    gameOver = true;
                } else if (data.draw) {
                    updateStatus("It's a draw!");
                    gameOver = true;
                } else {
                    currentPlayer = "X";
                    updateStatus("Player X's turn");
                }
            }
        });
    }

    document.getElementById("reset").addEventListener("click", function () {
        fetch("/reset", { method: "POST" }).then(() => location.reload());
    });
});
