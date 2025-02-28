import tkinter as tk
import random
from collections import Counter
from colorama import Fore

root = tk.Tk()
root.maxsize(300, 300)
root.geometry("%dx%d+%d+%d" % (300, 300, (root.winfo_screenwidth() / 2 - 150), (root.winfo_screenheight() / 2 - 150)))

player = "X"
game_mode = None
tttgrid = [""] * 9
game_over = False

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

def check_winner():
    winCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    for combo in winCombinations:
        if tttgrid[combo[0]] == tttgrid[combo[1]] == tttgrid[combo[2]] != "":
            return tttgrid[combo[0]]

    if "" not in tttgrid:
        return "tie"

    return None

def playerSwitch(button, pos):
    global player, game_over
    if game_over or button["text"] != " ":
        return

    if player == "X":
        print(Fore.GREEN + f"Player {player} has played button {button_map[pos]}")
    else:
        print(Fore.YELLOW + f"Player {player} has played button {button_map[pos]}")

    button.config(text=player)
    tttgrid[pos] = player
    winlose()

    if not game_over:
        player = "O" if player == "X" else "X"
        turn.config(text=f"It is {player}'s turn.")

    if game_mode == "1vBot" and player == "O" and not game_over:
        bot_move()

def bot_move():
    global player
    bot_pos = best_move()

    print(Fore.RED + f"AI has played button {button_map[bot_pos]}")

    buttons[bot_pos].config(text="O")
    tttgrid[bot_pos] = "O"
    winlose()

    if not game_over:
        player = "X"
        turn.config(text="It is X's turn.")

def winlose():
    global game_over
    winCombinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winCombinations:
        if tttgrid[combo[0]] == tttgrid[combo[1]] == tttgrid[combo[2]] != "":
            print(Fore.CYAN + f"Player {tttgrid[combo[0]]} wins!")
            turn.config(text=f"Player {tttgrid[combo[0]]} wins!")
            disable_buttons()
            game_over = True
            show_end_buttons()
            return
    if "" not in tttgrid:
        print(Fore.BLUE + "It's a tie!")
        turn.config(text="It's a tie!")
        disable_buttons()
        game_over = True
        show_end_buttons()

def disable_buttons():
    for button in buttons:
        button.config(state="disabled")

def show_end_buttons():
    tk.Button(root, text="Replay", command=lambda: start_game(game_mode)).grid(row=4, column=0, columnspan=3, pady=5)
    tk.Button(root, text="Main Menu", command=main_menu).grid(row=5, column=0, columnspan=3, pady=5)

def start_game(mode):
    global game_mode, player, game_over, tttgrid, turn, buttons
    game_mode = mode
    player = "X"
    game_over = False
    tttgrid = [""] * 9

    for widget in root.winfo_children():
        widget.destroy()

    turn = tk.Label(root, text="It is X's turn.", bg="yellow")
    turn.grid(row=0, column=3)

    global a, b, c, d, e, f, g, h, i
    a = tk.Button(root, text=" ", command=lambda: playerSwitch(a, 0), height=1, width=2)
    a.grid(row=1, column=1, padx=20, pady=20)

    b = tk.Button(root, text=" ", command=lambda: playerSwitch(b, 1), height=1, width=2)
    b.grid(row=1, column=2, padx=20, pady=20)

    c = tk.Button(root, text=" ", command=lambda: playerSwitch(c, 2), height=1, width=2)
    c.grid(row=1, column=3, padx=0, pady=20)

    d = tk.Button(root, text=" ", command=lambda: playerSwitch(d, 3), height=1, width=2)
    d.grid(row=2, column=1, padx=20, pady=20)

    e = tk.Button(root, text=" ", command=lambda: playerSwitch(e, 4), height=1, width=2)
    e.grid(row=2, column=2, padx=20, pady=20)

    f = tk.Button(root, text=" ", command=lambda: playerSwitch(f, 5), height=1, width=2)
    f.grid(row=2, column=3, padx=0, pady=20)

    g = tk.Button(root, text=" ", command=lambda: playerSwitch(g, 6), height=1, width=2)
    g.grid(row=3, column=1, padx=20, pady=20)

    h = tk.Button(root, text=" ", command=lambda: playerSwitch(h, 7), height=1, width=2)
    h.grid(row=3, column=2, padx=20, pady=20)

    i = tk.Button(root, text=" ", command=lambda: playerSwitch(i, 8), height=1, width=2)
    i.grid(row=3, column=3, padx=0, pady=20)

    buttons = [a, b, c, d, e, f, g, h, i]

    global button_map
    button_map = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I"}

    quit_button = tk.Button(root, text="Quit", command=root.destroy)
    quit_button.grid(row=0, column=2)

def main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="TIC-TAC-TOE\nBy Aayan Arora", bg="yellow").grid(row=0, column=0, columnspan=2)
    tk.Button(root, text="1v1 (Player vs Player)", command=lambda: start_game("1v1"), width=20).grid(row=1, column=0, columnspan=2, pady=10)
    tk.Button(root, text="1vBot (Player vs AI)", command=lambda: start_game("1vBot"), width=20).grid(row=2, column=0, columnspan=2, pady=10)

    turn = tk.Label(root, text="Select Game Mode", bg="yellow")  
    turn.grid(row=3, column=0, columnspan=2)

root.title("Tic-Tac-Toe")
root.configure(background="yellow")

main_menu()
root.mainloop()
