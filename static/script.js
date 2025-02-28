async function makeMove(position) {
    let response = await fetch("/play", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ position: position })
    });

    let data = await response.json();
    updateBoard(data.grid);

    if (data.winner) {
        document.getElementById("turn").innerText = data.winner === "tie" ? "It's a tie!" : `Player ${data.winner} wins!`;
    } else {
        document.getElementById("turn").innerText = `It is ${data.next}'s turn.`;
    }
}

async function resetGame() {
    let response = await fetch("/reset", { method: "POST" });
    let data = await response.json();
    updateBoard(data.grid);
    document.getElementById("turn").innerText = "It is X's turn.";
}

function updateBoard(grid) {
    grid.forEach((mark, index) => {
        document.getElementById(`cell${index}`).innerText = mark;
    });
}
