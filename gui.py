import time
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

import GameLogic
import DB

COLORS = {
    "zielone": "#6aaa64",
    "żółte": "#c9b458",
    "szare": "#787c7e"
}


guess = 0
won = False
trueWord = None
start = 0
entry = None
entry_var = None
user_nick = ""

def limit_entry_length(*args):
    global entry_var
    val = entry_var.get()
    if len(val) > 5:
        entry_var.set(val[:5])

def on_nick_enter(event):
    start_game()

def start_game():
    global trueWord, start, user_nick

    user_nick = nick_entry.get().strip()
    if user_nick == "":
        return

    trueWord = GameLogic.get_random_word()

    start_frame.pack_forget()
    game_frame.pack(expand=True)
    entry.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    entry.focus_set()

    start = time.time()
    print(f"DEBUG: Wylosowane słowo: {trueWord}")

def checkWin(tab):
    global won
    if all(color == "zielone" for color in tab):
        won = True
        end_game("Gratulacje! Wygrałeś!")
        end = time.time()
        DB.addUser(user_nick, won, int(end - start))
    elif guess == 6:
        end_game(["Przegrałeś!", f"Poprawne słowo to {trueWord.upper()}"])
        end = time.time()
        DB.addUser(user_nick, won, int(end - start))

def end_game(messages):
    global start

    entry.config(state='disabled')

    for widget in root.winfo_children():
        widget.destroy()

    end_frame = tb.Frame(root)
    end_frame.pack(expand=True)

    if isinstance(messages, list):
        for msg in messages:
            label = tb.Label(end_frame, text=msg, font=("Helvetica", 24), bootstyle="danger")
            label.pack(pady=5)
    else:
        label = tb.Label(end_frame, text=messages, font=("Helvetica", 24), bootstyle="success")
        label.pack(pady=20)

    time_taken = round(time.time() - start, 2)
    info_label = tb.Label(end_frame, text=f"Nick: {user_nick}\nCzas: {time_taken}s", font=("Helvetica", 16))
    info_label.pack(pady=10)

    restart_button = tb.Button(end_frame, text="Zagraj ponownie", command=restart_game, bootstyle="info-outline")
    restart_button.pack(pady=20)

def restart_game():
    global guess, won, trueWord
    guess = 0
    won = False
    trueWord = None

    for widget in root.winfo_children():
        widget.destroy()

    init_gui()

def on_enter(event):
    global guess, won, entry, entry_var
    if won:
        return

    slowo = entry_var.get().strip().lower()
    if len(slowo) != 5:
        return

    tab = GameLogic.check_guess(slowo, trueWord)
    if tab is None:
        return

    for i in range(5):
        labels[guess][i].config(text=slowo[i].upper())
        color = COLORS.get(tab[i], COLORS["szare"])
        frames[guess][i].config(bg=color)
        labels[guess][i].config(bg=color, fg="white")

    guess += 1
    entry_var.set("")
    checkWin(tab)

def init_gui():
    global root, start_frame, nick_entry, start_button, game_frame, entry, entry_var
    global frames, labels

    start_frame = tb.Frame(root, padding=20)
    start_frame.pack(expand=True)

    welcome_label = tb.Label(start_frame, text="Wpisz swój nick", font=("Helvetica", 20))
    welcome_label.pack(pady=10)

    nick_entry = tb.Entry(start_frame, font=("Helvetica", 16))
    nick_entry.pack(pady=10)
    nick_entry.focus_set()
    nick_entry.bind("<Return>", on_nick_enter)

    start_button = tb.Button(start_frame, text="Start", command=start_game, bootstyle="success")
    start_button.pack(pady=10)

    game_frame = tb.Frame(root, padding=10)

    frames = []
    labels = []

    for j in range(6):
        row_frames = []
        row_labels = []
        for i in range(5):
            frame = tk.Frame(game_frame, width=60, height=60, bg="#d3d3d3", bd=2, relief="solid")
            frame.grid(row=j, column=i, padx=5, pady=5)
            frame.grid_propagate(False)

            label = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), bg="#d3d3d3", fg="white")
            label.place(relx=0.5, rely=0.5, anchor="center")

            row_frames.append(frame)
            row_labels.append(label)

        frames.append(row_frames)
        labels.append(row_labels)

    entry_var = tk.StringVar()
    entry_var.trace_add("write", limit_entry_length)

    def is_valid_char_input(char):
        return char.isalpha() or char == ""

    vcmd = root.register(lambda P: is_valid_char_input(P))

    entry = tb.Entry(root, font=("Helvetica", 16), textvariable=entry_var,
                     validate="key", validatecommand=(vcmd, "%P"))
    entry.bind("<Return>", on_enter)

root = tb.Window(themename="flatly")
root.title("Wordle")
root.geometry("800x800")

init_gui()
root.mainloop()