document.addEventListener("DOMContentLoaded", function () {
    let cells = document.querySelectorAll(".cell");
    let message = document.getElementById("message");
    let resetBtn = document.getElementById("reset");

    // Handle cell click
    cells.forEach((cell, index) => {
        cell.addEventListener("click", function () {
            fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ position: index })
            })
            .then(response => response.json())
            .then(data => {
                updateBoard(data.grid);
                if (data.winner) {
                    message.innerText = `${data.winner} wins!`;
                }
            });
        });
    });

    // Update the board
    function updateBoard(grid) {
        grid.forEach((value, index) => {
            cells[index].innerText = value;
        });
    }

    // Reset game
    document.getElementById("reset").addEventListener("click", function () {
        fetch("/reset", { method: "POST" })
            .then(response => response.json())
            .then(data => {
                document.getElementById("message").innerText = data.message;
                updateBoard(data.board);  // Ensure board resets visually
                currentPlayer = data.current_player;  // Reset turn
            })
            .catch(error => console.error("Error resetting game:", error));
    });
    });
});